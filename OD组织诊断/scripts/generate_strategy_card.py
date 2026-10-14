#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD战略解码卡生成器
阶段1启动-战略解码专用脚本

功能：
- 生成战略解码结构化文档
- 支持BLM模型框架
- 输出HTML格式，支持一键导出PDF

输入参数：
- company_name: 公司名称（必填）
- project_name: 项目名称（必填）
- vision: 企业愿景
- mission: 企业使命
- values: 核心价值观列表
- strategic_goals: 战略目标列表，每项包含:
  - goal: 目标名称
  - kpis: KPI列表
  - owner: 负责人
- blm_model: BLM模型数据（可选）:
  - leadership: 领导力
  - vision: 战略愿景
  - Market_Insight: 市场洞察
  - Innovation_Offer: 创新焦点
  - Strategy: 策略
  - alignment: 组织对齐
  - teams: 团队
  - work_plan: 工作计划
"""

import argparse
import json
import sys
import os
from datetime import datetime

def get_chinese_font_name():
    """获取可用的中文字体名称（跨平台支持）"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    chinese_fonts = [
        # Windows
        'Microsoft YaHei',
        'SimHei',
        'SimSun',
        # macOS
        'PingFang SC',
        'STHeiti',
        'STSong',
        # Linux
        'Noto Sans CJK SC',
        'WenQuanYi Micro Hei',
        'DejaVu Sans'
    ]
    
    font_names = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
    
    for font in chinese_fonts:
        if font in font_names:
            return font
    
    return plt.rcParams['font.sans-serif'][0] if plt.rcParams['font.sans-serif'] else 'DejaVu Sans'

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime('%Y年%m月%d日')

