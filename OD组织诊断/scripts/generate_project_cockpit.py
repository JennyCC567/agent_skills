#!/usr/bin/env python3
"""
HTML项目驾驶舱生成器
生成包含进度甘特图、资源分配、风险矩阵的完整项目驾驶舱
支持可视化修复和直接下载功能
"""

import json
import sys
from pathlib import Path
from jinja2 import Template
from datetime import datetime


def get_embedded_js():
    """读取并内嵌JS库，确保HTML完全离线可用"""
    script_dir = Path(__file__).parent
    assets_dir = script_dir.parent / "assets"
    
    js_embed = ""
    
    # 读取ECharts库
    echarts_path = assets_dir / "echarts.min.js"
    if echarts_path.exists():
        with open(echarts_path, 'r', encoding='utf-8') as f:
            js_embed += f.read() + "\n"
    
    # 读取html2pdf库
    html2pdf_path = assets_dir / "html2pdf.bundle.min.js"
    if html2pdf_path.exists():
        with open(html2pdf_path, 'r', encoding='utf-8') as f:
            js_embed += f.read() + "\n"
    
    return js_embed


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "company_name": "XX公司",
        "project_name": "OD能力提升项目",
        "project_period": "2025-01 至 2025-06",
        "phases": [
            {"name": "启动", "start": "2025-01", "end": "2025-02", "progress": 100, "status": "完成"}
        ],
        "resources": [
            {"name": "OD顾问", "role": "顾问", "allocation": "100%"},
            {"name": "HRBP", "role": "项目经理", "allocation": "80%"}
        ],
        "risks": [
            {"name": "高层支持不足", "impact": "高", "probability": "中", "mitigation": "加强沟通"}
        ],
        "key_metrics": [
            {"name": "员工参与度", "current": 85, "target": 90, "unit": "%"},
            {"name": "培训覆盖率", "current": 60, "target": 100, "unit": "%"}
        ],
        "output_path": "./project_cockpit.html"
    }

    验证规则:
    - company_name 和 project_name 不能为空
    - phases, resources, risks 至少包含 1 项
    - output_path 必须以 .html 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'project_name' not in data or not data['project_name']:
        data['project_name'] = "OD项目"

    if 'project_period' not in data:
        data['project_period'] = "2025年"

    if 'phases' not in data or not isinstance(data['phases'], list):
        raise ValueError("缺少必需字段: phases 或phases格式错误")

    if len(data['phases']) == 0:
        raise ValueError("phases 必须至少包含 1 个阶段")

    if 'resources' not in data or not isinstance(data['resources'], list):
        data['resources'] = []

    if 'risks' not in data or not isinstance(data['risks'], list):
        data['risks'] = []

    if 'key_metrics' not in data or not isinstance(data['key_metrics'], list):
        data['key_metrics'] = []

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./project_cockpit.html"
    else:
        if not data['output_path'].endswith('.html'):
            raise ValueError("output_path 必须以 .html 结尾")

    return data


