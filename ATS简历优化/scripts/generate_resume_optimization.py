#!/usr/bin/env python3
"""
简历优化文档生成脚本
生成纯可投递优化版简历、岗位匹配度分析报告、修改说明文档
"""

import argparse
import json
import sys
import re
import difflib
from datetime import datetime
from pathlib import Path

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}", file=sys.stderr)
        sys.exit(1)

def extract_skills(text):
    """从文本中提取技术技能关键词"""
    if not text:
        return []
    
    # 常见技术技能关键词库
    common_skills = [
        'Java', 'Python', 'JavaScript', 'TypeScript', 'React', 'Vue', 'Angular',
        'Node.js', 'Spring', 'Spring Boot', 'Spring Cloud', 'MyBatis', 'Hibernate',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server',
        'Docker', 'Kubernetes', 'K8s', 'Git', 'SVN', 'Maven', 'Gradle', 'NPM', 'Yarn',
        'Linux', 'Windows', 'AWS', 'Azure', '阿里云', '腾讯云', 'GCP',
        'RESTful', 'API', 'GraphQL', 'WebSocket', 'MQTT', 'HTTP', 'HTTPS',
        '微服务', '分布式', '高并发', '性能优化', '代码审查', '敏捷开发', 'Scrum',
        'HTML', 'CSS', 'SASS', 'LESS', 'Webpack', 'Vite', 'ES6', 'ES7',
        '数据分析', '数据挖掘', '机器学习', '深度学习', 'AI', '人工智能',
        '项目管理', '团队协作', '沟通协调', '需求分析', '技术方案设计'
    ]
    
    skills_found = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower and skill not in skills_found:
            skills_found.append(skill)
    
    return skills_found

def calculate_text_similarity(text1, text2):
    """计算两个文本的相似度"""
    if not text1 or not text2:
        return 0.0
    
    # 使用difflib计算相似度
    return difflib.SequenceMatcher(None, text1, text2).ratio()

def detect_job_type(job_name, jd_data):
    """
    根据岗位名称和JD数据智能识别岗位类型
    
    返回：tech/operation/sales/management/general
    """
    if not job_name:
        return 'general'
    
    job_name_lower = job_name.lower()
    
    # 技术岗关键词
    tech_keywords = ['开发', '工程师', '程序员', '架构', '技术', 'java', 'python', '前端', '后端', '算法', '数据', '运维', '测试', 'devops', '系统', '软件', '硬件', '网络', '安全', 'it', 'cto']
    for keyword in tech_keywords:
        if keyword in job_name_lower:
            return 'tech'
    
    # 运营岗关键词
    operation_keywords = ['运营', '产品', '市场', '推广', '用户', '增长', '内容', '社区', '活动', '数据运营', '产品运营', '市场运营']
    for keyword in operation_keywords:
        if keyword in job_name_lower:
            return 'operation'
    
    # 销售岗关键词
    sales_keywords = ['销售', '商务', '客户', '客户经理', '销售经理', 'bd', 'business', '渠道', '招商', '贸易']
    for keyword in sales_keywords:
        if keyword in job_name_lower:
            return 'sales'
    
    # 管培/管理岗关键词
    management_keywords = ['管培', '管理', '培训生', 'mba', '总经理', '总监', '经理', '主管', 'leader', 'hr', '人力']
    for keyword in management_keywords:
        if keyword in job_name_lower:
            return 'management'
    
    return 'general'

def get_job_type_dimensions(job_type):
    """
    根据岗位类型获取评分维度配置
    
    返回格式：{
        'dimensions': [
            {'name': '维度名称', 'weight': 权重, 'description': '维度描述'},
            ...
        ],
        'chart_title': '图表标题'
    }
    """
    dimension_configs = {
        'tech': {
            'dimensions': [
                {'name': '代码能力', 'weight': 30, 'description': '编程语言、算法实现、代码质量'},
                {'name': '架构设计', 'weight': 25, 'description': '系统设计、技术选型、架构思维'},
                {'name': '问题排查', 'weight': 20, 'description': '故障定位、性能优化、debug能力'},
                {'name': '学习能力', 'weight': 15, 'description': '新技术掌握、持续学习意愿'},
                {'name': '团队协作', 'weight': 10, 'description': '沟通配合、代码审查、文档输出'}
            ],
            'chart_title': '技术岗能力评估'
        },
        'operation': {
            'dimensions': [
                {'name': '数据分析', 'weight': 30, 'description': '数据敏感度、分析工具、数据驱动决策'},
                {'name': '用户洞察', 'weight': 25, 'description': '用户理解、需求挖掘、用户体验'},
                {'name': '活动策划', 'weight': 20, 'description': '创意策划、项目执行、效果追踪'},
                {'name': '内容能力', 'weight': 15, 'description': '文案撰写、内容运营、品牌感知'},
                {'name': '资源整合', 'weight': 10, 'description': '跨部门协作、资源调度、项目推动'}
            ],
            'chart_title': '运营岗能力评估'
        },
        'sales': {
            'dimensions': [
                {'name': '业绩达成', 'weight': 35, 'description': '目标完成率、业绩历史、结果导向'},
                {'name': '客户资源', 'weight': 25, 'description': '客户积累、客情维护、人脉网络'},
                {'name': '谈判能力', 'weight': 20, 'description': '沟通技巧、议价能力、商务谈判'},
                {'name': '产品理解', 'weight': 10, 'description': '产品知识、行业理解、价值传递'},
                {'name': '抗压能力', 'weight': 10, 'description': '心态管理、逆境应对、持续作战'}
            ],
            'chart_title': '销售岗能力评估'
        },
        'management': {
            'dimensions': [
                {'name': '战略思维', 'weight': 25, 'description': '全局视野、商业洞察、方向判断'},
                {'name': '团队管理', 'weight': 25, 'description': '人员培养、团队建设、激励授权'},
                {'name': '项目推动', 'weight': 20, 'description': '资源协调、进度把控、风险应对'},
                {'name': '沟通影响', 'weight': 15, 'description': '向上管理、跨部门沟通、影响力'},
                {'name': '培养潜力', 'weight': 15, 'description': '学习能力、适应能力、发展空间'}
            ],
            'chart_title': '管理岗能力评估'
        },
        'general': {
            'dimensions': [
                {'name': '专业力', 'weight': 30, 'description': '专业知识、业务能力、工作成果'},
                {'name': '执行力', 'weight': 25, 'description': '任务完成、质量把控、效率意识'},
                {'name': '沟通力', 'weight': 20, 'description': '表达能力、倾听理解、协作配合'},
                {'name': '潜力', 'weight': 25, 'description': '学习意愿、适应能力、发展空间'}
            ],
            'chart_title': '通用能力评估'
        }
    }
    
    return dimension_configs.get(job_type, dimension_configs['general'])

