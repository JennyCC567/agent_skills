#!/usr/bin/env python3
"""
人才匹配脚本
功能：基于语义相似度和约束条件进行人才匹配

Phase 2 增强：
1. 技能匹配语义化（P2-Bug7）：TF-IDF + 余弦相似度语义匹配，Jaccard * 0.4 + 语义 * 0.6
2. 硬约束弹性化（P1-Bug6）：地域模糊匹配 + 城市圈、passive状态降权而非排除
3. 潜力评分增强（P2-Bug8）：985+211名校列表、学历梯度、职业轨迹、技能稀缺度、行业匹配

Phase 3 增强：
4. 技能知识图谱（P3）：通过技能关联关系图谱，对不完全匹配的技能给予部分加分
5. 偏见检测（P3）：匹配后自动检测性别/年龄/地域/学历偏见，输出检测报告
6. 交互式查询（P3）：匹配后初始化查询引擎，支持筛选/排序/聚合/对比分析
"""

import argparse
import json
import math
import os
import sys
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter

# Phase 3: 导入新增模块
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from skill_graph import SkillGraph
from bias_detector import BiasDetector
from query_engine import QueryEngine

# 尝试导入 sklearn（用于 TF-IDF 语义匹配），不可用时回退到纯 Python 实现
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as _sk_cosine_similarity
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False


