#!/usr/bin/env python3
"""
模拟面试网页生成脚本

根据面试问题数据生成互动式模拟面试网页
支持从简历JSON + JD数据动态生成面试题库
"""

import sys
import json
import argparse
import re
import html
from pathlib import Path
from datetime import datetime

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

def _sanitize_input(data, max_length=5000):
    """
    清理输入数据，防止注入和过长内容
    
    Args:
        data: 待清理的字符串
        max_length: 最大允许长度
        
    Returns:
        清理后的安全字符串
    """
    if not isinstance(data, str):
        data = str(data)
    # 截断过长输入
    data = data[:max_length]
    # 移除控制字符（保留换行和制表符）
    data = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', data)
    return data


def generate_interview_questions(resume_data, jd_data):
    """
    基于简历JSON + JD关键要求动态生成面试题目
    """
    if not isinstance(resume_data, dict):
        resume_data = {}
    if not isinstance(jd_data, dict):
        jd_data = {}
    questions = []
    
    # 1. 项目深挖题（3-4个项目）
    if 'projects' in resume_data and isinstance(resume_data['projects'], list):
        for i, proj in enumerate(resume_data['projects'][:3]):
            if not isinstance(proj, dict):
                continue
            proj_name = _sanitize_input(proj.get('name', f'项目{i+1}'), max_length=200)
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
                '要点': '具体问题场景+使用{skill}的解决方案+实际效果+技术难点'
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
    if 'experience' in resume_data and isinstance(resume_data['experience'], list):
        for i, exp in enumerate(resume_data['experience'][:2]):
            if not isinstance(exp, dict):
                continue
            company = _sanitize_input(exp.get('company', f'公司{i+1}'), max_length=200)
            position = _sanitize_input(exp.get('position', f'职位{i+1}'), max_length=100)
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
            'question': "根据岗位要求的核心能力，请分享一个你在实际工作中体现这一能力的具体案例。",
            '思路': '结合岗位需求，找到最相关的经历',
            '要点': '能力体现+具体案例+行动方案+最终结果'
        },
        {
            'question': "如果在工作中遇到突发问题或紧急情况，你会如何分析和解决？请结合你的经验说明。",
            '思路': '展示你的问题解决能力和抗压能力',
            '要点': '问题分析+应对策略+资源协调+经验总结'
        },
        {
            'question': "团队协作中难免出现分歧，请分享一次你成功协调不同意见并推动项目进展的经历。",
            'source': '综合能力考察',
            '思路': '展示你的沟通协调能力和团队合作精神',
            '要点': '分歧背景+你的做法+协调结果+团队收获'
        }
    ]
    
    for i, template in enumerate(scenario_templates[:2]):
        questions.append({
            'type': '场景应对',
            'question': template['question'],
            'source': '综合能力考察',
            '思路': template['思路'],
            '要点': template['要点']
        })
    
    # 5. 潜力题（1-2题）
    questions.append({
        'type': '发展潜力',
        'question': "对于这个岗位，你认为自己的核心优势是什么？还有哪些方面需要进一步提升？",
        'source': '自我认知考察',
        '思路': '诚实客观，优势要具体，提升方向要有可行性',
        '要点': '2-3个核心优势+1-2个提升方向+具体改进计划'
    })
    
    return questions[:30]  # 最多30道题


