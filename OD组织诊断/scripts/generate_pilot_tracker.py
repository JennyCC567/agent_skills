#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD试点追踪表生成器
阶段4试点-小范围验证专用脚本

功能：
- 生成试点项目追踪管理表
- 支持里程碑管理、风险追踪、反馈收集
- 输出HTML格式，支持一键导出PDF

输入参数：
- company_name: 公司名称（必填）
- project_name: 项目名称（必填）
- pilot_scope: 试点范围描述
- start_date: 开始日期
- end_date: 结束日期
- milestones: 里程碑列表，每项包含:
  - name: 里程碑名称
  - date: 计划日期
  - status: 状态(pending/in_progress/completed)
  - notes: 备注
- risks: 风险列表，每项包含:
  - name: 风险描述
  - impact: 影响程度(high/medium/low)
  - probability: 发生概率(high/medium/low)
  - mitigation: 应对措施
- learnings: 试点学习点列表
- recommendations: 建议列表
"""

import argparse
import json
from datetime import datetime

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime('%Y年%m月%d日')

def status_color(status):
    """状态颜色映射"""
    colors = {
        'pending': '#94a3b8',
        'in_progress': '#3b82f6',
        'completed': '#22c55e'
    }
    return colors.get(status, '#94a3b8')

def status_text(status):
    """状态文本映射"""
    texts = {
        'pending': '待开始',
        'in_progress': '进行中',
        'completed': '已完成'
    }
    return texts.get(status, '未知')

def impact_color(impact):
    """影响程度颜色"""
    colors = {
        'high': '#ef4444',
        'medium': '#f59e0b',
        'low': '#22c55e'
    }
    return colors.get(impact, '#94a3b8')

def generate_pilot_tracker(data):
    """生成试点追踪表HTML"""
    
    company_name = data.get('company_name', '公司')
    project_name = data.get('project_name', 'OD项目')
    pilot_scope = data.get('pilot_scope', '')
    start_date = data.get('start_date', '')
    end_date = data.get('end_date', '')
    milestones = data.get('milestones', [])
    risks = data.get('risks', [])
    learnings = data.get('learnings', [])
    recommendations = data.get('recommendations', [])
    generation_date = data.get('generation_date', get_current_date())
    
    # 计算进度
    total_milestones = len(milestones) if milestones else 0
    completed_milestones = len([m for m in milestones if m.get('status') == 'completed']) if milestones else 0
    progress = int(completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
    
    # 里程碑HTML
    milestones_html = ''
    for m in milestones:
        status = m.get('status', 'pending')
        milestones_html += f'''
        <tr>
            <td>{m.get('name', '')}</td>
            <td>{m.get('date', '')}</td>
            <td><span class="status-badge" style="background: {status_color(status)}">{status_text(status)}</span></td>
            <td>{m.get('notes', '-')}</td>
        </tr>
        '''
    
    if not milestones_html:
        milestones_html = '<tr><td colspan="4" class="placeholder">暂无里程碑，请补充...</td></tr>'
    
    # 风险HTML
    risks_html = ''
    for r in risks:
        impact = r.get('impact', 'medium')
        risks_html += f'''
        <tr>
            <td>{r.get('name', '')}</td>
            <td><span class="impact-badge" style="background: {impact_color(impact)}">{impact.upper()}</span></td>
            <td>{r.get('mitigation', '')}</td>
        </tr>
        '''
    
    if not risks_html:
        risks_html = '<tr><td colspan="3" class="placeholder">暂无风险，请补充...</td></tr>'
    
    # 学习点HTML
    learnings_html = ''
    for learning in learnings:
        learnings_html += f'<li>{learning}</li>'
    
    if not learnings_html:
        learnings_html = '<li class="placeholder">暂无试点学习点...</li>'
    
    # 建议HTML
    recommendations_html = ''
    for rec in recommendations:
        recommendations_html += f'<li>{rec}</li>'
    
    if not recommendations_html:
        recommendations_html = '<li class="placeholder">暂无建议...</li>'
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>试点追踪表 - {company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
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
            color: #0f172a;
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .progress-section {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .progress-bar {{
            height: 24px;
            background: #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            margin: 16px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #22c55e);
            border-radius: 12px;
            width: {progress}%;
            transition: width 0.3s ease;
        }}
        .progress-stats {{
            display: flex;
            justify-content: space-between;
            color: #64748b;
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
            color: #0f172a;
            font-size: 20px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #3b82f6;
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
            background: #f8fafc;
            color: #475569;
            font-weight: 600;
            font-size: 14px;
        }}
        td {{
            color: #334155;
            font-size: 14px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 12px;
            font-weight: 500;
        }}
        .impact-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            color: white;
            font-size: 12px;
            font-weight: 600;
        }}
        ul {{
            margin-left: 24px;
            color: #334155;
        }}
        ul li {{
            margin: 12px 0;
            line-height: 1.6;
        }}
        .placeholder {{
            color: #94a3b8;
            font-style: italic;
            text-align: center;
        }}
        .scope-box {{
            background: #f0f9ff;
            border: 1px solid #0ea5e9;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .scope-box h3 {{
            color: #0ea5e9;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .scope-box p {{
            color: #334155;
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
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
        }}
        .btn-pdf {{
            background: linear-gradient(135deg, #f97316, #ea580c);
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
            <h1>试点追踪表</h1>
            <p class="subtitle">{company_name} · {project_name} · {generation_date}</p>
        </div>

        <div class="progress-section">
            <h2>整体进度</h2>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
            <div class="progress-stats">
                <span>已完成里程碑：{completed_milestones}/{total_milestones}</span>
                <span>完成率：{progress}%</span>
            </div>
        </div>

        <div class="card">
            <h2>试点范围</h2>
            <div class="scope-box">
                <h3>范围描述</h3>
                <p>{pilot_scope if pilot_scope else '<span class="placeholder">请输入试点范围...</span>'}</p>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <div>
                    <strong>开始日期：</strong>{start_date if start_date else '-'}
                </div>
                <div>
                    <strong>结束日期：</strong>{end_date if end_date else '-'}
                </div>
            </div>
        </div>

        <div class="card">
            <h2>里程碑追踪</h2>
            <table>
                <thead>
                    <tr>
                        <th>里程碑</th>
                        <th>计划日期</th>
                        <th>状态</th>
                        <th>备注</th>
                    </tr>
                </thead>
                <tbody>
                    {milestones_html}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>风险追踪</h2>
            <table>
                <thead>
                    <tr>
                        <th>风险描述</th>
                        <th>影响程度</th>
                        <th>应对措施</th>
                    </tr>
                </thead>
                <tbody>
                    {risks_html}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>试点学习</h2>
            <ul>
                {learnings_html}
            </ul>
        </div>

        <div class="card">
            <h2>推广建议</h2>
            <ul>
                {recommendations_html}
            </ul>
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
            a.download = '试点追踪表_' + getCurrentDate() + '.html';
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
                    filename: '试点追踪表_' + getCurrentDate() + '.pdf',
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
    parser = argparse.ArgumentParser(description='OD试点追踪表生成器')
    parser.add_argument('--data', type=str, help='JSON数据字符串')
    parser.add_argument('--output_path', type=str, default='./pilot_tracker.html', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.data:
        data = json.loads(args.data)
    else:
        data = {
            'company_name': 'XX公司',
            'project_name': 'OD能力提升项目',
            'pilot_scope': '选取华东区3家门店作为首批试点',
            'start_date': '2025-01-01',
            'end_date': '2025-03-31',
            'milestones': [
                {'name': '试点启动', 'date': '2025-01-15', 'status': 'completed', 'notes': '已完成'},
                {'name': '方案部署', 'date': '2025-02-01', 'status': 'in_progress', 'notes': '进行中'},
                {'name': '效果评估', 'date': '2025-03-15', 'status': 'pending', 'notes': ''},
                {'name': '试点总结', 'date': '2025-03-31', 'status': 'pending', 'notes': ''}
            ],
            'risks': [
                {'name': '人员抵触', 'impact': 'high', 'mitigation': '加强沟通与培训'},
                {'name': '资源不足', 'impact': 'medium', 'mitigation': '提前申请预算'}
            ],
            'learnings': [
                '试点初期需要更多时间进行人员培训',
                '本地化管理更能获得员工支持'
            ],
            'recommendations': [
                '推广前完善培训体系',
                '建立快速响应机制'
            ],
            'generation_date': get_current_date()
        }
    
    html_content = generate_pilot_tracker(data)
    
    output_path = data.get('output_path', args.output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(json.dumps({'status': 'success', 'output_path': output_path}))


if __name__ == '__main__':
    main()