class TalentMatcher:
    """人才匹配器"""

    # =====================================================================
    # 985 + 211 高校列表（覆盖 50+ 所主要高校）
    # =====================================================================
    TOP_UNIVERSITIES = {
        # 985 高校
        "清华大学", "北京大学", "复旦大学", "上海交通大学", "浙江大学",
        "中国科学技术大学", "南京大学", "华中科技大学", "武汉大学", "中山大学",
        "西安交通大学", "哈尔滨工业大学", "同济大学", "四川大学", "东南大学",
        "北京航空航天大学", "北京师范大学", "南开大学", "天津大学", "厦门大学",
        "吉林大学", "山东大学", "中南大学", "大连理工大学", "电子科技大学",
        "重庆大学", "兰州大学", "东北大学", "湖南大学", "西北农林科技大学",
        "中国海洋大学", "国防科技大学", "中央民族大学", "华南理工大学", "华东师范大学",
        "中国人民大学", "中国农业大学", "北京理工大学", "西北工业大学",
        # 211 高校（非 985 的主要高校）
        "北京交通大学", "北京邮电大学", "北京化工大学", "北京外国语大学",
        "上海财经大学", "上海大学", "上海外国语大学", "华东理工大学",
        "南京航空航天大学", "南京理工大学", "南京师范大学", "苏州大学",
        "武汉理工大学", "中南财经政法大学", "西南财经大学", "西南交通大学",
        "西安电子科技大学", "哈尔滨工程大学", "合肥工业大学", "暨南大学",
        "华北电力大学", "中国传媒大学", "中央财经大学", "对外经济贸易大学",
        "北京科技大学", "东华大学", "河海大学", "中国政法大学",
        # 英文名及别名映射
        "Tsinghua", "Peking", "MIT", "Stanford", "Berkeley", "CMU",
        "Zhejiang", "Fudan", "SJTU", "USTC", "Nanjing", "Nankai", "Tongji",
    }

    # 技能同义词映射（用于语义匹配时的归一化）
    SKILL_SYNONYMS = {
        "distributed training": "分布式训练",
        "model optimization": "模型优化",
        "machine learning": "机器学习",
        "deep learning": "深度学习",
        "natural language processing": "NLP",
        "computer vision": "CV",
        "large language model": "大模型",
        "llm": "大模型",
        "prompt engineering": "提示工程",
        "rag": "检索增强生成",
        "retrieval augmented generation": "检索增强生成",
        "docker": "容器化",
        "kubernetes": "容器编排",
        "ci/cd": "持续集成",
        "mlops": "机器学习运维",
        "fastapi": "API框架",
        "tensorrt": "推理优化",
        "yolo": "目标检测",
        "opencv": "计算机视觉库",
    }

    # 城市圈定义（地域模糊匹配用）
    CITY_CIRCLES = {
        "京津冀": {"北京", "天津", "石家庄", "保定", "唐山", "廊坊", "承德", "张家口", "秦皇岛", "沧州"},
        "长三角": {"上海", "杭州", "苏州", "南京", "无锡", "宁波", "合肥", "常州", "南通", "嘉兴", "绍兴", "温州", "扬州", "镇江", "泰州"},
        "珠三角": {"深圳", "广州", "东莞", "佛山", "珠海", "中山", "惠州", "江门", "肇庆"},
        "成渝": {"成都", "重庆", "绵阳", "德阳", "南充", "宜宾"},
        "武汉": {"武汉", "长沙", "南昌"},
    }

    # 城市别名/简称映射
    CITY_ALIASES = {
        "北京市": "北京",
        "上海市": "上海",
        "深圳市": "深圳",
        "广州市": "广州",
        "杭州市": "杭州",
        "成都市": "成都",
        "南京市": "南京",
        "武汉市": "武汉",
        "西安市": "西安",
        "苏州市": "苏州",
    }

    def __init__(self, weights: Dict[str, float]):
        """
        初始化匹配器

        Args:
            weights: 权重配置，格式为 {"skill": 0.4, "experience": 0.3, "potential": 0.2, "culture": 0.1}
        """
        self.weights = weights
        self.required_fields = ["skills", "experience_years", "education_level"]

        # 技能匹配权重配置（可外部覆盖）
        self.skill_jaccard_weight = 0.4
        self.skill_semantic_weight = 0.6

        # passive 状态惩罚系数
        self.passive_penalty = 0.8

        # 城市圈匹配的地域降权系数
        self.city_circle_penalty = 0.85

        # 学历层次映射
        self._education_hierarchy = {
            "high_school": 0,
            "college": 1,
            "bachelor": 2,
            "master": 3,
            "phd": 4
        }

        # 学历加分梯度（用于潜力评分）
        self._education_bonus = {
            "phd": 1.0,
            "master": 0.7,
            "bachelor": 0.4,
            "college": 0.2,
            "high_school": 0.1
        }

        # 初始化 TF-IDF 向量化器（如果 sklearn 可用）
        self._tfidf_vectorizer = None
        if _SKLEARN_AVAILABLE:
            try:
                self._tfidf_vectorizer = TfidfVectorizer(
                    token_pattern=r'(?u)\b\w+\b',
                    ngram_range=(1, 2),
                    sublinear_tf=True
                )
            except Exception:
                self._tfidf_vectorizer = None

        # Phase 3: 初始化技能知识图谱
        self._skill_graph = SkillGraph()

        # Phase 3: 技能图谱关联加分上限（占总分比例）
        self.skill_graph_max_bonus = 0.15  # 最多加15分（百分制）

        # Phase 3: 存储偏见检测报告和查询引擎（匹配完成后可用）
        self.bias_analysis: Optional[Dict[str, Any]] = None
        self.query_engine: Optional[QueryEngine] = None

    # =====================================================================
    # 技能匹配语义化（P2-Bug7）
    # =====================================================================

    def _normalize_skill(self, skill: str) -> str:
        """技能名称归一化（处理同义词、大小写）"""
        lower = skill.lower().strip()
        # 检查同义词映射
        if lower in self.SKILL_SYNONYMS:
            return self.SKILL_SYNONYMS[lower]
        # 中文技能直接返回
        return skill.strip()

    def _calculate_skill_similarity(self, job_skills: List[str], candidate_skills: List[str]) -> Tuple[float, Dict[str, float]]:
        """
        计算技能相似度（Jaccard + 语义匹配融合）

        最终技能匹配分数 = Jaccard相似度 * 0.4 + 语义相似度 * 0.6

        Args:
            job_skills: 岗位技能列表
            candidate_skills: 候选人技能列表

        Returns:
            (综合技能匹配分数, 各子分数字典)
        """
        if not job_skills or not candidate_skills:
            return 0.0, {"jaccard": 0.0, "semantic": 0.0}

        # 归一化技能名称
        job_set = set(self._normalize_skill(s).lower() for s in job_skills)
        candidate_set = set(self._normalize_skill(s).lower() for s in candidate_skills)

        # 1. Jaccard 相似度（含覆盖率加权）
        intersection = job_set & candidate_set
        union = job_set | candidate_set
        if not union:
            jaccard = 0.0
        else:
            required_match = len(intersection) / len(job_set) if job_set else 0.0
            jaccard_raw = len(intersection) / len(union)
            jaccard = required_match * 0.7 + jaccard_raw * 0.3

        # 2. 语义相似度（TF-IDF + 余弦相似度）
        semantic = self._calculate_semantic_similarity(job_skills, candidate_skills)

        # 融合
        total = jaccard * self.skill_jaccard_weight + semantic * self.skill_semantic_weight

        return total, {"jaccard": round(jaccard, 4), "semantic": round(semantic, 4)}

    def _calculate_semantic_similarity(self, job_skills: List[str], candidate_skills: List[str]) -> float:
        """
        基于 TF-IDF + 余弦相似度计算技能语义相似度

        策略：
        1. 优先使用 sklearn TfidfVectorizer
        2. 不可用时回退到纯 Python TF-IDF 实现
        3. 均不可用时回退到基于字符重叠的近似语义匹配

        Args:
            job_skills: 岗位技能列表
            candidate_skills: 候选人技能列表

        Returns:
            语义相似度分数 (0-1)
        """
        # 归一化技能文本
        job_text = self._skills_to_text(job_skills)
        candidate_text = self._skills_to_text(candidate_skills)

        if not job_text or not candidate_text:
            return 0.0

        # 策略1: 使用 sklearn TfidfVectorizer
        if _SKLEARN_AVAILABLE and self._tfidf_vectorizer is not None:
            try:
                return self._tfidf_semantic(job_text, candidate_text)
            except Exception:
                pass

        # 策略2: 纯 Python TF-IDF
        try:
            return self._pure_python_tfidf_semantic(job_text, candidate_text)
        except Exception:
            pass

        # 策略3: 字符重叠回退
        return self._char_overlap_similarity(job_text, candidate_text)

    def _skills_to_text(self, skills: List[str]) -> str:
        """将技能列表转换为文本（归一化 + 空格连接）"""
        normalized = [self._normalize_skill(s) for s in skills]
        return " ".join(normalized)

    def _tfidf_semantic(self, job_text: str, candidate_text: str) -> float:
        """使用 sklearn TfidfVectorizer 计算语义相似度"""
        corpus = [job_text, candidate_text]
        tfidf_matrix = self._tfidf_vectorizer.fit_transform(corpus)
        sim = _sk_cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(max(0.0, min(1.0, sim)))

    def _pure_python_tfidf_semantic(self, job_text: str, candidate_text: str) -> float:
        """纯 Python 实现的 TF-IDF + 余弦相似度"""

        def tokenize(text: str) -> List[str]:
            """简易分词：按空格和常见分隔符分割，同时提取字符级 n-gram"""
            tokens = []
            # 词级 token
            for word in text.split():
                tokens.append(word.lower())
                # 对较长的词，提取 bigram
                if len(word) > 2:
                    for i in range(len(word) - 1):
                        tokens.append(word[i:i+2].lower())
            return tokens

        def compute_tfidf(text: str, idf: Dict[str, float]) -> Dict[str, float]:
            tokens = tokenize(text)
            if not tokens:
                return {}
            tf = Counter(tokens)
            total = len(tokens)
            return {term: (count / total) * idf.get(term, 1.0) for term, count in tf.items()}

        # 构建 IDF（基于这两个文档，使用平滑 IDF 公式）
        job_tokens = tokenize(job_text)
        candidate_tokens = tokenize(candidate_text)
        all_terms = set(job_tokens) | set(candidate_tokens)

        if not all_terms:
            return 0.0

        # 平滑 IDF: idf = ln((N+1)/(df+1)) + 1  （sklearn 默认使用的平滑公式）
        # N=2（两个文档），避免共享词的 IDF=0
        N = 2
        idf = {}
        for term in all_terms:
            df = (1 if term in job_tokens else 0) + (1 if term in candidate_tokens else 0)
            idf[term] = math.log((N + 1) / (df + 1)) + 1.0

        # 计算 TF-IDF 向量
        vec1 = compute_tfidf(job_text, idf)
        vec2 = compute_tfidf(candidate_text, idf)

        # 余弦相似度
        common_terms = set(vec1.keys()) & set(vec2.keys())
        if not common_terms:
            return 0.0

        dot_product = sum(vec1[t] * vec2[t] for t in common_terms)
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(max(0.0, min(1.0, dot_product / (norm1 * norm2))))

    def _char_overlap_similarity(self, text1: str, text2: str) -> str:
        """字符重叠相似度（最终回退方案）"""
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        if not set1 or not set2:
            return 0.0
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if union else 0.0

    # =====================================================================
    # 硬约束弹性化（P1-Bug6）
    # =====================================================================

    def _normalize_city(self, location: str) -> str:
        """城市名称归一化"""
        if not location:
            return ""
        # 去除"市"、"区"等后缀
        normalized = location.strip()
        for alias, std in self.CITY_ALIASES.items():
            if alias in normalized or std in normalized:
                return std
        # 去掉"市"后缀
        if normalized.endswith("市"):
            normalized = normalized[:-1]
        return normalized

    def _find_city_circle(self, city: str) -> Optional[str]:
        """查找城市所属的城市圈"""
        for circle_name, cities in self.CITY_CIRCLES.items():
            if city in cities:
                return circle_name
        return None

    def _match_location(self, job_location: str, candidate_location: str) -> Tuple[bool, float, str]:
        """
        地域弹性匹配

        匹配策略：
        1. 精确匹配 / 同城匹配：满分（1.0）
        2. 同城市圈匹配：降权（city_circle_penalty = 0.85）
        3. 跨城市圈匹配：进一步降权（cross_circle_penalty = 0.7），标注原因但不排除
           - 对于 AI 等高需求行业，异地人才是常见情况（可远程/可搬迁）
        4. 无地域约束：默认通过

        Returns:
            (是否匹配, 地域匹配权重, 匹配原因说明)
        """
        if not job_location or not candidate_location:
            return True, 1.0, ""  # 无地域约束，默认通过

        job_city = self._normalize_city(job_location)
        cand_city = self._normalize_city(candidate_location)

        # 1. 同城匹配（包含子串匹配，如"北京"匹配"北京海淀区"）
        if job_city == cand_city or job_city in cand_city or cand_city in job_city:
            return True, 1.0, ""

        # 2. 同城市圈匹配
        job_circle = self._find_city_circle(job_city)
        cand_circle = self._find_city_circle(cand_city)

        if job_circle and cand_circle and job_circle == cand_circle:
            return True, self.city_circle_penalty, f"地域放宽匹配（同属{job_circle}城市圈）"

        # 3. 跨城市圈匹配（不排除，但给予更低的权重）
        cross_circle_penalty = 0.7
        circle_info = ""
        if job_circle and cand_circle:
            circle_info = f"（{cand_circle}→{job_circle}跨区域）"
        return True, cross_circle_penalty, f"地域放宽匹配：异地人才{circle_info}"

    def _check_hard_constraints(self, candidate: Dict[str, Any],
                                constraints: Dict[str, Any]) -> Tuple[bool, List[str], float]:
        """
        检查硬约束条件（弹性化版本）

        弹性处理：
        - 地域：模糊匹配 + 同城/城市圈/跨城市圈降权
        - 薪资：超过上限但在合理范围内（<=1.5倍）降权而非排除
        - 在职状态：passive 不再排除，改为降权

        Returns:
            (是否通过, 弹性匹配原因列表, 惩罚系数)
        """
        flexible_reasons = []
        penalty = 1.0

        # 地域检查（弹性化）
        if "location" in constraints and constraints["location"]:
            matched, loc_weight, loc_reason = self._match_location(
                constraints["location"],
                candidate.get("current_location", "")
            )
            if not matched:
                return False, [], 0.0  # 地域完全不匹配，排除
            if loc_reason:
                flexible_reasons.append(loc_reason)
                penalty *= loc_weight

        # 薪资检查（弹性化：超出但合理范围内降权）
        if "max_salary" in constraints and constraints["max_salary"]:
            candidate_salary = candidate.get("expected_salary", 0)
            max_salary = constraints["max_salary"]
            if candidate_salary and candidate_salary > max_salary:
                # 超出但在 1.5 倍以内：降权处理
                if candidate_salary <= max_salary * 1.5:
                    salary_penalty = 0.85 * (max_salary / candidate_salary)
                    flexible_reasons.append(
                        f"薪资期望偏高降权处理（期望{candidate_salary}万 vs 上限{max_salary}万）"
                    )
                    penalty *= salary_penalty
                else:
                    # 超出 1.5 倍：仍为硬约束
                    return False, [], 0.0

        # 在职状态检查（弹性化：passive 降权而非排除）
        if "employment_status" in constraints and constraints["employment_status"]:
            candidate_status = candidate.get("employment_status", "").lower()
            required_status = constraints["employment_status"].lower()
            if required_status != candidate_status:
                if candidate_status == "passive":
                    flexible_reasons.append("被动求职者降权处理")
                    penalty *= self.passive_penalty
                else:
                    # 其他状态不匹配仍排除
                    return False, [], 0.0

        return True, flexible_reasons, penalty

    # =====================================================================
    # 潜力评分增强（P2-Bug8）
    # =====================================================================

    def _is_top_university(self, university: str) -> bool:
        """检查是否为 985/211 名校"""
        if not university:
            return False
        uni_lower = university.lower().strip()
        # 精确匹配
        for uni in self.TOP_UNIVERSITIES:
            if uni.lower() == uni_lower or uni in university or university in uni:
                return True
        return False

    def _calculate_education_background_score(self, candidate: Dict[str, Any]) -> float:
        """
        学历背景评分（潜力评分子项，权重 30%）

        考量维度：
        - 学历层次：博士 > 硕士 > 本科 > 其他
        - 名校加分：985/211 高校额外加分

        Returns:
            学历背景评分 (0-1)
        """
        edu_level = candidate.get("education_level", "bachelor").lower()
        base_score = self._education_bonus.get(edu_level, 0.3)

        # 名校加分
        education_list = candidate.get("education", [])
        is_top = False
        for edu in education_list:
            if isinstance(edu, dict):
                university = edu.get("university", "")
                if self._is_top_university(university):
                    is_top = True
                    break

        # 名校在学历基础上额外加分
        if is_top:
            bonus = 0.3
        else:
            bonus = 0.0

        return min(base_score * 0.7 + bonus, 1.0)

    def _calculate_career_trajectory_score(self, candidate: Dict[str, Any]) -> float:
        """
        职业轨迹评分（潜力评分子项，权重 30%）

        考量维度：
        - 晋升次数：有晋升记录加分
        - 跳槽频率：合理跳槽（每段工作 >= 2年）加分，频繁跳槽（< 1年）减分
        - 公司多样性：经历多家不同公司适度加分（跨界能力）
        - 职级成长：从工程师到专家/管理层的成长轨迹加分

        Returns:
            职业轨迹评分 (0-1)
        """
        work_exp = candidate.get("work_experience", [])
        if not work_exp:
            return 0.3  # 无工作经历，给基础分

        score = 0.0
        total_years = candidate.get("experience_years", 0)

        # 1. 晋升记录（最多 0.35 分）
        promotions = sum(1 for exp in work_exp if exp.get("promotion", False))
        score += min(promotions * 0.15, 0.35)

        # 2. 跳槽稳定性分析
        job_durations = []
        for exp in work_exp:
            years = exp.get("years", 0)
            job_durations.append(years)

        if job_durations:
            avg_duration = sum(job_durations) / len(job_durations)
            if avg_duration >= 3.0:
                score += 0.25  # 稳定，长期深耕
            elif avg_duration >= 2.0:
                score += 0.15  # 合理
            elif avg_duration >= 1.0:
                score += 0.05  # 偏短
            else:
                score -= 0.10  # 频繁跳槽，减分

        # 3. 公司多样性（适度加分，最多 0.15）
        companies = set(exp.get("company", "") for exp in work_exp)
        score += min(len(companies) * 0.05, 0.15)

        # 4. 职级成长轨迹（从低到高的发展路径加分）
        roles = [exp.get("role", "") for exp in work_exp]
        if len(roles) >= 2:
            # 检查是否有职级提升关键词
            senior_keywords = ["高级", "资深", "专家", "首席", "总监", "经理", "科学家"]
            has_senior = any(any(kw in role for kw in senior_keywords) for role in roles)
            if has_senior:
                score += 0.15

        # 5. 经验年限加分（资深者有积累）
        if total_years >= 10:
            score += 0.10
        elif total_years >= 5:
            score += 0.05

        return max(0.0, min(score, 1.0))

    def _calculate_skill_scarcity_score(self, candidate: Dict[str, Any],
                                       job_profile: Dict[str, Any]) -> float:
        """
        技能稀缺度评分（潜力评分子项，权重 25%）

        考量维度：
        - JD 要求中的核心技能，候选人具备则加分
        - 候选人拥有的非 JD 要求但高价值技能（如"团队管理"、"AI架构设计"）给予稀缺加分
        - 技能广度与深度的平衡

        Returns:
            技能稀缺度评分 (0-1)
        """
        candidate_skills = set(self._normalize_skill(s).lower() for s in candidate.get("skills", []))
        job_skills = set(self._normalize_skill(s).lower() for s in job_profile.get("skills", []))

        if not candidate_skills:
            return 0.0

        score = 0.0

        # 1. 核心技能覆盖度（JD 要求的技能匹配度）
        if job_skills:
            matched = candidate_skills & job_skills
            coverage = len(matched) / len(job_skills)
            score += coverage * 0.4

        # 2. 超出 JD 要求的额外技能（稀缺技能加分）
        extra_skills = candidate_skills - job_skills
        # 定义高价值/稀缺技能关键词
        scarce_keywords = {
            "强化学习", "分布式训练", "模型蒸馏", "ai架构设计", "团队管理",
            "技术规划", "模型优化", "distributed training", "model optimization",
            "技术专家", "首席科学家"
        }
        scarce_match = extra_skills & scarce_keywords
        score += min(len(scarce_match) * 0.15, 0.35)

        # 3. 技能广度（技能数量适中为佳，太多太杂也不好）
        skill_count = len(candidate_skills)
        if 5 <= skill_count <= 10:
            score += 0.15
        elif skill_count > 10:
            score += 0.10
        elif skill_count >= 3:
            score += 0.10

        # 4. 技能深度信号（具备深度相关的技能组合）
        depth_signals = {"pytorch", "tensorflow", "大模型", "nlp", "模型优化", "分布式训练"}
        depth_match = candidate_skills & depth_signals
        if len(depth_match) >= 3:
            score += 0.10

        return min(score, 1.0)

    def _calculate_industry_match_score(self, candidate: Dict[str, Any],
                                        job_profile: Dict[str, Any]) -> float:
        """
        行业匹配度评分（潜力评分子项，权重 15%）

        考量维度：
        - 候选人工作经历中的行业与 JD 行业匹配度
        - AI/互联网等高相关行业经验加分

        Returns:
            行业匹配度评分 (0-1)
        """
        job_industry = job_profile.get("industry", "").lower()
        work_exp = candidate.get("work_experience", [])

        if not job_industry or not work_exp:
            return 0.3  # 无行业信息，给基础分

        candidate_industries = []
        for exp in work_exp:
            ind = exp.get("industry", "").lower()
            if ind:
                candidate_industries.append(ind)

        if not candidate_industries:
            return 0.3

        # 精确匹配
        for ind in candidate_industries:
            if job_industry in ind or ind in job_industry:
                return 1.0

        # 模糊匹配（AI 相关行业互认）
        ai_related = {"ai", "人工智能", "互联网/ai", "互联网", "通信/ai", "金融科技"}
        job_is_ai = job_industry in ai_related or "ai" in job_industry
        for ind in candidate_industries:
            if job_is_ai and (ind in ai_related or "ai" in ind):
                return 0.7

        # 有相关行业经验
        return 0.4

    def _calculate_potential_score(self, candidate: Dict[str, Any],
                                   job_profile: Optional[Dict[str, Any]] = None) -> Tuple[float, Dict[str, float]]:
        """
        计算潜力分数（增强版）

        潜力评分 = 学历背景(30%) + 职业轨迹(30%) + 技能稀缺度(25%) + 行业匹配度(15%)

        Args:
            candidate: 候选人信息
            job_profile: 岗位画像（用于技能稀缺度和行业匹配度计算）

        Returns:
            (潜力总分, 各子维度分数字典)
        """
        if job_profile is None:
            job_profile = {}

        # 1. 学历背景（30%）
        edu_score = self._calculate_education_background_score(candidate)

        # 2. 职业轨迹（30%）
        career_score = self._calculate_career_trajectory_score(candidate)

        # 3. 技能稀缺度（25%）
        scarcity_score = self._calculate_skill_scarcity_score(candidate, job_profile)

        # 4. 行业匹配度（15%）
        industry_score = self._calculate_industry_match_score(candidate, job_profile)

        # 加权计算
        total = (
            edu_score * 0.30 +
            career_score * 0.30 +
            scarcity_score * 0.25 +
            industry_score * 0.15
        )

        sub_scores = {
            "education_background": round(edu_score, 4),
            "career_trajectory": round(career_score, 4),
            "skill_scarcity": round(scarcity_score, 4),
            "industry_match": round(industry_score, 4)
        }

        return min(total, 1.0), sub_scores

    # =====================================================================
    # 经验匹配 & 学历匹配（保持原有逻辑）
    # =====================================================================

    def _calculate_experience_match(self, job_years: int, candidate_years: int) -> float:
        """
        计算经验匹配度

        Args:
            job_years: 岗位要求年限
            candidate_years: 候选人实际年限

        Returns:
            经验匹配度分数 (0-1)
        """
        if job_years <= 0:
            return 1.0

        if candidate_years < job_years * 0.5:
            return 0.0
        elif candidate_years >= job_years:
            return 1.0
        else:
            # 线性插值
            ratio = candidate_years / job_years
            return 0.5 + (ratio - 0.5) * 0.5

    def _calculate_education_match(self, job_level: str, candidate_level: str) -> float:
        """
        计算学历匹配度

        Args:
            job_level: 岗位要求学历 (bachelor/master/phd)
            candidate_level: 候选人实际学历

        Returns:
            学历匹配度分数 (0-1)
        """
        job_score = self._education_hierarchy.get(job_level.lower(), 0)
        candidate_score = self._education_hierarchy.get(candidate_level.lower(), 0)

        if candidate_score >= job_score:
            return 1.0
        else:
            # 低于要求则扣分
            return candidate_score / job_score if job_score > 0 else 1.0

    # =====================================================================
    # 匹配理由生成（增强版，含弹性匹配标注）
    # =====================================================================

    def _generate_match_reason(self, job_profile: Dict[str, Any], candidate: Dict[str, Any],
                               scores: Dict[str, float], flexible_reasons: List[str],
                               potential_subscores: Dict[str, float]) -> str:
        """
        生成匹配理由说明（含弹性匹配标注）

        Args:
            job_profile: 岗位画像
            candidate: 候选人信息
            scores: 各维度分数
            flexible_reasons: 弹性匹配原因列表
            potential_subscores: 潜力评分各子维度分数

        Returns:
            匹配理由文本
        """
        reasons = []

        # 技能匹配理由
        if scores["skill"] > 0.7:
            matched_skills = set(self._normalize_skill(s).lower() for s in job_profile.get("skills", [])) & \
                           set(self._normalize_skill(s).lower() for s in candidate.get("skills", []))
            if matched_skills:
                reasons.append(f"技能匹配度高，掌握核心技能：{', '.join(list(matched_skills)[:3])}")
        elif scores["skill"] > 0.4:
            reasons.append("技能部分匹配，具备岗位所需部分核心能力")

        # 经验匹配理由
        if scores["experience"] > 0.8:
            reasons.append(f"经验丰富，工作{candidate.get('experience_years', 0)}年满足岗位要求")

        # 潜力理由（多维度）
        if scores["potential"] > 0.6:
            potential_parts = []
            if potential_subscores.get("education_background", 0) > 0.7:
                education_list = candidate.get("education", [])
                uni_name = ""
                for edu in education_list:
                    if isinstance(edu, dict) and self._is_top_university(edu.get("university", "")):
                        uni_name = edu.get("university", "")
                        break
                if uni_name:
                    potential_parts.append(f"名校背景({uni_name})")
                else:
                    potential_parts.append("学历背景优秀")
            if potential_subscores.get("career_trajectory", 0) > 0.6:
                potential_parts.append("职业成长轨迹良好")
            if potential_subscores.get("skill_scarcity", 0) > 0.6:
                potential_parts.append("具备稀缺技能")
            if potential_parts:
                reasons.append("潜力突出：" + "、".join(potential_parts))
            else:
                reasons.append("成长性强，具备良好发展潜力")

        # 行业经验理由
        job_industry = job_profile.get("industry", "")
        candidate_industries = [exp.get("industry", "") for exp in candidate.get("work_experience", [])]
        if job_industry and job_industry in candidate_industries:
            reasons.append(f"有{job_industry}行业经验")

        # 弹性匹配标注
        if flexible_reasons:
            reasons.append("【弹性匹配】" + "；".join(flexible_reasons))

        return "; ".join(reasons) if reasons else "基本符合岗位要求"

    # =====================================================================
    # 主匹配逻辑
    # =====================================================================

    def match(self, job_profile: Dict[str, Any], candidates: List[Dict[str, Any]],
              top_n: int = 10) -> List[Dict[str, Any]]:
        """
        执行人才匹配（Phase 3 增强版）

        Phase 3 新增：
        - 技能知识图谱关联加分：当候选人技能与JD技能不完全匹配时，通过图谱查找关联技能给予部分加分
        - 偏见检测：匹配完成后自动检测性别/年龄/地域/学历偏见
        - 查询引擎：匹配完成后初始化交互式查询引擎

        Args:
            job_profile: 岗位画像
            candidates: 候选人列表
            top_n: 返回前N个匹配结果

        Returns:
            匹配结果列表，按综合得分排序。每个结果包含 skill_graph_analysis 字段。
            匹配完成后可通过 self.bias_analysis 和 self.query_engine 访问偏见报告和查询引擎。
        """
        results = []

        for candidate in candidates:
            # 检查硬约束（弹性化）
            passed, flexible_reasons, penalty = self._check_hard_constraints(
                candidate, job_profile.get("constraints", {})
            )
            if not passed:
                continue

            # 计算技能匹配（语义化）
            skill_score, skill_subscores = self._calculate_skill_similarity(
                job_profile.get("skills", []),
                candidate.get("skills", [])
            )

            # 计算经验匹配
            exp_score = self._calculate_experience_match(
                job_profile.get("required_years", 0),
                candidate.get("experience_years", 0)
            )

            # 计算学历匹配
            edu_score = self._calculate_education_match(
                job_profile.get("required_education", "bachelor"),
                candidate.get("education_level", "bachelor")
            )

            # 计算潜力评分（增强版）
            potential_score, potential_subscores = self._calculate_potential_score(
                candidate, job_profile
            )

            # 汇总各维度分数
            scores = {
                "skill": skill_score,
                "experience": exp_score,
                "education": edu_score,
                "potential": potential_score
            }

            # 计算综合得分
            total_score = (
                scores["skill"] * self.weights.get("skill", 0.4) +
                scores["experience"] * self.weights.get("experience", 0.3) +
                scores["education"] * self.weights.get("education", 0.1) +
                scores["potential"] * self.weights.get("potential", 0.2)
            )

            # 应用弹性匹配惩罚系数
            if penalty < 1.0:
                total_score *= penalty

            # Phase 3: 技能知识图谱关联加分
            skill_graph_bonus, skill_graph_analysis = self._skill_graph.calculate_skill_bonus(
                job_profile.get("skills", []),
                candidate.get("skills", []),
                max_bonus=self.skill_graph_max_bonus
            )
            # skill_graph_bonus 是 0-0.15 的值，加到 0-1 的 total_score 上
            total_score += skill_graph_bonus
            # 百分制加分值（用于显示）
            skill_graph_bonus_points = round(skill_graph_bonus * 100, 2)

            # 生成匹配理由
            match_reason = self._generate_match_reason(
                job_profile, candidate, scores, flexible_reasons, potential_subscores
            )

            # Phase 3: 在匹配理由中追加技能图谱加分信息
            if skill_graph_analysis["details"]:
                graph_details = skill_graph_analysis["details"]
                detail_texts = []
                for d in graph_details:
                    detail_texts.append(
                        f"{d['job_skill']}<-{d['matched_via']}(强度:{d['relation_strength']})"
                    )
                match_reason += f"; 【技能图谱加分】{'，'.join(detail_texts)}（+{skill_graph_bonus_points}分）"

            # 构建结果
            result = {
                "candidate_id": candidate.get("id"),
                "candidate_name": candidate.get("name", "Unknown"),
                "total_score": round(total_score * 100, 2),
                "scores": {k: round(v * 100, 2) for k, v in scores.items()},
                "skill_subscores": skill_subscores,
                "potential_subscores": potential_subscores,
                "flexible_match": flexible_reasons if flexible_reasons else None,
                "penalty_applied": round(penalty, 4) if penalty < 1.0 else None,
                "match_reason": match_reason,
                "skill_graph_analysis": skill_graph_analysis,
                "profile": candidate
            }

            results.append(result)

        # 按综合得分排序
        results.sort(key=lambda x: x["total_score"], reverse=True)
        results = results[:top_n]

        # Phase 3: 偏见检测
        try:
            detector = BiasDetector(pass_threshold=60.0)
            self.bias_analysis = detector.detect_all(results, candidates)
        except Exception as e:
            print(f"⚠️ 偏见检测执行失败: {e}")
            self.bias_analysis = {"error": str(e), "summary": "偏见检测执行失败"}

        # Phase 3: 初始化查询引擎
        try:
            self.query_engine = QueryEngine(results)
        except Exception as e:
            print(f"⚠️ 查询引擎初始化失败: {e}")
            self.query_engine = None

        return results