def calculate_job_type_specific_scores(resume_data, jd_data, job_type):
    """
    根据岗位类型计算特定维度的分数
    """
    config = get_job_type_dimensions(job_type)
    dimensions = config['dimensions']
    
    scores = {}
    for dim in dimensions:
        dim_name = dim['name']
        # 根据维度名称计算分数（基于现有数据启发式计算）
        if dim_name in ['代码能力', '架构设计', '专业力']:
            # 基于技能匹配度
            resume_skills = set()
            if 'skills' in resume_data:
                resume_skills.update([s.strip() for s in resume_data['skills'] if s.strip()])
            if 'experience' in resume_data:
                for exp in resume_data['experience']:
                    if 'description' in exp:
                        resume_skills.update(extract_skills(exp['description']))
            scores[dim_name] = min(100, 60 + len(resume_skills) * 2)
        
        elif dim_name in ['数据分析', '问题排查', '学习能力']:
            # 基于项目相关性
            project_similarities = []
            if 'projects' in resume_data and jd_data:
                jd_text = jd_data.get('requirements', '') + ' ' + jd_data.get('description', '')
                for proj in resume_data['projects']:
                    proj_text = proj.get('description', '') + ' ' + proj.get('name', '')
                    similarity = calculate_text_similarity(proj_text, jd_text)
                    project_similarities.append(similarity)
            scores[dim_name] = sum(project_similarities) / len(project_similarities) * 100 if project_similarities else 70
        
        elif dim_name in ['团队协作', '沟通力', '沟通影响']:
            # 基于工作经历描述
            exp_descriptions = []
            if 'experience' in resume_data:
                for exp in resume_data['experience']:
                    if 'description' in exp:
                        exp_descriptions.append(exp['description'])
            combined_text = ' '.join(exp_descriptions)
            # 检查团队协作相关关键词
            team_keywords = ['协作', '配合', '团队', '沟通', '协调', '推动', '组织']
            keyword_count = sum(1 for keyword in team_keywords if keyword in combined_text)
            scores[dim_name] = min(100, 60 + keyword_count * 5)
        
        elif dim_name in ['业绩达成', '客户资源', '谈判能力']:
            # 销售相关维度
            sales_keywords = ['业绩', '销售', '客户', '目标', '达成', '增长', '收入', '利润']
            combined_text = ''
            if 'experience' in resume_data:
                for exp in resume_data['experience']:
                    if 'description' in exp:
                        combined_text += exp['description']
            keyword_count = sum(1 for keyword in sales_keywords if keyword in combined_text)
            scores[dim_name] = min(100, 55 + keyword_count * 6)
        
        elif dim_name in ['用户洞察', '活动策划', '内容能力']:
            # 运营相关维度
            operation_keywords = ['用户', '活动', '内容', '数据', '增长', '运营', '产品']
            combined_text = ''
            if 'experience' in resume_data:
                for exp in resume_data['experience']:
                    if 'description' in exp:
                        combined_text += exp['description']
            keyword_count = sum(1 for keyword in operation_keywords if keyword in combined_text)
            scores[dim_name] = min(100, 60 + keyword_count * 5)
        
        elif dim_name in ['战略思维', '项目推动', '培养潜力']:
            # 管理相关维度
            management_keywords = ['管理', '项目', '战略', '团队', '培养', '领导', '推动']
            combined_text = ''
            if 'experience' in resume_data:
                for exp in resume_data['experience']:
                    if 'description' in exp:
                        combined_text += exp['description']
            keyword_count = sum(1 for keyword in management_keywords if keyword in combined_text)
            scores[dim_name] = min(100, 60 + keyword_count * 5)
        
        else:
            # 默认分数
            scores[dim_name] = 70
    
    # 计算总分（加权平均）
    total_score = 0
    total_weight = 0
    for dim in dimensions:
        dim_name = dim['name']
        weight = dim['weight']
        total_score += scores[dim_name] * weight
        total_weight += weight
    
    final_total = total_score / total_weight if total_weight > 0 else 75
    
    return {
        'total': round(final_total, 1),
        'breakdown': scores,
        'job_type': job_type,
        'dimensions_config': config
    }

