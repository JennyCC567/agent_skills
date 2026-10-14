#!/usr/bin/env python3
"""
HTML诊断报告生成器
基于Jinja2模板生成交互式HTML诊断报告
"""

import json
import sys
import base64
from pathlib import Path
from jinja2 import Template


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "title": "XX公司组织健康度诊断报告",
        "sections": [
            {
                "heading": "一、诊断背景",
                "content": "本次诊断基于麦肯锡7S模型..."
            },
            {
                "heading": "二、7S模型分析",
                "content": "从雷达图可以看出...",
                "chart_path": "./radar_chart.png"
            }
        ],
        "output_path": "./od_diagnosis_report.html"
    }

    验证规则:
    - title不能为空
    - sections至少包含1个章节
    - 每个章节必须有heading和content
    - chart_path是可选的
    - output_path必须以.html结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'title' not in data or not data['title']:
        raise ValueError("缺少必需字段: title 或title为空")

    if 'sections' not in data:
        raise ValueError("缺少必需字段: sections")

    # 检查sections是否为列表
    if not isinstance(data['sections'], list):
        raise ValueError("sections 必须是列表格式")

    # 检查sections是否为空
    if len(data['sections']) == 0:
        raise ValueError("sections 至少需要包含1个章节")

    # 验证每个章节
    for idx, section in enumerate(data['sections']):
        if not isinstance(section, dict):
            raise ValueError(f"第{idx+1}个章节必须是字典格式")

        if 'heading' not in section or not section['heading']:
            raise ValueError(f"第{idx+1}个章节缺少heading字段或heading为空")

        if 'content' not in section:
            raise ValueError(f"第{idx+1}个章节缺少content字段")

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./od_diagnosis_report.html"
    else:
        # 验证output_path
        if not data['output_path'].endswith('.html'):
            raise ValueError("output_path 必须以 .html 结尾")

    return data


def encode_image_to_base64(image_path):
    """
    将图片转换为base64编码，用于嵌入HTML

    参数:
        image_path: 图片路径

    返回:
        str: base64编码的字符串，如果图片不存在返回None
    """
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        return None


def generate_html_report(data):
    """
    生成HTML报告

    参数:
        data: 包含报告标题、章节和输出路径的字典

    返回:
        str: 生成的HTML文件路径
    """
    title = data['title']
    sections = data['sections']
    output_path = Path(data['output_path'])

    # 将图片转换为base64
    for section in sections:
        if 'chart_path' in section and section['chart_path']:
            chart_base64 = encode_image_to_base64(section['chart_path'])
            if chart_base64:
                # 检测图片类型
                image_type = 'png' if section['chart_path'].endswith('.png') else 'jpeg'
                section['chart_base64'] = f"data:image/{image_type};base64,{chart_base64}"
            else:
                section['chart_base64'] = None

    # HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .header .subtitle {
            font-size: 14px;
            opacity: 0.9;
        }

        .content {
            padding: 40px 30px;
        }

        .section {
            margin-bottom: 35px;
            border-left: 4px solid #667eea;
            padding-left: 20px;
        }

        .section h2 {
            color: #667eea;
            font-size: 20px;
            margin-bottom: 15px;
            font-weight: bold;
        }

        .section p {
            color: #555;
            font-size: 15px;
            line-height: 1.8;
            margin-bottom: 15px;
            text-align: justify;
        }

        .chart-container {
            margin: 20px 0;
            text-align: center;
        }

        .chart-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 13px;
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
            }
        }

        @media (max-width: 600px) {
            .header h1 {
                font-size: 22px;
            }
            .content {
                padding: 20px 15px;
            }
            .section h2 {
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="subtitle">组织发展诊断报告</div>
        </div>

        <div class="content">
            {% for section in sections %}
            <div class="section">
                <h2>{{ section.heading }}</h2>
                {% if section.chart_base64 %}
                <div class="chart-container">
                    <img src="{{ section.chart_base64 }}" alt="图表">
                </div>
                {% endif %}
                <p>{{ section.content }}</p>
            </div>
            {% endfor %}

            <!-- 统一免责申明 -->
            <div class="section" style="border-left-color: #3b82f6; background: #f0f9ff; padding: 20px; border-radius: 8px; margin-top: 30px;">
                <p style="margin: 0; font-size: 13px; line-height: 1.8;">
                    <strong style="color: #3b82f6;">免责申明：</strong> 本工具由AI基于专业理论、行业实践、公开政府文件、权威机构白皮书及行业报告生成。所有生成报告、分析及建议均基于您提供的数据得出，仅供参考，不构成正式管理咨询、法律意见或商业决策依据，任何决策及后果由您自行承担。
                </p>
            </div>
        </div>

        <div class="footer">
            <p>本报告由 OD 组织发展助手 生成</p>
            <p>{{ generation_date }}</p>
        </div>
    </div>
</body>
</html>"""

    # 渲染模板
    template = Template(html_template)
    from datetime import datetime
    generation_date = datetime.now().strftime('%Y年%m月%d日')

    html_content = template.render(
        title=title,
        sections=sections,
        generation_date=generation_date
    )

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_html_report.py '<JSON数据>'")
        print("示例: python generate_html_report.py '{\"title\":\"诊断报告\",\"sections\":[{\"heading\":\"背景\",\"content\":\"内容\"}]}'")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成HTML报告
        result_path = generate_html_report(data)

        print(f"HTML报告已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