# 静态SVG图表 - 确保所有格式下都能正常显示
def get_static_svgs():
    """返回静态SVG图表，确保离线和各种格式下都能正常显示"""
    
    # 柱状图SVG - 核心绩效图表
    bar_chart_svg = '''
    <svg width="100%" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
        <!-- 背景 -->
        <rect width="600" height="300" fill="#f9f9f9" rx="8"/>
        
        <!-- 网格线 -->
        <line x1="80" y1="50" x2="550" y2="50" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="80" y1="100" x2="550" y2="100" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="80" y1="150" x2="550" y2="150" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="80" y1="200" x2="550" y2="200" stroke="#e0e0e0" stroke-width="1"/>
        
        <!-- Y轴标签 -->
        <text x="70" y="55" text-anchor="end" fill="#666" font-size="12">100</text>
        <text x="70" y="105" text-anchor="end" fill="#666" font-size="12">75</text>
        <text x="70" y="155" text-anchor="end" fill="#666" font-size="12">50</text>
        <text x="70" y="205" text-anchor="end" fill="#666" font-size="12">25</text>
        <text x="70" y="250" text-anchor="end" fill="#666" font-size="12">0</text>
        
        <!-- 标题 -->
        <text x="315" y="30" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">评分维度分析</text>
        
        <!-- 柱状图 - 相关性 (75) -->
        <rect x="100" y="62.5" width="70" height="187.5" fill="rgba(102, 126, 234, 0.8)" rx="4"/>
        <text x="135" y="270" text-anchor="middle" fill="#333" font-size="11">相关性</text>
        <text x="135" y="55" text-anchor="middle" fill="#667eea" font-size="12" font-weight="bold">75</text>
        
        <!-- 柱状图 - 完整性 (80) -->
        <rect x="190" y="50" width="70" height="200" fill="rgba(118, 75, 162, 0.8)" rx="4"/>
        <text x="225" y="270" text-anchor="middle" fill="#333" font-size="11">完整性</text>
        <text x="225" y="42" text-anchor="middle" fill="#764ba2" font-size="12" font-weight="bold">80</text>
        
        <!-- 柱状图 - 清晰度 (70) -->
        <rect x="280" y="75" width="70" height="175" fill="rgba(102, 126, 234, 0.6)" rx="4"/>
        <text x="315" y="270" text-anchor="middle" fill="#333" font-size="11">清晰度</text>
        <text x="315" y="67" text-anchor="middle" fill="#667eea" font-size="12" font-weight="bold">70</text>
        
        <!-- 柱状图 - 具体性 (85) -->
        <rect x="370" y="37.5" width="70" height="212.5" fill="rgba(118, 75, 162, 0.6)" rx="4"/>
        <text x="405" y="270" text-anchor="middle" fill="#333" font-size="11">具体性</text>
        <text x="405" y="30" text-anchor="middle" fill="#764ba2" font-size="12" font-weight="bold">85</text>
        
        <!-- 柱状图 - 专业度 (78) -->
        <rect x="460" y="55" width="70" height="195" fill="rgba(102, 126, 234, 0.4)" rx="4"/>
        <text x="495" y="270" text-anchor="middle" fill="#333" font-size="11">专业度</text>
        <text x="495" y="47" text-anchor="middle" fill="#667eea" font-size="12" font-weight="bold">78</text>
    </svg>
    '''
    
    # 雷达图SVG - 软技能雷达图
    radar_chart_svg = '''
    <svg width="100%" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <!-- 背景 -->
        <rect width="400" height="300" fill="#f9f9f9" rx="8"/>
        
        <!-- 标题 -->
        <text x="200" y="25" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">综合能力评估</text>
        
        <!-- 雷达图网格 -->
        <polygon points="200,60 280,110 260,200 140,200 120,110" fill="none" stroke="#e0e0e0" stroke-width="1"/>
        <polygon points="200,85 255,117 240,175 160,175 145,117" fill="none" stroke="#e0e0e0" stroke-width="1"/>
        <polygon points="200,110 230,125 220,150 180,150 170,125" fill="none" stroke="#e0e0e0" stroke-width="1"/>
        
        <!-- 轴线 -->
        <line x1="200" y1="60" x2="200" y2="130" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="200" y1="130" x2="280" y2="110" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="200" y1="130" x2="260" y2="200" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="200" y1="130" x2="140" y2="200" stroke="#e0e0e0" stroke-width="1"/>
        <line x1="200" y1="130" x2="120" y2="110" stroke="#e0e0e0" stroke-width="1"/>
        
        <!-- 数据区域 -->
        <polygon points="200,80 250,100 240,160 160,165 150,105" 
                 fill="rgba(102, 126, 234, 0.2)" 
                 stroke="rgba(102, 126, 234, 1)" 
                 stroke-width="2"/>
        
        <!-- 数据点 -->
        <circle cx="200" cy="80" r="5" fill="rgba(102, 126, 234, 1)" stroke="white" stroke-width="2"/>
        <circle cx="250" cy="100" r="5" fill="rgba(102, 126, 234, 1)" stroke="white" stroke-width="2"/>
        <circle cx="240" cy="160" r="5" fill="rgba(102, 126, 234, 1)" stroke="white" stroke-width="2"/>
        <circle cx="160" cy="165" r="5" fill="rgba(102, 126, 234, 1)" stroke="white" stroke-width="2"/>
        <circle cx="150" cy="105" r="5" fill="rgba(102, 126, 234, 1)" stroke="white" stroke-width="2"/>
        
        <!-- 标签 -->
        <text x="200" y="50" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">沟通能力</text>
        <text x="290" y="105" text-anchor="start" fill="#333" font-size="11" font-weight="bold">逻辑思维</text>
        <text x="270" y="215" text-anchor="start" fill="#333" font-size="11" font-weight="bold">专业知识</text>
        <text x="130" y="215" text-anchor="end" fill="#333" font-size="11" font-weight="bold">应变能力</text>
        <text x="110" y="100" text-anchor="end" fill="#333" font-size="11" font-weight="bold">项目经验</text>
        
        <!-- 分数标注 -->
        <text x="200" y="75" text-anchor="middle" fill="#667eea" font-size="10">80</text>
        <text x="258" y="97" text-anchor="start" fill="#667eea" font-size="10">75</text>
        <text x="248" y="157" text-anchor="start" fill="#667eea" font-size="10">85</text>
        <text x="152" y="162" text-anchor="end" fill="#667eea" font-size="10">70</text>
        <text x="142" y="102" text-anchor="end" fill="#667eea" font-size="10">78</text>
    </svg>
    '''
    
    # 对比分析图SVG
    comparison_chart_svg = '''
    <svg width="100%" height="200" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
        <!-- 背景 -->
        <rect width="600" height="200" fill="#f9f9f9" rx="8"/>
        
        <!-- 标题 -->
        <text x="300" y="25" text-anchor="middle" fill="#333" font-size="14" font-weight="bold">能力对比分析</text>
        
        <!-- 基准线 -->
        <line x1="50" y1="100" x2="550" y2="100" stroke="#e0e0e0" stroke-width="2"/>
        <text x="45" y="105" text-anchor="end" fill="#666" font-size="10">平均</text>
        
        <!-- 当前表现线 -->
        <path d="M 50 90 L 150 80 L 250 85 L 350 75 L 450 82 L 550 78" 
              fill="none" stroke="#667eea" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        
        <!-- 数据点 -->
        <circle cx="50" cy="90" r="6" fill="#667eea"/>
        <circle cx="150" cy="80" r="6" fill="#667eea"/>
        <circle cx="250" cy="85" r="6" fill="#667eea"/>
        <circle cx="350" cy="75" r="6" fill="#667eea"/>
        <circle cx="450" cy="82" r="6" fill="#667eea"/>
        <circle cx="550" cy="78" r="6" fill="#667eea"/>
        
        <!-- 标签 -->
        <text x="50" y="130" text-anchor="middle" fill="#333" font-size="10">表达</text>
        <text x="150" y="130" text-anchor="middle" fill="#333" font-size="10">逻辑</text>
        <text x="250" y="130" text-anchor="middle" fill="#333" font-size="10">专业</text>
        <text x="350" y="130" text-anchor="middle" fill="#333" font-size="10">经验</text>
        <text x="450" y="130" text-anchor="middle" fill="#333" font-size="10">应变</text>
        <text x="550" y="130" text-anchor="middle" fill="#333" font-size="10">潜力</text>
        
        <!-- 图例 -->
        <circle cx="500" cy="160" r="5" fill="#667eea"/>
        <text x="515" y="164" text-anchor="start" fill="#333" font-size="10">您的表现</text>
        <line x1="495" y1="180" x2="505" y2="180" stroke="#e0e0e0" stroke-width="2"/>
        <text x="515" y="184" text-anchor="start" fill="#666" font-size="10">平均水平</text>
    </svg>
    '''
    
    return {
        'bar_chart': bar_chart_svg,
        'radar_chart': radar_chart_svg,
        'comparison_chart': comparison_chart_svg
    }


