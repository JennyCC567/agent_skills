#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结合行业性质的针对性面试题生成工具
支持DCMM 2.0对齐版个人数据保护
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# 行业知识库
INDUSTRY_KNOWLEDGE = {
    "互联网/电商": {
        "typical_scenarios": "典型场景：高并发秒杀、AB实验、推荐算法迭代、用户增长飞轮。面试常问系统设计、数据驱动决策。",
        "hot_topics": ["AI驱动的用户增长", "大模型在电商中的应用", "私域流量运营"],
        "technical_points": ["分布式系统设计", "微服务架构", "Redis缓存", "消息队列", "性能优化"],
        "business_points": ["用户增长", "转化率优化", "GMV提升", "复购率"]
    },
    "金融": {
        "typical_scenarios": "典型场景：风控模型、量化策略、合规审查、流动性压力测试。注重严谨性、监管敏感度和结果解释力。",
        "hot_topics": ["金融科技监管趋严", "AI在风险管理中的应用", "数字人民币"],
        "technical_points": ["风控建模", "时间序列预测", "合规审查", "数据安全"],
        "business_points": ["风险管理", "合规经营", "客户信任", "收益稳定"]
    },
    "咨询": {
        "typical_scenarios": "典型场景：市场规模预估、商业尽调、降本增效专题。注重逻辑框架、MECE原则、快速估算能力。",
        "hot_topics": ["数字化转型咨询", "ESG战略咨询", "产业互联网"],
        "technical_points": ["MECE原则", "SWOT分析", "波特五力", "BCG矩阵"],
        "business_points": ["战略规划", "运营优化", "组织变革", "市场进入"]
    },
    "智能制造": {
        "typical_scenarios": "典型场景：产线良率优化、预测性维护、工业物联网落地。注重跨部门协同与ROI计算。",
        "hot_topics": ["工业4.0", "数字孪生", "智能制造升级"],
        "technical_points": ["PLC编程", "工业物联网", "MES系统", "自动化"],
        "business_points": ["降本增效", "质量提升", "安全生产", "智能化转型"]
    },
    "快消": {
        "typical_scenarios": "典型场景：品牌营销、渠道管理、新品上市、供应链优化。注重市场敏感度和执行效率。",
        "hot_topics": ["内容电商", "D2C模式", "国潮品牌"],
        "technical_points": ["品牌定位", "营销策划", "渠道管理", "供应链"],
        "business_points": ["市场份额", "品牌影响力", "销售增长", "渠道下沉"]
    },
    "医疗健康": {
        "typical_scenarios": "典型场景：临床试验、医疗质量管控、医保政策合规。注重专业性和伦理规范。",
        "hot_topics": ["互联网医疗", "AI辅助诊断", "健康管理"],
        "technical_points": ["医疗法规", "临床试验", "质量管理", "数据安全"],
        "business_points": ["医疗质量", "患者满意度", "成本控制", "合规经营"]
    },
    "教育": {
        "typical_scenarios": "典型场景：课程设计、教学质量评估、教育信息化。注重教育理念和用户体验。",
        "hot_topics": ["在线教育", "AI教育", "终身学习"],
        "technical_points": ["课程开发", "教学设计", "教育技术", "质量评估"],
        "business_points": ["教学质量", "学员满意度", "续费率", "品牌口碑"]
    }
}

# 企业类型模板
COMPANY_TYPE_TEMPLATES = {
    "外企": {
        "focus": "注重国际化视野、跨文化沟通、流程规范、英语能力",
        "typical_questions": ["跨文化团队协作", "流程优化", "英语沟通"]
    },
    "初创": {
        "focus": "注重快速学习、多面手能力、执行力、创新精神",
        "typical_questions": ["0到1搭建", "快速迭代", "资源有限情况下解决问题"]
    },
    "上市公司": {
        "focus": "注重规范管理、数据驱动、风险控制、 shareholder价值",
        "typical_questions": ["规范化管理", "财报解读", "合规经营"]
    },
    "国企": {
        "focus": "注重政治站位、稳定性、团队协作、政策敏感度",
        "typical_questions": ["团队协作", "稳定性", "政策理解"]
    }
}