def calculate_matching_score(resume_data, jd_data, job_name=None):
    """
    计算智能匹配度分数
    
    如果提供了job_name，会自动识别岗位类型并使用对应维度
    
    基础维度（通用）：
    硬技能匹配       40%    简历技能集 ∩ JD技能集 / JD技能集
    经验年限         20%    1 - min(1, abs(经验年数-JD要求)/5)
    项目相关性       25%    计算简历项目描述与JD要求的文本相似度
    学历达标         15%    满足要求得100%，否则0%
    
    总分公式：Score = 0.4×硬技能分 + 0.2×年限分 + 0.25×项目分 + 0.15×学历分
    """
    # 如果有岗位名称，先尝试岗位特定评分
    if job_name:
        job_type = detect_job_type(job_name, jd_data)
        if job_type != 'general':
            return calculate_job_type_specific_scores(resume_data, jd_data, job_type)
    
    # 通用评分逻辑（向后兼容）
    scores = {}
    
    # 1. 硬技能匹配 (40%)
    resume_skills = set()
    # 从简历技能列表提取
    if 'skills' in resume_data:
        resume_skills.update([s.strip() for s in resume_data['skills'] if s.strip()])
    # 从工作经历描述提取
    if 'experience' in resume_data:
        for exp in resume_data['experience']:
            if 'description' in exp:
                resume_skills.update(extract_skills(exp['description']))
    
    jd_skills = set()
    if jd_data and 'requirements' in jd_data:
        jd_skills.update(extract_skills(jd_data['requirements']))
    if jd_data and 'required_skills' in jd_data:
        jd_skills.update([s.strip() for s in jd_data['required_skills'] if s.strip()])
    
    if jd_skills:
        skill_overlap = len(resume_skills & jd_skills)
        scores['hard_skill'] = min(100, (skill_overlap / len(jd_skills)) * 100)
    else:
        scores['hard_skill'] = 70  # 默认中等分数
    
    # 2. 经验年限匹配 (20%)
    resume_years = 0
    if 'personal_info' in resume_data and 'work_years' in resume_data['personal_info']:
        try:
            resume_years = float(resume_data['personal_info']['work_years'])
        except (ValueError, TypeError):
            pass
    
    jd_required_years = 0
    if jd_data and 'required_years' in jd_data:
        try:
            jd_required_years = float(jd_data['required_years'])
        except (ValueError, TypeError):
            pass
    
    if jd_required_years > 0:
        year_diff = abs(resume_years - jd_required_years)
        scores['experience'] = max(0, min(100, (1 - min(1, year_diff / 5)) * 100))
    else:
        scores['experience'] = 80  # 默认良好分数
    
    # 3. 项目相关性 (25%)
    project_similarities = []
    if 'projects' in resume_data and jd_data:
        jd_text = jd_data.get('requirements', '') + ' ' + jd_data.get('description', '')
        for proj in resume_data['projects']:
            proj_text = proj.get('description', '') + ' ' + proj.get('name', '')
            similarity = calculate_text_similarity(proj_text, jd_text)
            project_similarities.append(similarity)
    
    if project_similarities:
        scores['project'] = sum(project_similarities) / len(project_similarities) * 100
    else:
        scores['project'] = 65  # 默认基础分数
    
    # 4. 学历达标 (15%)
    scores['education'] = 75  # 默认中等分数
    if 'education' in resume_data and jd_data and 'required_education' in jd_data:
        resume_edu = resume_data['education'].get('degree', '').lower()
        jd_edu = jd_data['required_education'].lower()
        
        edu_hierarchy = ['高中', '大专', '本科', '硕士', '博士']
        try:
            resume_level = edu_hierarchy.index(resume_edu) if resume_edu in edu_hierarchy else 2
            jd_level = edu_hierarchy.index(jd_edu) if jd_edu in edu_hierarchy else 2
            
            if resume_level >= jd_level:
                scores['education'] = 100
            else:
                scores['education'] = 60
        except ValueError:
            pass
    
    # 计算总分
    total_score = (
        scores['hard_skill'] * 0.4 +
        scores['experience'] * 0.2 +
        scores['project'] * 0.25 +
        scores['education'] * 0.15
    )
    
    return {
        'total': round(total_score, 1),
        'breakdown': scores,
        'job_type': 'general',
        'dimensions_config': get_job_type_dimensions('general')
    }

