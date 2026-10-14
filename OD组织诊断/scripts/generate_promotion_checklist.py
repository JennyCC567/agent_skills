#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD推广检查单生成器
阶段5推广-全面落地专用脚本

功能：
- 生成变革推广全面落地检查清单
- 基于Kotter八步法
- 输出HTML格式，支持一键导出PDF

输入参数：
- company_name: 公司名称（必填）
- project_name: 项目名称（必填）
- kotter_steps: Kotter八步法检查项，每项包含:
  - step: 步骤名称
  - description: 步骤描述
  - check_items: 检查项列表
  - status: 完成状态(pending/in_progress/completed)
  - evidence: 完成证据
- rollout_plan: 推广计划列表
- success_criteria: 成功标准
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
        'in_progress': '#f59e0b',
        'completed': '#22c55e'
    }
    return colors.get(status, '#94a3b8')

def status_text(status):
    """状态文本映射"""
    texts = {
        'pending': '未开始',
        'in_progress': '进行中',
        'completed': '已完成'
    }
    return texts.get(status, '未知')

def generate_promotion_checklist(data):
    """生成推广检查单HTML"""
    
    company_name = data.get('company_name', '公司')
    project_name = data.get('project_name', 'OD项目')
    kotter_steps = data.get('kotter_steps', [])
    rollout_plan = data.get('rollout_plan', [])
    success_criteria = data.get('success_criteria', [])
    generation_date = data.get('generation_date', get_current_date())
    
    # Kotter八步法默认数据
    default_kotter = [
        {'step': '1. 创造紧迫感', 'description': '让员工认识到变革的必要性', 'check_items': ['变革紧迫性分析报告', '管理层宣贯会议', '员工沟通会'], 'status': 'pending'},
        {'step': '2. 建立指导联盟', 'description': '组建变革领导团队', 'check_items': ['变革领导小组成立', '职责分工明确', '团队能力评估'], 'status': 'pending'},
        {'step': '3. 确立战略愿景', 'description': '明确变革目标和方向', 'check_items': ['战略解码完成', '目标分解到部门', 'KPI设定'], 'status': 'pending'},
        {'step': '4. 广泛沟通愿景', 'description': '让员工理解并认同变革', 'check_items': ['多渠道宣传', '培训覆盖全员', '问答互动'], 'status': 'pending'},
        {'step': '5. 授权广泛行动', 'description': '消除变革障碍，鼓励行动', 'check_items': ['障碍识别与排除', '授权机制建立', '快速成功案例'], 'status': 'pending'},
        {'step': '6. 创造短期成果', 'description': '通过可见成果建立信心', 'check_items': ['试点成功', '成果可视化', '及时表彰'], 'status': 'pending'},
        {'step': '7. 巩固成果深化变革', 'description': '利用成果推动更多变革', 'check_items': ['经验总结推广', '持续改进机制', '扩大覆盖范围'], 'status': 'pending'},
        {'step': '8. 将变革融入文化', 'description': '固化成功做法，形成文化', 'check_items': ['制度修订', '流程优化', '文化内化'], 'status': 'pending'}
    ]
    
    if not kotter_steps:
        kotter_steps = default_kotter
    
    # 计算进度
    total_steps = len(kotter_steps)
    completed_steps = len([s for s in kotter_steps if s.get('status') == 'completed'])
    in_progress_steps = len([s for s in kotter_steps if s.get('status') == 'in_progress'])
    overall_progress = int((completed_steps + in_progress_steps * 0.5) / total_steps * 100)
    
    # Kotter步骤HTML
    kotter_html = ''
    for s in kotter_steps:
        status = s.get('status', 'pending')
        check_items = s.get('check_items', [])
        
        check_items_html = '<ul class="check-list">'
        for item in check_items:
            check_items_html += f'<li>☐ {item}</li>'
        check_items_html += '</ul>'
        
        kotter_html += f'''
        <div class="kotter-step" data-status="{status}">
            <div class="step-header">
                <h3>{s.get('step', '')}</h3>
                <span class="status-badge" style="background: {status_color(status)}">{status_text(status)}</span>
            </div>
            <p class="step-desc">{s.get('description', '')}</p>
            {check_items_html}
            <div class="evidence">
                <strong>完成证据：</strong>
                <span class="evidence-text">{s.get('evidence', '<span class="placeholder">请上传完成证据...</span>')}</span>
            </div>
        </div>
        '''
    
    # 推广计划HTML
    rollout_html = ''
    for plan in rollout_plan:
        rollout_html += f'''
        <tr>
            <td>{plan.get('phase', '')}</td>
            <td>{plan.get('timeline', '')}</td>
            <td>{plan.get('scope', '')}</td>
            <td>{plan.get('owner', '')}</td>
            <td><span class="status-badge" style="background: {status_color(plan.get('status', 'pending'))}">{status_text(plan.get('status', 'pending'))}</span></td>
        </tr>
        '''
    
    if not rollout_html:
        rollout_html = '<tr><td colspan="5" class="placeholder">暂无推广计划，请补充...</td></tr>'
    
    # 成功标准HTML
    criteria_html = ''
    for criterion in success_criteria:
        criteria_html += f'<li>✓ {criterion}</li>'
    
    if not criteria_html:
        criteria_html = '<li class="placeholder">暂无成功标准，请补充...</li>'
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>推广检查单 - {company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
            background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
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
            color: #064e3b;
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .progress-overview {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .stat-card .number {{
            font-size: 32px;
            font-weight: 700;
            color: #064e3b;
        }}
        .stat-card .label {{
            color: #64748b;
            font-size: 14px;
            margin-top: 4px;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            color: #064e3b;
            font-size: 20px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #10b981;
        }}
        .kotter-step {{
            background: #f0fdf4;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            border-left: 4px solid #10b981;
        }}
        .kotter-step[data-status="in_progress"] {{
            border-left-color: #f59e0b;
            background: #fffbeb;
        }}
        .kotter-step[data-status="completed"] {{
            border-left-color: #22c55e;
        }}
        .step-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .step-header h3 {{
            color: #064e3b;
            font-size: 16px;
        }}
        .step-desc {{
            color: #64748b;
            font-size: 14px;
            margin-bottom: 12px;
        }}
        .check-list {{
            margin: 0;
            padding-left: 20px;
            color: #334155;
        }}
        .check-list li {{
            margin: 6px 0;
            font-size: 14px;
        }}
        .evidence {{
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px dashed #cbd5e1;
            font-size: 13px;
            color: #64748b;
        }}
        .evidence-text {{
            color: #334155;
        }}
        .placeholder {{
            color: #94a3b8;
            font-style: italic;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 12px;
            font-weight: 500;
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
            background: #f0fdf4;
            color: #064e3b;
            font-weight: 600;
            font-size: 14px;
        }}
        td {{
            color: #334155;
            font-size: 14px;
        }}
        ul {{ margin-left: 24px; }}
        ul li {{
            margin: 8px 0;
            color: #334155;
            font-size: 14px;
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
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }}
        .btn-pdf {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
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
            <h1>推广检查单</h1>
            <p class="subtitle">{company_name} · {project_name} · {generation_date}</p>
        </div>

        <div class="progress-overview">
            <div class="stat-card">
                <div class="number">{overall_progress}%</div>
                <div class="label">整体进度</div>
            </div>
            <div class="stat-card">
                <div class="number">{completed_steps}</div>
                <div class="label">已完成</div>
            </div>
            <div class="stat-card">
                <div class="number">{in_progress_steps}</div>
                <div class="label">进行中</div>
            </div>
            <div class="stat-card">
                <div class="number">{total_steps - completed_steps - in_progress_steps}</div>
                <div class="label">未开始</div>
            </div>
        </div>

        <div class="card">
            <h2>Kotter八步法检查</h2>
            {kotter_html}
        </div>

        <div class="card">
            <h2>推广计划</h2>
            <table>
                <thead>
                    <tr>
                        <th>阶段</th>
                        <th>时间</th>
                        <th>范围</th>
                        <th>负责人</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {rollout_html}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>成功标准</h2>
            <ul>
                {criteria_html}
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
            a.download = '推广检查单_' + getCurrentDate() + '.html';
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
                    filename: '推广检查单_' + getCurrentDate() + '.pdf',
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
    parser = argparse.ArgumentParser(description='OD推广检查单生成器')
    parser.add_argument('--data', type=str, help='JSON数据字符串')
    parser.add_argument('--output_path', type=str, default='./promotion_checklist.html', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.data:
        data = json.loads(args.data)
    else:
        data = {
            'company_name': 'XX公司',
            'project_name': 'OD能力提升项目',
            'rollout_plan': [
                {'phase': '第一阶段', 'timeline': 'Q1', 'scope': '华东区', 'owner': '张总', 'status': 'completed'},
                {'phase': '第二阶段', 'timeline': 'Q2', 'scope': '华南区', 'owner': '李总', 'status': 'in_progress'},
                {'phase': '第三阶段', 'timeline': 'Q3', 'scope': '华北区', 'owner': '王总', 'status': 'pending'}
            ],
            'success_criteria': [
                '全员覆盖率达到95%以上',
                '核心指标提升10%以上',
                '员工满意度提升15%'
            ],
            'generation_date': get_current_date()
        }
    
    html_content = generate_promotion_checklist(data)
    
    output_path = data.get('output_path', args.output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(json.dumps({'status': 'success', 'output_path': output_path}))


if __name__ == '__main__':
    main()