def load_json(file_path: str) -> Any:
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, file_path: str) -> None:
    """保存 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='人才匹配脚本（Phase 3 增强版）')
    parser.add_argument('--job', required=True, help='岗位画像文件路径（JSON格式）')
    parser.add_argument('--candidates', required=True, help='候选人画像列表文件路径（JSON格式）')
    parser.add_argument('--weights', required=True, help='权重配置文件路径（JSON格式）')
    parser.add_argument('--output', required=True, help='输出文件路径（JSON格式）')
    parser.add_argument('--top-n', type=int, default=10, help='返回前N个匹配结果')

    args = parser.parse_args()

    # 加载数据
    print(f"加载岗位画像: {args.job}")
    job_profile = load_json(args.job)

    print(f"加载候选人列表: {args.candidates}")
    candidates = load_json(args.candidates)

    print(f"加载权重配置: {args.weights}")
    weights = load_json(args.weights)

    # 执行匹配
    print(f"开始匹配分析，共有 {len(candidates)} 位候选人...")
    matcher = TalentMatcher(weights)
    results = matcher.match(job_profile, candidates, top_n=args.top_n)

    # Phase 3: 构建包含偏见分析和技能图谱数据的完整输出
    output_data = {
        "results": results,
        "bias_analysis": matcher.bias_analysis,
        "skill_graph_summary": matcher._skill_graph.get_graph_summary(),
        "skill_graph_data": matcher._skill_graph.export_graph_json()
    }

    # 保存结果
    print(f"保存结果到: {args.output}")
    save_json(output_data, args.output)

    # 输出统计信息
    print("\n匹配结果统计:")
    print(f"  输入候选人数: {len(candidates)}")
    print(f"  匹配成功数: {len(results)}")
    if results:
        print(f"  最高得分: {results[0]['total_score']}")
        print(f"  最低得分: {results[-1]['total_score']}")
        print(f"  平均得分: {sum(r['total_score'] for r in results) / len(results):.2f}")

        # 输出弹性匹配详情
        flexible_count = sum(1 for r in results if r.get('flexible_match'))
        if flexible_count:
            print(f"  弹性匹配人数: {flexible_count}")
            for r in results:
                if r.get('flexible_match'):
                    print(f"    - {r['candidate_name']}: {'; '.join(r['flexible_match'])}")

        # 输出技能语义匹配详情
        print("\n  技能匹配详情 (Jaccard + 语义):")
        for r in results:
            subs = r.get('skill_subscores', {})
            print(f"    {r['candidate_name']}: Jaccard={subs.get('jaccard', 0):.2f}, "
                  f"Semantic={subs.get('semantic', 0):.2f}, "
                  f"Combined={r['scores']['skill']:.1f}")

        # 输出潜力评分详情
        print("\n  潜力评分详情 (学历30% + 职业轨迹30% + 技能稀缺25% + 行业匹配15%):")
        for r in results:
            subs = r.get('potential_subscores', {})
            print(f"    {r['candidate_name']}: 学历={subs.get('education_background', 0):.2f}, "
                  f"职业={subs.get('career_trajectory', 0):.2f}, "
                  f"稀缺={subs.get('skill_scarcity', 0):.2f}, "
                  f"行业={subs.get('industry_match', 0):.2f}, "
                  f"总分={r['scores']['potential']:.1f}")

        # Phase 3: 输出技能图谱加分详情
        print("\n  技能图谱加分详情:")
        for r in results:
            graph = r.get('skill_graph_analysis', {})
            if graph.get('details'):
                print(f"    {r['candidate_name']}: 加分={graph['bonus']*100:.2f}分")
                for d in graph['details']:
                    print(f"      JD技能[{d['job_skill']}] <- 候选人技能[{d['matched_via']}] "
                          f"(强度:{d['relation_strength']}, +{d['bonus_points']}分)")
            else:
                print(f"    {r['candidate_name']}: 无图谱加分")

        # Phase 3: 输出偏见检测结果
        if matcher.bias_analysis and 'summary' in matcher.bias_analysis:
            print(f"\n  偏见检测结果:")
            print(f"    综合风险: {matcher.bias_analysis.get('overall_risk', '未知')}")
            print(f"    检测到偏见数: {matcher.bias_analysis.get('detected_count', 0)}")
            print(f"    摘要: {matcher.bias_analysis.get('summary', '无')}")

        # Phase 3: 输出查询引擎状态
        if matcher.query_engine:
            print(f"\n  查询引擎已初始化（当前{len(matcher.query_engine)}条结果可查询）")

    print("\n匹配完成!")


if __name__ == "__main__":
    main()