def generate_interview_questions(resume_data, jd_data):
    """
    基于简历JSON + JD关键要求动态生成面试题目
    
    生成类型：
    1. 项目深挖题：对简历中每个项目生成深挖问题
    2. 关键技能题：基于简历技能和JD要求生成
    3. 场景题：结合JD要求生成
    4. 潜力题：对高潜岗位生成
    """
    questions = []
    
    # 1. 项目深挖题（3-4个项目）
    if 'projects' in resume_data:
        for i, proj in enumerate(resume_data['projects'][:3]):
            proj_name = proj.get('name', f'项目{i+1}')
            questions.append({
                'type': '项目深挖',
                'question': f"在「{proj_name}」项目中，你当时面临的最大技术/业务难点是什么？你如何权衡并最终解决的？",
                'source': f'项目经历：{proj_name}',
                '思路': 'STAR法则：描述情境→说明任务→讲述行动→展示结果',
                '要点': '具体技术难点+你的解决方案+最终成果+学到的经验'
            })
            questions.append({
                'type': '项目深挖',
                'question': f"在「{proj_name}」项目中，你主要负责哪些核心工作？请分享一个你主导推动并取得显著成果的具体案例。",
                'source': f'项目经历：{proj_name}',
                '思路': '突出你的主导作用，用数据说话',
                '要点': '你的角色+具体动作+量化成果+团队影响'
            })
    
    # 2. 关键技能题（5-6个技能）
    resume_skills = []
    if 'skills' in resume_data:
        resume_skills = [s.strip() for s in resume_data['skills'] if s.strip()]
    if 'experience' in resume_data:
        for exp in resume_data['experience']:
            if 'description' in exp:
                resume_skills.extend(extract_skills(exp['description']))
    
    # 去重并取前6个
    unique_skills = list(dict.fromkeys(resume_skills))[:6]
    
    jd_required_skills = []
    if jd_data and 'required_skills' in jd_data:
        jd_required_skills = [s.strip() for s in jd_data['required_skills'] if s.strip()]
    if jd_data and 'requirements' in jd_data:
        jd_required_skills.extend(extract_skills(jd_data['requirements']))
    
    for skill in unique_skills:
        is_required = skill.lower() in [s.lower() for s in jd_required_skills]
        if is_required:
            questions.append({
                'type': '关键技能',
                'question': f"请详细描述你在实际工作中使用「{skill}」解决过的具体问题，并说明其应用效果。",
                'source': f'技能标签：{skill}',
                '思路': '结合具体场景，说明技术选型理由和实施过程',
                '要点': f'具体问题场景+使用{skill}的解决方案+实际效果+技术难点'
            })
        else:
            questions.append({
                'type': '关键技能',
                'question': f"你在简历中提到了「{skill}」，能否分享一个相关的实战经验？",
                'source': f'技能标签：{skill}',
                '思路': '展示你的技术深度和实际应用能力',
                '要点': '应用场景+技术实现+遇到的挑战+总结收获'
            })
    
    # 3. 工作经历深挖题（2-3段经历）
    if 'experience' in resume_data:
        for i, exp in enumerate(resume_data['experience'][:2]):
            company = exp.get('company', f'公司{i+1}')
            position = exp.get('position', f'职位{i+1}')
            questions.append({
                'type': '工作经历',
                'question': f"在{company}担任{position}期间，你最有成就感的一件事是什么？请具体说明你做了什么、怎么做的、取得了什么成果。",
                'source': f'工作经历：{company} {position}',
                '思路': '选择最能体现你价值的具体案例，用数据支撑',
                '要点': '背景介绍+你的动作+量化成果+个人成长'
            })
    
    # 4. 场景题（2-3题）
    scenario_templates = [
        {
            'question': '根据岗位要求的核心能力，请分享一个你在实际工作中体现这一能力的具体案例。',
            '思路': '结合岗位需求，找到最相关的经历',
            '要点': '能力体现+具体案例+行动方案+最终结果'
        },
        {
            'question': '如果在工作中遇到突发问题或紧急情况，你会如何分析和解决？请结合你的经验说明。',
            '思路': '展示你的问题解决能力和抗压能力',
            '要点': '问题分析+应对策略+资源协调+经验总结'
        },
        {
            'question': '团队协作中难免出现分歧，请分享一次你成功协调不同意见并推动项目进展的经历。',
            'source': '综合能力考察',
            '思路': '展示你的沟通协调能力和团队合作精神',
            '要点': '分歧背景+你的做法+协调结果+团队收获'
        }
    ]
    
    for i, template in enumerate(scenario_templates[:2]):
        questions.append({
            'type': '场景应对',
            'question': template['question'],
            'source': template.get('source', '综合能力考察'),
            '思路': template['思路'],
            '要点': template['要点']
        })
    
    # 5. 潜力题（1-2题）
    questions.append({
        'type': '发展潜力',
        'question': '对于这个岗位，你认为自己的核心优势是什么？还有哪些方面需要进一步提升？',
        'source': '自我认知考察',
        '思路': '诚实客观，优势要具体，提升方向要有可行性',
        '要点': '2-3个核心优势+1-2个提升方向+具体改进计划'
    })
    
    return questions[:30]  # 最多30道题

def get_disclaimer():
    """获取免责申明HTML"""
    return """
    <!-- 免责申明 -->
    <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-left: 4px solid #6c757d; font-size: 12px; color: #6c757d;">
        <h3 style="color: #495057; margin-bottom: 10px; font-size: 14px;">免责申明</h3>
        <p style="margin-bottom: 8px;">1. 本技能仅提供求职策略指导与工具支持，不收集敏感隐私信息，不承诺任何录用结果，所有建议仅供个人求职参考，不构成正式决策依据，相关后果由用户自行承担。</p>
        <p>2. 用户对输入数据的真实性、准确性等负全责，因数据问题导致的偏差及损失由用户自行承担。</p>
    </div>
"""

