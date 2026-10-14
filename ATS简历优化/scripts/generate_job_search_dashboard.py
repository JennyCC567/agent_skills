#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
求职进度看板生成脚本
生成漏斗式求职进度看板，直观展示ATS分→面试通过率→offer拿到率
"""

import argparse
import json
from datetime import datetime
import random


def generate_dashboard_html(
    ats_score: int = 75,
    total_applications: int = 10,
    interview_invites: int = 4,
    offers: int = 1,
    job_title: str = "高级Java开发工程师",
    target_company: str = "互联网行业"
) -> str:
    """
    生成求职进度看板HTML
    
    Args:
        ats_score: ATS评分（0-100）
        total_applications: 总投递数
        interview_invites: 面试邀请数
        offers: offer数量
        job_title: 目标岗位
        target_company: 目标公司
    
    Returns:
        HTML字符串
    """
    # 计算转化率
    interview_rate = (interview_invites / total_applications * 100) if total_applications > 0 else 0
    offer_rate = (offers / interview_invites * 100) if interview_invites > 0 else 0
    overall_success_rate = (offers / total_applications * 100) if total_applications > 0 else 0
    
    # 动态生成时间
    now = datetime.now()
    generated_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
    
    # 生成改进建议
    suggestions = []
    
    if ats_score < 70:
        suggestions.append({
            "type": "warning",
            "title": "ATS评分偏低",
            "content": "建议优化简历关键词，提高ATS评分到80分以上",
            "priority": "高"
        })
    elif ats_score < 85:
        suggestions.append({
            "type": "info",
            "title": "ATS评分良好",
            "content": "继续优化简历细节，争取达到90分以上",
            "priority": "中"
        })
    else:
        suggestions.append({
            "type": "success",
            "title": "ATS评分优秀",
            "content": "保持现有简历质量，继续投递",
            "priority": "低"
        })
    
    if interview_rate < 30:
        suggestions.append({
            "type": "warning",
            "title": "面试邀请率偏低",
            "content": "建议优化简历的匹配度，突出核心技能和项目经验",
            "priority": "高"
        })
    elif interview_rate < 50:
        suggestions.append({
            "type": "info",
            "title": "面试邀请率良好",
            "content": "继续优化，争取达到50%以上",
            "priority": "中"
        })
    
    if offers == 0:
        suggestions.append({
            "type": "warning",
            "title": "暂无Offer",
            "content": "建议加强面试准备，提升面试表现",
            "priority": "高"
        })
    
    # 生成漏斗图SVG
    funnel_svg = generate_funnel_svg(ats_score, interview_rate, offer_rate, overall_success_rate)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>求职进度看板 - {job_title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            font-size: 32px;
            color: #667eea;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .header .subtitle {{
            color: #666;
            font-size: 16px;
        }}

        .header .meta {{
            margin-top: 16px;
            display: flex;
            gap: 24px;
            flex-wrap: wrap;
        }}

        .header .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #888;
            font-size: 14px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }}

        .kpi-card .label {{
            color: #888;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .kpi-card .value {{
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .kpi-card .value.green {{
            color: #10b981;
        }}

        .kpi-card .value.blue {{
            color: #3b82f6;
        }}

        .kpi-card .value.purple {{
            color: #8b5cf6;
        }}

        .kpi-card .value.orange {{
            color: #f59e0b;
        }}

        .kpi-card .change {{
            font-size: 13px;
            color: #10b981;
        }}

        .kpi-card .change.negative {{
            color: #ef4444;
        }}

        .funnel-section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .funnel-section h2 {{
            font-size: 24px;
            color: #667eea;
            margin-bottom: 24px;
        }}

        .funnel-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 32px;
        }}

        .funnel-stages {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            width: 100%;
            max-width: 600px;
        }}

        .funnel-stage {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
            text-align: center;
        }}

        .funnel-stage.level-2 {{
            width: 80%;
            margin: 0 auto;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}

        .funnel-stage.level-3 {{
            width: 60%;
            margin: 0 auto;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}

        .funnel-stage.level-4 {{
            width: 40%;
            margin: 0 auto;
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}

        .funnel-stage .stage-label {{
            font-size: 16px;
            margin-bottom: 8px;
            opacity: 0.9;
        }}

        .funnel-stage .stage-value {{
            font-size: 28px;
            font-weight: 700;
        }}

        .funnel-stage .stage-count {{
            font-size: 14px;
            opacity: 0.8;
            margin-top: 4px;
        }}

        .data-section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .data-section h2 {{
            font-size: 24px;
            color: #667eea;
            margin-bottom: 24px;
        }}

        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}

        .data-item {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}

        .data-item .label {{
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .data-item .value {{
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
        }}

        .suggestions-section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .suggestions-section h2 {{
            font-size: 24px;
            color: #667eea;
            margin-bottom: 24px;
        }}

        .suggestion-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .suggestion-card {{
            border-left: 4px solid #e5e7eb;
            padding: 16px 20px;
            background: #f9fafb;
            border-radius: 0 12px 12px 0;
            transition: all 0.3s ease;
        }}

        .suggestion-card:hover {{
            background: #f3f4f6;
        }}

        .suggestion-card.warning {{
            border-left-color: #f59e0b;
            background: #fffbeb;
        }}

        .suggestion-card.warning:hover {{
            background: #fef3c7;
        }}

        .suggestion-card.info {{
            border-left-color: #3b82f6;
            background: #eff6ff;
        }}

        .suggestion-card.info:hover {{
            background: #dbeafe;
        }}

        .suggestion-card.success {{
            border-left-color: #10b981;
            background: #ecfdf5;
        }}

        .suggestion-card.success:hover {{
            background: #d1fae5;
        }}

        .suggestion-card .title {{
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .suggestion-card .title .priority {{
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 10px;
            background: #e5e7eb;
            color: #6b7280;
        }}

        .suggestion-card.warning .title .priority {{
            background: #fed7aa;
            color: #92400e;
        }}

        .suggestion-card .content {{
            color: #6b7280;
            line-height: 1.6;
        }}

        .tips-section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .tips-section h2 {{
            font-size: 24px;
            color: #667eea;
            margin-bottom: 24px;
        }}

        .tips-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}

        .tip-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}

        .tip-card h3 {{
            font-size: 16px;
            color: #1f2937;
            margin-bottom: 12px;
        }}

        .tip-card p {{
            color: #6b7280;
            font-size: 14px;
            line-height: 1.6;
        }}

        .footer {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            color: #888;
            font-size: 14px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .footer .generated-time {{
            color: #666;
            font-weight: 500;
        }}

        .export-buttons {{
            display: flex;
            gap: 16px;
            justify-content: center;
            margin-bottom: 24px;
        }}

        .btn {{
            padding: 12px 28px;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}

        .btn-secondary {{
            background: #f3f4f6;
            color: #374151;
        }}

        .btn-secondary:hover {{
            background: #e5e7eb;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .container {{
                max-width: none;
            }}

            .export-buttons {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>
                <span>📊</span>
                求职进度看板
            </h1>
            <p class="subtitle">求职进度追踪与优化建议 - {job_title} @ {target_company}</p>
            <div class="meta">
                <div class="meta-item">
                    <span>🎯</span>
                    <span>目标岗位：{job_title}</span>
                </div>
                <div class="meta-item">
                    <span>🏢</span>
                    <span>目标行业：{target_company}</span>
                </div>
                <div class="meta-item">
                    <span>📅</span>
                    <span>更新时间：{generated_time}</span>
                </div>
            </div>
        </div>

        <!-- 导出按钮 -->
        <div class="export-buttons">
            <button class="btn btn-primary" onclick="window.print()">
                <span>📄</span>
                导出PDF
            </button>
            <button class="btn btn-secondary" onclick="location.reload()">
                <span>🔄</span>
                刷新数据
            </button>
        </div>

        <!-- KPI指标 -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="label">ATS评分</div>
                <div class="value blue">{ats_score}</div>
                <div class="change">简历通过率预测</div>
            </div>
            <div class="kpi-card">
                <div class="label">总投递数</div>
                <div class="value purple">{total_applications}</div>
                <div class="change">简历投递次数</div>
            </div>
            <div class="kpi-card">
                <div class="label">面试邀请</div>
                <div class="value green">{interview_invites}</div>
                <div class="change">面试率：{interview_rate:.1f}%</div>
            </div>
            <div class="kpi-card">
                <div class="label">Offer数量</div>
                <div class="value orange">{offers}</div>
                <div class="change">成功率：{overall_success_rate:.1f}%</div>
            </div>
        </div>

        <!-- 漏斗图 -->
        <div class="funnel-section">
            <h2>🎯 求职漏斗分析</h2>
            <div class="funnel-stages">
                <div class="funnel-stage">
                    <div class="stage-label">ATS评分</div>
                    <div class="stage-value">{ats_score}分</div>
                    <div class="stage-count">简历筛选阶段</div>
                </div>
                <div class="funnel-stage level-2">
                    <div class="stage-label">面试邀请率</div>
                    <div class="stage-value">{interview_rate:.1f}%</div>
                    <div class="stage-count">{interview_invites}/{total_applications}</div>
                </div>
                <div class="funnel-stage level-3">
                    <div class="stage-label">面试通过率</div>
                    <div class="stage-value">{offer_rate:.1f}%</div>
                    <div class="stage-count">{offers}/{interview_invites}</div>
                </div>
                <div class="funnel-stage level-4">
                    <div class="stage-label">最终成功率</div>
                    <div class="stage-value">{overall_success_rate:.1f}%</div>
                    <div class="stage-count">{offers}/{total_applications}</div>
                </div>
            </div>
        </div>

        <!-- 详细数据 -->
        <div class="data-section">
            <h2>📈 详细数据</h2>
            <div class="data-grid">
                <div class="data-item">
                    <div class="label">简历投递</div>
                    <div class="value">{total_applications}</div>
                </div>
                <div class="data-item">
                    <div class="label">面试邀请</div>
                    <div class="value">{interview_invites}</div>
                </div>
                <div class="data-item">
                    <div class="label">Offer数量</div>
                    <div class="value">{offers}</div>
                </div>
                <div class="data-item">
                    <div class="label">整体成功率</div>
                    <div class="value">{overall_success_rate:.1f}%</div>
                </div>
            </div>
        </div>

        <!-- 改进建议 -->
        <div class="suggestions-section">
            <h2>💡 优化建议</h2>
            <div class="suggestion-list">
'''
    
    # 添加建议卡片
    for suggestion in suggestions:
        html += f'''
                <div class="suggestion-card {suggestion['type']}">
                    <div class="title">
                        {suggestion['title']}
                        <span class="priority">{suggestion['priority']}</span>
                    </div>
                    <div class="content">
                        {suggestion['content']}
                    </div>
                </div>
'''
    
    html += '''
            </div>
        </div>

        <!-- 实用技巧 -->
        <div class="tips-section">
            <h2>✨ 求职实用技巧</h2>
            <div class="tips-grid">
                <div class="tip-card">
                    <h3>📋 简历优化</h3>
                    <p>每份简历都要针对具体岗位进行定制，突出与JD要求匹配的关键词和技能。</p>
                </div>
                <div class="tip-card">
                    <h3>🎤 面试准备</h3>
                    <p>使用STAR法则回答问题，准备2-3个具体项目案例，展示你的解决问题能力。</p>
                </div>
                <div class="tip-card">
                    <h3>📊 数据追踪</h3>
                    <p>记录每次投递的岗位、公司、结果，定期分析数据，找出需要改进的环节。</p>
                </div>
            </div>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>本求职进度看板由简历优化与面试准备系统生成，数据仅供参考</p>
            <p class="generated-time">生成时间：{generated_time}</p>
        </div>
    </div>

    <script>
        // 页面加载完成后的动画效果
        document.addEventListener('DOMContentLoaded', function() {
            const kpiCards = document.querySelectorAll('.kpi-card');
            kpiCards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
    </script>
</body>
</html>'''
    
    return html


def generate_funnel_svg(ats_score: int, interview_rate: float, offer_rate: float, overall_success_rate: float) -> str:
    """
    生成漏斗图SVG（备用函数）
    
    Args:
        ats_score: ATS评分
        interview_rate: 面试率
        offer_rate: Offer率
        overall_success_rate: 整体成功率
    
    Returns:
        SVG字符串
    """
    svg = '''
    <svg width="500" height="400" xmlns="http://www.w3.org/2000/svg">
        <!-- 这是一个备用的SVG漏斗图 -->
        <rect x="0" y="0" width="500" height="400" fill="white"/>
        <text x="250" y="200" text-anchor="middle" font-size="16" fill="#666">
            漏斗图已内联在HTML中
        </text>
    </svg>
    '''
    return svg


def write_html_with_bom(html_content: str, output_path: str) -> None:
    """
    写入带BOM的UTF-8 HTML文件，防止中文乱码
    
    Args:
        html_content: HTML内容
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8-sig') as f:
        f.write(html_content)


