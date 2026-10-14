#!/usr/bin/env python3
"""
ATS评分模拟器
适配扣子平台 Skill，无第三方依赖，运行稳定
"""

import re
import argparse
import json
from typing import List, Dict, Any
from pathlib import Path

# 技能同义词库（全部小写）
SKILL_SYNONYMS = {
    "java": ["java", "j2ee", "spring", "jvm", "maven", "springboot", "spring boot", "spring cloud"],
    "python": ["python", "django", "flask", "numpy", "pandas", "tensorflow", "pytorch", "sklearn"],
    "javascript": ["javascript", "js", "node.js", "nodejs", "react", "vue", "angular", "typescript", "ts"],
    "项目管理": ["pmp", "agile", "scrum", "jira", "project management", "项目管理", "敏捷开发"],
    "数据分析": ["sql", "excel", "tableau", "power bi", "数据分析", "数据挖掘", "数据可视化", "hadoop", "spark"],
    "数据库": ["mysql", "postgresql", "mongodb", "redis", "oracle", "sql server", "数据库", "db"],
    "云服务": ["aws", "azure", "阿里云", "腾讯云", "gcp", "云计算", "docker", "kubernetes", "k8s"],
    "前端开发": ["html", "css", "sass", "less", "webpack", "vite", "前端", "前端开发"],
    "后端开发": ["后端", "后端开发", "api", "restful", "微服务", "分布式", "高并发"],
    "测试": ["测试", "qa", "测试工程师", "自动化测试", "selenium", "junit", "单元测试"],
}