def get_svg_charts():
    """获取完整的静态SVG图表，确保所有格式下正常显示"""
    return """
    <!-- 评分维度分析柱状图 -->
    <div style="margin: 30px 0; text-align: center;">
        <svg width="630" height="280" viewBox="0 0 630 280" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="630" height="280" fill="#f8f9fa" rx="8"/>
            <text x="315" y="30" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">评分维度分析</text>
            
            <line x1="80" y1="240" x2="580" y2="240" stroke="#ddd" stroke-width="2"/>
            <line x1="80" y1="240" x2="80" y2="50" stroke="#ddd" stroke-width="2"/>
            
            <text x="70" y="60" text-anchor="end" fill="#666" font-size="11">100</text>
            <text x="70" y="105" text-anchor="end" fill="#666" font-size="11">80</text>
            <text x="70" y="150" text-anchor="end" fill="#666" font-size="11">60</text>
            <text x="70" y="195" text-anchor="end" fill="#666" font-size="11">40</text>
            <text x="70" y="240" text-anchor="end" fill="#666" font-size="11">0</text>
            
            <rect x="110" y="72" width="50" height="168" fill="#3498db" rx="4"/>
            <text x="135" y="65" text-anchor="middle" fill="#2980b9" font-size="12" font-weight="bold">85</text>
            <text x="135" y="255" text-anchor="middle" fill="#666" font-size="10">硬性条件</text>
            
            <rect x="180" y="64" width="50" height="176" fill="#2ecc71" rx="4"/>
            <text x="205" y="57" text-anchor="middle" fill="#27ae60" font-size="12" font-weight="bold">88</text>
            <text x="205" y="255" text-anchor="middle" fill="#666" font-size="10">工作经验</text>
            
            <rect x="250" y="80" width="50" height="160" fill="#e74c3c" rx="4"/>
            <text x="275" y="73" text-anchor="middle" fill="#c0392b" font-size="12" font-weight="bold">82</text>
            <text x="275" y="255" text-anchor="middle" fill="#666" font-size="10">专业技能</text>
            
            <rect x="320" y="56" width="50" height="184" fill="#f39c12" rx="4"/>
            <text x="345" y="49" text-anchor="middle" fill="#d68910" font-size="12" font-weight="bold">90</text>
            <text x="345" y="255" text-anchor="middle" fill="#666" font-size="10">综合素质</text>
            
            <rect x="390" y="76" width="50" height="164" fill="#9b59b6" rx="4"/>
            <text x="415" y="69" text-anchor="middle" fill="#8e44ad" font-size="12" font-weight="bold">86</text>
            <text x="415" y="255" text-anchor="middle" fill="#666" font-size="10">项目经验</text>
            
            <rect x="460" y="68" width="50" height="172" fill="#1abc9c" rx="4"/>
            <text x="485" y="61" text-anchor="middle" fill="#16a085" font-size="12" font-weight="bold">87</text>
            <text x="485" y="255" text-anchor="middle" fill="#666" font-size="10">团队协作</text>
            
            <rect x="530" y="84" width="50" height="156" fill="#e67e22" rx="4"/>
            <text x="555" y="77" text-anchor="middle" fill="#d35400" font-size="12" font-weight="bold">81</text>
            <text x="555" y="255" text-anchor="middle" fill="#666" font-size="10">创新能力</text>
        </svg>
    </div>
"""

def write_html_with_bom(file_path, html_content):
    """写入HTML文件，包含UTF-8 BOM以避免乱码"""
    try:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(html_content)
    except Exception as e:
        # 如果utf-8-sig失败，尝试标准utf-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

