#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业对标分析工具
基于行业基准数据进行组织效能对比分析
"""

import json
import argparse
from datetime import datetime


# 行业基准数据
INDUSTRY_BENCHMARKS = {
    '互联网': {
        'per_capita_revenue': 120,
        'turnover_rate': 20,
        'decision_days': 5,
        'management_span': 10,
        'engagement': 78,
        'productivity': 85,
        'innovation': 80
    },
    '制造业': {
        'per_capita_revenue': 60,
        'turnover_rate': 15,
        'decision_days': 10,
        'management_span': 8,
        'engagement': 75,
        'productivity': 78,
        'innovation': 65
    },
    '金融': {
        'per_capita_revenue': 100,
        'turnover_rate': 14,
        'decision_days': 20,
        'management_span': 7,
        'engagement': 76,
        'productivity': 80,
        'innovation': 70
    },
    '快消': {
        'per_capita_revenue': 80,
        'turnover_rate': 20,
        'decision_days': 7,
        'management_span': 9,
        'engagement': 74,
        'productivity': 82,
        'innovation': 68
    },
    '医疗': {
        'per_capita_revenue': 70,
        'turnover_rate': 14,
        'decision_days': 15,
        'management_span': 7,
        'engagement': 77,
        'productivity': 76,
        'innovation': 72
    }
}


def generate_benchmark_report(data):
    """生成行业对标分析报告"""
    company_name = data.get('company_name', '未知企业')
    industry = data.get('industry', '互联网')
    metrics = data.get('metrics', {})
    current_date = datetime.now().strftime('%Y年%m月%d日')

    benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS['互联网'])

    # 计算差距
    comparisons = []
    for key, label in [
        ('per_capita_revenue', '人均创收(万)'),
        ('turnover_rate', '员工流失率(%)'),
        ('decision_days', '决策周期(天)'),
        ('management_span', '管理幅度'),
        ('engagement', '员工敬业度'),
        ('productivity', '组织效能'),
        ('innovation', '创新活力')
    ]:
        actual = metrics.get(key, 0)
        bench = benchmark.get(key, 0)

        # 流失率和决策周期越低越好
        if key in ['turnover_rate', 'decision_days']:
            diff = ((bench - actual) / bench * 100) if bench > 0 else 0
            status = '优秀' if diff > 10 else ('良好' if diff > 0 else ('需改善' if diff > -10 else '严重不足'))
        else:
            diff = ((actual - bench) / bench * 100) if bench > 0 else 0
            status = '优秀' if diff > 10 else ('良好' if diff > 0 else ('需改善' if diff > -10 else '严重不足'))

        comparisons.append({
            'metric': label,
            'actual': actual,
            'benchmark': bench,
            'diff': diff,
            'status': status
        })

    # 计算综合得分
    positive_score = sum([c['diff'] for c in comparisons if c['diff'] > 0])
    total_score = min(100, 50 + positive_score)

    # 生成洞察
    insights = []
    for c in comparisons:
        if c['status'] == '严重不足':
            insights.append(f"{c['metric']}严重落后于行业，需立即改进")
        elif c['status'] == '需改善':
            insights.append(f"{c['metric']}低于行业平均，建议优化")

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>行业对标分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 40px; border-radius: 16px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 14px; }}
        .score-section {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 30px; text-align: center; }}
        .main-score {{ font-size: 72px; font-weight: bold; color: #11998e; }}
        .score-label {{ color: #666; margin-top: 8px; }}
        .benchmark-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 30px; }}
        .benchmark-card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .benchmark-card h3 {{ font-size: 14px; color: #666; margin-bottom: 12px; }}
        .benchmark-values {{ display: flex; justify-content: space-between; align-items: center; }}
        .benchmark-values .actual {{ font-size: 24px; font-weight: bold; color: #333; }}
        .benchmark-values .vs {{ color: #999; font-size: 12px; }}
        .benchmark-values .bench {{ color: #11998e; font-size: 16px; }}
        .status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; margin-top: 8px; }}
        .status-excellent {{ background: #d1fae5; color: #059669; }}
        .status-good {{ background: #dbeafe; color: #2563eb; }}
        .status-warning {{ background: #fef3c7; color: #d97706; }}
        .status-danger {{ background: #fee2e2; color: #dc2626; }}
        .insights-section {{ background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 30px; }}
        .insights-section h2 {{ font-size: 16px; margin-bottom: 16px; color: #333; }}
        .insight-item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; color: #555; }}
        .insight-item:last-child {{ border-bottom: none; }}
        .footer {{ text-align: center; padding: 20px; color: #999; font-size: 12px; }}
        .action-bar {{ position: fixed; bottom: 20px; right: 20px; display: flex; gap: 10px; }}
        .action-btn {{ padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; font-weight: 500; transition: transform 0.2s; color: white; }}
        .action-btn:hover {{ transform: translateY(-2px); }}
        @media print {{ .action-bar {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>行业对标分析报告</h1>
            <div class="subtitle">{company_name} | {industry}行业 | {current_date}</div>
        </div>

        <div class="score-section">
            <div class="main-score">{total_score:.0f}</div>
            <div class="score-label">综合对标得分（满分100）</div>
        </div>

        <div class="benchmark-grid">
            {''.join([f'''<div class="benchmark-card">
                <h3>{c['metric']}</h3>
                <div class="benchmark-values">
                    <span class="actual">{c['actual']}</span>
                    <span class="vs">vs</span>
                    <span class="bench">行业{c['benchmark']}</span>
                </div>
                <span class="status-badge status-{'excellent' if c['status']=='优秀' else 'good' if c['status']=='良好' else 'warning' if c['status']=='需改善' else 'danger'}">{c['status']} ({'+' if c['diff'] > 0 else ''}{c['diff']:.1f}%)</span>
            </div>''' for c in comparisons])}
        </div>

        <div class="insights-section">
            <h2>关键洞察</h2>
            {''.join([f'<div class="insight-item">{i}</div>' for i in insights]) if insights else '<div class="insight-item">整体表现与行业持平，继续保持</div>'}
        </div>

        <div class="footer">
            <p>本报告由OD组织发展助手生成 | {current_date}</p>
            <p style="margin-top: 8px;">数据来源：行业基准数据库（2024年度）</p>
        </div>
    </div>

    <div class="action-bar">
        <button class="action-btn" style="background: #11998e;" onclick="window.print()">下载HTML</button>
        <button class="action-btn" style="background: #38ef7d;" onclick="window.print()">导出PDF</button>
    </div>
</body>
</html>'''

    return html_content


def main():
    parser = argparse.ArgumentParser(description='行业对标分析工具')
    parser.add_argument('--data', required=True, help='JSON格式的对标数据')
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
        report = generate_benchmark_report(data)

        output_path = data.get('output_path', './benchmark_report.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(json.dumps({'status': 'success', 'output': output_path}, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