def identify_industry_from_jd(jd_text: str) -> Dict[str, Any]:
    """
    从JD中识别行业信息

    Args:
        jd_text: 岗位描述文本

    Returns:
        包含行业、企业类型、热点话题的字典
    """
    jd_lower = jd_text.lower()

    # 行业识别
    industry = "通用行业"
    industry_keywords = {
        "互联网/电商": ["互联网", "电商", "电子商务", "拼多多", "阿里", "腾讯", "字节", "美团", "京东", "网易"],
        "金融": ["金融", "银行", "证券", "基金", "保险", "投资", "风控", "信贷"],
        "咨询": ["咨询", "顾问", "战略", "管理咨询", "麦肯锡", "波士顿", "贝恩"],
        "智能制造": ["制造", "工业", "工厂", "产线", "自动化", "机器人", "工业4.0"],
        "快消": ["快消", "零售", "消费品", "宝洁", "联合利华", "可口可乐", "百事"],
        "医疗健康": ["医疗", "健康", "医院", "医生", "药企", "制药", "生物"],
        "教育": ["教育", "培训", "学校", "教师", "课程", "在线教育"]
    }

    for ind, keywords in industry_keywords.items():
        for keyword in keywords:
            if keyword in jd_text:
                industry = ind
                break
        if industry != "通用行业":
            break

    # 企业类型识别
    company_type = "其他"
    company_keywords = {
        "外企": ["外企", "外资", "跨国", "global", "international"],
        "初创": ["初创", "创业", "startup", "种子轮", "天使轮"],
        "上市公司": ["上市", "上市公司", "public company", "ipo"],
        "国企": ["国企", "国有", "央企", "事业单位"]
    }

    for ct, keywords in company_keywords.items():
        for keyword in keywords:
            if keyword in jd_lower:
                company_type = ct
                break
        if company_type != "其他":
            break

    # 获取行业热点话题
    industry_info = INDUSTRY_KNOWLEDGE.get(industry, {})
    hot_topics = industry_info.get("hot_topics", ["行业发展趋势", "数字化转型", "人才竞争"])

    return {
        "industry": industry,
        "company_type": company_type,
        "hot_topics": hot_topics
    }


def extract_resume_experiences(resume_text: str) -> List[Dict]:
    """
    从简历中提取经历信息

    Args:
        resume_text: 简历文本

    Returns:
        经历列表
    """
    experiences = []

    # 简单的项目/经历提取
    project_patterns = [
        r'项目[名称]*[：:]\s*([^\n]+)',
        r'负责[的]*(项目|工作)[：:]\s*([^\n]+)',
        r'经历[：:]\s*([^\n]+)'
    ]

    for pattern in project_patterns:
        matches = re.findall(pattern, resume_text)
        for match in matches:
            exp_text = match if isinstance(match, str) else match[-1]
            if exp_text and len(exp_text) > 5:
                experiences.append({"type": "project", "content": exp_text})

    # 提取数据成果
    data_patterns = [
        r'(\d+%|增长\d+|提升\d+|优化\d+|节省\d+)',
        r'(\d+万|\d+亿|\d+千)'
    ]

    for pattern in data_patterns:
        matches = re.findall(pattern, resume_text)
        for match in matches[:3]:  # 只取前3个
            experiences.append({"type": "achievement", "content": f"数据成果：{match}"})

    return experiences if experiences else [{"type": "general", "content": "综合工作经历"}]


def extract_skills_from_resume(resume_text: str) -> List[str]:
    """
    从简历中提取技能

    Args:
        resume_text: 简历文本

    Returns:
        技能列表
    """
    # 常见技术技能
    common_skills = [
        "Java", "Python", "JavaScript", "TypeScript", "Go", "C++", "C#",
        "React", "Vue", "Angular", "Node.js", "Spring", "Django", "Flask",
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Kafka", "RabbitMQ",
        "Docker", "Kubernetes", "Git", "Linux", "AWS", "阿里云", "腾讯云",
        "机器学习", "深度学习", "数据分析", "数据挖掘", "统计学",
        "产品经理", "项目管理", "UI设计", "UX设计", "运营", "市场", "销售"
    ]

    found_skills = []
    for skill in common_skills:
        if skill in resume_text:
            found_skills.append(skill)

    return found_skills[:8]  # 最多返回8个技能