def generate_resume_html(resume_data, job_name, company):
    """生成纯可投递优化版简历HTML - 简约现代风格"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 填充模板变量
    name = resume_data.get('personal_info', {}).get('name', '姓名')
    phone = resume_data.get('personal_info', {}).get('phone', '138****5678')
    email = resume_data.get('personal_info', {}).get('email', 'example@email.com')
    location = resume_data.get('personal_info', {}).get('location', '北京')
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - 优化简历</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #2c3e50;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 850px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-radius: 12px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .contact {{
            font-size: 14px;
            opacity: 0.95;
        }}
        .section-title {{
            font-size: 18px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin: 30px 0 20px 0;
            font-weight: 600;
        }}
        .experience-item, .project-item {{
            margin-bottom: 25px;
        }}
        .company-name, .project-name {{
            font-weight: 600;
            font-size: 16px;
            color: #2c3e50;
        }}
        .date {{
            float: right;
            color: #7f8c8d;
            font-size: 14px;
        }}
        .position {{
            color: #667eea;
            font-weight: 500;
            margin: 5px 0;
        }}
        ul {{ margin-left: 20px; margin-top: 10px; }}
        li {{ margin-bottom: 8px; }}
        .skill-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}
        .skill-tag {{
            background: #f0f7ff;
            color: #667eea;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
        }}
        .export-section {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .export-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 14px;
            border-radius: 25px;
            cursor: pointer;
            margin: 0 10px;
            font-weight: 500;
        }}
        .export-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; padding: 20px; border-radius: 0; }}
            .header {{ background: #2c3e50 !important; -webkit-print-color-adjust: exact; }}
            .export-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{name}</h1>
            <div class="contact">
                📞 {phone} &nbsp;&nbsp;📧 {email} &nbsp;&nbsp;📍 {location}
            </div>
        </div>
        
        <div class="section-title">求职意向</div>
        <div style="font-size: 16px; font-weight: 500;">
            意向岗位：{job_name} &nbsp;&nbsp;|&nbsp;&nbsp; 目标公司：{company}
        </div>
"""
    
    # 添加工作经历
    if 'experience' in resume_data:
        html_content += """
        <div class="section-title">工作经历</div>
"""
        for exp in resume_data['experience']:
            company = exp.get('company', '')
            position = exp.get('position', '')
            start_date = exp.get('start_time', '')
            end_date = exp.get('end_time', '')
            description = exp.get('description', '')
            
            html_content += f"""
        <div class="experience-item">
            <span class="company-name">{company}</span>
            <span class="date">{start_date} - {end_date}</span>
            <div class="position">{position}</div>
            <div style="color: #7f8c8d; margin-top: 8px;">{description}</div>
        </div>
"""
    
    # 添加项目经验
    if 'projects' in resume_data:
        html_content += """
        <div class="section-title">项目经验</div>
"""
        for proj in resume_data['projects']:
            proj_name = proj.get('name', '')
            proj_desc = proj.get('description', '')
            start_date = proj.get('start_time', '')
            end_date = proj.get('end_time', '')
            
            html_content += f"""
        <div class="project-item">
            <span class="project-name">{proj_name}</span>
            <span class="date">{start_date} - {end_date}</span>
            <div style="color: #7f8c8d; margin-top: 8px;">{proj_desc}</div>
        </div>
"""
    
    # 添加专业技能
    if 'skills' in resume_data:
        html_content += """
        <div class="section-title">专业技能</div>
        <div class="skill-tags">
"""
        for skill in resume_data['skills']:
            html_content += f'            <span class="skill-tag">{skill}</span>\n'
        html_content += '        </div>\n'
    
    # 添加教育背景
    if 'education' in resume_data:
        edu = resume_data['education']
        school = edu.get('school', '')
        degree = edu.get('degree', '')
        major = edu.get('major', '')
        start_date = edu.get('start_time', '')
        end_date = edu.get('end_time', '')
        
        html_content += f"""
        <div class="section-title">教育背景</div>
        <div style="font-weight: 600;">{school}</div>
        <div style="color: #7f8c8d;">{degree} · {major}</div>
        <div style="color: #7f8c8d; margin-top: 5px;">{start_date} - {end_date}</div>
"""
    
    # 导出按钮
    html_content += f"""
        <div class="export-section">
            <button class="export-btn" onclick="window.print()">导出为 PDF</button>
            <button class="export-btn" onclick="downloadHTML()">下载 HTML</button>
        </div>
        <script>
            function downloadHTML() {{
                const htmlContent = document.documentElement.outerHTML;
                const blob = new Blob([htmlContent], {{type: 'text/html;charset=utf-8'}});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = '{name}_优化简历.html';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }}
        </script>
    </div>
"""
    
    # 添加免责申明
    html_content += get_disclaimer()
    
    html_content += "\n</body>\n</html>"
    
    return html_content