def main():
    parser = argparse.ArgumentParser(description='生成求职进度看板')
    parser.add_argument('--ats-score', type=int, default=75, 
                        help='ATS评分（0-100）')
    parser.add_argument('--total-applications', type=int, default=10, 
                        help='总投递数')
    parser.add_argument('--interview-invites', type=int, default=4, 
                        help='面试邀请数')
    parser.add_argument('--offers', type=int, default=1, 
                        help='Offer数量')
    parser.add_argument('--job-title', type=str, default="高级Java开发工程师", 
                        help='目标岗位')
    parser.add_argument('--company', type=str, default="互联网行业", 
                        help='目标公司/行业')
    parser.add_argument('--output', type=str, 
                        default="./job_search_dashboard.html", 
                        help='输出HTML文件路径')
    
    args = parser.parse_args()
    
    try:
        # 生成HTML
        html = generate_dashboard_html(
            ats_score=args.ats_score,
            total_applications=args.total_applications,
            interview_invites=args.interview_invites,
            offers=args.offers,
            job_title=args.job_title,
            target_company=args.company
        )
        
        # 写入文件
        write_html_with_bom(html, args.output)
        
        print(f"✅ 求职进度看板已生成：{args.output}")
        print(f"📊 ATS评分：{args.ats_score}分")
        print(f"📈 总投递：{args.total_applications}，面试：{args.interview_invites}，Offer：{args.offers}")
        
    except Exception as e:
        print(f"❌ 生成求职进度看板失败：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