def generate_behavioral_questions(experiences: List[Dict], industry: str) -> List[Dict]:
    """
    生成行为面试题

    Args:
        experiences: 经历列表
        industry: 行业

    Returns:
        面试题列表
    """
    questions = []

    behavioral_templates = [
        {
            "template": "在「{exp}」中，你当时面临的最大挑战是什么？你如何权衡并最终解决的？",
            "intent": "考察问题解决能力、决策能力、压力应对"
        },
        {
            "template": "请分享一个在「{exp}」中，你通过数据驱动决策带来明显改进的例子。",
            "intent": "考察数据意识、分析能力、结果导向"
        },
        {
            "template": "在「{exp}」中，你是否遇到过团队协作或跨部门沟通的困难？你是如何处理的？",
            "intent": "考察团队协作、沟通能力、冲突解决"
        },
        {
            "template": "回顾「{exp}」，如果让你重新做一次，你会在哪些方面做出不同的决策？为什么？",
            "intent": "考察复盘能力、学习能力、自我认知"
        }
    ]

    for i, exp in enumerate(experiences[:4]):
        template = behavioral_templates[i % len(behavioral_templates)]
        exp_content = exp.get("content", "这段经历")
        question = template["template"].format(exp=exp_content[:30] + "..." if len(exp_content) > 30 else exp_content)

        questions.append({
            "type": "行为面试题",
            "question": question,
            "intent": template["intent"]
        })

    return questions


def generate_technical_questions(skills: List[str], jd_requirements: str, industry: str) -> List[Dict]:
    """
    生成技术/业务深挖题

    Args:
        skills: 技能列表
        jd_requirements: JD要求
        industry: 行业

    Returns:
        面试题列表
    """
    questions = []
    industry_info = INDUSTRY_KNOWLEDGE.get(industry, {})

    # 基于技能的问题
    skill_templates = [
        "请详细描述你在实际工作中使用「{skill}」解决过的具体问题，并说明其效果。",
        "在{industry}行业场景下，「{skill}」通常会遇到哪些典型挑战？你是如何应对的？",
        "对比一下「{skill}」与同类技术/方法的优劣势，你在什么情况下会选择使用它？"
    ]

    for i, skill in enumerate(skills[:4]):
        template = skill_templates[i % len(skill_templates)]
        question = template.format(skill=skill, industry=industry)

        questions.append({
            "type": "技术/业务深挖题",
            "question": question,
            "intent": f"考察{skill}的实际应用能力和深度理解"
        })

    # 基于行业场景的问题
    industry_scenarios = industry_info.get("typical_scenarios", "")
    if industry_scenarios:
        questions.append({
            "type": "技术/业务深挖题",
            "question": f"结合{industry}行业的典型场景，你认为这个岗位最需要具备哪些核心能力？请结合你的经验说明。",
            "intent": "考察行业理解、岗位匹配度、业务思维"
        })

    return questions


def generate_industry_questions(hot_topics: List[str], industry: str) -> List[Dict]:
    """
    生成行业认知与案例面试题

    Args:
        hot_topics: 热点话题
        industry: 行业

    Returns:
        面试题列表
    """
    questions = []

    for topic in hot_topics[:3]:
        questions.append({
            "type": "行业认知与案例面",
            "question": f"如何看待{industry}行业近期的「{topic}」趋势？这对本岗位的工作会带来哪些影响？",
            "intent": "考察行业敏感度、趋势洞察、前瞻性思维"
        })

    questions.append({
        "type": "行业认知与案例面",
        "question": f"如果公司要在{industry}行业进行一项新业务探索，你认为应该优先考虑哪些因素？请提出你的分析框架。",
        "intent": "考察商业敏感度、战略思维、分析框架"
    })

    return questions


