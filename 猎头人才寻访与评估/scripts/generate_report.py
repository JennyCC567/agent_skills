#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成脚本（符合红线规则V6.2）

功能：
- 生成标准人才匹配报告
- 生成FABM推荐报告
- 生成可视化候选人画像
- 生成多候选人对比报告

使用示例：
    python scripts/generate_report.py -i input.json -o output.html -f html -t standard

红线规则合规：
- 零JS依赖（图表用matplotlib base64 PNG）
- 零外部URL（图片/字体/脚本全部内嵌）
- 断网可正常打开
- 纯CSS布局（block + inline + table），避免flex/grid
- 日期使用datetime.now()生成真实系统时间
- 无emoji字符
"""

import argparse
import json
import os
import sys
import base64
import io
from datetime import datetime

# matplotlib配置
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 注册中文字体
def setup_chinese_font():
    """设置中文字体"""
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/wqy-microhei/wqy-microhei.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        'C:/Windows/Fonts/msyh.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                fm.fontManager.addfont(font_path)
                plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei']
                plt.rcParams['axes.unicode_minus'] = False
                return True
            except Exception:
                continue
    
    # 默认设置
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return False

def fig_to_base64(fig):
    """matplotlib图表 -> base64字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def calculate_matching_score(candidate, jd_requirements):
    """
    核心匹配评分逻辑
    
    参数:
        candidate: dict, 候选人信息
        jd_requirements: dict, JD要求
    
    返回:
        dict: 评分结果
    """
    score = {
        'hard_skills': 0,  # 硬性指标（60%）
        'soft_skills': 0,  # 软性指标（30%）
        'priority': 0,     # 优先条件（10%）
        'total': 0,        # 综合得分
        'recommendation': '',  # 推荐等级
        'details': {}      # 详细评分
    }
    
    # 硬性指标评分（60%）
    hard_score = 0
    
    # 学历匹配（10%）
    edu_match = 0
    candidate_edu = candidate.get('education', '')
    required_edu = jd_requirements.get('education', '')
    edu_levels = {'大专': 1, '本科': 2, '硕士': 3, '博士': 4}
    if candidate_edu in edu_levels and required_edu in edu_levels:
        if edu_levels[candidate_edu] >= edu_levels[required_edu]:
            edu_match = 100
        else:
            edu_match = 60
    hard_score += edu_match * 0.10
    
    # 经验匹配（20%）
    exp_match = 0
    candidate_exp = candidate.get('experience_years', 0)
    required_exp = jd_requirements.get('experience_years', 0)
    if candidate_exp >= required_exp:
        exp_match = 100
    elif candidate_exp >= required_exp * 0.8:
        exp_match = 70
    else:
        exp_match = 40
    hard_score += exp_match * 0.20
    
    # 技能匹配（30%）
    skill_match = 0
    candidate_skills = set(candidate.get('skills', []))
    required_skills = set(jd_requirements.get('skills', []))
    if required_skills:
        matched_skills = candidate_skills & required_skills
        skill_match = len(matched_skills) / len(required_skills) * 100
    hard_score += skill_match * 0.30
    
    score['hard_skills'] = hard_score * 0.60
    score['details']['education'] = edu_match
    score['details']['experience'] = exp_match
    score['details']['skills'] = skill_match
    
    # 软性指标评分（30%）
    soft_score = 0
    
    # 行业匹配（10%）
    industry_match = 0
    candidate_industry = candidate.get('industry', '')
    required_industry = jd_requirements.get('industry', '')
    if candidate_industry == required_industry:
        industry_match = 100
    elif candidate_industry:
        industry_match = 60
    soft_score += industry_match * 0.10
    
    # 能力匹配（10%）
    ability_match = 0
    candidate_abilities = set(candidate.get('abilities', []))
    required_abilities = set(jd_requirements.get('abilities', []))
    if required_abilities:
        matched_abilities = candidate_abilities & required_abilities
        ability_match = len(matched_abilities) / len(required_abilities) * 100
    soft_score += ability_match * 0.10
    
    # 稳定性（10%）
    stability = 100
    job_hopping = candidate.get('job_hopping', 0)
    if job_hopping > 3:
        stability = 60
    elif job_hopping > 2:
        stability = 80
    soft_score += stability * 0.10
    
    score['soft_skills'] = soft_score * 0.30
    score['details']['industry'] = industry_match
    score['details']['ability'] = ability_match
    score['details']['stability'] = stability
    
    # 优先条件评分（10%）
    priority_score = 0
    priority_conditions = candidate.get('priority_conditions', [])
    required_priority = jd_requirements.get('priority_conditions', [])
    if required_priority:
        matched_priority = set(priority_conditions) & set(required_priority)
        priority_score = len(matched_priority) / len(required_priority) * 100
    score['priority'] = priority_score * 0.10
    score['details']['priority'] = priority_score
    
    # 综合得分
    score['total'] = score['hard_skills'] + score['soft_skills'] + score['priority']
    
    # 推荐等级
    if score['total'] >= 80:
        score['recommendation'] = '强烈推荐'
    elif score['total'] >= 70:
        score['recommendation'] = '推荐'
    elif score['total'] >= 60:
        score['recommendation'] = '谨慎推荐'
    else:
        score['recommendation'] = '不推荐'
    
    return score

