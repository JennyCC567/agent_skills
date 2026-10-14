#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD组织健康度诊断报告生成器（V6.2合规版）
使用matplotlib生成base64 PNG图表，零JS依赖
"""

import json
import sys
import os
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from od_chart_utils import generate_radar_chart, generate_bar_chart

def generate_dashboard_html(data, output_path):
    """生成组织健康度诊断报告HTML"""
    company_name = data.get("company_name", "贵公司")
    report_title = data.get("report_title", "组织健康度诊断报告")
    
    # 获取7S数据
    seven_s_data = data.get("seven_s_data", {})
    current = seven_s_data.get("current", [0, 7, 6, 5, 8, 6, 7])
    target = seven_s_data.get("target", [9, 9, 8, 8, 9, 8, 9])
    
    # 生成雷达图base64
    radar_b64 = generate_radar_chart(
        dimensions=["战略", "结构", "制度", "价值观", "技能", "领导力", "人才"],
        values=current,
        title="当前组织健康度"
    )
    
    # 生成对比柱状图
    bar_b64 = generate_bar_chart(
        categories=["战略", "结构", "制度", "价值观", "技能", "领导力", "人才"],
        values=current,
        title="7S维度评分"
    )
    
    # 生成日期
    report_date = datetime.now().strftime("%Y年%m月%d日")
    
    # 生成HTML（纯CSS布局，无Flex/Grid，无JS依赖）
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'WenQuanYi Micro Hei', 'Microsoft YaHei', sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 850px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #1F4E79 0%, #2CA58D 100%);
            color: white;
            padding: 40px;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .section h2 {{
            font-size: 20px;
            color: #1F4E79;
            border-left: 4px solid #2CA58D;
            padding-left: 12px;
            margin-bottom: 20px;
        }}
        .chart-container {{
            text-align: center;
            padding: 20px;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
        }}
        .metrics-grid {{
            display: table;
            width: 100%;
            border-spacing: 10px;
        }}
        .metric-card {{
            display: table-cell;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
            width: 25%;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #2CA58D;
        }}
        .metric-label {{
            font-size: 12px;
            margin-top: 5px;
        }}
        .recommendations {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
        }}
        .rec-item {{
            padding: 12px;
            margin-bottom: 10px;
            background: white;
            border-radius: 6px;
            border-left: 3px solid #2CA58D;
        }}
        .rec-title {{
            font-weight: bold;
            color: #1F4E79;
        }}
        .action-bar {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .btn {{
            display: inline-block;
            padding: 12px 30px;
            background: #1F4E79;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            margin: 0 10px;
        }}
        .btn:hover {{
            background: #2CA58D;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
        @media print {{
            body {{ background: white !important; }}
            .container {{ max-width: 100% !important; padding: 0 !important; }}
            .action-bar {{ display: none !important; }}
            .section {{ box-shadow: none !important; page-break-inside: avoid; }}
            img {{ max-width: 100% !important; page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{report_title}</h1>
            <p>{company_name} | {report_date}</p>
        </div>
        
        <div class="section">
            <h2>一、组织健康度概览</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{sum(current)/len(current):.1f}</div>
                    <div class="metric-label">综合评分</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(current)}</div>
                    <div class="metric-label">评估维度</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{sum(1 for c in current if c < 6)}</div>
                    <div class="metric-label">待改善项</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{"良好" if sum(current)/len(current) >= 7 else "一般"}</div>
                    <div class="metric-label">健康状态</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>二、7S模型雷达图</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,{radar_b64}" alt="7S雷达图">
            </div>
        </div>
        
        <div class="section">
            <h2>三、维度评分对比</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,{bar_b64}" alt="维度评分">
            </div>
        </div>
        
        <div class="section">
            <h2>四、改进建议</h2>
            <div class="recommendations">
                <div class="rec-item">
                    <div class="rec-title">[推荐] 战略维度提升计划</div>
                    <p>建议开展战略澄清工作坊，明确3-5年发展方向和核心目标</p>
                </div>
                <div class="rec-item">
                    <div class="rec-title">[推荐] 人才梯队建设</div>
                    <p>启动人才盘点项目，识别关键岗位继任者和发展对象</p>
                </div>
                <div class="rec-item">
                    <div class="rec-title">[推荐] 制度流程优化</div>
                    <p>梳理核心业务流程，识别瓶颈环节并优化</p>
                </div>
            </div>
        </div>
        
        <div class="action-bar">
            <button class="btn" onclick="window.print()">导出PDF</button>
            <button class="btn" onclick="downloadHTML()">下载HTML</button>
        </div>
        
        <div class="footer">
            <p>本报告基于您提供的数据生成，仅供参考</p>
            <p>生成时间：{report_date}</p>
        </div>
    </div>
    
    <script>
        function downloadHTML() {{
            var html = document.documentElement.outerHTML;
            var blob = new Blob([html], {{ type: 'text/html' }});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = '组织健康度诊断报告_{report_date}.html';
            a.click();
            URL.revokeObjectURL(url);
        }}
    </script>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return {"status": "success", "output_path": output_path}

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_echarts_dashboard.py '<json_data>'")
        sys.exit(1)
    
    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)
    
    output_path = data.get("output_path", "./dashboard.html")
    result = generate_dashboard_html(data, output_path)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