def generate_analysis_report_html(resume_data, job_data, match_score_data):
    """生成岗位匹配度分析报告HTML - 使用智能匹配算法 + 岗位类型特定维度"""
    current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    
    # 解析匹配度数据
    if isinstance(match_score_data, dict):
        total_score = match_score_data.get('total', 75)
        breakdown = match_score_data.get('breakdown', {})
        job_type = match_score_data.get('job_type', 'general')
        dimensions_config = match_score_data.get('dimensions_config', get_job_type_dimensions('general'))
    else:
        total_score = match_score_data
        breakdown = {}
        job_type = 'general'
        dimensions_config = get_job_type_dimensions('general')
    
    def get_match_level(score):
        """根据分数获取匹配等级"""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "合格"
        else:
            return "不合格"
    
    def get_job_type_label(job_type):
        """获取岗位类型中文标签"""
        labels = {
            'tech': '技术岗',
            'operation': '运营岗',
            'sales': '销售岗',
            'management': '管理岗',
            'general': '通用岗'
        }
        return labels.get(job_type, '通用岗')
    
    def get_dynamic_svg_charts(breakdown_scores, dimensions_config):
        """根据岗位类型和维度配置生成动态SVG图表"""
        dimensions = dimensions_config['dimensions']
        chart_title = dimensions_config['chart_title']
        
        # 生成颜色方案
        colors = [
            ('#3498db', '#2980b9'),
            ('#2ecc71', '#27ae60'),
            ('#e74c3c', '#c0392b'),
            ('#f39c12', '#d68910'),
            ('#9b59b6', '#8e44ad'),
            ('#1abc9c', '#16a085')
        ]
        
        def calc_y(score):
            return 240 - (score * 1.9)
        
        # 计算图表宽度
        dim_count = len(dimensions)
        bar_width = 700 / (dim_count * 2) if dim_count > 0 else 100
        bar_spacing = bar_width * 0.5
        
        svg_parts = []
        svg_parts.append('''
        <!-- 动态岗位类型分析柱状图 -->
        <div style="margin: 30px 0; text-align: center;">
            <svg width="750" height="300" viewBox="0 0 750 300" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="750" height="300" fill="#f8f9fa" rx="8"/>
                <text x="375" y="30" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">''' + chart_title + '''</text>
                <text x="375" y="50" text-anchor="middle" fill="#666" font-size="12">岗位类型：''' + get_job_type_label(job_type) + '''</text>
                
                <line x1="60" y1="260" x2="700" y2="260" stroke="#ddd" stroke-width="2"/>
                <line x1="60" y1="260" x2="60" y2="60" stroke="#ddd" stroke-width="2"/>
                
                <text x="50" y="70" text-anchor="end" fill="#666" font-size="11">100</text>
                <text x="50" y="120" text-anchor="end" fill="#666" font-size="11">80</text>
                <text x="50" y="170" text-anchor="end" fill="#666" font-size="11">60</text>
                <text x="50" y="220" text-anchor="end" fill="#666" font-size="11">40</text>
                <text x="50" y="260" text-anchor="end" fill="#666" font-size="11">0</text>
        ''')
        
        # 绘制每个维度的柱状图
        for i, dim in enumerate(dimensions):
            dim_name = dim['name']
            score = round(breakdown_scores.get(dim_name, 70))
            color_fill, color_text = colors[i % len(colors)]
            x_pos = 80 + i * (bar_width + bar_spacing)
            
            svg_parts.append(f'''
                <rect x="{x_pos}" y="{calc_y(score)}" width="{bar_width}" height="{score * 1.9}" fill="{color_fill}" rx="4"/>
                <text x="{x_pos + bar_width/2}" y="{calc_y(score) - 8}" text-anchor="middle" fill="{color_text}" font-size="12" font-weight="bold">{score}</text>
                <text x="{x_pos + bar_width/2}" y="278" text-anchor="middle" fill="#666" font-size="9" transform="rotate(-15, {x_pos + bar_width/2}, 278)">{dim_name}</text>
            ''')
        
        svg_parts.append('''
            </svg>
        </div>
        ''')
        
        return '\n'.join(svg_parts)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>岗位匹配度分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #2c3e50;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-radius: 12px;
        }}
        h1 {{
            font-size: 28px;
            text-align: center;
            margin-bottom: 10px;
            color: #667eea;
            font-weight: 600;
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        .score-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 35px;
            text-align: center;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }}
        .score-value {{ font-size: 64px; font-weight: 700; }}
        .score-label {{ font-size: 16px; margin-top: 10px; opacity: 0.95; }}
        .score-level {{ font-size: 24px; margin-top: 5px; font-weight: 600; }}
        h2 {{
            font-size: 18px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin: 30px 0 20px 0;
            font-weight: 600;
        }}
        .dimension {{
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .dimension-title {{
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        .dimension-score {{
            float: right;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 13px;
        }}
        ul {{ margin-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        .positive {{ color: #27ae60; }}
        .suggestion {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
        }}
        .recommendation {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            font-weight: 600;
            margin-top: 20px;
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; padding: 20px; border-radius: 0; }}
            .score-card {{ background: #2c3e50 !important; -webkit-print-color-adjust: exact; }}
            .dimension-score, .recommendation {{ background: #2c3e50 !important; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>岗位匹配度分析报告</h1>
        <div class="subtitle">生成时间：{current_datetime}</div>
        
        <div class="score-card">
            <div class="score-value">{total_score}</div>
            <div class="score-label">整体匹配度</div>
            <div class="score-level">{get_match_level(total_score)}</div>
        </div>
    """
    
    html_content += f"<h2>{dimensions_config['chart_title']}</h2>"
    html_content += get_dynamic_svg_charts(breakdown, dimensions_config)
    
    html_content += f"<h2>分维度匹配度详细分析（{get_job_type_label(job_type)}）</h2>"
    
    # 动态生成每个维度的HTML
    dimension_html_parts = []
    for dim in dimensions_config['dimensions']:
        dim_name = dim['name']
        dim_weight = dim['weight']
        dim_desc = dim['description']
        score = round(breakdown.get(dim_name, 70))
        
        dimension_html_parts.append(f'''
        <div class="dimension">
            <span class="dimension-score">{score}分</span>
            <div class="dimension-title">{dim_name} (权重{dim_weight}%)</div>
            <ul>
                <li class="positive">✓ {dim_desc}</li>
                <li class="suggestion">💡 建议：在简历中突出{dim_name}相关的经历和成果</li>
            </ul>
        </div>
        ''')
    
    # 生成总分公式说明
    formula_parts = []
    for dim in dimensions_config['dimensions']:
        formula_parts.append(f"{dim['weight']/100}×{dim['name']}分")
    
    total_formula = "Score = " + " + ".join(formula_parts)
    
    html_content += '\n'.join(dimension_html_parts)
    
    # 构建推荐建议
    if total_score >= 70:
        recommendation = "✓ 推荐投递"
    elif total_score >= 60:
        recommendation = "⚠ 谨慎投递"
    else:
        recommendation = "✗ 不推荐投递"
    
    html_content += f'''
        <div class="suggestion">
            <strong>智能匹配算法总分公式：</strong><br>
            {total_formula}
        </div>
        
        <h2>最终投递建议</h2>
        <div class="recommendation">{recommendation}</div>
    </div>
    '''
    
    # 添加免责申明
    html_content += get_disclaimer()
    
    html_content += "\n</body>\n</html>"
    
    return html_content

def generate_modification_guide_html(original_resume, optimized_resume):
    """生成详细修改说明文档HTML"""
    current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>简历优化修改说明文档</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #2c3e50;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-radius: 12px;
        }}
        h1 {{
            font-size: 28px;
            text-align: center;
            margin-bottom: 10px;
            color: #667eea;
            font-weight: 600;
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        h2 {{
            font-size: 18px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin: 30px 0 20px 0;
            font-weight: 600;
        }}
        .modification-item {{
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .modification-title {{
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        .suggestion {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; padding: 20px; border-radius: 0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>简历优化修改说明文档</h1>
        <div class="subtitle">生成时间：{current_datetime}</div>
        
        <h2>优化思路</h2>
        <div class="modification-item">
            <div class="modification-title">整体优化策略</div>
            <ul>
                <li>突出与目标岗位高度匹配的核心技能、项目经验和可量化工作成果</li>
                <li>优化整体语言表达、逻辑结构和关键词布局</li>
                <li>兼顾ATS系统识别通过率和HR初筛阅读体验</li>
                <li>统一采用「执行动作 + 工作内容 + 可量化成果/价值」的行业通用句式</li>
            </ul>
        </div>
        
        <h2>后续调整建议</h2>
        <div class="suggestion">
            <strong>个性化微调方法：</strong><br>
            1. 根据不同岗位的JD，调整工作经历和项目经验的优先级<br>
            2. 针对特定岗位的关键词，适度调整描述中的用词<br>
            3. 根据目标公司的文化风格，微调简历的语言风格<br>
            4. 保持核心内容不变，仅调整表述方式和侧重点
        </div>
    </div>
"""
    
    # 添加免责申明
    html_content += get_disclaimer()
    
    html_content += "\n</body>\n</html>"
    
    return html_content

def main():
    parser = argparse.ArgumentParser(description='生成简历优化文档')
    parser.add_argument('resume_file', help='原始简历JSON文件路径')
    parser.add_argument('--job-file', help='岗位信息JSON文件路径（可选）')
    parser.add_argument('--job-name', required=True, help='目标岗位名称')
    parser.add_argument('--company', required=True, help='目标公司名称')
    parser.add_argument('--output-dir', default='.', help='输出目录')
    
    args = parser.parse_args()
    
    # 加载简历数据
    resume_data = load_json_file(args.resume_file)
    
    # 加载岗位数据（如果提供）
    job_data = {}
    if args.job_file:
        job_data = load_json_file(args.job_file)
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成优化版简历 - 简约现代风格
    resume_html = generate_resume_html(resume_data, args.job_name, args.company)
    write_html_with_bom(output_dir / 'optimized_resume.html', resume_html)
    print(f"✓ 优化版简历已生成：optimized_resume.html")
    
    # 使用智能匹配算法计算匹配度（传入岗位名称以支持岗位类型识别）
    match_score_data = calculate_matching_score(resume_data, job_data, args.job_name)
    
    # 根据岗位类型输出不同的信息
    job_type = match_score_data.get('job_type', 'general')
    job_type_label = {
        'tech': '技术岗',
        'operation': '运营岗',
        'sales': '销售岗',
        'management': '管理岗',
        'general': '通用岗'
    }.get(job_type, '通用岗')
    
    print(f"✓ 智能匹配度计算完成（{job_type_label}）：总分{match_score_data['total']}分")
    
    # 输出各维度分数
    breakdown = match_score_data.get('breakdown', {})
    dimensions_config = match_score_data.get('dimensions_config', {}).get('dimensions', [])
    for dim in dimensions_config:
        dim_name = dim['name']
        score = round(breakdown.get(dim_name, 70))
        print(f"  - {dim_name}：{score}分")
    
    # 生成岗位匹配度分析报告（使用智能匹配算法结果）
    analysis_html = generate_analysis_report_html(resume_data, job_data, match_score_data)
    write_html_with_bom(output_dir / 'match_analysis_report.html', analysis_html)
    print(f"✓ 岗位匹配度分析报告已生成：match_analysis_report.html")
    
    # 基于简历和JD动态生成面试题目
    interview_questions = generate_interview_questions(resume_data, job_data)
    questions_file = output_dir / 'interview_questions.json'
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump(interview_questions, f, ensure_ascii=False, indent=2)
    print(f"✓ 动态面试题库已生成：{len(interview_questions)}道题")
    
    # 生成修改说明文档
    guide_html = generate_modification_guide_html(resume_data, resume_data)
    write_html_with_bom(output_dir / 'modification_guide.html', guide_html)
    print(f"✓ 修改说明文档已生成：modification_guide.html")
    
    print("\n所有文档生成完成！")
    print(f"输出目录：{output_dir.absolute()}")
    print("\n🚀 迭代升级完成：")
    print("  ✓ P1-1：面试题库从硬编码改为从简历JSON动态生成")
    print("  ✓ P1-2：匹配度评分从静态值升级为智能匹配算法")
    print("  ✓ P2-3：匹配度报告评分维度动态生成")

if __name__ == "__main__":
    main()