def main(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    扣子 Skill 标准入口
    """
    try:
        # 1. 安全提取输入
        resume_text = args.get("resume_text", "") or ""
        jd_req = args.get("jd_requirements") or {}
        format_info = args.get("resume_format_info") or {}
        
        # 确保必需字段存在
        required_skills = jd_req.get("required_skills") or []
        # 过滤空字符串技能
        required_skills = [s for s in required_skills if s and s.strip()]
        
        # 2. 关键词匹配
        matched_skills, missing_skills = match_skills(resume_text, required_skills)
        total_required = len(required_skills)
        match_rate = len(matched_skills) / total_required if total_required > 0 else 1.0
        
        # 3. 格式评分
        format_score = calculate_format_score(format_info)
        
        # 4. 经验年限评分（从简历文本中提取）
        exp_score = extract_experience_score(resume_text, jd_req.get("min_experience_years"))
        
        # 5. 学历评分（简单关键词匹配）
        edu_score = extract_education_score(resume_text, jd_req.get("education_level"))
        
        # 6. 综合 ATS 评分（加权）
        ats_score = int(
            match_rate * 50 +
            (format_score / 100.0) * 30 +
            exp_score * 10 +
            edu_score * 10
        )
        # 限制在 0-100 之间
        ats_score = max(0, min(100, ats_score))
        
        # 7. 生成改进建议
        suggestions = []
        if missing_skills:
            suggestions.append(f"简历中缺失以下关键技能: {', '.join(missing_skills)}")
        if format_score < 70:
            suggestions.append("简历包含表格或图片，建议转为纯文本+项目符号，以提高ATS解析准确性")
        if not format_info.get("has_contact_masked", False):
            suggestions.append("联系方式未脱敏，建议将手机号中间四位替换为****")
        if exp_score < 0.8:
            suggestions.append("简历中体现的工作经验年限可能不足，建议突出相关项目经历")
        if edu_score < 0.8:
            suggestions.append("学历信息未明确或未达要求，请补充教育背景")
        
        return {
            "ats_score": ats_score,
            "keyword_match_rate": round(match_rate, 2),
            "missing_skills": missing_skills,
            "format_score": format_score,
            "suggestions": suggestions
        }
    
    except Exception as e:
        # 任何未预期的错误，返回安全的默认值
        return {
            "ats_score": 50,
            "keyword_match_rate": 0.5,
            "missing_skills": [],
            "format_score": 60,
            "suggestions": [f"评分服务暂时不可用（{str(e)}），请稍后重试"]
        }


def match_skills(resume_text: str, required_skills: List[str]) -> tuple:
    """匹配技能，返回 (matched, missing)"""
    if not resume_text:
        return [], required_skills[:]
    
    resume_lower = resume_text.lower()
    matched = []
    missing = []
    
    for skill in required_skills:
        if not skill:
            continue
        skill_lower = skill.lower()
        synonyms = SKILL_SYNONYMS.get(skill_lower, [skill_lower])
        found = any(syn in resume_lower for syn in synonyms)
        if found:
            matched.append(skill)
        else:
            missing.append(skill)
    return matched, missing


def calculate_format_score(info: Dict) -> int:
    """计算格式得分，满分100"""
    score = 100
    if info.get("has_table"):
        score -= 20
    if info.get("has_image"):
        score -= 30
    if not info.get("has_contact_masked"):
        score -= 10
    return max(0, min(100, score))


def extract_experience_score(resume_text: str, min_years: Any) -> float:
    """从简历文本中提取工作经验年限，返回 0~1 的得分"""
    if not resume_text or min_years is None:
        return 1.0
    
    try:
        min_years = float(min_years)
    except (ValueError, TypeError):
        return 1.0
    
    patterns = [
        r'(\d+(?:\.\d+)?)\s*年\s*(?:以上|经验)?',
        r'经验\s*(\d+(?:\.\d+)?)\s*年',
        r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*年',
        r'(\d{4})\s*[-至到]\s*(\d{4}|\s*至今\s*)',
    ]
    years_found = []
    for pat in patterns:
        matches = re.findall(pat, resume_text)
        for m in matches:
            if isinstance(m, tuple):
                if len(m) == 2:
                    # 处理年份范围
                    try:
                        year1 = float(m[0])
                        if m[1].replace(' ', '') == '至今':
                            # 至今用当前年份计算
                            from datetime import datetime
                            current_year = datetime.now().year
                            years_found.append(current_year - year1)
                        else:
                            year2 = float(m[1])
                            years_found.append(abs(year2 - year1))
                    except (ValueError, TypeError):
                        pass
            else:
                try:
                    years_found.append(float(m))
                except (ValueError, TypeError):
                    pass
    
    if not years_found:
        return 1.0
    
    max_exp = max(years_found)
    if max_exp >= min_years:
        return 1.0
    else:
        return max(0.5, max_exp / min_years)


def extract_education_score(resume_text: str, required_level: str) -> float:
    """简单判断学历是否满足要求，返回 0~1 得分"""
    if not required_level or not resume_text:
        return 1.0
    
    required_level = required_level.lower()
    level_map = {
        "博士": 5, "博士研究生": 5, "phd": 5,
        "硕士": 4, "硕士研究生": 4, "master": 4,
        "本科": 3, "学士": 3, "bachelor": 3,
        "大专": 2, "专科": 2, "associate": 2,
        "高中": 1, "中专": 1, "high school": 1,
    }
    req_score = level_map.get(required_level, 3)
    
    found_level = 0
    for level, score in level_map.items():
        if level in resume_text:
            found_level = max(found_level, score)
    
    if found_level >= req_score:
        return 1.0
    elif found_level == 0:
        return 0.8
    else:
        return 0.5


def main_cli():
    """命令行接口，用于本地测试"""
    parser = argparse.ArgumentParser(description='ATS评分模拟器')
    parser.add_argument('--resume-file', help='简历文本文件路径')
    parser.add_argument('--jd-file', help='JD需求JSON文件路径')
    parser.add_argument('--format-file', help='格式信息JSON文件路径（可选）')
    parser.add_argument('--output', help='输出JSON文件路径（可选）')
    
    args = parser.parse_args()
    
    # 读取简历文本
    resume_text = ""
    if args.resume_file:
        with open(args.resume_file, 'r', encoding='utf-8') as f:
            resume_text = f.read()
    
    # 读取JD需求
    jd_requirements = {}
    if args.jd_file:
        with open(args.jd_file, 'r', encoding='utf-8') as f:
            jd_requirements = json.load(f)
    
    # 读取格式信息
    resume_format_info = {}
    if args.format_file:
        with open(args.format_file, 'r', encoding='utf-8') as f:
            resume_format_info = json.load(f)
    
    # 调用评分函数
    result = main({
        "resume_text": resume_text,
        "jd_requirements": jd_requirements,
        "resume_format_info": resume_format_info
    })
    
    # 输出结果
    print("=== ATS评分结果 ===")
    print(f"综合评分: {result['ats_score']}")
    print(f"关键词匹配率: {result['keyword_match_rate']}")
    print(f"格式评分: {result['format_score']}")
    print(f"\n缺失技能:")
    for skill in result['missing_skills']:
        print(f"  - {skill}")
    print(f"\n改进建议:")
    for suggestion in result['suggestions']:
        print(f"  - {suggestion}")
    
    # 保存结果到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main_cli()