def generate_industry_specific_interview(
    resume_text: str,
    jd_text: str,
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    生成结合行业性质的针对性面试题

    Args:
        resume_text: 简历文本
        jd_text: 岗位描述文本
        output_file: 输出文件路径（可选）

    Returns:
        包含面试题的字典
    """
    # 1. 识别行业信息
    industry_info = identify_industry_from_jd(jd_text)
    industry = industry_info["industry"]
    company_type = industry_info["company_type"]
    hot_topics = industry_info["hot_topics"]

    # 2. 获取行业知识
    industry_knowledge = INDUSTRY_KNOWLEDGE.get(industry, {})
    extra_context = industry_knowledge.get("typical_scenarios", "通用行业场景，请结合JD深入提问。")

    # 3. 提取简历信息
    experiences = extract_resume_experiences(resume_text)
    skills = extract_skills_from_resume(resume_text)

    # 4. 生成面试题
    behavioral_questions = generate_behavioral_questions(experiences, industry)
    technical_questions = generate_technical_questions(skills, jd_text, industry)
    industry_questions = generate_industry_questions(hot_topics, industry)

    # 5. 合并所有题目
    all_questions = behavioral_questions + technical_questions + industry_questions

    # 6. 生成输出
    result = {
        "meta": {
            "generation_date": datetime.now().strftime("%Y年%m月%d日"),
            "industry": industry,
            "company_type": company_type,
            "hot_topics": hot_topics,
            "industry_context": extra_context
        },
        "questions": {
            "behavioral": behavioral_questions,
            "technical": technical_questions,
            "industry": industry_questions
        },
        "all_questions": all_questions
    }

    # 7. 输出到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入Markdown格式
            f.write(f"# 针对性面试题生成报告\n\n")
            f.write(f"**生成日期**：{result['meta']['generation_date']}\n\n")
            f.write(f"**目标行业**：{industry}\n\n")
            f.write(f"**企业类型**：{company_type}\n\n")
            f.write(f"**行业热点**：{'; '.join(hot_topics)}\n\n")

            f.write(f"## 行业背景知识\n\n")
            f.write(f"{extra_context}\n\n")

            f.write(f"---\n\n")

            # 行为面试题
            f.write(f"## 一、行为面试题（{len(behavioral_questions)}题）\n\n")
            for q in behavioral_questions:
                f.write(f"### 题目\n")
                f.write(f"{q['question']}\n\n")
                f.write(f"💡考察意图：{q['intent']}\n\n")

            # 技术/业务深挖题
            f.write(f"## 二、技术/业务深挖题（{len(technical_questions)}题）\n\n")
            for q in technical_questions:
                f.write(f"### 题目\n")
                f.write(f"{q['question']}\n\n")
                f.write(f"💡考察意图：{q['intent']}\n\n")

            # 行业认知与案例面
            f.write(f"## 三、行业认知与案例面（{len(industry_questions)}题）\n\n")
            for q in industry_questions:
                f.write(f"### 题目\n")
                f.write(f"{q['question']}\n\n")
                f.write(f"💡考察意图：{q['intent']}\n\n")

            f.write(f"---\n\n")
            f.write(f"## 使用说明\n\n")
            f.write(f"- 本题库基于「三维定位法」生成：简历弱点深挖 + JD硬性要求 + 行业特性\n")
            f.write(f"- 建议按顺序提问，行为面→技术面→行业认知面\n")
            f.write(f"- 可根据实际面试时间调整题目数量\n")

    return result


def main():
    parser = argparse.ArgumentParser(description="结合行业性质的针对性面试题生成工具")
    parser.add_argument("--resume-file", required=True, help="简历文本文件路径")
    parser.add_argument("--jd-file", required=True, help="岗位描述文件路径")
    parser.add_argument("--output", help="输出文件路径（Markdown格式）")

    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.resume_file, 'r', encoding='utf-8') as f:
            resume_text = f.read()

        with open(args.jd_file, 'r', encoding='utf-8') as f:
            jd_text = f.read()
    except Exception as e:
        print(f"错误：读取文件失败 - {e}", file=sys.stderr)
        sys.exit(1)

    # 生成面试题
    try:
        result = generate_industry_specific_interview(
            resume_text=resume_text,
            jd_text=jd_text,
            output_file=args.output
        )

        print(f"=== 针对性面试题生成成功 ===\n")
        print(f"目标行业：{result['meta']['industry']}")
        print(f"企业类型：{result['meta']['company_type']}")
        print(f"行业热点：{'; '.join(result['meta']['hot_topics'])}")
        print(f"\n生成题目统计：")
        print(f"- 行为面试题：{len(result['questions']['behavioral'])}题")
        print(f"- 技术/业务深挖题：{len(result['questions']['technical'])}题")
        print(f"- 行业认知与案例面：{len(result['questions']['industry'])}题")
        print(f"- 总计：{len(result['all_questions'])}题")

        if args.output:
            print(f"\n详细报告已保存至：{args.output}")

    except Exception as e:
        print(f"错误：生成面试题失败 - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
