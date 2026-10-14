#!/usr/bin/env python3
"""
PDF概念卡生成器
生成 OD 入门概念卡 PDF 文档，包含核心定义、与HR区别、关键模型
修复：解决中文字符显示问题
"""

import json
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def setup_chinese_fonts():
    """
    设置中文字体支持
    尝试使用系统字体或备用方案（跨平台支持）
    """
    import platform

    font_paths = []

    system = platform.system()

    if system == 'Windows':
        font_paths = [
            'C:\\Windows\\Fonts\\msyh.ttc',  # 微软雅黑
            'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
            'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
        ]
    elif system == 'Darwin':  # macOS
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',  # PingFang
            '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体
            '/System/Library/Fonts/STSong.ttf',  # 宋体
        ]
    else:  # Linux
        font_paths = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',  # Noto Sans CJK
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # DejaVu Sans（回退）
        ]

    for font_path in font_paths:
        try:
            if Path(font_path).exists():
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
        except:
            continue

    # 如果都失败，返回 None（使用默认字体，中文可能无法显示）
    return None


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "company_name": "XX公司",
        "title": "OD 组织发展入门概念卡",
        "content": {
            "definition": "OD（Organization Development）组织发展...",
            "difference": "传统HR关注个体绩效...",
            "key_models": ["麦肯锡7S模型", "BLM业务领先模型", "杨三角"]
        },
        "output_path": "./od_concept_card.pdf"
    }

    验证规则:
    - company_name 和 title 不能为空
    - content 必须包含 definition 和 difference
    - output_path 必须以 .pdf 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'title' not in data or not data['title']:
        data['title'] = "OD 组织发展入门概念卡"

    if 'content' not in data:
        raise ValueError("缺少必需字段: content")

    content = data['content']
    if 'definition' not in content:
        raise ValueError("content 必须包含 definition 字段")
    if 'difference' not in content:
        raise ValueError("content 必须包含 difference 字段")

    if 'key_models' not in content:
        data['content']['key_models'] = ["麦肯锡7S模型", "BLM业务领先模型", "杨三角"]

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./od_concept_card.pdf"
    else:
        if not data['output_path'].lower().endswith('.pdf'):
            raise ValueError("output_path 必须以 .pdf 结尾")

    return data


def generate_pdf_card(data):
    """
    生成 PDF 概念卡

    参数:
        data: 包含公司信息和内容的字典

    返回:
        str: 生成的 PDF 文件路径
    """
    company_name = data['company_name']
    title = data['title']
    content = data['content']
    output_path = Path(data['output_path'])

    # 设置中文字体
    chinese_font_name = setup_chinese_fonts()
    use_chinese = chinese_font_name is not None

    # 创建 PDF 文档（A5 尺寸）
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A5,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm
    )

    # 获取样式
    styles = getSampleStyleSheet()

    # 自定义样式
    title_font = chinese_font_name if use_chinese else 'Helvetica-Bold'
    body_font = chinese_font_name if use_chinese else 'Helvetica'

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=title_font,
        fontSize=18,
        textColor=colors.HexColor('#1e293b'),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName=title_font,
        fontSize=14,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=body_font,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )

    # 构建内容
    story = []

    # 封面
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"<b>{title}</b>", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"<i>{company_name}</i>", ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontName=body_font,
        fontSize=12,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER
    )))
    story.append(Spacer(1, 2*cm))

    # 分隔线
    story.append(Table([['']], colWidths=[18*cm], style=TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#e2e8f0'))
    ])))
    story.append(Spacer(1, 0.5*cm))

    # OD 定义
    story.append(Paragraph("什么是 OD？", subtitle_style))
    story.append(Paragraph(content['definition'], body_style))
    story.append(Spacer(1, 0.5*cm))

    # OD vs HR 区别
    story.append(Paragraph("OD vs 传统 HR", subtitle_style))
    story.append(Paragraph(content['difference'], body_style))
    story.append(Spacer(1, 0.5*cm))

    # 关键模型表格
    story.append(Paragraph("关键 OD 模型", subtitle_style))
    models_data = [['模型名称', '应用场景']]
    for model in content['key_models']:
        models_data.append([model, '组织诊断/变革设计'])

    models_table = Table(models_data, colWidths=[6*cm, 6*cm])
    models_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), title_font),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f1f5f9')),
        ('FONTNAME', (0, 1), (-1, -1), body_font),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    story.append(models_table)
    story.append(Spacer(1, 0.5*cm))

    # 核心本质
    story.append(Paragraph("核心本质", subtitle_style))
    story.append(Paragraph(
        "OD 不是做培训、不是搞团建，而是以战略为导向的系统性组织能力建设。",
        body_style
    ))
    story.append(Spacer(1, 2*cm))

    # 底部信息
    story.append(Paragraph(
        "<font size=8 color='#94a3b8'>本概念卡由 OD 组织发展助手 生成</font>",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontName=body_font,
            alignment=TA_CENTER
        )
    ))

    # 生成 PDF
    doc.build(story)

    # 检查字体问题警告
    if not use_chinese:
        import warnings
        warnings.warn("警告：未找到中文字体，PDF中的中文可能无法正常显示。建议安装中文字体或使用HTML格式输出。")

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_pdf_concept_card.py '<JSON数据>'")
        print("示例: python generate_pdf_concept_card.py '{\"company_name\":\"XX公司\",\"content\":{\"definition\":\"OD是...\",\"difference\":\"OD vs HR...\"}}'")
        print("\n提示：如果PDF中文无法显示，建议使用HTML格式输出（generate_diagnostic_questionnaire.py）")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成 PDF
        result_path = generate_pdf_card(data)

        print(f"PDF概念卡已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