def generate_project_cockpit(data):
    """
    生成 HTML 项目驾驶舱

    参数:
        data: 包含项目信息的字典

    返回:
        str: 生成的 HTML 文件路径
    """
    company_name = data['company_name']
    project_name = data['project_name']
    project_period = data['project_period']
    phases = data['phases']
    resources = data['resources']
    risks = data['risks']
    key_metrics = data['key_metrics']
    output_path = Path(data['output_path'])

    # 获取内嵌的JS库，确保HTML完全离线可用
    embedded_js = get_embedded_js()

    # 生成甘特图数据
    gantt_data = []
    for idx, phase in enumerate(phases):
        gantt_data.append({
            'name': phase['name'],
            'progress': phase.get('progress', 0),
            'status': phase.get('status', '未开始')
        })

    # 生成资源分配数据
    resource_data = []
    for res in resources:
        allocation = res.get('allocation', '0%').replace('%', '')
        resource_data.append({
            'name': res['name'],
            'role': res['role'],
            'allocation': float(allocation) if allocation else 0
        })

    # 生成风险数据 - 修复：保留原始中文值，同时生成数字映射值
    impact_map = {'低': 1, '中': 2, '高': 3}
    prob_map = {'低': 1, '中': 2, '高': 3}
    risk_data = []
    for risk in risks:
        # 获取原始值
        impact_text = risk.get('impact', '中')
        prob_text = risk.get('probability', '中')
        
        # 映射为数字
        impact_value = impact_map.get(impact_text, 2)
        prob_value = prob_map.get(prob_text, 2)
        
        risk_data.append({
            'name': risk['name'],
            'impact_text': impact_text,  # 原始中文
            'impact_value': impact_value,  # 数字映射
            'probability_text': prob_text,  # 原始中文
            'probability_value': prob_value,  # 数字映射
            'mitigation': risk.get('mitigation', ''),
            'x': prob_value,
            'y': impact_value
        })

    # 生成关键指标数据
    metrics_data = []
    for metric in key_metrics:
        metrics_data.append({
            'name': metric['name'],
            'current': metric.get('current', 0),
            'target': metric.get('target', 100),
            'unit': metric.get('unit', '')
        })

    # HTML模板
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - 项目驾驶舱</title>
    <script>
    // 内嵌JS库，确保完全离线可用
    {embedded_js}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 20px;
        }}
        .cockpit-container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        .header h1 {{
            font-size: 32px;
            margin-bottom: 8px;
            color: white;
        }}
        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
            color: white;
        }}
        .download-bar {{
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .btn {{
            background: #3b82f6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .btn:hover {{
            background: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }}
        .btn:active {{
            transform: translateY(0);
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            margin-bottom: 24px;
        }}
        .card {{
            background: #1e293b;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #334155;
        }}
        .card-full {{
            grid-column: span 2;
        }}
        .card-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #f1f5f9;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .chart-container {{
            width: 100%;
            height: 300px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        .metric-card {{
            background: #334155;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        .metric-name {{
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 4px;
        }}
        .metric-target {{
            font-size: 12px;
            color: #64748b;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status-completed {{ background: #22c55e; color: white; }}
        .status-in-progress {{ background: #f59e0b; color: white; }}
        .status-not-started {{ background: #64748b; color: white; }}
        .disclaimer {{
            margin-top: 24px;
            padding: 16px;
            background: #1e293b;
            border-left: 4px solid #ef4444;
            border-radius: 8px;
            font-size: 12px;
            color: #94a3b8;
            line-height: 1.6;
        }}
        .disclaimer strong {{
            color: #dc2626;
        }}
        .no-data {{
            text-align: center;
            padding: 40px;
            color: #94a3b8;
            font-size: 14px;
        }}
        @media (max-width: 1200px) {{
            .dashboard-grid {{ grid-template-columns: 1fr; }}
            .card-full {{ grid-column: span 1; }}
        }}
        @media print {{
            body {{ background: white; color: black; }}
            .download-bar {{ display: none; }}
            .cockpit-container {{ max-width: 100%; }}
            .card {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="cockpit-container">
        <div class="header">
            <h1>🚀 {project_name} - 项目驾驶舱</h1>
            <div class="subtitle">{company_name} | {project_period} | 实时监控</div>
        </div>

        <!-- 关键指标 -->
        <div class="card card-full">
            <div class="card-title">📊 关键指标概览</div>
            <div class="metrics-grid">
                {"".join([f'''
                <div class="metric-card">
                    <div class="metric-name">{m['name']}</div>
                    <div class="metric-value">{m['current']}{m['unit']}</div>
                    <div class="metric-target">目标: {m['target']}{m['unit']}</div>
                </div>
                ''' for m in metrics_data])}
            </div>
        </div>

        <!-- 项目进度甘特图 -->
        <div class="card card-full">
            <div class="card-title">⏱️ 项目进度追踪</div>
            <div id="ganttChart" class="chart-container"></div>
        </div>

        <!-- 资源分配饼图 -->
        <div class="card">
            <div class="card-title">👥 资源分配</div>
            <div id="resourceChart" class="chart-container"></div>
        </div>

        <!-- 风险矩阵散点图 -->
        <div class="card">
            <div class="card-title">⚠️ 风险矩阵</div>
            <div id="riskChart" class="chart-container"></div>
        </div>

        <!-- 阶段列表 -->
        <div class="card card-full">
            <div class="card-title">📋 阶段详细列表</div>
            <div style="margin-top: 16px;">
                {"".join([f'''
                <div style="display: flex; align-items: center; padding: 12px; background: #334155; margin-bottom: 8px; border-radius: 8px;">
                    <span style="width: 40px; font-weight: 700; color: #3b82f6;">{idx + 1}</span>
                    <span style="flex: 1; margin: 0 16px;">{p['name']}</span>
                    <div style="flex: 2; height: 8px; background: #475569; border-radius: 4px; overflow: hidden;">
                        <div style="width: {p.get('progress', 0)}%; height: 100%; background: #3b82f6;"></div>
                    </div>
                    <span style="margin-left: 16px; font-size: 14px;">{p.get('progress', 0)}%</span>
                    <span style="margin-left: 16px;" class="status-badge {'status-completed' if p.get('status') == '完成' else 'status-in-progress' if p.get('status') == '进行中' else 'status-not-started'}">{p.get('status', '未开始')}</span>
                </div>
                ''' for idx, p in enumerate(phases)])}
            </div>
        </div>

        <!-- 免责申明 -->
        <div class="card card-full" style="background: #1e293b; border-color: #334155;">
            <div style="padding: 20px; color: #94a3b8; font-size: 13px; line-height: 1.8;">
                <strong style="color: #3b82f6;">免责申明：</strong> 本工具由AI基于专业理论、行业实践、公开政府文件、权威机构白皮书及行业报告生成。所有生成报告、分析及建议均基于您提供的数据得出，仅供参考，不构成正式管理咨询、法律意见或商业决策依据，任何决策及后果由您自行承担。
            </div>
        </div>

        <!-- 操作按钮 -->
        <div class="download-bar">
            <button class="btn" onclick="downloadHTML()">
                🌐 下载HTML
            </button>
            <button class="btn" onclick="downloadPDF()">
                📄 下载PDF
            </button>
        </div>
    </div>

    <!-- 数据对象 -->
    <script>
        var projectData = {{
            phases: {json.dumps(phases, ensure_ascii=False)},
            resources: {json.dumps(resource_data, ensure_ascii=False)},
            risks: {json.dumps(risk_data, ensure_ascii=False)},
            metrics: {json.dumps(metrics_data, ensure_ascii=False)},
            projectName: "{project_name}"
        }};
    </script>

    <!-- 图表初始化 -->
    <script>
        // 初始化所有图表
        function initCharts() {{
            try {{
                initGanttChart();
                initResourceChart();
                initRiskChart();
            }} catch (error) {{
                console.error('图表初始化失败:', error);
                alert('图表加载失败，请刷新页面重试');
            }}
        }}

        // 项目进度甘特图
        function initGanttChart() {{
            var chart = echarts.init(document.getElementById('ganttChart'));
            var phaseNames = projectData.phases.map(p => p.name);
            var progressValues = projectData.phases.map(p => p.progress || 0);

            var option = {{
                tooltip: {{
                    trigger: 'axis',
                    axisPointer: {{ type: 'shadow' }}
                }},
                xAxis: {{
                    type: 'category',
                    data: phaseNames,
                    axisLabel: {{ color: '#94a3b8' }},
                    axisLine: {{ lineStyle: {{ color: '#334155' }} }}
                }},
                yAxis: {{
                    type: 'value',
                    max: 100,
                    axisLabel: {{ formatter: '{{value}}%', color: '#94a3b8' }},
                    axisLine: {{ lineStyle: {{ color: '#334155' }} }},
                    splitLine: {{ lineStyle: {{ color: '#334155', type: 'dashed' }} }}
                }},
                series: [{{
                    type: 'bar',
                    data: progressValues,
                    barWidth: '50%',
                    itemStyle: {{
                        color: function(params) {{
                            var colors = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
                            return colors[params.dataIndex % colors.length];
                        }},
                        borderRadius: [4, 4, 0, 0]
                    }},
                    label: {{
                        show: true,
                        position: 'top',
                        formatter: '{{c}}%',
                        color: '#f1f5f9'
                    }}
                }}]
            }};
            chart.setOption(option);
            return chart;
        }}

        // 资源分配饼图
        function initResourceChart() {{
            var chart = echarts.init(document.getElementById('resourceChart'));
            var data = projectData.resources.map(r => ({{
                name: r.name,
                value: r.allocation
            }}));

            var option = {{
                tooltip: {{
                    trigger: 'item',
                    formatter: '{{b}}: {{c}}% ({{d}}%)'
                }},
                legend: {{
                    orient: 'vertical',
                    right: 10,
                    top: 'center',
                    textStyle: {{ color: '#94a3b8' }}
                }},
                series: [{{
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: true,
                    itemStyle: {{
                        borderRadius: 10,
                        borderColor: '#1e293b',
                        borderWidth: 2
                    }},
                    label: {{
                        show: false,
                        position: 'center'
                    }},
                    emphasis: {{
                        label: {{
                            show: true,
                            fontSize: 18,
                            fontWeight: 'bold',
                            color: '#f1f5f9'
                        }},
                        itemStyle: {{
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }}
                    }},
                    labelLine: {{ show: false }},
                    data: data
                }}]
            }};
            chart.setOption(option);
            return chart;
        }}

        // 风险矩阵散点图 - 修复版本
        function initRiskChart() {{
            var chart = echarts.init(document.getElementById('riskChart'));
            
            // 检查是否有风险数据
            if (!projectData.risks || projectData.risks.length === 0) {{
                document.getElementById('riskChart').innerHTML = '<div class="no-data">暂无风险数据</div>';
                return null;
            }}
            
            // 使用Python端已经转换好的数字值
            var data = projectData.risks.map(r => ({{
                name: r.name,
                value: [r.probability_value, r.impact_value],  // 使用数字坐标
                mitigation: r.mitigation,
                itemStyle: {{
                    color: r.probability_value >= 2 && r.impact_value >= 2 ? '#ef4444' :
                           r.probability_value >= 2 || r.impact_value >= 2 ? '#f59e0b' : '#22c55e'
                }}
            }}));

            var option = {{
                tooltip: {{
                    formatter: function(params) {{
                        // 使用原始中文值显示
                        var impactMap = {{1: '低', 2: '中', 3: '高'}};
                        var probMap = {{1: '低', 2: '中', 3: '高'}};
                        var risk = projectData.risks[params.dataIndex];
                        return '<strong>' + params.data.name + '</strong><br/>' +
                               '影响程度: ' + risk.impact_text + '<br/>' +
                               '发生概率: ' + risk.probability_text + '<br/>' +
                               '应对措施: ' + (risk.mitigation || '无');
                    }},
                    backgroundColor: '#1e293b',
                    borderColor: '#334155',
                    textStyle: {{ color: '#e2e8f0' }}
                }},
                grid: {{
                    left: '10%',
                    right: '10%',
                    bottom: '15%',
                    top: '10%'
                }},
                xAxis: {{
                    type: 'value',
                    name: '发生概率',
                    nameTextStyle: {{ color: '#94a3b8' }},
                    min: 0,
                    max: 4,
                    axisLabel: {{
                        formatter: function(value) {{
                            var map = {{1: '低', 2: '中', 3: '高'}};
                            return map[value] || '';
                        }},
                        color: '#94a3b8'
                    }},
                    axisLine: {{ lineStyle: {{ color: '#334155' }} }},
                    splitLine: {{ lineStyle: {{ color: '#334155', type: 'dashed' }} }}
                }},
                yAxis: {{
                    type: 'value',
                    name: '影响程度',
                    nameTextStyle: {{ color: '#94a3b8' }},
                    min: 0,
                    max: 4,
                    axisLabel: {{
                        formatter: function(value) {{
                            var map = {{1: '低', 2: '中', 3: '高'}};
                            return map[value] || '';
                        }},
                        color: '#94a3b8'
                    }},
                    axisLine: {{ lineStyle: {{ color: '#334155' }} }},
                    splitLine: {{ lineStyle: {{ color: '#334155', type: 'dashed' }} }}
                }},
                series: [{{
                    type: 'scatter',
                    symbolSize: 40,
                    data: data,
                    itemStyle: {{
                        borderRadius: 8,
                        borderWidth: 2,
                        borderColor: '#1e293b'
                    }},
                    label: {{
                        show: true,
                        position: 'top',
                        formatter: function(params) {{
                            return params.data.name;
                        }},
                        color: '#f1f5f9',
                        fontSize: 12
                    }},
                    emphasis: {{
                        itemStyle: {{
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }}
                    }}
                }}]
            }};
            chart.setOption(option);
            return chart;
        }}

        // 下载HTML
        function downloadHTML() {{
            var htmlContent = document.documentElement.outerHTML;
            var blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = projectData.projectName + '_驾驶舱.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        // 下载PDF功能
        function downloadPDF() {{
            var element = document.querySelector('.cockpit-container');
            var opt = {{
                margin: 10,
                filename: projectData.projectName + '_驾驶舱.pdf',
                image: {{ type: 'jpeg', quality: 0.98 }},
                html2canvas: {{ scale: 2, useCORS: true }},
                jsPDF: {{ unit: 'mm', format: 'a4', orientation: 'landscape' }}
            }};

            var btn = document.querySelector('button[onclick="downloadPDF()"]');
            var originalText = btn.textContent;
            btn.textContent = '正在生成PDF...';
            btn.disabled = true;

            html2pdf().set(opt).from(element).save().then(function() {{
                btn.textContent = originalText;
                btn.disabled = false;
            }}).catch(function(err) {{
                console.error('PDF生成失败:', err);
                alert('PDF生成失败，请尝试使用浏览器打印功能');
                btn.textContent = originalText;
                btn.disabled = false;
            }});
        }}

        // 页面加载完成后初始化
        window.addEventListener('load', initCharts);
        window.addEventListener('resize', function() {{
            setTimeout(function() {{
                var charts = [
                    echarts.getInstanceByDom(document.getElementById('ganttChart')),
                    echarts.getInstanceByDom(document.getElementById('resourceChart')),
                    echarts.getInstanceByDom(document.getElementById('riskChart'))
                ];
                charts.forEach(chart => {{
                    if (chart) chart.resize();
                }});
            }}, 100);
        }});
    </script>
</body>
</html>"""

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_project_cockpit.py '<JSON数据>'")
        print("示例: python generate_project_cockpit.py '{\"company_name\":\"XX公司\",\"project_name\":\"OD项目\",\"phases\":[...]}'")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成驾驶舱
        result_path = generate_project_cockpit(data)

        print(f"HTML项目驾驶舱已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