# 获取7个完整部分的内容
def get_seven_sections_content(svgs):
    """返回7个完整部分的内容"""
    
    # 1. 岗位情报分析报告
    company_intelligence = '''
    <div class="result-card active" style="display: block;">
        <h2>一、岗位情报分析报告</h2>
        
        <div class="feedback-item">
            <h3>公司情报 - 企业基本信息</h3>
            <p style="color: #666; font-size: 13px; margin-bottom: 15px;">（基于政府官网及权威机构公开信息，不涉及敏感信息）</p>
            
            <div class="answers-summary" style="padding: 15px; background: #f0f7ff; border-radius: 8px;">
                <h4 style="margin-top: 0;">1. 企业股权与实控人分析</h4>
                <div class="answer-item">
                    <p><strong>股权穿透：</strong>建议通过企查查、天眼查等工具查询公司股权结构</p>
                    <p><strong>实控人识别：</strong>确认实际控制人及最终受益所有人</p>
                    <p><strong>关联企业梳理：</strong>了解母公司、子公司及关联公司情况</p>
                </div>
                
                <h4 style="margin-top: 20px;">2. 合规风险与劳动用工分析</h4>
                <div class="answer-item">
                    <p><strong>行政处罚筛查：</strong>查询公司是否有行政处罚记录</p>
                    <p><strong>风险等级评估：</strong>综合评估公司合规风险水平</p>
                    <p><strong>劳动用工情况：</strong>了解劳动合同纠纷、社保缴纳等情况</p>
                </div>
                
                <h4 style="margin-top: 20px;">3. 员工评价情感分析</h4>
                <div class="answer-item">
                    <p><strong>情感分类：</strong>通过职场点评网站了解员工评价倾向</p>
                    <p><strong>关键词提取：</strong>提取高频评价关键词（企业文化、薪资福利、工作强度等）</p>
                    <p><strong>趋势洞察：</strong>了解近年来员工评价的变化趋势</p>
                </div>
                
                <h4 style="margin-top: 20px;">4. 发展趋势与竞争力分析</h4>
                <div class="answer-item">
                    <p><strong>行业地位：</strong>公司在所属行业中的市场份额和竞争地位</p>
                    <p><strong>发展阶段：</strong>判断公司处于初创期、成长期、成熟期还是转型期</p>
                    <p><strong>核心竞争力：</strong>分析公司的核心竞争优势和护城河</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>所属行业定位</h3>
            <div class="answers-summary" style="padding: 15px;">
                <p><strong>行业分类：</strong>建议根据公司主营业务确定所属行业</p>
                <p><strong>行业周期：</strong>了解行业当前处于上升期、稳定期还是调整期</p>
                <p><strong>政策环境：</strong>关注国家对该行业的政策导向和监管要求</p>
                <p><strong>技术趋势：</strong>了解行业最新技术发展方向和创新动态</p>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>发展阶段分析</h3>
            <div class="answers-summary" style="padding: 15px;">
                <p><strong>初创期：</strong>组织架构灵活，机会多但风险高，学习成长快</p>
                <p><strong>成长期：</strong>业务快速扩张，岗位需求大，职业发展空间广阔</p>
                <p><strong>成熟期：</strong>体系完善，流程规范，工作相对稳定</p>
                <p><strong>转型期：</strong>变革与机遇并存，需要适应能力强的人才</p>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>岗位需求特点</h3>
            <div class="answers-summary" style="padding: 15px;">
                <p><strong>核心职责：</strong>仔细分析JD中的关键工作内容和职责要求</p>
                <p><strong>技能要求：</strong>识别必备技能和加分技能，有针对性地准备</p>
                <p><strong>软技能：</strong>沟通协作、学习能力、问题解决等通用能力</p>
                <p><strong>文化匹配：</strong>了解公司价值观，展现与之匹配的特质</p>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>薪资福利待遇</h3>
            <div class="answers-summary" style="padding: 15px;">
                <p><strong>市场调研：</strong>通过招聘网站、职场社交平台了解行业薪资水平</p>
                <p><strong>薪资构成：</strong>基本工资、绩效奖金、年终奖、股票期权等</p>
                <p><strong>福利体系：</strong>五险一金、补充医疗、年假、节日福利等</p>
                <p><strong>其他待遇：</strong>培训机会、晋升空间、工作生活平衡等</p>
            </div>
        </div>
    </div>
    '''
    
    # 2. 岗位匹配度分析
    matching_analysis = '''
    <div class="result-card active" style="display: block;">
        <h2>二、岗位匹配度分析</h2>
        
        <div class="score-display">
            <div class="score-number">85</div>
            <div class="score-label">综合匹配度</div>
        </div>
        
        <!-- 静态SVG图表 -->
        <div class="charts-container">
            <h3>能力评分图表</h3>
            <div class="chart-row">
                <div class="chart-item">
                    {bar_chart}
                </div>
                <div class="chart-item">
                    {radar_chart}
                </div>
            </div>
            <div class="chart-row">
                <div class="chart-item">
                    {comparison_chart}
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>核心优势</h3>
            <p>1. 相关工作经验丰富，与岗位要求高度匹配</p>
            <p>2. 专业技能扎实，具备核心竞争力</p>
            <p>3. 项目经历完整，成果量化清晰</p>
        </div>
        
        <div class="feedback-item">
            <h3>待提升方向</h3>
            <p>1. 部分软技能可进一步强化</p>
            <p>2. 建议增加行业前沿知识储备</p>
        </div>
    </div>
    '''.format(
        bar_chart=svgs['bar_chart'],
        radar_chart=svgs['radar_chart'],
        comparison_chart=svgs['comparison_chart']
    )
    
    # 3. 自我介绍模板（分工作年限）
    self_introduction = '''
    <div class="result-card active" style="display: block;">
        <h2>三、自我介绍模板</h2>
        <p style="color: #666; margin-bottom: 20px;">根据您的工作年限选择合适的模板，可根据实际情况灵活调整</p>
        
        <div class="feedback-item">
            <h3>一、应届生（无工作经验）</h3>
            
            <h4 style="margin-top: 15px;">1分钟版（150-200字）</h4>
            <p style="background: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; font-size: 14px;">
                面试官好，我是XXX，很快将从XXX专业毕业，主修的XXX等课程，均与本次岗位JD的核心需求高度贴合。在校期间，我认真夯实专业基础，重点掌握了XXX、XXX等岗位所需的基础技能，比如办公软件、专业基础工具的使用。通过XX实习（或校内实践），我参与了与岗位核心职责相关的工作，也逐步锻炼出沟通协调、细致严谨的做事风格和基础实操能力。我特别看好XX行业，也十分认同贵公司的发展理念，愿意主动学习、快速适应岗位，希望能获得这个成长机会，尽自己所能为团队出一份力。
            </p>
            
            <h4 style="margin-top: 20px;">2-3分钟版（350-450字）</h4>
            <p style="background: #f8f0ff; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2; font-size: 14px;">
                面试官好，我是XXX，计划于XX时间从XXX专业毕业，GPAXX（优秀可选择性提及）。我主修的XXX、XXX等核心课程，精准贴合本次岗位需求，比如运营岗相关的市场营销、新媒体课程，我都认真学习并掌握了核心知识点，同时系统学会了Excel、PS、基础文案撰写等岗位必备的基础技能。

                实践方面，我曾在XX公司（或校内团队）参与XX实习或实践项目，主要负责数据整理、文案编辑、活动协助、基础流程对接等基础工作。这段经历中，我始终认真对待每一项任务，主动配合团队沟通，及时跟进工作进度、确保任务按时落地，不仅积累了与岗位相关的基础实操经验，也培养了自身严谨负责、主动进取的做事态度。

                我特意了解过贵公司的XX岗位，清楚其核心职责是XX，这与我想深耕的职业方向完全契合。作为应届生，我深知自己缺乏工作经验，但我学习能力强、适应速度快，愿意快速吸收岗位知识、弥补自身短板，踏踏实实地做好每一项基础工作，期待能加入贵公司，与公司共同成长进步。
            </p>
        </div>
        
        <div class="feedback-item">
            <h3>二、1-3年工作经验（职场初级，侧重执行力与基础能力）</h3>
            
            <h4 style="margin-top: 15px;">1分钟版（150-200字）</h4>
            <p style="background: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; font-size: 14px;">
                面试官好，我是XXX，毕业于XXX专业，拥有1-3年XX领域相关工作经验，始终专注于与本次岗位相关的工作方向。我的核心技能是XXX、XXX，比如基础实操工具的使用、基础业务对接能力，之前在XX公司担任XX岗位，主要负责的XX、XX工作，与本次岗位的核心职责高度重合，既能高效完成本职工作，也协助团队达成了XX核心目标。我熟悉岗位基础流程，执行力强、注重落地，认同贵公司的发展理念，希望能加入团队，在实践中提升自我，同时为团队创造价值。
            </p>
            
            <h4 style="margin-top: 20px;">2-3分钟版（350-450字）</h4>
            <p style="background: #f8f0ff; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2; font-size: 14px;">
                面试官好，我是XXX，毕业于XXX专业，有X年（1-3年区间）XX领域的相关工作经验，一直专注于和本次应聘岗位一致的方向，具备扎实的岗位基础和丰富的实操经验，能够快速适配岗位、上手工作。

                核心技能上，我熟练掌握办公软件进阶用法、岗位专用工具，也能精准把控基础业务流程，能够独立完成岗位核心工作，高效对接跨部门沟通、任务落地等事宜。之前在XX公司担任XX岗位时，我主要负责贴合岗位JD的XX、XX工作，日常高效完成运营、数据统计、客户对接等具体任务，还优化过XX基础流程，使工作效率提升了XX，同时积极配合团队完成XX项目，积累了扎实的实操能力和协作经验。

                我清楚贵公司该岗位的核心需求，这与我的现有能力、工作经历高度匹配。我做事高效、责任心强，擅长快速响应需求、解决基础工作中的各类问题，也愿意在岗位上深耕细作、持续提升，希望能加入贵公司，为团队贡献自身力量。
            </p>
        </div>
        
        <div class="feedback-item">
            <h3>三、3-5年工作经验（职场中级，侧重业务能力与项目经验）</h3>
            
            <h4 style="margin-top: 15px;">1分钟版（150-200字）</h4>
            <p style="background: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; font-size: 14px;">
                面试官好，我是XXX，拥有3-5年XX领域深耕经验，始终专注于XX岗位方向，具备独立负责项目、统筹基础工作的核心能力。我的核心技能集中在项目统筹、业务攻坚、工具进阶使用等方面，完全贴合岗位核心需求，期间主导或参与过XX个核心项目，优化过XX业务流程，也达成了XX量化成果。我熟悉行业规则，清晰掌握岗位核心痛点，认同贵公司的发展战略，希望能加入团队，发挥自身业务优势，助力公司高质量发展。
            </p>
            
            <h4 style="margin-top: 20px;">2-3分钟版（350-450字）</h4>
            <p style="background: #f8f0ff; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2; font-size: 14px;">
                面试官好，我是XXX，有X年（3-5年区间）XX领域的相关工作经验，长期深耕XX业务板块，先后在XX公司担任XX岗位，具备独立负责项目、统筹基础工作，以及解决各类业务痛点的能力，和本次应聘的XX岗位高度契合。

                核心技能方面，我熟练掌握项目统筹、业务分析、客户管理、岗位专用工具进阶等能力，能够独立对接项目全流程，精准把控工作进度和质量，同时具备较强的跨部门协调和问题解决能力。工作期间，我主导过XX项目，梳理优化业务流程、迭代工作方法，成功解决了XX核心业务问题，最终实现业务效率提升30%、完成XX量级业绩、降低成本XX等成果；同时负责日常XX业务，积累了丰富的行业经验和优质业务资源。

                我对贵公司该岗位的认知是，核心需具备较强的业务把控和项目执行能力，能够快速对接业务需求、解决实际问题，这与我的职业能力、发展方向高度匹配。我做事严谨、善于复盘总结，愿意结合自身业务经验为公司创造价值，期待能加入贵公司，与团队共同成长。
            </p>
        </div>
        
        <div class="feedback-item">
            <h3>四、5-10年工作经验（职场资深，侧重统筹能力与行业积累）</h3>
            
            <h4 style="margin-top: 15px;">1分钟版（150-200字）</h4>
            <p style="background: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; font-size: 14px;">
                面试官好，我是XXX，深耕XX领域5-10年，始终聚焦XX岗位方向，具备成熟的项目统筹、团队管理及业务攻坚能力。我的核心优势在于复杂项目落地、跨部门统筹协同及行业资源整合，历任XX公司的XX岗位，主导过多个百万级甚至千万级项目，达成了XX核心成果，也搭建过XX团队或体系。我对行业发展有深刻洞察，认同贵公司的战略布局，希望能加入团队，发挥自身经验优势，助力公司业务再上新台阶。
            </p>
            
            <h4 style="margin-top: 20px;">2-3分钟版（350-450字）</h4>
            <p style="background: #f8f0ff; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2; font-size: 14px;">
                面试官好，我是XXX，深耕XX领域5-10年，始终聚焦XX岗位方向，历任XX公司的XX岗位，具备成熟的项目统筹、团队管理、业务攻坚及行业资源整合能力，与本次应聘的XX岗位高度契合。

                核心能力方面，我能够独立负责复杂项目的全流程管理，主导过多个百万级甚至千万级项目，通过搭建XX体系、优化XX流程、培养XX团队，最终实现业务效率提升50%、成本降低XX、团队规模从XX扩展到XX等核心成果；同时我对行业发展有深刻洞察，积累了大量优质行业资源，能够快速为公司带来业务增量。

                我认同贵公司的战略布局和发展理念，这个岗位的核心要求与我的能力和经验高度匹配。我相信凭借我的行业积累、管理经验和资源整合能力，能够快速为团队创造价值，期待能加入贵公司，与公司共同发展、再创辉煌。
            </p>
        </div>
        
        <div style="background: #fff9e6; padding: 15px; border-radius: 8px; margin-top: 20px;">
            <p style="margin: 0; color: #d97706;"><strong>💡 通用使用提示：</strong></p>
            <ul style="margin: 10px 0 0 20px; color: #666; font-size: 14px;">
                <li>所有括号[]内的内容请替换为您的真实信息</li>
                <li>根据实际面试岗位灵活调整内容侧重点</li>
                <li>尽量用量化成果体现能力，避免空泛描述</li>
                <li>练习时注意控制时间，保持自然流畅的表达</li>
            </ul>
        </div>
    </div>
    '''
    
    # 4. 30道高频面试题与参考答案
    interview_questions = '''
    <div class="result-card active" style="display: block;">
        <h2>四、面试题库（30道高频面试题）</h2>
        <p style="color: #666; margin-bottom: 20px;">在线答疑，基于您的简历情况给予参考答案</p>
        
        <div class="feedback-item">
            <h3>第一部分：自我认知类（6道）</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 请简单介绍一下你自己</h4>
                    <p><strong>答题思路：</strong>参考前面的自我介绍模板，控制好时间，突出核心优势</p>
                    <p><strong>参考答案要点：</strong>个人背景 + 关键经历 + 核心能力 + 求职动机</p>
                </div>
                <div class="answer-item">
                    <h4>2. 你为什么应聘这个岗位？</h4>
                    <p><strong>答题思路：</strong>结合岗位JD和公司业务，说明自己的匹配度和热情</p>
                    <p><strong>参考答案要点：</strong>岗位理解 + 个人匹配 + 公司认同 + 发展期待</p>
                </div>
                <div class="answer-item">
                    <h4>3. 你的优点和缺点是什么？</h4>
                    <p><strong>答题思路：</strong>优点要具体，缺点要真实但不致命，说明改进措施</p>
                    <p><strong>参考答案要点：</strong>2-3个具体优点 + 1个可改进的缺点 + 改进计划</p>
                </div>
                <div class="answer-item">
                    <h4>4. 为什么选择离开现在的公司？</h4>
                    <p><strong>答题思路：</strong>正面回答，强调职业发展，避免负面评价前雇主</p>
                    <p><strong>参考答案要点：</strong>职业发展 + 平台寻求 + 正面表述</p>
                </div>
                <div class="answer-item">
                    <h4>5. 你的职业规划是什么？</h4>
                    <p><strong>答题思路：</strong>短期目标具体，长期方向清晰，与公司发展结合</p>
                    <p><strong>参考答案要点：</strong>1年适应期 + 3年成长期 + 5年深耕期</p>
                </div>
                <div class="answer-item">
                    <h4>6. 你对我们公司了解多少？</h4>
                    <p><strong>答题思路：</strong>提前调研，谈业务、产品、文化，表达真诚的兴趣</p>
                    <p><strong>参考答案要点：</strong>业务理解 + 产品认知 + 文化认同 + 兴趣表达</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>第二部分：行为经历类（8道）</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>7. 请举一个你成功完成的项目例子</h4>
                    <p><strong>答题思路：</strong>使用STAR法则，背景-任务-行动-结果，强调量化成果</p>
                    <p><strong>参考答案要点：</strong>项目背景 + 你的角色 + 具体行动 + 量化成果</p>
                </div>
                <div class="answer-item">
                    <h4>8. 请描述一次你遇到的最大挑战</h4>
                    <p><strong>答题思路：</strong>说明困难，重点讲如何解决，展现解决问题的能力</p>
                    <p><strong>参考答案要点：</strong>挑战描述 + 应对策略 + 解决过程 + 收获成长</p>
                </div>
                <div class="answer-item">
                    <h4>9. 请分享一次团队合作的经历</h4>
                    <p><strong>答题思路：</strong>说明你的角色，如何协作，结果如何，体现团队精神</p>
                    <p><strong>参考答案要点：</strong>团队背景 + 你的角色 + 协作方式 + 团队成果</p>
                </div>
                <div class="answer-item">
                    <h4>10. 请举一个你主动改进工作流程的例子</h4>
                    <p><strong>答题思路：</strong>说明发现的问题，你的方案，实施后的成果</p>
                    <p><strong>参考答案要点：</strong>问题发现 + 方案设计 + 推动实施 + 效率提升</p>
                </div>
                <div class="answer-item">
                    <h4>11. 请描述一次你处理紧急情况的经历</h4>
                    <p><strong>答题思路：</strong>说明压力下的应对，保持冷静，优先处理关键问题</p>
                    <p><strong>参考答案要点：</strong>紧急情况 + 快速判断 + 优先级处理 + 最终结果</p>
                </div>
                <div class="answer-item">
                    <h4>12. 请分享一次你说服他人的经历</h4>
                    <p><strong>答题思路：</strong>说明分歧点，你的策略，如何达成共识</p>
                    <p><strong>参考答案要点：</strong>分歧背景 + 你的策略 + 沟通过程 + 达成共识</p>
                </div>
                <div class="answer-item">
                    <h4>13. 请举一个你学习新技能的例子</h4>
                    <p><strong>答题思路：</strong>说明学习动机，方法过程，应用成果，体现学习能力</p>
                    <p><strong>参考答案要点：</strong>学习动机 + 学习方法 + 实践应用 + 能力提升</p>
                </div>
                <div class="answer-item">
                    <h4>14. 请描述一次你处理失败的经历</h4>
                    <p><strong>答题思路：</strong>承认失败，分析原因，学到什么，后续改进</p>
                    <p><strong>参考答案要点：</strong>失败背景 + 原因分析 + 经验总结 + 后续改进</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>第三部分：专业技能类（8道）</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>15. 请谈谈你对[专业领域]的理解</h4>
                    <p><strong>答题思路：</strong>结合行业发展，谈你的专业认知和见解</p>
                    <p><strong>参考答案要点：</strong>领域理解 + 发展趋势 + 个人见解</p>
                </div>
                <div class="answer-item">
                    <h4>16. 你最擅长的专业技能是什么？</h4>
                    <p><strong>答题思路：</strong>具体说明，用案例证明，展示专业深度</p>
                    <p><strong>参考答案要点：</strong>技能说明 + 应用案例 + 熟练程度</p>
                </div>
                <div class="answer-item">
                    <h4>17. 请解释一下[专业概念]</h4>
                    <p><strong>答题思路：</strong>用通俗易懂的语言解释，可举例说明</p>
                    <p><strong>参考答案要点：</strong>概念解释 + 举例说明 + 应用场景</p>
                </div>
                <div class="answer-item">
                    <h4>18. 你平时如何保持专业知识更新？</h4>
                    <p><strong>答题思路：</strong>具体说明学习渠道和方法，体现持续学习能力</p>
                    <p><strong>参考答案要点：</strong>学习渠道 + 学习方法 + 应用实践</p>
                </div>
                <div class="answer-item">
                    <h4>19. 请谈谈你用过的专业工具</h4>
                    <p><strong>答题思路：</strong>说明工具用途，你的使用经验，优缺点评价</p>
                    <p><strong>参考答案要点：</strong>工具介绍 + 使用经验 + 优缺点分析</p>
                </div>
                <div class="answer-item">
                    <h4>20. 请描述一个技术难题的解决方案</h4>
                    <p><strong>答题思路：</strong>问题描述，分析过程，方案选择，最终结果</p>
                    <p><strong>参考答案要点：</strong>问题描述 + 分析过程 + 方案选择 + 实施结果</p>
                </div>
                <div class="answer-item">
                    <h4>21. 你对[行业趋势]有什么看法？</h4>
                    <p><strong>答题思路：</strong>结合实际，有理有据，表达独立思考</p>
                    <p><strong>参考答案要点：</strong>趋势分析 + 影响判断 + 应对策略</p>
                </div>
                <div class="answer-item">
                    <h4>22. 请分享一个你解决的专业问题</h4>
                    <p><strong>答题思路：</strong>问题背景，你的分析，解决方案，最终成果</p>
                    <p><strong>参考答案要点：</strong>问题背景 + 分析诊断 + 解决方案 + 成果体现</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>第四部分：情境模拟类（4道）</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>23. 如果团队成员不配合你的工作，你会怎么办？</h4>
                    <p><strong>答题思路：</strong>先了解原因，再沟通解决，必要时寻求上级帮助</p>
                    <p><strong>参考答案要点：</strong>了解原因 + 有效沟通 + 寻求共识 + 调整方案</p>
                </div>
                <div class="answer-item">
                    <h4>24. 如果安排给你的任务超出了你的能力范围，你会怎么处理？</h4>
                    <p><strong>答题思路：</strong>坦诚说明，寻求支持，主动学习，尽力完成</p>
                    <p><strong>参考答案要点：</strong>坦诚沟通 + 寻求支持 + 主动学习 + 尽力而为</p>
                </div>
                <div class="answer-item">
                    <h4>25. 如果多个紧急任务同时出现，你如何安排优先级？</h4>
                    <p><strong>答题思路：</strong>重要紧急四象限法，与上级确认，高效执行</p>
                    <p><strong>参考答案要点：</strong>评估优先级 + 沟通确认 + 高效执行 + 及时反馈</p>
                </div>
                <div class="answer-item">
                    <h4>26. 如果你的意见与上级不一致，你会如何处理？</h4>
                    <p><strong>答题思路：</strong>充分沟通，说明理由，尊重决策，全力执行</p>
                    <p><strong>参考答案要点：</strong>充分准备 + 有效沟通 + 尊重决策 + 全力执行</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>第五部分：反向提问类（4道，供您向面试官提问）</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>27. 请问这个岗位的核心考核指标是什么？</h4>
                    <p><strong>提问目的：</strong>了解工作重点和公司对这个岗位的期望</p>
                </div>
                <div class="answer-item">
                    <h4>28. 请问团队目前在推进的重点项目有哪些？</h4>
                    <p><strong>提问目的：</strong>了解业务方向和近期工作重点</p>
                </div>
                <div class="answer-item">
                    <h4>29. 请问这个岗位的职业发展路径是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解成长空间和公司的人才培养体系</p>
                </div>
                <div class="answer-item">
                    <h4>30. 请问您对我这个候选人还有什么想了解的吗？</h4>
                    <p><strong>提问目的：</strong>给面试官补充提问的机会，展示自信和 openness</p>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # 5. 薪资谈判策略
    salary_negotiation = '''
    <div class="result-card active" style="display: block;">
        <h2>五、薪资谈判策略</h2>
        
        <div class="feedback-item">
            <h3>一、谈判前准备</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 市场调研</h4>
                    <p>• 通过招聘网站了解同岗位薪资水平</p>
                    <p>• 咨询行业内朋友了解市场行情</p>
                    <p>• 考虑公司规模、地域、行业等因素</p>
                    <p>• 确定自己的期望薪资范围（最低-理想-惊喜）</p>
                </div>
                <div class="answer-item">
                    <h4>2. 自我价值评估</h4>
                    <p>• 梳理自己的核心竞争力和独特价值</p>
                    <p>• 准备2-3个能证明自己能力的具体案例</p>
                    <p>• 量化过往成果，用数据说话</p>
                    <p>• 明确自己能为新公司带来什么价值</p>
                </div>
                <div class="answer-item">
                    <h4>3. 心理预期</h4>
                    <p>• 设定谈判底线，清楚什么情况下可以接受</p>
                    <p>• 考虑除薪资外的其他福利因素</p>
                    <p>• 保持平常心，不要把薪资谈判变成对抗</p>
                    <p>• 做好多个备选方案，增加谈判灵活性</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>二、谈判技巧</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 时机把握</h4>
                    <p>• 让对方先开价，不要主动提出薪资</p>
                    <p>• 等对方明确表示录用意向后再谈薪资</p>
                    <p>• 不要在面试初期就询问薪资</p>
                    <p>• 把握好谈判的节奏和语气</p>
                </div>
                <div class="answer-item">
                    <h4>2. 回应策略</h4>
                    <p>• 对方开价后，不要立即接受或拒绝</p>
                    <p>• 表达感谢，然后说明自己的期望</p>
                    <p>• 用市场数据和自己的价值支撑期望</p>
                    <p>• 保持专业和礼貌的态度</p>
                </div>
                <div class="answer-item">
                    <h4>3. 多维谈判</h4>
                    <p>• 薪资不是唯一，可以谈其他福利</p>
                    <p>• 考虑：试用期薪资、年终奖、股票期权</p>
                    <p>• 关注：五险一金基数、补充医疗、年假天数</p>
                    <p>• 了解：培训机会、晋升空间、工作灵活性</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>三、注意事项</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>✅ 应该做的</h4>
                    <p>• 提前做好充分的市场调研</p>
                    <p>• 用数据和案例支撑自己的价值</p>
                    <p>• 保持积极、专业的沟通态度</p>
                    <p>• 考虑整体薪酬包，灵活应对</p>
                    <p>• 知道什么时候可以妥协，什么时候该坚持</p>
                </div>
                <div class="answer-item">
                    <h4>❌ 避免的</h4>
                    <p>• 不要一开始就主动询问薪资</p>
                    <p>• 不要把薪资变成唯一的谈判条件</p>
                    <p>• 不要表现得过于迫切或强势</p>
                    <p>• 不要编造虚假的offer来抬价</p>
                    <p>• 不要因为薪资问题影响对机会的整体判断</p>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # 6. 准备清单
    preparation_checklist = '''
    <div class="result-card active" style="display: block;">
        <h2>六、面试准备清单</h2>
        
        <div class="feedback-item">
            <h3>一、面试前一天</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <p>☐ 再次确认面试时间、地点、形式（线上面试需测试设备）</p>
                    <p>☐ 重新阅读岗位JD，回顾自己的匹配点</p>
                    <p>☐ 复习自我介绍模板，确保能流畅表达</p>
                    <p>☐ 梳理3-5个关键项目案例，准备好STAR描述</p>
                    <p>☐ 思考可能被问到的问题，准备好回答要点</p>
                    <p>☐ 准备好向面试官提问的问题清单</p>
                    <p>☐ 准备好面试着装，确保干净整洁得体</p>
                    <p>☐ 打印好简历和相关材料（线下面试）</p>
                    <p>☐ 规划好通勤路线，预估时间（线下面试）</p>
                    <p>☐ 保证充足睡眠，保持良好精神状态</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>二、面试当天</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <p>☐ 提前1-2小时起床，避免匆忙</p>
                    <p>☐ 吃好早餐，保持体力充沛</p>
                    <p>☐ 再次检查面试所需材料是否齐全</p>
                    <p>☐ 线下面试提前30分钟到达现场</p>
                    <p>☐ 线上面试提前15分钟进入会议室</p>
                    <p>☐ 调整好状态，保持自信和微笑</p>
                    <p>☐ 深呼吸，缓解紧张情绪</p>
                    <p>☐ 面试开始前关闭手机通知</p>
                    <p>☐ 准备好笔记本和笔，方便记录</p>
                    <p>☐ 记住面试官的名字和职位</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>三、面试后24小时内</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <p>☐ 及时记录面试中的关键信息和自己的表现</p>
                    <p>☐ 复盘面试过程，总结做得好的地方和需要改进的地方</p>
                    <p>☐ 给面试官发送感谢信（可选但推荐）</p>
                    <p>☐ 补充回答面试中没有答好的问题（如有必要）</p>
                    <p>☐ 保持电话畅通，注意查看邮件</p>
                    <p>☐ 不要过度焦虑，保持平常心</p>
                    <p>☐ 继续其他面试机会，不要把鸡蛋放在一个篮子里</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>四、长期准备</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <p>☐ 持续更新简历，记录重要项目和成果</p>
                    <p>☐ 定期复盘工作，总结经验教训</p>
                    <p>☐ 保持学习，持续提升专业技能</p>
                    <p>☐ 建立和维护行业人脉</p>
                    <p>☐ 关注行业动态和市场机会</p>
                    <p>☐ 定期进行模拟面试，保持面试状态</p>
                    <p>☐ 明确职业目标，制定发展计划</p>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # 7. 反向提问建议
    reverse_questions = '''
    <div class="result-card active" style="display: block;">
        <h2>七、反向提问建议</h2>
        
        <div class="feedback-item">
            <h3>一、关于岗位和工作</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 请问这个岗位的核心考核指标是什么？</h4>
                    <p><strong>提问目的：</strong>了解工作重点和公司对这个岗位的期望，判断自己是否能胜任</p>
                </div>
                <div class="answer-item">
                    <h4>2. 请问这个岗位在团队中的定位和价值是什么？</h4>
                    <p><strong>提问目的：</strong>了解这个岗位的重要性，以及它如何为团队创造价值</p>
                </div>
                <div class="answer-item">
                    <h4>3. 请问这个岗位目前面临的最大挑战是什么？</h4>
                    <p><strong>提问目的：</strong>了解工作难点，判断自己是否有能力应对这些挑战</p>
                </div>
                <div class="answer-item">
                    <h4>4. 请问日常的工作内容和时间分配是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解真实的工作状态，看是否符合自己的预期</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>二、关于团队和文化</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 请问团队目前的规模和架构是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解团队情况，判断自己是否能融入</p>
                </div>
                <div class="answer-item">
                    <h4>2. 请问团队的工作风格和氛围是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解企业文化，看是否与自己的价值观匹配</p>
                </div>
                <div class="answer-item">
                    <h4>3. 请问团队内部的协作和沟通方式是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解工作流程，判断是否适合自己</p>
                </div>
                <div class="answer-item">
                    <h4>4. 请问您认为团队最看重员工的哪些品质？</h4>
                    <p><strong>提问目的：</strong>了解公司的用人标准，看自己是否契合</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>三、关于发展和成长</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 请问这个岗位的职业发展路径是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解成长空间，判断是否有长期发展机会</p>
                </div>
                <div class="answer-item">
                    <h4>2. 请问公司有哪些培训和学习资源？</h4>
                    <p><strong>提问目的：</strong>了解公司对人才培养的重视程度</p>
                </div>
                <div class="answer-item">
                    <h4>3. 请问在这个岗位上做得好的员工有什么共同特点？</h4>
                    <p><strong>提问目的：</strong>了解成功标准，找到努力方向</p>
                </div>
                <div class="answer-item">
                    <h4>4. 请问公司如何评价和激励员工？</h4>
                    <p><strong>提问目的：</strong>了解绩效考核和激励机制</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>四、关于招聘流程</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>1. 请问接下来的招聘流程是怎样的？</h4>
                    <p><strong>提问目的：</strong>了解后续安排，做好心理准备</p>
                </div>
                <div class="answer-item">
                    <h4>2. 请问什么时候能知道面试结果？</h4>
                    <p><strong>提问目的：</strong>了解时间线，避免盲目等待</p>
                </div>
                <div class="answer-item">
                    <h4>3. 请问您对我这个候选人还有什么想了解的吗？</h4>
                    <p><strong>提问目的：</strong>给面试官补充提问的机会，展示自信和开放性</p>
                </div>
            </div>
        </div>
        
        <div class="feedback-item">
            <h3>提问策略</h3>
            <div class="answers-summary" style="padding: 15px;">
                <div class="answer-item">
                    <h4>✅ 好的提问特点</h4>
                    <p>• 表现出你对公司和岗位的 genuine interest</p>
                    <p>• 帮助你了解真实的工作环境和文化</p>
                    <p>• 展示你的思考深度和职业成熟度</p>
                    <p>• 让对话更平等，建立双向沟通</p>
                </div>
                <div class="answer-item">
                    <h4>❌ 应该避免的问题</h4>
                    <p>• 不要问Google一下就能知道答案的问题</p>
                    <p>• 不要过早询问薪资福利（除非对方先提）</p>
                    <p>• 不要问过于负面或挑战性的问题</p>
                    <p>• 不要一下子问太多问题，选择2-3个最关心的</p>
                </div>
            </div>
        </div>
    </div>
    '''
    
    return {
        'company_intelligence': company_intelligence,
        'matching_analysis': matching_analysis,
        'self_introduction': self_introduction,
        'interview_questions': interview_questions,
        'salary_negotiation': salary_negotiation,
        'preparation_checklist': preparation_checklist,
        'reverse_questions': reverse_questions
    }


# 获取免责申明
def get_disclaimer():
    """返回标准免责申明"""
    return '''
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px; border-left: 4px solid #6c757d;">
        <h3 style="color: #495057; margin-top: 0;">免责申明</h3>
        <p style="color: #666; font-size: 14px; line-height: 1.8; margin: 10px 0;">
            <strong>1.</strong> 本技能仅提供求职策略指导与工具支持，不收集敏感隐私信息，不承诺任何录用结果，所有建议仅供个人求职参考，不构成正式决策依据，相关后果由用户自行承担。
        </p>
        <p style="color: #666; font-size: 14px; line-height: 1.8; margin: 10px 0;">
            <strong>2.</strong> 用户对输入数据的真实性、准确性等负全责，因数据问题导致的偏差及损失由用户自行承担。
        </p>
    </div>
    '''


def generate_dynamic_interview_html(questions_list):
    """基于动态生成的面试题目列表生成HTML"""
    
    if not questions_list:
        # 如果没有动态题目，返回空内容
        return '''
    <div class="result-card active" style="display: block;">
        <h2>四、面试题库</h2>
        <p style="color: #666; margin-bottom: 20px;">暂无面试题目，请提供简历数据以生成个性化题库</p>
    </div>
    '''
    
    html_parts = []
    html_parts.append('''
    <div class="result-card active" style="display: block;">
        <h2>四、面试题库（{}道个性化面试题）</h2>
        <p style="color: #666; margin-bottom: 20px;">基于您的简历情况动态生成，在线答疑</p>
    '''.format(len(questions_list)))
    
    # 按题目类型分组
    question_types = {}
    for q in questions_list:
        q_type = q.get('type', '其他')
        if q_type not in question_types:
            question_types[q_type] = []
        question_types[q_type].append(q)
    
    for q_type, type_questions in question_types.items():
        safe_q_type = html.escape(str(q_type))
        html_parts.append(f'''
        <div class="feedback-item">
            <h3>{safe_q_type}类（{len(type_questions)}道）</h3>
            <div class="answers-summary" style="padding: 15px;">
        ''')
        
        for i, q in enumerate(type_questions, 1):
            question = html.escape(str(q.get('question', '')))
            source = html.escape(str(q.get('source', '')))
            思路 = html.escape(str(q.get('思路', '')))
            要点 = html.escape(str(q.get('要点', '')))
            
            html_parts.append(f'''
                <div class="answer-item">
                    <h4>{i}. {question}</h4>
                    <p style="font-size: 12px; color: #667eea; margin-bottom: 8px;">📌 来源：{source}</p>
                    <p><strong>答题思路：</strong>{思路}</p>
                    <p><strong>参考答案要点：</strong>{要点}</p>
                </div>
            ''')
        
        html_parts.append('''
            </div>
        </div>
        ''')
    
    html_parts.append('</div>')
    return '\n'.join(html_parts)

# 主HTML生成函数
def generate_interview_web(questions_data, job_name, company_name, output_path, dynamic_questions=None):
    """
    生成模拟面试网页
    
    Args:
        questions_data: 面试问题数据
        job_name: 岗位名称
        company_name: 公司名称
        output_path: 输出文件路径
        dynamic_questions: 动态生成的面试题目列表
    """
    
    # 对用户输入进行HTML转义，防止注入
    safe_job_name = html.escape(str(job_name)) if job_name else ''
    safe_company_name = html.escape(str(company_name)) if company_name else ''

    # 获取静态SVG图表
    svgs = get_static_svgs()
    
    # 获取7个完整部分的内容
    sections = get_seven_sections_content(svgs)
    
    # 如果有动态生成的面试题目，替换原有内容
    if dynamic_questions:
        sections['interview_questions'] = generate_dynamic_interview_html(dynamic_questions)
    
    # 获取免责申明
    disclaimer = get_disclaimer()
    
    # 获取当前时间
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    current_datetime = now.strftime('%Y年%m月%d日 %H:%M')
    
    # 构建完整HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_job_name} - 面试准备一站式报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Microsoft YaHei", "微软雅黑", "SimSun", "宋体", "Heiti", "黑体", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .header .info {{
            margin-top: 15px;
            font-size: 14px;
            opacity: 0.8;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        /* 章节导航 */
        .nav-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 30px;
        }}
        
        .nav-btn {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .nav-btn:hover {{
            background: #667eea;
            color: white;
        }}
        
        .nav-btn.active {{
            background: #667eea;
            color: white;
        }}
        
        .result-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
        }}
        
        .result-card h2 {{
            color: #667eea;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        
        .result-card h3 {{
            color: #333;
            font-size: 18px;
            margin: 20px 0 15px 0;
        }}
        
        .result-card p {{
            color: #555;
            font-size: 15px;
            margin: 10px 0;
        }}
        
        .feedback-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }}
        
        .feedback-item h3 {{
            color: #333;
            font-size: 16px;
            margin: 0 0 10px 0;
        }}
        
        .feedback-item h4 {{
            color: #667eea;
            font-size: 15px;
            margin: 15px 0 10px 0;
        }}
        
        .feedback-item p {{
            color: #666;
            font-size: 14px;
            margin: 8px 0;
        }}
        
        .score-display {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            margin: 20px 0;
        }}
        
        .score-number {{
            font-size: 72px;
            font-weight: bold;
            color: white;
            line-height: 1;
        }}
        
        .score-label {{
            font-size: 18px;
            color: white;
            margin-top: 10px;
            opacity: 0.9;
        }}
        
        /* 图表容器 */
        .charts-container {{
            margin: 30px 0;
        }}
        
        .charts-container h3 {{
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .chart-row {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .chart-item {{
            flex: 1;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .answers-summary {{
            margin-top: 20px;
        }}
        
        .answer-item {{
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .answer-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        
        /* 下载区域 - 移至文档末尾 */
        .download-section {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }}
        
        .download-section h3 {{
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .download-options {{
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .download-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            min-width: 180px;
        }}
        
        .download-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        
        .download-card .icon {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .download-card .title {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .download-card .desc {{
            font-size: 12px;
            opacity: 0.9;
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .header {{
                padding: 25px 20px;
            }}
            
            .header h1 {{
                font-size: 22px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .nav-buttons {{
                justify-content: center;
            }}
            
            .chart-row {{
                flex-direction: column;
            }}
            
            .download-options {{
                flex-direction: column;
                align-items: center;
            }}
            
            .download-card {{
                width: 100%;
                max-width: 280px;
            }}
        }}
        
        /* 打印样式优化 */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
            
            .nav-buttons,
            .download-section {{
                display: none !important;
            }}
            
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 {safe_job_name} - 面试准备一站式报告</h1>
            <p>公司：{safe_company_name}</p>
            <div class="info">
                生成时间：{current_datetime}
            </div>
        </div>
        
        <div class="content">
            <!-- 章节导航 -->
            <div class="nav-buttons">
                <button class="nav-btn active" onclick="showSection(1)">一、岗位情报</button>
                <button class="nav-btn" onclick="showSection(2)">二、匹配度分析</button>
                <button class="nav-btn" onclick="showSection(3)">三、自我介绍</button>
                <button class="nav-btn" onclick="showSection(4)">四、面试题库</button>
                <button class="nav-btn" onclick="showSection(5)">五、薪资谈判</button>
                <button class="nav-btn" onclick="showSection(6)">六、准备清单</button>
                <button class="nav-btn" onclick="showSection(7)">七、反向提问</button>
            </div>
            
            <!-- 1. 岗位情报分析 -->
            {sections['company_intelligence']}
            
            <!-- 2. 岗位匹配度分析 -->
            {sections['matching_analysis']}
            
            <!-- 3. 自我介绍模板 -->
            {sections['self_introduction']}
            
            <!-- 4. 面试题库 -->
            {sections['interview_questions']}
            
            <!-- 5. 薪资谈判策略 -->
            {sections['salary_negotiation']}
            
            <!-- 6. 准备清单 -->
            {sections['preparation_checklist']}
            
            <!-- 7. 反向提问建议 -->
            {sections['reverse_questions']}
            
            <!-- 免责申明 - 移至文档末尾 -->
            {disclaimer}
            
            <!-- 下载区域 - 移至文档末尾 -->
            <div class="download-section">
                <h3>📥 下载报告</h3>
                <div class="download-options">
                    <div class="download-card" onclick="downloadHTML()">
                        <div class="icon">📄</div>
                        <div class="title">HTML</div>
                        <div class="desc">在线查看/下载</div>
                    </div>
                    <div class="download-card" onclick="downloadPDF()">
                        <div class="icon">📕</div>
                        <div class="title">PDF</div>
                        <div class="desc">在线查看/下载</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 章节切换功能
        const totalSections = 7;
        let currentSection = 1;
        
        function showSection(sectionNum) {{
            currentSection = sectionNum;
            
            // 更新导航按钮状态
            document.querySelectorAll('.nav-btn').forEach((btn, index) => {{
                btn.classList.remove('active');
                if (index + 1 === sectionNum) {{
                    btn.classList.add('active');
                }}
            }});
        }}
        
        // HTML下载功能
        function downloadHTML() {{
            const htmlContent = document.documentElement.outerHTML;
            const blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            const now = new Date();
            const fileName = `面试一站式报告_{current_date}.html`;
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = fileName;
            link.click();
        }}
        
        // PDF下载功能（通过浏览器打印）
        function downloadPDF() {{
            window.print();
        }}
    </script>
</body>
</html>'''
    
    # 写入文件 - 使用utf-8-sig编码添加BOM，确保Windows下Word正确识别
    try:
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write(html_content)
        print(f"✅ 面试准备一站式网页已生成：{output_path}")
        print(f"📅 生成时间：{current_datetime}")
        return True
    except Exception as e:
        # 如果utf-8-sig失败，回退到标准utf-8
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ 面试准备一站式网页已生成（UTF-8编码）：{output_path}")
            print(f"📅 生成时间：{current_datetime}")
            return True
        except Exception as e2:
            print(f"❌ 文件写入失败：{e}")
            print(f"❌ 第二次尝试也失败：{e2}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成模拟面试网页')
    parser.add_argument('--resume-file', help='简历JSON文件路径（用于动态生成题目）')
    parser.add_argument('--job-file', help='岗位信息JSON文件路径（可选）')
    parser.add_argument('--questions-file', help='面试问题JSON文件路径（传统方式）')
    parser.add_argument('--job-name', required=True, help='岗位名称')
    parser.add_argument('--company', required=True, help='公司名称')
    parser.add_argument('--output', required=True, help='输出HTML文件路径')
    
    args = parser.parse_args()
    
    questions_data = {}
    dynamic_questions = None
    
    # 优先使用简历JSON动态生成题目
    if args.resume_file:
        try:
            with open(args.resume_file, 'r', encoding='utf-8') as f:
                resume_data = json.load(f)
            
            # 加载岗位数据（如果提供）
            job_data = {}
            if args.job_file:
                try:
                    with open(args.job_file, 'r', encoding='utf-8') as f:
                        job_data = json.load(f)
                except Exception as e:
                    print(f"⚠️ 读取岗位文件失败：{e}，将使用默认数据")
            
            # 动态生成面试题目
            dynamic_questions = generate_interview_questions(resume_data, job_data)
            print(f"✓ 基于简历动态生成{len(dynamic_questions)}道面试题目")
            
        except Exception as e:
            print(f"❌ 读取简历文件失败：{e}")
            return 1
    
    # 传统方式：读取面试问题数据
    elif args.questions_file:
        try:
            with open(args.questions_file, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
        except Exception as e:
            print(f"❌ 读取问题文件失败：{e}")
            return 1
    else:
        print("❌ 请提供 --resume-file 或 --questions-file 参数")
        return 1
    
    # 生成网页
    success = generate_interview_web(
        questions_data,
        args.job_name,
        args.company,
        args.output,
        dynamic_questions
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
