#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLM×杨三角双模型诊断工具
中西合璧的全面组织诊断，融合战略与组织、能力与意愿
"""

import json
import argparse
from datetime import datetime
from pathlib import Path


def get_chinese_font():
    """跨平台获取中文字体"""
    import platform
    import os

    fonts = {
        'Windows': ['微软雅黑', '宋体', 'SimHei'],
        'Darwin': ['PingFang SC', 'STHeiti', 'Arial Unicode MS'],
        'Linux': ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']
    }

    system = platform.system()
    font_list = fonts.get(system, fonts['Linux'])

    try:
        from matplotlib import font_manager
        for font in font_list:
            font_path = font_manager.findfont(font_manager.FontProperties(family=font))
            if font_path:
                return font
    except:
        pass

    return font_list[0]


def generate_diagnosis_report(data):
    """生成BLM×杨三角双模型诊断报告"""
    company_name = data.get('company_name', '未知企业')
    industry = data.get('industry', '通用')
    current_date = datetime.now().strftime('%Y年%m月%d日')

    blm = data.get('blm_data', {})
    yang = data.get('yang_data', {})

    # BLM模型评分（1-10分）
    blm_scores = {
        '战略意图': blm.get('vision', 5),
        '市场洞察': blm.get('market_insight', 5),
        '创新焦点': blm.get('innovation', 5),
        '业务设计': blm.get('strategy', 5),
        '关键任务': blm.get('execution', 5),
        '正式组织': blm.get('talent', 5),
        '氛围文化': blm.get('culture', 5)
    }

    # 杨三角评分（1-10分）
    yang_scores = {
        '员工思维': yang.get('thought', 5),
        '员工能力': yang.get('skill', 5),
        '员工治理': yang.get('motivation', 5)
    }

    # 计算综合得分
    blm_avg = sum(blm_scores.values()) / len(blm_scores)
    yang_avg = sum(yang_scores.values()) / len(yang_scores)
    overall_score = (blm_avg + yang_avg) / 2

    # 生成建议
    suggestions = []

    # BLM分析
    for dimension, score in blm_scores.items():
        if score < 6:
            suggestions.append(f"[BLM-{dimension}] {score}分，需重点关注")

    # 杨三角分析
    for dimension, score in yang_scores.items():
        if score < 6:
            suggestions.append(f"[杨三角-{dimension}] {score}分，需重点关注")

    # 整合分析
    if blm_avg < 6 and yang_avg < 6:
        synthesis = "战略与组织能力双低，需系统性变革"
    elif blm_avg < 6:
        synthesis = "战略解码与执行能力不足，需强化BLM方法论"
    elif yang_avg < 6:
        synthesis = "组织能力（人才/文化）薄弱，需强化组织建设"
    else:
        synthesis = "整体状况良好，可持续优化提升"

    # 生成雷达图配置
    radar_config = {
        'blm': [
            {'name': '战略意图', 'value': blm_scores['战略意图']},
            {'name': '市场洞察', 'value': blm_scores['市场洞察']},
            {'name': '创新焦点', 'value': blm_scores['创新焦点']},
            {'name': '业务设计', 'value': blm_scores['业务设计']},
            {'name': '关键任务', 'value': blm_scores['关键任务']},
            {'name': '正式组织', 'value': blm_scores['正式组织']},
            {'name': '氛围文化', 'value': blm_scores['氛围文化']}
        ],
        'yang': [
            {'name': '员工思维', 'value': yang_scores['员工思维']},
            {'name': '员工能力', 'value': yang_scores['员工能力']},
            {'name': '员工治理', 'value': yang_scores['员工治理']}
        ]
    }

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BLM×杨三角双模型诊断报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 16px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 14px; }}
        .summary-cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); text-align: center; }}
        .card .score {{ font-size: 48px; font-weight: bold; margin-bottom: 8px; }}
        .card .label {{ color: #666; font-size: 14px; }}
        .card.blm .score {{ color: #667eea; }}
        .card.yang .score {{ color: #f093fb; }}
        .card.overall .score {{ color: #4facfe; }}
        .content-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
        .section {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .section h2 {{ font-size: 18px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #f0f0f0; }}
        .section.blm h2 {{ color: #667eea; border-color: #667eea; }}
        .section.yang h2 {{ color: #f093fb; border-color: #f093fb; }}
        .metric-item {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f5f5f5; }}
        .metric-item:last-child {{ border-bottom: none; }}
        .metric-name {{ color: #333; }}
        .metric-bar {{ flex: 1; height: 8px; background: #f0f0f0; border-radius: 4px; margin: 0 15px; overflow: hidden; }}
        .metric-bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
        .blm .metric-bar-fill {{ background: linear-gradient(90deg, #667eea, #764ba2); }}
        .yang .metric-bar-fill {{ background: linear-gradient(90deg, #f093fb, #f5576c); }}
        .metric-value {{ font-weight: bold; min-width: 40px; text-align: right; }}
        .synthesis-section {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 30px; }}
        .synthesis-section h2 {{ font-size: 18px; margin-bottom: 16px; color: #333; }}
        .synthesis-text {{ font-size: 16px; color: #555; padding: 16px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #4facfe; }}
        .suggestions {{ background: #fffbeb; border-radius: 12px; padding: 24px; margin-bottom: 30px; }}
        .suggestions h2 {{ font-size: 16px; margin-bottom: 16px; color: #92400e; }}
        .suggestion-item {{ padding: 10px 0; border-bottom: 1px dashed #fcd34d; }}
        .suggestion-item:last-child {{ border-bottom: none; }}
        .footer {{ text-align: center; padding: 20px; color: #999; font-size: 12px; }}
        .action-bar {{ position: fixed; bottom: 20px; right: 20px; display: flex; gap: 10px; }}
        .action-btn {{ padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; font-weight: 500; transition: transform 0.2s; }}
        .action-btn:hover {{ transform: translateY(-2px); }}
        .btn-download {{ background: #4facfe; color: white; }}
        .btn-pdf {{ background: #f5576c; color: white; }}
        @media print {{ .action-bar {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>BLM×杨三角双模型诊断报告</h1>
            <div class="subtitle">{company_name} | {industry} | {current_date}</div>
        </div>

        <div class="summary-cards">
            <div class="card blm">
                <div class="score">{blm_avg:.1f}</div>
                <div class="label">BLM战略与组织评分</div>
            </div>
            <div class="card yang">
                <div class="score">{yang_avg:.1f}</div>
                <div class="label">杨三角组织能力评分</div>
            </div>
            <div class="card overall">
                <div class="score">{overall_score:.1f}</div>
                <div class="label">综合诊断评分</div>
            </div>
        </div>

        <div class="content-grid">
            <div class="section blm">
                <h2>BLM模型分析（战略与执行）</h2>
                <div class="metrics">
                    {''.join([f'''<div class="metric-item">
                        <span class="metric-name">{name}</span>
                        <div class="metric-bar"><div class="metric-bar-fill" style="width: {score*10}%"></div></div>
                        <span class="metric-value">{score}</span>
                    </div>''' for name, score in blm_scores.items()])}
                </div>
            </div>

            <div class="section yang">
                <h2>杨三角分析（组织能力）</h2>
                <div class="metrics">
                    {''.join([f'''<div class="metric-item">
                        <span class="metric-name">{name}</span>
                        <div class="metric-bar"><div class="metric-bar-fill" style="width: {score*10}%"></div></div>
                        <span class="metric-value">{score}</span>
                    </div>''' for name, score in yang_scores.items()])}
                </div>
                <div style="margin-top: 24px; padding: 16px; background: #fdf2f8; border-radius: 8px;">
                    <h3 style="font-size: 14px; color: #be185d; margin-bottom: 12px;">杨三角解读</h3>
                    <p style="font-size: 13px; color: #666;">
                        杨三角强调组织能力的三个支柱：
                        <br>• <strong>员工思维</strong>：员工是否愿做（意愿/动机）
                        <br>• <strong>员工能力</strong>：员工是否善于做（能力/技能）
                        <br>• <strong>员工治理</strong>：组织是否允许做（机制/流程）
                    </p>
                </div>
            </div>
        </div>

        <div class="synthesis-section">
            <h2>整合诊断结论</h2>
            <div class="synthesis-text">{synthesis}</div>
        </div>

        <div class="suggestions">
            <h2>改进建议</h2>
            {''.join([f'<div class="suggestion-item">{s}</div>' for s in suggestions]) if suggestions else '<div class="suggestion-item">整体表现良好，建议持续优化</div>'}
        </div>

        <div class="footer">
            <p>本报告由OD组织发展助手生成 | {current_date}</p>
            <p style="margin-top: 8px;">免责声明：本报告仅供参考，不构成任何决策依据</p>
        </div>
    </div>

    <div class="action-bar">
        <button class="action-btn btn-download" onclick="window.print()">下载HTML</button>
        <button class="action-btn btn-pdf" onclick="window.print()">导出PDF</button>
    </div>
</body>
</html>'''

    return html_content


def main():
    parser = argparse.ArgumentParser(description='BLM×杨三角双模型诊断工具')
    parser.add_argument('--data', required=True, help='JSON格式的诊断数据')
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
        report = generate_diagnosis_report(data)

        output_path = data.get('output_path', './blm_yang_diagnosis.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(json.dumps({'status': 'success', 'output': output_path}, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
