#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高管一键简报 - 3页Executive Summary PPT
"""

import json
import argparse

def generate_executive_summary(data):
    from datetime import datetime
    company_name = data.get("company_name", "贵公司")
    project_name = data.get("project_name", "OD变革项目")
    duration = data.get("duration", "6个月")
    budget = data.get("budget", "待定")
    roi = data.get("roi", "待评估")
    key_success = data.get("key_success", ["组织诊断", "方案设计", "实施落地"])
    risks = data.get("risks", ["变革阻力", "资源约束"])
    findings = data.get("findings", ["组织效能有待提升", "人才结构需优化"])
    recommendations = data.get("recommendations", ["启动组织诊断", "制定变革方案"])
    date = datetime.now().strftime('%Y年%m月%d日')
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Summary - ''' + company_name + '''</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f7fa; }
        .slide { min-height: 100vh; padding: 60px; display: flex; flex-direction: column; justify-content: center; background: white; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .slide-cover { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; }
        .slide-cover h1 { font-size: 56px; margin-bottom: 20px; font-weight: 300; }
        .slide-cover .subtitle { font-size: 24px; opacity: 0.8; margin-bottom: 40px; }
        .slide-cover .meta { font-size: 16px; opacity: 0.6; margin-top: auto; }
        .slide-title { font-size: 36px; color: #1a1a2e; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 3px solid #0f3460; }
        .key-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-bottom: 40px; }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 16px; text-align: center; }
        .metric-value { font-size: 48px; font-weight: bold; margin-bottom: 10px; }
        .metric-label { font-size: 16px; opacity: 0.9; }
        .content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
        .content-section h3 { font-size: 20px; color: #0f3460; margin-bottom: 20px; padding-left: 15px; border-left: 4px solid #667eea; }
        .content-list { list-style: none; }
        .content-list li { padding: 12px 0; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; }
        .content-list li::before { content: "→"; color: #667eea; margin-right: 15px; font-size: 18px; }
        .timeline { display: flex; justify-content: space-between; margin-top: 40px; padding: 30px; background: #f8f9fa; border-radius: 16px; }
        .timeline-item { text-align: center; flex: 1; }
        .timeline-item .phase { font-size: 14px; color: #666; margin-bottom: 10px; }
        .timeline-item .duration { font-size: 24px; font-weight: bold; color: #0f3460; }
        .slide-footer { margin-top: auto; padding-top: 30px; border-top: 1px solid #e8e8e8; font-size: 14px; color: #999; display: flex; justify-content: space-between; }
        .action-bar { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-top: 20px; }
        .btn { display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 8px; text-decoration: none; font-weight: 500; cursor: pointer; border: none; font-size: 16px; }
        .btn-outline { background: white; color: #667eea; border: 2px solid #667eea; }
    </style>
</head>
<body>
    <!-- Slide 1: 封面 -->
    <div class="slide slide-cover">
        <div class="subtitle">EXECUTIVE SUMMARY</div>
        <h1>''' + project_name + '''</h1>
        <div style="font-size: 20px; opacity: 0.8; margin-bottom: 20px;">''' + company_name + ''' · 组织发展变革项目</div>
        <div class="meta">报告日期：''' + date + ''' | 机密文件</div>
    </div>
    
    <!-- Slide 2: 核心发现 -->
    <div class="slide">
        <div class="slide-title">一、核心发现与关键指标</div>
        <div class="key-metrics">
            <div class="metric-card"><div class="metric-value">''' + duration + '''</div><div class="metric-label">预计周期</div></div>
            <div class="metric-card"><div class="metric-value">''' + budget + '''</div><div class="metric-label">项目预算</div></div>
            <div class="metric-card"><div class="metric-value">''' + roi + '''</div><div class="metric-label">预期ROI</div></div>
        </div>
        <div class="content-grid">
            <div class="content-section">
                <h3>关键发现</h3>
                <ul class="content-list">'''
    
    for finding in findings:
        html += '<li>' + finding + '</li>'
    
    html += '''</ul>
            </div>
            <div class="content-section">
                <h3>推荐行动</h3>
                <ul class="content-list">'''
    
    for rec in recommendations:
        html += '<li>' + rec + '</li>'
    
    html += '''</ul>
            </div>
        </div>
        <div class="slide-footer"><span>机密文件 · 仅供内部使用</span><span>''' + company_name + '''</span></div>
    </div>
    
    <!-- Slide 3: 关键成功因素与风险 -->
    <div class="slide">
        <div class="slide-title">二、关键成功因素与风险管控</div>
        <div class="content-grid">
            <div class="content-section">
                <h3>成功的关键因素</h3>
                <ul class="content-list">'''
    
    for item in key_success:
        html += '<li>' + item + '</li>'
    
    html += '''</ul>
            </div>
            <div class="content-section">
                <h3>主要风险与应对</h3>
                <ul class="content-list">'''
    
    for risk in risks:
        html += '<li>' + risk + '</li>'
    
    html += '''</ul>
            </div>
        </div>
        <div class="timeline">
            <div class="timeline-item"><div class="phase">阶段一</div><div class="duration">诊断评估</div></div>
            <div class="timeline-item"><div class="phase">阶段二</div><div class="duration">方案设计</div></div>
            <div class="timeline-item"><div class="phase">阶段三</div><div class="duration">实施落地</div></div>
            <div class="timeline-item"><div class="phase">阶段四</div><div class="duration">固化优化</div></div>
        </div>
        <div class="slide-footer"><span>机密文件 · 仅供内部使用</span><span>''' + company_name + '''</span></div>
    </div>
    
    <div class="action-bar">
        <button onclick="downloadHTML()" class="btn">下载完整报告</button>
        <button onclick="window.print()" class="btn btn-outline" style="margin-left:15px;">打印/导出PDF</button>
    </div>
    
    <script>
        function downloadHTML() {
            const html = document.documentElement.outerHTML;
            const blob = new Blob([html], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Executive_Summary_''' + project_name.replace(' ', '_') + '''_' + new Date().toISOString().slice(0,10) + '.html';
            a.click();
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>'''
    return html

def main():
    parser = argparse.ArgumentParser(description='高管一键简报 - 3页Executive Summary')
    parser.add_argument('--data', '-d', default='{}', help='项目数据JSON')
    parser.add_argument('--output', '-o', default='./executive_summary.html', help='输出文件路径')
    args = parser.parse_args()
    
    try:
        data = json.loads(args.data)
    except:
        data = {}
    
    html = generate_executive_summary(data)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(json.dumps({"status": "success", "output_path": args.output}, ensure_ascii=False))

if __name__ == "__main__":
    main()
