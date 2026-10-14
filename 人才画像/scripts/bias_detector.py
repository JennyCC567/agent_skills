#!/usr/bin/env python3
"""
偏见检测模块（Phase 3 增强）

功能：
1. 检测匹配结果中可能存在的偏见：
   - 性别偏见：检查不同性别的候选人通过率是否有显著差异
   - 年龄偏见：检查不同年龄段（<30, 30-40, >40）的匹配率差异
   - 地域偏见：检查特定地域候选人是否被系统性低估
   - 学历偏见：检查非名校但经验丰富者是否被过度惩罚
2. 提供 BiasDetector 类，输入匹配结果列表，输出偏见检测报告（dict格式）
3. 在 talent_matcher.py 的匹配结果中附加 bias_analysis 字段
4. 在 report_generator.py 中增加偏见检测报告章节

检测逻辑使用统计学基础方法（通过率比较、均值差异），不依赖外部库
"""

import json
import argparse
import math
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict


class BiasDetector:
    """偏见检测器"""

    # 年龄分段
    AGE_GROUPS = {
        "young": "30岁以下",
        "middle": "30-40岁",
        "senior": "40岁以上"
    }

    # 偏见阈值
    PASS_RATE_DIFF_THRESHOLD = 0.15  # 通过率差异阈值（15%）
    SCORE_DIFF_THRESHOLD = 10.0      # 分数差异阈值（10分）
    MIN_GROUP_SIZE = 2               # 最小分组大小（低于此值不进行检测）

    # 985/211名校列表（与 talent_matcher.py 保持一致）
    TOP_UNIVERSITIES = {
        "清华大学", "北京大学", "复旦大学", "上海交通大学", "浙江大学",
        "中国科学技术大学", "南京大学", "华中科技大学", "武汉大学", "中山大学",
        "西安交通大学", "哈尔滨工业大学", "同济大学", "四川大学", "东南大学",
        "北京航空航天大学", "北京师范大学", "南开大学", "天津大学", "厦门大学",
        "吉林大学", "山东大学", "中南大学", "大连理工大学", "电子科技大学",
        "重庆大学", "兰州大学", "东北大学", "湖南大学", "西北农林科技大学",
        "中国海洋大学", "国防科技大学", "中央民族大学", "华南理工大学", "华东师范大学",
        "中国人民大学", "中国农业大学", "北京理工大学", "西北工业大学",
        "北京交通大学", "北京邮电大学", "北京化工大学", "北京外国语大学",
        "上海财经大学", "上海大学", "上海外国语大学", "华东理工大学",
        "南京航空航天大学", "南京理工大学", "南京师范大学", "苏州大学",
        "武汉理工大学", "中南财经政法大学", "西南财经大学", "西南交通大学",
        "西安电子科技大学", "哈尔滨工程大学", "合肥工业大学", "暨南大学",
        "华北电力大学", "中国传媒大学", "中央财经大学", "对外经济贸易大学",
        "北京科技大学", "东华大学", "河海大学", "中国政法大学",
        "Tsinghua", "Peking", "MIT", "Stanford", "Berkeley", "CMU",
        "Zhejiang", "Fudan", "SJTU", "USTC", "Nanjing", "Nankai", "Tongji",
    }

    def __init__(self, pass_threshold: float = 60.0):
        """
        初始化偏见检测器

        Args:
            pass_threshold: 通过阈值（匹配分数>=此值视为"通过"）
        """
        self.pass_threshold = pass_threshold

    def _is_top_university(self, university: str) -> bool:
        """检查是否为名校"""
        if not university:
            return False
        uni_lower = university.lower().strip()
        for uni in self.TOP_UNIVERSITIES:
            if uni.lower() == uni_lower or uni in university or university in uni:
                return True
        return False

    def _get_candidate_gender(self, candidate: Dict[str, Any]) -> str:
        """获取候选人性别"""
        profile = candidate.get("profile", candidate)
        gender = profile.get("gender", candidate.get("gender", ""))
        if not gender:
            # 尝试从姓名推断（中文姓名最后字）
            name = candidate.get("candidate_name", profile.get("name", ""))
            if name:
                last_char = name[-1] if len(name) >= 1 else ""
                # 常见女性用字
                female_chars = {"婷", "华", "芳", "丽", "敏", "静", "燕", "梅", "玲", "红",
                                "霞", "娟", "琳", "萍", "娜", "莹", "倩", "颖", "雯", "薇"}
                if last_char in female_chars:
                    return "female"
                return "male"
        return gender.lower() if gender else "unknown"

    def _get_candidate_age_group(self, candidate: Dict[str, Any]) -> str:
        """获取候选人年龄段"""
        profile = candidate.get("profile", candidate)
        age = profile.get("age", candidate.get("age", 0))
        if not age:
            # 尝试从经验年限估算年龄（假设22岁开始工作）
            exp_years = profile.get("experience_years", candidate.get("experience_years", 0))
            estimated_age = 22 + exp_years
            age = estimated_age

        if age < 30:
            return "young"
        elif age <= 40:
            return "middle"
        else:
            return "senior"

    def _get_candidate_location(self, candidate: Dict[str, Any]) -> str:
        """获取候选人地域"""
        profile = candidate.get("profile", candidate)
        location = profile.get("current_location", candidate.get("current_location", ""))
        if not location:
            work_exp = profile.get("work_experience", [])
            if work_exp:
                location = work_exp[-1].get("location", "")
        return location or "unknown"

    def _get_candidate_university(self, candidate: Dict[str, Any]) -> str:
        """获取候选人毕业院校"""
        profile = candidate.get("profile", candidate)
        education = profile.get("education", candidate.get("education", []))
        if isinstance(education, list) and education:
            for edu in education:
                if isinstance(edu, dict):
                    uni = edu.get("university", "")
                    if uni:
                        return uni
        return ""

    def _get_candidate_score(self, candidate: Dict[str, Any]) -> float:
        """获取候选人匹配分数"""
        return float(candidate.get("total_score", candidate.get("match_score", 0)))

    def _is_passed(self, candidate: Dict[str, Any]) -> bool:
        """判断候选人是否通过"""
        return self._get_candidate_score(candidate) >= self.pass_threshold

    def _cohen_d(self, group1: List[float], group2: List[float]) -> float:
        """
        计算Cohen's d效应量

        d = (mean1 - mean2) / pooled_std

        Returns:
            Cohen's d 值
        """
        if len(group1) < 2 or len(group2) < 2:
            diff = (sum(group1) / len(group1) - sum(group2) / len(group2)) if group1 and group2 else 0
            return diff / 10.0  # 粗略估计

        mean1 = sum(group1) / len(group1)
        mean2 = sum(group2) / len(group2)

        var1 = sum((x - mean1) ** 2 for x in group1) / (len(group1) - 1)
        var2 = sum((x - mean2) ** 2 for x in group2) / (len(group2) - 1)

        pooled_std = math.sqrt((var1 + var2) / 2)
        if pooled_std == 0:
            return 0.0

        return (mean1 - mean2) / pooled_std

    def _interpret_effect_size(self, d: float) -> str:
        """解释效应量"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "可忽略"
        elif abs_d < 0.5:
            return "小效应"
        elif abs_d < 0.8:
            return "中等效应"
        else:
            return "大效应"

    def _interpret_risk_level(self, d: float, rate_diff: float) -> str:
        """评估偏见风险等级"""
        abs_d = abs(d)
        abs_rate = abs(rate_diff)
        if abs_d >= 0.8 or abs_rate >= self.PASS_RATE_DIFF_THRESHOLD:
            return "高风险"
        elif abs_d >= 0.5 or abs_rate >= self.PASS_RATE_DIFF_THRESHOLD * 0.5:
            return "中风险"
        elif abs_d >= 0.2:
            return "低风险"
        else:
            return "无风险"

    # =====================================================================
    # 偏见检测方法
    # =====================================================================

    def detect_gender_bias(self, results: List[Dict[str, Any]],
                           all_candidates: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        性别偏见检测

        检查不同性别的候选人通过率和平均匹配分数是否有显著差异

        Args:
            results: 匹配结果列表
            all_candidates: 所有候选人列表（含未匹配的，用于计算通过率）

        Returns:
            性别偏见检测报告
        """
        # 按性别分组
        gender_scores = defaultdict(list)
        gender_passed = defaultdict(int)
        gender_total = defaultdict(int)

        # 使用匹配结果
        for r in results:
            gender = self._get_candidate_gender(r)
            score = self._get_candidate_score(r)
            gender_scores[gender].append(score)
            gender_total[gender] += 1
            if self._is_passed(r):
                gender_passed[gender] += 1

        # 如果有全部候选人数据，补充未匹配的
        if all_candidates:
            matched_ids = {r.get("candidate_id") for r in results}
            for c in all_candidates:
                cid = c.get("id")
                if cid and cid not in matched_ids:
                    gender = self._get_candidate_gender(c)
                    gender_total[gender] += 1

        # 计算统计量
        groups = {}
        for gender, scores in gender_scores.items():
            total = gender_total[gender]
            passed = gender_passed[gender]
            groups[gender] = {
                "count": total,
                "matched_count": len(scores),
                "pass_count": passed,
                "pass_rate": round(passed / total, 4) if total > 0 else 0,
                "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
                "max_score": round(max(scores), 2) if scores else 0,
                "min_score": round(min(scores), 2) if scores else 0,
            }

        # 比较性别间差异
        comparisons = []
        genders = list(groups.keys())
        for i in range(len(genders)):
            for j in range(i + 1, len(genders)):
                g1, g2 = genders[i], genders[j]
                scores1 = gender_scores.get(g1, [])
                scores2 = gender_scores.get(g2, [])

                if len(scores1) >= 1 and len(scores2) >= 1:
                    d = self._cohen_d(scores1, scores2)
                    rate_diff = groups[g1]["pass_rate"] - groups[g2]["pass_rate"]
                    score_diff = groups[g1]["avg_score"] - groups[g2]["avg_score"]

                    comparisons.append({
                        "group_a": g1,
                        "group_b": g2,
                        "score_diff": round(score_diff, 2),
                        "pass_rate_diff": round(rate_diff, 4),
                        "cohen_d": round(d, 4),
                        "effect_size": self._interpret_effect_size(d),
                        "risk_level": self._interpret_risk_level(d, rate_diff)
                    })

        # 判断是否存在偏见
        has_bias = any(c["risk_level"] in ["高风险", "中风险"] for c in comparisons)
        bias_details = [c for c in comparisons if c["risk_level"] in ["高风险", "中风险"]]

        return {
            "bias_type": "性别偏见",
            "detected": has_bias,
            "risk_level": max((c["risk_level"] for c in comparisons), key=lambda x: ["无风险", "低风险", "中风险", "高风险"].index(x)) if comparisons else "无风险",
            "groups": groups,
            "comparisons": comparisons,
            "bias_details": bias_details,
            "recommendation": self._generate_recommendation("性别", has_bias, bias_details) if has_bias else "未检测到显著性别偏见"
        }

    def detect_age_bias(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        年龄偏见检测

        检查不同年龄段（<30, 30-40, >40）的匹配率和平均分差异

        Args:
            results: 匹配结果列表

        Returns:
            年龄偏见检测报告
        """
        age_scores = defaultdict(list)
        age_passed = defaultdict(int)
        age_total = defaultdict(int)

        for r in results:
            age_group = self._get_candidate_age_group(r)
            score = self._get_candidate_score(r)
            age_scores[age_group].append(score)
            age_total[age_group] += 1
            if self._is_passed(r):
                age_passed[age_group] += 1

        groups = {}
        for ag, scores in age_scores.items():
            total = age_total[ag]
            passed = age_passed[ag]
            groups[ag] = {
                "label": self.AGE_GROUPS.get(ag, ag),
                "count": total,
                "pass_count": passed,
                "pass_rate": round(passed / total, 4) if total > 0 else 0,
                "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
                "max_score": round(max(scores), 2) if scores else 0,
                "min_score": round(min(scores), 2) if scores else 0,
            }

        # 比较
        comparisons = []
        age_groups = list(groups.keys())
        for i in range(len(age_groups)):
            for j in range(i + 1, len(age_groups)):
                a1, a2 = age_groups[i], age_groups[j]
                scores1 = age_scores.get(a1, [])
                scores2 = age_scores.get(a2, [])

                if len(scores1) >= 1 and len(scores2) >= 1:
                    d = self._cohen_d(scores1, scores2)
                    rate_diff = groups[a1]["pass_rate"] - groups[a2]["pass_rate"]
                    score_diff = groups[a1]["avg_score"] - groups[a2]["avg_score"]

                    comparisons.append({
                        "group_a": groups[a1]["label"],
                        "group_b": groups[a2]["label"],
                        "score_diff": round(score_diff, 2),
                        "pass_rate_diff": round(rate_diff, 4),
                        "cohen_d": round(d, 4),
                        "effect_size": self._interpret_effect_size(d),
                        "risk_level": self._interpret_risk_level(d, rate_diff)
                    })

        has_bias = any(c["risk_level"] in ["高风险", "中风险"] for c in comparisons)
        bias_details = [c for c in comparisons if c["risk_level"] in ["高风险", "中风险"]]

        return {
            "bias_type": "年龄偏见",
            "detected": has_bias,
            "risk_level": max((c["risk_level"] for c in comparisons), key=lambda x: ["无风险", "低风险", "中风险", "高风险"].index(x)) if comparisons else "无风险",
            "groups": groups,
            "comparisons": comparisons,
            "bias_details": bias_details,
            "recommendation": self._generate_recommendation("年龄", has_bias, bias_details) if has_bias else "未检测到显著年龄偏见"
        }

    def detect_geographic_bias(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        地域偏见检测

        检查特定地域候选人是否被系统性低估

        Args:
            results: 匹配结果列表

        Returns:
            地域偏见检测报告
        """
        loc_scores = defaultdict(list)
        loc_passed = defaultdict(int)
        loc_total = defaultdict(int)

        for r in results:
            location = self._get_candidate_location(r)
            score = self._get_candidate_score(r)
            loc_scores[location].append(score)
            loc_total[location] += 1
            if self._is_passed(r):
                loc_passed[location] += 1

        groups = {}
        for loc, scores in loc_scores.items():
            total = loc_total[loc]
            passed = loc_passed[loc]
            groups[loc] = {
                "count": total,
                "pass_count": passed,
                "pass_rate": round(passed / total, 4) if total > 0 else 0,
                "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
            }

        # 计算全局平均分
        all_scores = [self._get_candidate_score(r) for r in results]
        global_avg = sum(all_scores) / len(all_scores) if all_scores else 0

        # 检查是否有地域被系统性低估
        comparisons = []
        locations = list(groups.keys())
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                l1, l2 = locations[i], locations[j]
                scores1 = loc_scores.get(l1, [])
                scores2 = loc_scores.get(l2, [])

                if len(scores1) >= 1 and len(scores2) >= 1:
                    d = self._cohen_d(scores1, scores2)
                    rate_diff = groups[l1]["pass_rate"] - groups[l2]["pass_rate"]
                    score_diff = groups[l1]["avg_score"] - groups[l2]["avg_score"]

                    comparisons.append({
                        "group_a": l1,
                        "group_b": l2,
                        "score_diff": round(score_diff, 2),
                        "pass_rate_diff": round(rate_diff, 4),
                        "cohen_d": round(d, 4),
                        "effect_size": self._interpret_effect_size(d),
                        "risk_level": self._interpret_risk_level(d, rate_diff)
                    })

        # 检查是否有地域显著低于全局平均
        underperforming = []
        for loc, info in groups.items():
            if info["count"] >= self.MIN_GROUP_SIZE:
                diff = info["avg_score"] - global_avg
                if diff < -self.SCORE_DIFF_THRESHOLD:
                    underperforming.append({
                        "location": loc,
                        "avg_score": info["avg_score"],
                        "global_avg": round(global_avg, 2),
                        "score_gap": round(diff, 2),
                        "risk_level": "中风险" if diff < -20 else "低风险"
                    })

        has_bias = (any(c["risk_level"] in ["高风险", "中风险"] for c in comparisons)
                    or len(underperforming) > 0)

        return {
            "bias_type": "地域偏见",
            "detected": has_bias,
            "risk_level": "中风险" if underperforming else "无风险",
            "global_avg_score": round(global_avg, 2),
            "groups": groups,
            "comparisons": comparisons,
            "underperforming_locations": underperforming,
            "recommendation": self._generate_recommendation("地域", has_bias, underperforming) if has_bias else "未检测到显著地域偏见"
        }

    def detect_education_bias(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        学历偏见检测

        检查非名校但经验丰富者是否被过度惩罚

        逻辑：
        - 将候选人分为"名校"和"非名校"两组
        - 在经验年限相似的情况下，比较两组的匹配分数差异
        - 特别关注"非名校+经验丰富"的候选人是否分数偏低

        Args:
            results: 匹配结果列表

        Returns:
            学历偏见检测报告
        """
        top_uni_scores = []
        non_top_uni_scores = []
        top_uni_experienced = []
        non_top_uni_experienced = []

        group_details = {
            "top_university": {"count": 0, "scores": [], "avg_score": 0, "pass_rate": 0},
            "non_top_university": {"count": 0, "scores": [], "avg_score": 0, "pass_rate": 0}
        }

        for r in results:
            profile = r.get("profile", r)
            university = self._get_candidate_university(r)
            is_top = self._is_top_university(university)
            score = self._get_candidate_score(r)
            exp_years = profile.get("experience_years", 0)

            if is_top:
                top_uni_scores.append(score)
                group_details["top_university"]["count"] += 1
                if exp_years >= 5:
                    top_uni_experienced.append(score)
            else:
                non_top_uni_scores.append(score)
                group_details["non_top_university"]["count"] += 1
                if exp_years >= 5:
                    non_top_uni_experienced.append(score)

        # 计算各组统计量
        for key, scores_list in [("top_university", top_uni_scores), ("non_top_university", non_top_uni_scores)]:
            if scores_list:
                group_details[key]["scores"] = scores_list
                group_details[key]["avg_score"] = round(sum(scores_list) / len(scores_list), 2)
                group_details[key]["pass_rate"] = round(
                    sum(1 for s in scores_list if s >= self.pass_threshold) / len(scores_list), 4
                )
                group_details[key]["max_score"] = round(max(scores_list), 2)
                group_details[key]["min_score"] = round(min(scores_list), 2)

        # 比较名校vs非名校
        comparison = None
        if top_uni_scores and non_top_uni_scores:
            d = self._cohen_d(top_uni_scores, non_top_uni_scores)
            score_diff = group_details["top_university"]["avg_score"] - group_details["non_top_university"]["avg_score"]
            rate_diff = group_details["top_university"]["pass_rate"] - group_details["non_top_university"]["pass_rate"]

            comparison = {
                "group_a": "名校",
                "group_b": "非名校",
                "score_diff": round(score_diff, 2),
                "pass_rate_diff": round(rate_diff, 4),
                "cohen_d": round(d, 4),
                "effect_size": self._interpret_effect_size(d),
                "risk_level": self._interpret_risk_level(d, rate_diff)
            }

        # 特别检测：非名校+经验丰富者是否被过度惩罚
        experienced_bias = None
        if top_uni_experienced and non_top_uni_experienced:
            exp_d = self._cohen_d(top_uni_experienced, non_top_uni_experienced)
            exp_score_diff = (sum(top_uni_experienced) / len(top_uni_experienced)) - \
                           (sum(non_top_uni_experienced) / len(non_top_uni_experienced))

            experienced_bias = {
                "description": "经验丰富的非名校候选人 vs 经验丰富的名校候选人",
                "top_uni_experienced_avg": round(sum(top_uni_experienced) / len(top_uni_experienced), 2),
                "non_top_uni_experienced_avg": round(sum(non_top_uni_experienced) / len(non_top_uni_experienced), 2),
                "score_diff": round(exp_score_diff, 2),
                "cohen_d": round(exp_d, 4),
                "effect_size": self._interpret_effect_size(exp_d),
                "over_penalized": exp_score_diff > self.SCORE_DIFF_THRESHOLD,
                "risk_level": "高风险" if exp_score_diff > 20 else ("中风险" if exp_score_diff > 10 else "低风险") if exp_score_diff > 0 else "无风险"
            }

        # 判断偏见
        has_bias = False
        risk_level = "无风险"
        if comparison and comparison["risk_level"] in ["高风险", "中风险"]:
            has_bias = True
            risk_level = comparison["risk_level"]
        if experienced_bias and experienced_bias.get("over_penalized"):
            has_bias = True
            risk_level = "高风险" if risk_level != "高风险" and experienced_bias["risk_level"] == "高风险" else risk_level

        bias_details = []
        if comparison and comparison["risk_level"] in ["高风险", "中风险"]:
            bias_details.append(comparison)
        if experienced_bias and experienced_bias.get("over_penalized"):
            bias_details.append(experienced_bias)

        return {
            "bias_type": "学历偏见",
            "detected": has_bias,
            "risk_level": risk_level,
            "groups": group_details,
            "comparison": comparison,
            "experienced_bias_analysis": experienced_bias,
            "bias_details": bias_details,
            "recommendation": self._generate_recommendation("学历", has_bias, bias_details) if has_bias else "未检测到显著学历偏见"
        }

    def _generate_recommendation(self, bias_type: str, has_bias: bool,
                                 details: List[Dict[str, Any]]) -> str:
        """生成偏见抑制建议"""
        if not has_bias:
            return f"未检测到显著{bias_type}偏见"

        recs = [f"检测到可能的{bias_type}偏见，建议采取以下措施："]

        for d in details:
            if "score_diff" in d:
                if d.get("over_penalized"):
                    recs.append(f"  - 经验丰富的非名校候选人平均分低于名校候选人 {d.get('score_diff', 0)} 分，"
                               f"建议调整匹配权重，增加经验年限的权重占比")
                elif "group_a" in d:
                    risk = d.get("risk_level", "")
                    recs.append(f"  - {d.get('group_a', '')} vs {d.get('group_b', '')}: "
                               f"分数差异 {d.get('score_diff', 0)} 分（{risk}），"
                               f"建议审查评分逻辑中是否存在隐含偏见")

        recs.append("  - 建议引入公平性约束，对受影响群体给予适当补偿分数")
        recs.append("  - 建议增加人工复核环节，对边缘候选人进行二次评估")

        return "\n".join(recs)

    # =====================================================================
    # 综合检测
    # =====================================================================

    def detect_all(self, results: List[Dict[str, Any]],
                   all_candidates: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行全面的偏见检测

        Args:
            results: 匹配结果列表
            all_candidates: 所有候选人列表（含未匹配的）

        Returns:
            完整的偏见检测报告
        """
        if not results:
            return {
                "error": "匹配结果为空，无法进行偏见检测",
                "bias_reports": {},
                "overall_risk": "无风险",
                "summary": "无数据可分析"
            }

        gender_report = self.detect_gender_bias(results, all_candidates)
        age_report = self.detect_age_bias(results)
        geo_report = self.detect_geographic_bias(results)
        edu_report = self.detect_education_bias(results)

        # 综合风险评估
        risk_levels = [r["risk_level"] for r in [gender_report, age_report, geo_report, edu_report]]
        risk_order = ["无风险", "低风险", "中风险", "高风险"]
        overall_risk = max(risk_levels, key=lambda x: risk_order.index(x)) if risk_levels else "无风险"

        # 检测到的偏见数量
        detected_count = sum(1 for r in [gender_report, age_report, geo_report, edu_report] if r["detected"])

        summary_parts = []
        if gender_report["detected"]:
            summary_parts.append(f"性别偏见({gender_report['risk_level']})")
        if age_report["detected"]:
            summary_parts.append(f"年龄偏见({age_report['risk_level']})")
        if geo_report["detected"]:
            summary_parts.append(f"地域偏见({geo_report['risk_level']})")
        if edu_report["detected"]:
            summary_parts.append(f"学历偏见({edu_report['risk_level']})")

        summary = f"共检测到 {detected_count} 项潜在偏见" if detected_count > 0 else "未检测到显著偏见"
        if summary_parts:
            summary += "：" + "、".join(summary_parts)

        return {
            "bias_reports": {
                "gender_bias": gender_report,
                "age_bias": age_report,
                "geographic_bias": geo_report,
                "education_bias": edu_report
            },
            "overall_risk": overall_risk,
            "detected_count": detected_count,
            "summary": summary,
            "pass_threshold": self.pass_threshold,
            "total_candidates_analyzed": len(results),
            "recommendations": self._collect_recommendations(gender_report, age_report, geo_report, edu_report)
        }

    def _collect_recommendations(self, *reports) -> List[str]:
        """收集所有偏见抑制建议"""
        recs = []
        for report in reports:
            if report["detected"]:
                recs.append(report["recommendation"])
        return recs


# =====================================================================
# 独立运行入口
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description='偏见检测器（Phase 3）')
    parser.add_argument('--data', required=True, help='匹配结果JSON文件路径')
    parser.add_argument('--all-candidates', help='全部候选人JSON文件路径（可选，用于更准确的通过率计算）')
    parser.add_argument('--output', help='输出报告JSON文件路径')
    parser.add_argument('--threshold', type=float, default=60.0, help='通过阈值（默认60分）')

    args = parser.parse_args()

    # 加载数据
    with open(args.data, 'r', encoding='utf-8') as f:
        loaded = json.load(f)

    # Phase 3: 兼容 talent_matcher.py 新输出格式（dict with "results" key）
    if isinstance(loaded, dict) and 'results' in loaded:
        results = loaded['results']
    else:
        results = loaded

    all_candidates = None
    if args.all_candidates:
        with open(args.all_candidates, 'r', encoding='utf-8') as f:
            all_candidates = json.load(f)

    # 执行偏见检测
    detector = BiasDetector(pass_threshold=args.threshold)
    report = detector.detect_all(results, all_candidates)

    # 输出报告
    print("=" * 60)
    print("偏见检测报告")
    print("=" * 60)
    print(f"  分析候选人数量: {report['total_candidates_analyzed']}")
    print(f"  通过阈值: {report['pass_threshold']} 分")
    print(f"  综合风险等级: {report['overall_risk']}")
    print(f"  检测到偏见数量: {report['detected_count']}")
    print(f"  摘要: {report['summary']}")

    # 输出各维度详情
    for bias_key, bias_report in report['bias_reports'].items():
        print(f"\n{'─' * 60}")
        print(f"  [{bias_report['bias_type']}]")
        print(f"  检测到偏见: {'是' if bias_report['detected'] else '否'}")
        print(f"  风险等级: {bias_report['risk_level']}")

        if 'groups' in bias_report:
            print(f"  分组统计:")
            for group_name, stats in bias_report['groups'].items():
                if isinstance(stats, dict) and 'avg_score' in stats:
                    print(f"    {group_name}: 人数={stats.get('count', 0)}, "
                          f"平均分={stats.get('avg_score', 0)}, "
                          f"通过率={stats.get('pass_rate', 0)}")

        if bias_report.get('comparisons'):
            print(f"  组间比较:")
            for comp in bias_report['comparisons']:
                print(f"    {comp.get('group_a', '')} vs {comp.get('group_b', '')}: "
                      f"分数差={comp.get('score_diff', 0)}, "
                      f"效应量={comp.get('effect_size', '')}, "
                      f"风险={comp.get('risk_level', '')}")

        if bias_report['detected']:
            print(f"  建议: {bias_report['recommendation']}")

    # 输出综合建议
    if report['recommendations']:
        print(f"\n{'=' * 60}")
        print("综合偏见抑制建议:")
        for rec in report['recommendations']:
            print(f"  {rec}")

    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n偏见检测报告已保存到: {args.output}")

    print(f"\n{'=' * 60}")
    print("偏见检测完成!")


if __name__ == "__main__":
    main()