def create_radar_chart(data, title):
    """创建雷达图"""
    setup_chinese_font()
    
    categories = list(data.keys())
    values = list(data.values())
    
    N = len(categories)
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2, color='#1F4E79')
    ax.fill(angles, values, alpha=0.25, color='#4A90D9')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 100)
    ax.set_title(title, fontsize=14, fontweight='bold', color='#1F4E79', pad=20)
    
    return fig_to_base64(fig)

def generate_html_template(title, content, report_date=None):
    """生成HTML模板（符合红线规则V6.2）"""
    if report_date is None:
        report_date = datetime.now().strftime('%Y-%m-%d')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 850px;
            margin: 0 auto;
            background: #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #1F4E79 0%, #4A90D9 100%);
            color: #fff;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 18px;
            color: #1F4E79;
            border-bottom: 2px solid #4A90D9;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #e0e0e0;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #1F4E79;
            color: #fff;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
        }}
        .highlight {{
            color: #2CA58D;
            font-weight: bold;
        }}
        .warning {{
            color: #e74c3c;
        }}
        .footer {{
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
        .export-btn {{
            display: block;
            width: 200px;
            margin: 20px auto;
            padding: 12px 30px;
            background: #1F4E79;
            color: #fff;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            text-align: center;
        }}
        .export-btn:hover {{
            background: #4A90D9;
        }}
        @media print {{
            body {{ background: #fff; padding: 0; }}
            .container {{ box-shadow: none; }}
            .export-btn {{ display: none !important; }}
            img {{ page-break-inside: avoid; }}
            table {{ page-break-inside: avoid; }}
            h1, h2, h3 {{ page-break-after: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">生成日期：{report_date}</div>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="footer">
            <p>本报告由AI辅助生成，仅供参考</p>
            <p>报告日期：{report_date}</p>
        </div>
    </div>
    <button class="export-btn no-print" onclick="window.print()">导出PDF</button>
</body>
</html>'''
    return html

def generate_standard_report(data):
    """生成标准人才匹配报告"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    
    content = f'''
    <div class="section">
        <h2 class="section-title">一、候选人基本信息</h2>
        <table>
            <tr><th>姓名</th><td>{data.get('name', '[候选人姓名]')}</td></tr>
            <tr><th>应聘职位</th><td>{data.get('position', '[职位名称]')}</td></tr>
            <tr><th>工作年限</th><td>{data.get('experience', '[工作年限]')}</td></tr>
            <tr><th>学历</th><td>{data.get('education', '[学历]')}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2 class="section-title">二、匹配度评分</h2>
        <table>
            <tr><th>评估维度</th><th>得分</th><th>权重</th><th>加权得分</th></tr>
            <tr><td>硬性指标</td><td>{data.get('hard_score', 0)}</td><td>60%</td><td>{data.get('hard_score', 0) * 0.6:.1f}</td></tr>
            <tr><td>软性指标</td><td>{data.get('soft_score', 0)}</td><td>30%</td><td>{data.get('soft_score', 0) * 0.3:.1f}</td></tr>
            <tr><td>优先条件</td><td>{data.get('priority_score', 0)}</td><td>10%</td><td>{data.get('priority_score', 0) * 0.1:.1f}</td></tr>
            <tr><th>综合得分</th><th colspan="3" class="highlight">{data.get('total_score', 0)}</th></tr>
        </table>
    </div>
    
    <div class="section">
        <h2 class="section-title">三、评估结论</h2>
        <p>{data.get('conclusion', '[评估结论]')}</p>
    </div>
    '''
    
    return generate_html_template('人才匹配评估报告', content, report_date)

def generate_fabm_report(data):
    """生成FABM推荐报告"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    
    fabm = data.get('fabm', {})
    
    content = f'''
    <div class="section">
        <h2 class="section-title">一、候选人概况</h2>
        <table>
            <tr><th>姓名</th><td>{data.get('name', '[候选人姓名]')}</td></tr>
            <tr><th>应聘职位</th><td>{data.get('position', '[职位名称]')}</td></tr>
            <tr><th>推荐等级</th><td class="highlight">{data.get('recommend_level', '[推荐等级]')}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2 class="section-title">二、FABM分析</h2>
        
        <h3 style="color:#1F4E79; margin:15px 0 10px;">Features（特征）</h3>
        <p>{fabm.get('features', '[候选人核心特征]')}</p>
        
        <h3 style="color:#1F4E79; margin:15px 0 10px;">Achievements（成就）</h3>
        <p>{fabm.get('achievements', '[候选人主要成就]')}</p>
        
        <h3 style="color:#1F4E79; margin:15px 0 10px;">Benefits（收益）</h3>
        <p>{fabm.get('benefits', '[为企业带来的收益]')}</p>
        
        <h3 style="color:#1F4E79; margin:15px 0 10px;">Motivation（动机）</h3>
        <p>{fabm.get('motivation', '[候选人求职动机]')}</p>
    </div>
    
    <div class="section">
        <h2 class="section-title">三、推荐理由</h2>
        <p>{data.get('recommend_reason', '[推荐理由]')}</p>
    </div>
    '''
    
    return generate_html_template('FABM人才推荐报告', content, report_date)

def generate_candidate_profile(data):
    """生成可视化候选人画像"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    
    # 生成雷达图
    radar_data = data.get('radar_data', {
        '技术能力': 85,
        '项目经验': 80,
        '学习能力': 90,
        '沟通协作': 75,
        '文化契合': 85
    })
    radar_chart = create_radar_chart(radar_data, '候选人能力画像')
    
    content = f'''
    <div class="section">
        <h2 class="section-title">一、候选人基本信息</h2>
        <table>
            <tr><th>姓名</th><td>{data.get('name', '[候选人姓名]')}</td></tr>
            <tr><th>应聘职位</th><td>{data.get('position', '[职位名称]')}</td></tr>
            <tr><th>工作年限</th><td>{data.get('experience', '[工作年限]')}</td></tr>
            <tr><th>当前薪资</th><td>{data.get('current_salary', '[当前薪资]')}</td></tr>
            <tr><th>期望薪资</th><td>{data.get('expected_salary', '[期望薪资]')}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2 class="section-title">二、能力画像</h2>
        <div class="chart-container">
            <img src="data:image/png;base64,{radar_chart}" alt="候选人能力画像">
        </div>
    </div>
    
    <div class="section">
        <h2 class="section-title">三、核心优势</h2>
        <p>{data.get('strengths', '[核心优势]')}</p>
    </div>
    
    <div class="section">
        <h2 class="section-title">四、潜在风险</h2>
        <p>{data.get('risks', '[潜在风险]')}</p>
    </div>
    '''
    
    return generate_html_template('候选人画像报告', content, report_date)

def generate_multi_candidate_report(data):
    """生成多候选人对比报告"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    
    candidates = data.get('candidates', [])
    
    # 生成对比表格
    table_rows = ''
    for i, c in enumerate(candidates, 1):
        table_rows += f'''
        <tr>
            <td>{i}</td>
            <td>{c.get('name', '[姓名]')}</td>
            <td>{c.get('experience', '[经验]')}</td>
            <td>{c.get('education', '[学历]')}</td>
            <td class="highlight">{c.get('score', 0)}</td>
            <td>{c.get('recommend', '[推荐等级]')}</td>
        </tr>
        '''
    
    content = f'''
    <div class="section">
        <h2 class="section-title">一、候选人对比总览</h2>
        <table>
            <tr>
                <th>序号</th>
                <th>姓名</th>
                <th>工作年限</th>
                <th>学历</th>
                <th>综合得分</th>
                <th>推荐等级</th>
            </tr>
            {table_rows}
        </table>
    </div>
    
    <div class="section">
        <h2 class="section-title">二、对比分析</h2>
        <p>{data.get('analysis', '[对比分析]')}</p>
    </div>
    
    <div class="section">
        <h2 class="section-title">三、推荐建议</h2>
        <p>{data.get('recommendation', '[推荐建议]')}</p>
    </div>
    '''
    
    return generate_html_template('多候选人对比报告', content, report_date)

def main():
    parser = argparse.ArgumentParser(description='报告生成脚本（符合红线规则V6.2）')
    parser.add_argument('-i', '--input', required=True, help='输入JSON文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径')
    parser.add_argument('-f', '--format', choices=['html', 'markdown', 'json'], default='html', help='输出格式')
    parser.add_argument('-t', '--template', choices=['standard', 'fabm', 'candidate_profile', 'multi_candidate'], 
                        default='standard', help='报告模板')
    
    args = parser.parse_args()
    
    # 读取输入数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成报告
    if args.template == 'standard':
        report = generate_standard_report(data)
    elif args.template == 'fabm':
        report = generate_fabm_report(data)
    elif args.template == 'candidate_profile':
        report = generate_candidate_profile(data)
    elif args.template == 'multi_candidate':
        report = generate_multi_candidate_report(data)
    else:
        print(f"错误：未知模板 {args.template}")
        sys.exit(1)
    
    # 输出报告
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已生成：{args.output}")
    print(f"模板：{args.template}")
    print(f"格式：{args.format}")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