def generate_blm_strategy_card(data):
    """生成BLM战略解码卡HTML"""
    
    company_name = data.get('company_name', '公司')
    project_name = data.get('project_name', 'OD项目')
    vision = data.get('vision', '')
    mission = data.get('mission', '')
    values = data.get('values', [])
    strategic_goals = data.get('strategic_goals', [])
    blm_model = data.get('blm_model', {})
    generation_date = data.get('generation_date', get_current_date())
    
    # 战略目标HTML
    goals_html = ''
    for i, goal in enumerate(strategic_goals, 1):
        kpis_html = '<ul class="kpi-list">'
        for kpi in goal.get('kpis', []):
            kpis_html += f'<li>{kpi}</li>'
        kpis_html += '</ul>'
        goals_html += f'''
        <div class="goal-card">
            <h4>目标{i}：{goal.get('goal', '')}</h4>
            <div class="goal-meta">
                <span class="owner">负责人：{goal.get('owner', '')}</span>
            </div>
            <div class="kpis">
                <strong>关键指标：</strong>
                {kpis_html}
            </div>
        </div>
        '''
    
    if not goals_html:
        goals_html = '<p class="placeholder">暂无战略目标，请补充...</p>'
    
    # BLM模型HTML
    blm_items = [
        ('leadership', '领导力', blm_model.get('leadership', '')),
        ('vision', '战略愿景', blm_model.get('vision', '')),
        ('Market_Insight', '市场洞察', blm_model.get('Market_Insight', '')),
        ('Innovation_Offer', '创新焦点', blm_model.get('Innovation_Offer', '')),
        ('Strategy', '策略', blm_model.get('Strategy', '')),
        ('alignment', '组织对齐', blm_model.get('alignment', '')),
        ('teams', '团队', blm_model.get('teams', '')),
        ('work_plan', '工作计划', blm_model.get('work_plan', '')),
    ]
    
    blm_html = ''
    for item_id, item_name, item_value in blm_items:
        blm_html += f'''
        <div class="blm-item">
            <h4>{item_name}</h4>
            <p>{item_value if item_value else '<span class="placeholder-text">请输入...</span>'}</p>
        </div>
        '''
    
    # 价值观HTML
    values_html = ''
    for value in values:
        values_html += f'<span class="value-tag">{value}</span>'
    
    if not values_html:
        values_html = '<span class="placeholder">暂无价值观，请补充...</span>'
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>战略解码卡 - {company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 24px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #1a1a2e;
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            color: #1a1a2e;
            font-size: 20px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #4361ee;
        }}
        .vision-mission {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }}
        .vision-box, .mission-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #4361ee;
        }}
        .vision-box h3, .mission-box h3 {{
            color: #4361ee;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .vision-box p, .mission-box p {{
            color: #333;
            font-size: 16px;
            line-height: 1.6;
        }}
        .values-section {{
            margin-bottom: 24px;
        }}
        .value-tag {{
            display: inline-block;
            background: linear-gradient(135deg, #4361ee, #3a0ca3);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            margin: 4px;
            font-size: 14px;
        }}
        .placeholder {{ color: #999; font-style: italic; }}
        .goal-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 16px;
            border-left: 4px solid #f72585;
        }}
        .goal-card h4 {{
            color: #1a1a2e;
            margin-bottom: 8px;
        }}
        .goal-meta {{
            margin-bottom: 12px;
        }}
        .owner {{
            color: #666;
            font-size: 14px;
        }}
        .kpi-list {{
            margin-left: 20px;
            color: #444;
        }}
        .kpi-list li {{
            margin: 4px 0;
        }}
        .blm-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }}
        .blm-item {{
            background: #f8f9fa;
            padding: 16px;
            border-radius: 12px;
            border-top: 3px solid #4361ee;
        }}
        .blm-item h4 {{
            color: #4361ee;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .blm-item p {{
            color: #444;
            line-height: 1.6;
            min-height: 60px;
        }}
        .placeholder-text {{
            color: #ccc;
            font-style: italic;
        }}
        .disclaimer {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 16px;
            margin-top: 24px;
            font-size: 12px;
            color: #856404;
        }}
        .action-bar {{
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 12px 24px;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            display: flex;
            gap: 12px;
        }}
        .action-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-html {{
            background: linear-gradient(135deg, #4361ee, #3a0ca3);
            color: white;
        }}
        .btn-pdf {{
            background: linear-gradient(135deg, #f72585, #b5179e);
            color: white;
        }}
        .action-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        @media print {{
            .action-bar {{ display: none !important; }}
            body {{ background: white; padding: 0; }}
            .card {{ box-shadow: none; border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>战略解码卡</h1>
            <p class="subtitle">{company_name} · {project_name} · {generation_date}</p>
        </div>

        <div class="card">
            <h2>愿景与使命</h2>
            <div class="vision-mission">
                <div class="vision-box">
                    <h3>企业愿景</h3>
                    <p>{vision if vision else '<span class="placeholder">请输入企业愿景...</span>'}</p>
                </div>
                <div class="mission-box">
                    <h3>企业使命</h3>
                    <p>{mission if mission else '<span class="placeholder">请输入企业使命...</span>'}</p>
                </div>
            </div>
            <div class="values-section">
                <h3>核心价值观</h3>
                {values_html}
            </div>
        </div>

        <div class="card">
            <h2>战略目标</h2>
            {goals_html}
        </div>

        <div class="card">
            <h2>BLM战略解码模型</h2>
            <div class="blm-grid">
                {blm_html}
            </div>
        </div>

        <div class="disclaimer">
            <strong>免责声明：</strong>本报告由OD组织发展助手自动生成，数据来源为用户提供。所有分析内容仅供管理决策参考，不构成专业法律或财务建议。上传数据已做数据脱敏处理。
        </div>
    </div>

    <div class="action-bar">
        <button class="action-btn btn-html" onclick="downloadHTML()">🌐 下载 HTML</button>
        <button class="action-btn btn-pdf" onclick="downloadPDF()">📄 导出 PDF</button>
    </div>

    <script src="../assets/html2pdf.bundle.min.js"></script>
    <script>
        function getCurrentDate() {{
            const now = new Date();
            return now.getFullYear() + '年' + String(now.getMonth() + 1).padStart(2, '0') + '月' + String(now.getDate()).padStart(2, '0') + '日';
        }}

        function downloadHTML() {{
            const htmlContent = document.documentElement.outerHTML;
            const blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '战略解码卡_' + getCurrentDate() + '.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        async function downloadPDF() {{
            const btn = document.querySelector('.btn-pdf');
            btn.disabled = true;
            btn.textContent = '⏳ 生成中...';
            
            try {{
                const element = document.querySelector('.container');
                const opt = {{
                    margin: 10,
                    filename: '战略解码卡_' + getCurrentDate() + '.pdf',
                    image: {{ type: 'jpeg', quality: 0.98 }},
                    html2canvas: {{ scale: 2, useCORS: true }},
                    jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
                }};
                await html2pdf().set(opt).from(element).save();
            }} catch (error) {{
                alert('PDF导出失败：' + error.message);
            }} finally {{
                btn.disabled = false;
                btn.textContent = '📄 导出 PDF';
            }}
        }}
    </script>
</body>
</html>'''
    
    return html_content


def main():
    parser = argparse.ArgumentParser(description='OD战略解码卡生成器')
    parser.add_argument('--data', type=str, help='JSON数据字符串')
    parser.add_argument('--output_path', type=str, default='./strategy_card.html', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.data:
        data = json.loads(args.data)
    else:
        # 默认示例数据
        data = {
            'company_name': 'XX公司',
            'project_name': 'OD能力提升项目',
            'vision': '成为行业领先的创新型企业',
            'mission': '为客户创造价值，为员工创造机会',
            'values': ['创新', '协作', '客户导向', '追求卓越'],
            'strategic_goals': [
                {
                    'goal': '提升组织效能',
                    'kpis': ['人均产出提升15%', '流程周期缩短20%'],
                    'owner': 'HR总监'
                },
                {
                    'goal': '强化人才梯队',
                    'kpis': ['关键岗位储备率100%', '人才流失率<5%'],
                    'owner': '人才发展负责人'
                }
            ],
            'generation_date': get_current_date()
        }
    
    html_content = generate_blm_strategy_card(data)
    
    output_path = data.get('output_path', args.output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(json.dumps({'status': 'success', 'output_path': output_path}))


if __name__ == '__main__':
    main()
