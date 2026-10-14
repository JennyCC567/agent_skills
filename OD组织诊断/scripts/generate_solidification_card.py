#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD固化复盘卡生成器
阶段6固化-机制建设专用脚本

功能：
- 生成变革成果固化和项目复盘报告
- 支持成功经验沉淀、机制固化、持续改进
- 输出HTML格式，支持一键导出PDF

输入参数：
- company_name: 公司名称（必填）
- project_name: 项目名称（必填）
- project_duration: 项目周期
- key_achievements: 关键成果列表
- success_factors: 成功要素列表
- lessons_learned: 经验教训列表
- institutionalized_changes: 制度化变革列表
- continuous_improvements: 持续改进计划
- metrics_summary: 指标总结
"""

import argparse
import json
from datetime import datetime

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime('%Y年%m月%d日')

def generate_solidification_card(data):
    """生成固化复盘卡HTML"""
    
    company_name = data.get('company_name', '公司')
    project_name = data.get('project_name', 'OD项目')
    project_duration = data.get('project_duration', '')
    key_achievements = data.get('key_achievements', [])
    success_factors = data.get('success_factors', [])
    lessons_learned = data.get('lessons_learned', [])
    institutionalized_changes = data.get('institutionalized_changes', [])
    continuous_improvements = data.get('continuous_improvements', [])
    metrics_summary = data.get('metrics_summary', {})
    generation_date = data.get('generation_date', get_current_date())
    
    # 关键成果HTML
    achievements_html = ''
    for achievement in key_achievements:
        metric = achievement.get('metric', '')
        value = achievement.get('value', '')
        achievements_html += f'''
        <div class="achievement-card">
            <div class="metric">{metric}</div>
            <div class="value">{value}</div>
        </div>
        '''
    
    if not achievements_html:
        achievements_html = '<p class="placeholder">暂无关键成果，请补充...</p>'
    
    # 成功要素HTML
    factors_html = ''
    for factor in success_factors:
        factors_html += f'<li>{factor}</li>'
    
    if not factors_html:
        factors_html = '<li class="placeholder">暂无成功要素，请补充...</li>'
    
    # 经验教训HTML
    lessons_html = ''
    for lesson in lessons_learned:
        lessons_html += f'<li>{lesson}</li>'
    
    if not lessons_html:
        lessons_html = '<li class="placeholder">暂无经验教训，请补充...</li>'
    
    # 制度化变革HTML
    changes_html = ''
    for change in institutionalized_changes:
        changes_html += f'''
        <tr>
            <td>{change.get('area', '')}</td>
            <td>{change.get('change', '')}</td>
            <td>{change.get('owner', '')}</td>
            <td>{change.get('timeline', '')}</td>
        </tr>
        '''
    
    if not changes_html:
        changes_html = '<tr><td colspan="4" class="placeholder">暂无制度化变革，请补充...</td></tr>'
    
    # 持续改进HTML
    improvements_html = ''
    for imp in continuous_improvements:
        improvements_html += f'''
        <div class="improvement-item">
            <h4>{imp.get('title', '')}</h4>
            <p>{imp.get('description', '')}</p>
            <div class="improvement-meta">
                <span>负责人：{imp.get('owner', '')}</span>
                <span>计划时间：{imp.get('timeline', '')}</span>
            </div>
        </div>
        '''
    
    if not improvements_html:
        improvements_html = '<p class="placeholder">暂无持续改进计划，请补充...</p>'
    
    # 指标总结HTML
    metrics_html = ''
    for key, value in metrics_summary.items():
        metrics_html += f'''
        <div class="metric-item">
            <div class="metric-name">{key}</div>
            <div class="metric-value">{value}</div>
        </div>
        '''
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>固化复盘卡 - {company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
            background: linear-gradient(135deg, #312e81 0%, #4c1d95 100%);
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
            text-align: center;
        }}
        .header h1 {{
            color: #312e81;
            font-size: 32px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .header .duration {{
            display: inline-block;
            background: #eef2ff;
            color: #4f46e5;
            padding: 8px 20px;
            border-radius: 20px;
            margin-top: 12px;
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
            color: #312e81;
            font-size: 20px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #8b5cf6;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .card h2::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 20px;
            background: #8b5cf6;
            border-radius: 2px;
        }}
        .achievements-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }}
        .achievement-card {{
            background: linear-gradient(135deg, #8b5cf6, #a855f7);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
        }}
        .achievement-card .metric {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 8px;
        }}
        .achievement-card .value {{
            font-size: 28px;
            font-weight: 700;
        }}
        .section-title {{
            color: #64748b;
            font-size: 14px;
            margin-bottom: 12px;
        }}
        ul {{
            margin-left: 24px;
            color: #334155;
        }}
        ul li {{
            margin: 10px 0;
            line-height: 1.6;
        }}
        .placeholder {{
            color: #94a3b8;
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background: #f5f3ff;
            color: #7c3aed;
            font-weight: 600;
            font-size: 14px;
        }}
        td {{
            color: #334155;
            font-size: 14px;
        }}
        .improvement-item {{
            background: #f5f3ff;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #8b5cf6;
        }}
        .improvement-item h4 {{
            color: #7c3aed;
            margin-bottom: 8px;
        }}
        .improvement-item p {{
            color: #64748b;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .improvement-meta {{
            display: flex;
            gap: 16px;
            font-size: 12px;
            color: #94a3b8;
        }}
        .metrics-summary {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        .metric-item {{
            background: #f5f3ff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        .metric-name {{
            color: #64748b;
            font-size: 12px;
            margin-bottom: 8px;
        }}
        .metric-value {{
            color: #7c3aed;
            font-size: 20px;
            font-weight: 700;
        }}
        .conclusion {{
            background: linear-gradient(135deg, #7c3aed, #a855f7);
            color: white;
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            margin-top: 24px;
        }}
        .conclusion h3 {{
            font-size: 20px;
            margin-bottom: 12px;
        }}
        .conclusion p {{
            opacity: 0.9;
            line-height: 1.6;
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
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
            color: white;
        }}
        .btn-pdf {{
            background: linear-gradient(135deg, #ec4899, #db2777);
            color: white;
        }}
        .action-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        @media print {{
            .action-bar {{ display: none !important; }}
            body {{ background: white; padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>固化复盘卡</h1>
            <p class="subtitle">{company_name} · {project_name}</p>
            <span class="duration">项目周期：{project_duration if project_duration else '请补充...'}</span>
        </div>

        <div class="card">
            <h2>关键成果</h2>
            <div class="achievements-grid">
                {achievements_html}
            </div>
        </div>

        <div class="card">
            <h2>经验总结</h2>
            <div class="section-title">成功要素</div>
            <ul>
                {factors_html}
            </ul>
            <div class="section-title" style="margin-top: 24px;">经验教训</div>
            <ul>
                {lessons_html}
            </ul>
        </div>

        <div class="card">
            <h2>制度化变革</h2>
            <table>
                <thead>
                    <tr>
                        <th>领域</th>
                        <th>变革内容</th>
                        <th>责任人</th>
                        <th>完成时间</th>
                    </tr>
                </thead>
                <tbody>
                    {changes_html}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>持续改进</h2>
            {improvements_html}
        </div>

        <div class="card">
            <h2>指标总结</h2>
            <div class="metrics-summary">
                {metrics_html if metrics_html else '<p class="placeholder">暂无指标数据...</p>'}
            </div>
        </div>

        <div class="conclusion">
            <h3>变革成果已固化</h3>
            <p>恭喜您完成了本次组织发展项目的全部阶段。<br>期待新机制为组织带来持续价值！</p>
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
            a.download = '固化复盘卡_' + getCurrentDate() + '.html';
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
                    filename: '固化复盘卡_' + getCurrentDate() + '.pdf',
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
    parser = argparse.ArgumentParser(description='OD固化复盘卡生成器')
    parser.add_argument('--data', type=str, help='JSON数据字符串')
    parser.add_argument('--output_path', type=str, default='./solidification_card.html', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.data:
        data = json.loads(args.data)
    else:
        data = {
            'company_name': 'XX公司',
            'project_name': 'OD能力提升项目',
            'project_duration': '2025-01-01 至 2025-12-31',
            'key_achievements': [
                {'metric': '组织效能提升', 'value': '+25%'},
                {'metric': '员工满意度', 'value': '92%'},
                {'metric': '人才储备率', 'value': '100%'}
            ],
            'success_factors': [
                '高层领导持续支持',
                '充分的资源投入',
                '有效的沟通机制'
            ],
            'lessons_learned': [
                '试点阶段需要更多时间',
                '培训体系需提前建立'
            ],
            'institutionalized_changes': [
                {'area': '组织架构', 'change': '优化部门设置', 'owner': 'HR总监', 'timeline': '2025-12'},
                {'area': '绩效管理', 'change': 'OKR全面推行', 'owner': '绩效经理', 'timeline': '2026-01'}
            ],
            'continuous_improvements': [
                {'title': '文化建设深化', 'description': '将OD理念融入企业文化', 'owner': '企业文化负责人', 'timeline': '2026-Q1'}
            ],
            'metrics_summary': {
                '项目周期': '12个月',
                '参与人数': '500+',
                '覆盖部门': '10个',
                '关键指标': '100%完成'
            },
            'generation_date': get_current_date()
        }
    
    html_content = generate_solidification_card(data)
    
    output_path = data.get('output_path', args.output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(json.dumps({'status': 'success', 'output_path': output_path}))


if __name__ == '__main__':
    main()
