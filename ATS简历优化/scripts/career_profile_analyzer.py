#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业阶段分析与简历策略推荐模块
从简历文本中提取工作年限，自动判断职业阶段，输出个性化简历优化策略

使用方式：
  python scripts/career_profile_analyzer.py --resume resume.txt --output result.json
  python scripts/career_profile_analyzer.py --resume resume.txt --job-category 技术 --output result.json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple


class CareerProfileAnalyzer:
    """职业阶段分析与简历策略推荐引擎"""

    # ============================================================
    # 职业阶段定义
    # ============================================================
    CAREER_STAGES = {
        '应届生': {
            'range': (0, 0),
            'label': '应届毕业生 / 在校生',
            'description': '尚未正式入职，以教育背景、实习经历和项目经验为核心竞争力'
        },
        '1-3年': {
            'range': (1, 3),
            'label': '职场成长期',
            'description': '具备基础实操经验，需突出技能成长与项目成果'
        },
        '3-5年': {
            'range': (3, 5),
            'label': '专业成熟期',
            'description': '独立负责模块，需突出专业能力深度与业绩数据'
        },
        '5-10年': {
            'range': (5, 10),
            'label': '管理转型期',
            'description': '具备管理经验或资深专业能力，需突出管理成果与业务影响'
        },
        '10年+': {
            'range': (10, 99),
            'label': '战略领导期',
            'description': '高层管理或行业专家，需突出战略视野与行业影响力'
        }
    }

    # ============================================================
    # 岗位类型定义
    # ============================================================
    JOB_CATEGORIES = {
        '技术岗': {
            'keywords': [
                '开发', '工程师', '架构', '算法', '测试', '运维', '前端', '后端',
                '全栈', '数据', 'DBA', '安全', '嵌入式', '硬件', '固件', '研发',
                'Java', 'Python', 'Go', 'C++', 'React', 'Vue', 'Linux', 'K8s',
                'Docker', 'MySQL', 'Redis', '微服务', '分布式', '机器学习',
                '深度学习', 'NLP', 'CV', '大数据', '云计算', 'DevOps', 'SRE',
                '技术总监', 'CTO', '技术经理'
            ],
            'weight': 0.35
        },
        '管理岗': {
            'keywords': [
                '总监', '经理', '主管', 'VP', '总裁', '总经理', 'CEO', 'COO',
                '负责人', '部长', '主任', '部长', '部门', '团队管理', '统筹',
                '战略', '规划', '预算', '组织', '人力', '行政', '管理'
            ],
            'weight': 0.25
        },
        '销售岗': {
            'keywords': [
                '销售', '商务', '客户', '大客户', 'BD', '渠道', '区域',
                '客户经理', '销售经理', '商务拓展', 'KA', '代理商',
                '签约', '回款', '业绩', '提成', 'CRM'
            ],
            'weight': 0.20
        },
        '运营岗': {
            'keywords': [
                '运营', '用户', '内容', '活动', '新媒体', '增长', '社区',
                '产品运营', '数据运营', '电商', '直播', '短视频', '社群',
                '私域', '品牌', '市场', '营销', '公关', 'PR', 'SEO', 'SEM',
                '投放', '推广'
            ],
            'weight': 0.15
        },
        '职能岗': {
            'keywords': [
                '财务', '会计', 'HR', '人力资源', '招聘', '薪酬', '绩效',
                '法务', '合规', '审计', '采购', '行政', '秘书', '翻译',
                '设计', 'UI', 'UX', '文案', '编辑', '记者'
            ],
            'weight': 0.05
        }
    }

    # ============================================================
    # 各职业阶段的简历优化策略
    # ============================================================
    RESUME_STRATEGIES = {
        '应届生': {
            'recommended_focus': [
                '教育背景与专业相关性：突出核心课程、GPA、奖学金等学术成就',
                '实习/实践经历：用STAR法则描述实习中的具体职责与成果',
                '项目经验：课程设计、毕业设计、竞赛项目、开源贡献',
                '技能证书：专业认证、语言能力、工具熟练度',
                '校园经历：学生会、社团、志愿者等体现软实力的经历'
            ],
            'module_order': [
                '个人信息',
                '求职意向',
                '教育背景',
                '实习/实践经历',
                '项目经验',
                '专业技能',
                '证书与荣誉',
                '校园经历'
            ],
            'page_limit': '1页',
            'page_limit_max': 1,
            'content_guidance': {
                '教育背景': '详细展开，包含核心课程（与岗位相关的3-5门）、GPA/排名、学术成果',
                '实习经历': '每段实习3-5条要点，使用STAR法则，尽量量化成果',
                '项目经验': '2-4个项目，每个项目包含背景、职责、技术栈、成果',
                '技能清单': '分类列出，标注熟练程度（精通/熟练/掌握/了解）',
                '自我评价': '不超过3条，每条有事实支撑，避免空话套话'
            },
            'keyword_strategy': '从JD中提取核心技能词，在学习经历和项目经历中自然植入',
            'common_mistakes': [
                '篇幅超过1页（应届生简历应控制在1页）',
                '缺少量化数据（用数字说话：提升了xx%、完成了xx个项目）',
                '教育背景过于简略（应展开核心课程和学术成就）',
                '堆砌课程名称而不突出与岗位的相关性',
                '实习经历写成岗位职责说明而非个人成果展示'
            ]
        },
        '1-3年': {
            'recommended_focus': [
                '专业技能与工具：突出已掌握的技术栈和工具链，标注熟练程度',
                '项目成果：用数据证明个人贡献，强调独立承担的工作模块',
                '成长轨迹：展示从基础执行到独立负责的成长过程',
                '行业认知：体现对所在行业的理解和业务敏感度',
                '学习能力：快速掌握新技能、新工具的案例'
            ],
            'module_order': [
                '个人信息',
                '求职意向',
                '工作经历',
                '项目经验',
                '专业技能',
                '教育背景',
                '证书与荣誉'
            ],
            'page_limit': '1-2页',
            'page_limit_max': 2,
            'content_guidance': {
                '工作经历': '每段工作5-8条要点，突出个人独立负责的模块和成果',
                '项目经验': '2-4个核心项目，重点描述个人角色和可量化成果',
                '技能清单': '按类别分组，突出与目标岗位匹配的核心技能',
                '教育背景': '精简为1-2行（学校+专业+学历+毕业年份）'
            },
            'keyword_strategy': '将JD核心关键词自然融入工作经历描述中，确保ATS通过率',
            'common_mistakes': [
                '工作经历写成岗位说明书，缺少个人成果',
                '项目描述缺少量化数据（提升了多少、节省了多少）',
                '技能清单堆砌关键词而缺少实际项目佐证',
                '教育背景占比过大，挤压工作经历篇幅',
                '缺少职业成长轨迹的呈现'
            ]
        },
        '3-5年': {
            'recommended_focus': [
                '专业深度：在某个领域的深耕成果，技术方案设计与落地能力',
                '业务影响力：工作成果对业务指标的直接贡献（营收/效率/成本）',
                '独立操盘能力：独立负责项目/模块/业务线的经验',
                '跨团队协作：与产品、设计、运营等多团队的协同经验',
                '方法论沉淀：形成的工作方法论、SOP、最佳实践'
            ],
            'module_order': [
                '个人信息',
                '求职意向',
                '工作经历',
                '核心项目',
                '专业能力',
                '教育背景'
            ],
            'page_limit': '2页',
            'page_limit_max': 2,
            'content_guidance': {
                '工作经历': '每段工作6-8条要点，重点突出独立负责的业务模块和业绩数据',
                '核心项目': '3-5个项目，按重要性排序，每个项目包含背景、方案、成果',
                '专业能力': '分维度展示（专业技能+管理能力+行业知识），附具体案例',
                '教育背景': '精简为1行'
            },
            'keyword_strategy': '围绕JD核心要求，在工作经历中嵌入行业术语和管理关键词',
            'common_mistakes': [
                '仍停留在执行层面描述，缺少独立操盘和决策的体现',
                '项目描述过于技术化，缺少业务价值维度的说明',
                '缺少跨团队协作和资源协调能力的展示',
                '没有呈现系统性的方法论或可复用的经验沉淀',
                '篇幅控制不当（过长显得不够精炼，过短无法展示深度）'
            ]
        },
        '5-10年': {
            'recommended_focus': [
                '管理经验：团队规模、管理幅度、人才培养成果',
                '业务操盘：负责的业务板块规模、P&L责任、战略目标达成',
                '体系建设：搭建的流程、制度、标准、体系',
                '行业资源：行业人脉、合作伙伴、供应商资源',
                '战略执行：将公司战略拆解为可执行方案并落地的能力'
            ],
            'module_order': [
                '个人信息',
                '求职意向',
                '职业概述',
                '工作经历',
                '核心业绩',
                '管理能力',
                '教育背景',
                '行业资源与认证'
            ],
            'page_limit': '2-3页',
            'page_limit_max': 3,
            'content_guidance': {
                '职业概述': '3-4句话概括职业历程、核心能力和管理风格',
                '工作经历': '每段工作包含管理幅度（团队规模、汇报线）+ 核心业绩（量化）',
                '核心业绩': '挑选3-5个代表性业绩，用数据说明业务影响',
                '管理能力': '团队搭建、制度建设、人才培养、跨部门协作的具体案例',
                '教育背景': '精简为1行，如有MBA/EMBA可适当展开'
            },
            'keyword_strategy': '突出管理层级关键词（团队管理、战略规划、预算管控、体系建设）',
            'common_mistakes': [
                '还在详细列举具体执行层面的工作内容',
                '管理团队的经验描述过于笼统，缺少团队规模和具体成果',
                '缺少体系建设的成果（搭建了什么制度、流程、标准）',
                '没有职业概述模块，HR难以快速了解候选人定位',
                '业绩描述缺少业务视角（只说做了什么，不说对业务的影响）'
            ]
        },
        '10年+': {
            'recommended_focus': [
                '战略视野：行业趋势判断、业务战略规划、商业模式创新',
                '行业影响力：行业演讲、出版物、标准制定、行业奖项',
                '组织搭建：从0到1组建团队、组织架构设计、人才梯队建设',
                '商业化成果：营收规模、利润增长、市场份额、融资成果',
                '企业文化与价值观：管理理念、领导风格、企业文化建设'
            ],
            'module_order': [
                '个人信息',
                '求职意向',
                '高管概述',
                '核心成就',
                '职业经历',
                '行业影响',
                '教育背景',
                '社会职务与荣誉'
            ],
            'page_limit': '3页（原则上不超过4页）',
            'page_limit_max': 4,
            'content_guidance': {
                '高管概述': '4-5句话概括职业高度、行业地位、核心价值主张',
                '核心成就': '5-8项标志性成就，涵盖战略决策、组织建设、商业成果',
                '职业经历': '聚焦近10-15年，每段经历突出战略决策和经营成果',
                '行业影响': '行业演讲、媒体采访、出版物、行业标准参与、社会职务',
                '教育背景': '精简展示，如有知名商学院背景可适当突出'
            },
            'keyword_strategy': '使用战略层关键词（战略规划、商业模式、组织变革、资本运作、行业生态）',
            'common_mistakes': [
                '简历篇幅过长，事无巨细地列举所有经历',
                '还在描述执行层面的工作内容，缺少战略高度',
                '缺少行业影响力的展示（演讲、出版、标准制定等）',
                '没有清晰的职业定位和价值主张',
                '教育背景和社会职务占比过大，挤压核心成就篇幅'
            ]
        }
    }

    # ============================================================
    # 岗位类型简历结构差异
    # ============================================================
    JOB_TYPE_STRUCTURES = {
        '技术岗': {
            'module_priority': [
                ('专业技能', 0.25),
                ('工作经历', 0.25),
                ('项目经验', 0.25),
                ('教育背景', 0.10),
                ('开源贡献/技术博客', 0.08),
                ('证书与荣誉', 0.07)
            ],
            'content_allocation': {
                '专业技能': '按类别分组（语言/框架/数据库/工具/云），标注熟练程度',
                '工作经历': '突出技术挑战、解决方案、性能指标（QPS/延迟/可用性）',
                '项目经验': '技术架构图描述、技术选型理由、核心难点攻克、量化性能提升',
                '教育背景': 'CS相关专业优先展示，突出算法/数据结构竞赛成绩'
            },
            'keyword_strategy': '精确匹配JD中的技术栈关键词，包含框架版本和工具名称',
            'unique_requirements': [
                'GitHub/开源项目链接（如有高星项目）',
                '技术博客/专栏链接',
                'LeetCode/竞赛排名（应届生适用）',
                '技术专利（如有）'
            ]
        },
        '管理岗': {
            'module_priority': [
                ('职业概述/高管概述', 0.15),
                ('工作经历', 0.30),
                ('核心业绩', 0.20),
                ('管理能力', 0.15),
                ('教育背景', 0.10),
                ('行业资源与认证', 0.10)
            ],
            'content_allocation': {
                '职业概述': '3-4句话概括管理幅度、行业经验、核心成就',
                '工作经历': '每段经历突出管理幅度（团队规模、预算规模）和经营成果',
                '核心业绩': '用数据展示业务增长、成本优化、组织效率提升',
                '管理能力': '团队搭建、制度建设、人才培养、跨部门协作案例'
            },
            'keyword_strategy': '管理层级关键词 + 业务成果关键词 + 行业术语',
            'unique_requirements': [
                '明确标注管理团队规模',
                '展示P&L责任范围',
                '突出制度建设与流程优化成果',
                'MBA/EMBA等管理学位加分'
            ]
        },
        '销售岗': {
            'module_priority': [
                ('工作经历', 0.30),
                ('核心业绩', 0.25),
                ('客户资源', 0.15),
                ('专业技能', 0.10),
                ('教育背景', 0.10),
                ('证书与荣誉', 0.10)
            ],
            'content_allocation': {
                '工作经历': '突出客户开发数量、签约金额、回款率、客户续约率',
                '核心业绩': '用数据展示销售业绩达成率、排名、增长率',
                '客户资源': '行业客户资源、渠道资源、合作伙伴网络',
                '专业技能': 'CRM工具、销售方法论（SPIN/ Challenger等）、行业知识'
            },
            'keyword_strategy': '业绩数据关键词 + 行业客户关键词 + 销售方法论关键词',
            'unique_requirements': [
                '业绩达成率必须有具体数字（如120%达成、Top 3排名）',
                '客户案例展示（脱敏处理）',
                '行业人脉与渠道资源说明',
                '销售竞赛/表彰记录'
            ]
        },
        '运营岗': {
            'module_priority': [
                ('工作经历', 0.25),
                ('项目经验', 0.25),
                ('核心数据', 0.20),
                ('专业技能', 0.10),
                ('教育背景', 0.10),
                ('证书与荣誉', 0.10)
            ],
            'content_allocation': {
                '工作经历': '突出运营的渠道、用户规模、增长数据、转化指标',
                '项目经验': '完整的运营项目闭环：目标-策略-执行-复盘-成果',
                '核心数据': '用户增长、活跃度、转化率、GMV、ROI等关键指标',
                '专业技能': '数据分析工具、内容创作能力、活动策划能力、平台运营经验'
            },
            'keyword_strategy': '运营指标关键词 + 平台名称 + 工具名称 + 行业术语',
            'unique_requirements': [
                '运营数据必须量化（DAU/GMV/转化率/留存率等）',
                '展示完整的运营方法论和SOP',
                '平台运营经验需具体（抖音/小红书/微信等）',
                '活动策划需展示完整案例'
            ]
        },
        '职能岗': {
            'module_priority': [
                ('工作经历', 0.30),
                ('专业技能', 0.20),
                ('项目经验', 0.15),
                ('证书与资质', 0.15),
                ('教育背景', 0.10),
                ('荣誉与奖项', 0.10)
            ],
            'content_allocation': {
                '工作经历': '突出流程优化、制度建设、风险管控、效率提升',
                '专业技能': '专业工具（ERP/OA/财务软件）、法规政策、行业认证',
                '项目经验': '制度搭建、系统上线、流程改造、合规审计等项目',
                '证书与资质': 'CPA/CFA/人力资源管理师/法律职业资格等专业认证'
            },
            'keyword_strategy': '专业术语 + 工具名称 + 法规政策关键词 + 行业认证',
            'unique_requirements': [
                '专业资质证书是硬门槛（CPA/法律资格等）',
                '展示制度建设和流程优化成果',
                '合规与风险管控经验',
                '跨部门协作与服务意识'
            ]
        }
    }

    def __init__(self):
        """初始化分析器"""
        self._compile_patterns()

    def _compile_patterns(self):
        """预编译正则表达式模式"""
        self.patterns = {
            # 工作年限匹配
            'experience_years': re.compile(
                r'(?:工作|从业|经验|从事)\s*(?:了|共|达|有|累计)?\s*'
                r'(\d{1,2})\s*(?:年|年以上)',
                re.IGNORECASE
            ),
            # 毕业年份
            'graduation_year': re.compile(
                r'(?:毕业|毕业于|届)\s*[:：]?\s*(\d{4})\s*[年届]?'
            ),
            # 在职时间范围
            'work_period': re.compile(
                r'(\d{4})[.\-/年]\s*(?:\d{1,2})?\s*[月]?\s*[-–—~至到]\s*'
                r'(?:至今|现|(\d{4})[.\-/年]\s*(?:\d{1,2})?\s*[月]?)'
            ),
            # 学历
            'education': re.compile(
                r'(博士|硕士|研究生|本科|大专|专科|学士|MBA|EMBA|MPA)',
                re.IGNORECASE
            ),
        }

    def extract_years_of_experience(self, resume_text: str) -> Tuple[float, str]:
        """
        从简历文本中提取工作年限

        策略优先级：
        1. 直接匹配"X年工作经验"等明确表述
        2. 根据工作经历时间区间计算
        3. 根据毕业年份推算

        :param resume_text: 简历纯文本
        :return: (工作年限数值, 提取来源说明)
        """
        # 策略1：直接匹配工作年限描述
        match = self.patterns['experience_years'].search(resume_text)
        if match:
            years = float(match.group(1))
            return years, 'explicit_statement'

        # 策略2：根据工作时间区间计算
        periods = self.patterns['work_period'].findall(resume_text)
        if periods:
            from datetime import datetime as dt
            current_year = dt.now().year
            earliest_start = current_year

            for start_str, end_str in periods:
                try:
                    start_year = int(start_str)
                    if start_year < earliest_start:
                        earliest_start = start_year
                except (ValueError, TypeError):
                    continue

            if earliest_start < current_year:
                years = current_year - earliest_start
                if years > 0 and years < 50:
                    return float(years), 'work_period_calculation'

        # 策略3：根据毕业年份推算
        grad_match = self.patterns['graduation_year'].search(resume_text)
        if grad_match:
            from datetime import datetime as dt
            current_year = dt.now().year
            grad_year = int(grad_match.group(1))
            if 1970 < grad_year <= current_year:
                years = current_year - grad_year
                if years >= 0 and years < 50:
                    return float(years), 'graduation_year_calculation'

        # 无法提取，默认为0
        return 0.0, 'default'

    def determine_career_stage(self, years: float) -> str:
        """
        根据工作年限判断职业阶段

        :param years: 工作年限
        :return: 职业阶段名称
        """
        for stage_name, stage_info in self.CAREER_STAGES.items():
            low, high = stage_info['range']
            if low <= years <= high:
                return stage_name
        return '10年+'

    def detect_job_category(self, resume_text: str, jd_text: str = '') -> str:
        """
        根据简历和JD文本检测岗位类型

        综合简历和JD中的关键词匹配度，加权计算最匹配的岗位类型

        :param resume_text: 简历纯文本
        :param jd_text: JD纯文本（可选）
        :return: 岗位类型名称
        """
        combined_text = resume_text + ' ' + jd_text
        scores = {}

        for category, info in self.JOB_CATEGORIES.items():
            score = 0
            for keyword in info['keywords']:
                count = combined_text.lower().count(keyword.lower())
                score += count * info['weight']
            scores[category] = score

        if not scores or max(scores.values()) == 0:
            return '技术岗'  # 默认

        best_match = max(scores, key=scores.get)
        return best_match

    def get_resume_strategy(self, career_stage: str) -> Dict[str, Any]:
        """
        获取指定职业阶段的简历优化策略

        :param career_stage: 职业阶段
        :return: 简历策略详情
        """
        return self.RESUME_STRATEGIES.get(career_stage, self.RESUME_STRATEGIES['1-3年'])

    def get_job_type_structure(self, job_category: str) -> Dict[str, Any]:
        """
        获取指定岗位类型的简历模块结构

        :param job_category: 岗位类型
        :return: 岗位简历结构详情
        """
        return self.JOB_TYPE_STRUCTURES.get(job_category, self.JOB_TYPE_STRUCTURES['技术岗'])

    def analyze(self, resume_text: str, jd_text: str = '',
                job_category_hint: str = '') -> Dict[str, Any]:
        """
        完整分析流程：提取工作年限 -> 判断职业阶段 -> 检测岗位类型 -> 输出策略

        :param resume_text: 简历纯文本
        :param jd_text: JD纯文本（可选）
        :param job_category_hint: 用户指定的岗位类型（可选）
        :return: 完整分析结果
        """
        # 1. 提取工作年限
        years, source = self.extract_years_of_experience(resume_text)

        # 2. 判断职业阶段
        career_stage = self.determine_career_stage(years)

        # 3. 检测岗位类型
        if job_category_hint and job_category_hint in self.JOB_CATEGORIES:
            job_category = job_category_hint
        else:
            job_category = self.detect_job_category(resume_text, jd_text)

        # 4. 获取策略
        resume_strategy = self.get_resume_strategy(career_stage)
        job_structure = self.get_job_type_structure(job_category)

        # 5. 组合输出
        result = {
            'career_stage': career_stage,
            'career_stage_label': self.CAREER_STAGES[career_stage]['label'],
            'career_stage_description': self.CAREER_STAGES[career_stage]['description'],
            'years_of_experience': years,
            'experience_source': source,
            'job_category': job_category,
            'resume_strategy': {
                'recommended_focus': resume_strategy['recommended_focus'],
                'module_order': resume_strategy['module_order'],
                'page_limit': resume_strategy['page_limit'],
                'page_limit_max': resume_strategy['page_limit_max'],
                'content_guidance': resume_strategy['content_guidance'],
                'keyword_strategy': resume_strategy['keyword_strategy'],
                'common_mistakes': resume_strategy['common_mistakes']
            },
            'job_type_structure': {
                'module_priority': job_structure['module_priority'],
                'content_allocation': job_structure['content_allocation'],
                'keyword_strategy': job_structure['keyword_strategy'],
                'unique_requirements': job_structure['unique_requirements']
            },
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0'
        }

        return result

    def generate_strategy_summary(self, result: Dict[str, Any]) -> str:
        """
        将分析结果转换为可读的文本摘要

        :param result: analyze() 的输出
        :return: 格式化的策略摘要文本
        """
        lines = []
        lines.append('=' * 60)
        lines.append('职业阶段分析与简历策略报告')
        lines.append('生成时间: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        lines.append('=' * 60)
        lines.append('')

        # 基本信息
        lines.append('[基本信息]')
        lines.append('  工作年限: {} 年'.format(result['years_of_experience']))
        lines.append('  职业阶段: {} ({})'.format(
            result['career_stage'], result['career_stage_label']))
        lines.append('  岗位类型: {}'.format(result['job_category']))
        lines.append('')

        # 阶段特征
        lines.append('[阶段特征]')
        lines.append('  {}'.format(result['career_stage_description']))
        lines.append('')

        # 简历优化策略
        lines.append('[简历优化策略]')
        lines.append('  建议页数: {}'.format(result['resume_strategy']['page_limit']))
        lines.append('')

        lines.append('  重点突出内容:')
        for i, focus in enumerate(result['resume_strategy']['recommended_focus'], 1):
            lines.append('    {}. {}'.format(i, focus))
        lines.append('')

        lines.append('  模块推荐顺序:')
        for i, module in enumerate(result['resume_strategy']['module_order'], 1):
            lines.append('    {}. {}'.format(i, module))
        lines.append('')

        lines.append('  关键词策略: {}'.format(result['resume_strategy']['keyword_strategy']))
        lines.append('')

        # 岗位类型结构
        lines.append('[岗位类型: {} - 简历结构建议]'.format(result['job_category']))
        lines.append('')

        lines.append('  模块篇幅分配:')
        for module, ratio in result['job_type_structure']['module_priority']:
            pct = int(ratio * 100)
            lines.append('    {} : {}%'.format(module.ljust(16), pct))
        lines.append('')

        lines.append('  特殊要求:')
        for req in result['job_type_structure']['unique_requirements']:
            lines.append('    - {}'.format(req))
        lines.append('')

        # 常见错误提醒
        lines.append('[常见错误提醒]')
        for i, mistake in enumerate(result['resume_strategy']['common_mistakes'], 1):
            lines.append('  {}. {}'.format(i, mistake))
        lines.append('')

        lines.append('=' * 60)
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='职业阶段分析与简历策略推荐工具'
    )
    parser.add_argument(
        '--resume', required=True,
        help='简历文本文件路径（.txt/.md）'
    )
    parser.add_argument(
        '--jd', default='',
        help='JD文本文件路径（可选）'
    )
    parser.add_argument(
        '--job-category', default='',
        choices=['', '技术岗', '管理岗', '销售岗', '运营岗', '职能岗'],
        help='岗位类型（可选，不指定则自动检测）'
    )
    parser.add_argument(
        '--output', default='',
        help='输出JSON文件路径（不指定则输出到标准输出）'
    )
    parser.add_argument(
        '--summary', action='store_true',
        help='同时输出可读的策略摘要'
    )

    args = parser.parse_args()

    # 读取简历
    try:
        with open(args.resume, 'r', encoding='utf-8') as f:
            resume_text = f.read()
    except FileNotFoundError:
        print('错误: 找不到文件 {}'.format(args.resume), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print('错误: 读取简历文件失败 - {}'.format(str(e)), file=sys.stderr)
        sys.exit(1)

    # 读取JD（可选）
    jd_text = ''
    if args.jd:
        try:
            with open(args.jd, 'r', encoding='utf-8') as f:
                jd_text = f.read()
        except FileNotFoundError:
            print('警告: 找不到JD文件 {}，将仅基于简历分析'.format(args.jd), file=sys.stderr)
        except Exception as e:
            print('警告: 读取JD文件失败 - {}'.format(str(e)), file=sys.stderr)

    # 执行分析
    analyzer = CareerProfileAnalyzer()
    result = analyzer.analyze(
        resume_text=resume_text,
        jd_text=jd_text,
        job_category_hint=args.job_category
    )

    # 输出JSON
    json_output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print('分析结果已保存至: {}'.format(args.output))
    else:
        print(json_output)

    # 输出摘要（可选）
    if args.summary:
        summary = analyzer.generate_strategy_summary(result)
        print('\n' + summary)


if __name__ == '__main__':
    main()
