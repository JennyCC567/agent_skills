#!/usr/bin/env python3
"""
Word诊断简报生成器
生成 Word 格式的个人诊断分析简报，包含封面、诊断结果、雷达图、改进建议
"""

import json
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "company_name": "XX公司",
        "employee_name": "张三",
        "department": "销售部",
        "report_title": "个人诊断分析简报",
        "seven_s_scores": {"strategy": 7, "structure": 5, "systems": 6, "style": 7, "staff": 6, "skills": 4, "shared_values": 8},
        "analysis": "整体组织能力良好...",
        "recommendations": ["建议1", "建议2"],
        "chart_path": "./radar_chart.png",
        "output_path": "./diagnosis_report.docx"
    }

    验证规则:
    - company_name 和 employee_name 不能为空
    - seven_s_scores 必须包含全部7个维度，值为1-10
    - output_path 必须以 .docx 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'employee_name' not in data or not data['employee_name']:
        data['employee_name'] = "未指定"

    if 'department' not in data:
        data['department'] = "未指定"

    if 'report_title' not in data:
        data['report_title'] = "个人诊断分析简报"

    if 'seven_s_scores' not in data:
        raise ValueError("缺少必需字段: seven_s_scores")

    # 验证7S评分
    seven_s = data['seven_s_scores']
    required_dims = ['strategy', 'structure', 'systems', 'style', 'staff', 'skills', 'shared_values']
    for dim in required_dims:
        if dim not in seven_s:
            raise ValueError(f"seven_s_scores 缺少必需维度: {dim}")
        val = seven_s[dim]
        if not isinstance(val, (int, float)) or val < 1 or val > 10:
            raise ValueError(f"{dim} 评分必须在1-10之间")

    if 'analysis' not in data:
        data['analysis'] = "暂无分析内容"

    if 'recommendations' not in data:
        data['recommendations'] = []

    if 'chart_path' not in data:
        data['chart_path'] = None

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./diagnosis_report.docx"
    else:
        if not data['output_path'].endswith('.docx'):
            raise ValueError("output_path 必须以 .docx 结尾")

    return data


def get_chinese_font_name():
    """
    获取可用的中文字体名称（跨平台支持）

    返回:
        str: 可用的中文字体名称，如果都不可用返回None
    """
    import platform

    # 按优先级检测中文字体
    font_candidates = []

    system = platform.system()

    if system == 'Windows':
        font_candidates = ['微软雅黑', '宋体', '黑体', 'SimSun', 'Microsoft YaHei']
    elif system == 'Darwin':  # macOS
        font_candidates = ['PingFang SC', 'STHeiti', 'STSong', 'Heiti SC']
    else:  # Linux
        font_candidates = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']

    # 检测字体是否可用
    from docx.oxml.ns import qn
    from docx.shared import Pt

    # 由于python-docx没有直接的字体检测API，我们使用候选字体列表
    # 实际渲染时，Word会回退到系统默认字体
    return font_candidates[0] if font_candidates else None


def add_chinese_font(run):
    """为中文字符设置字体"""
    font_name = get_chinese_font_name()
    if font_name:
        run.font.name = font_name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    else:
        # 如果没有找到中文字体，使用默认设置
        run.font.name = 'Calibri'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')  # 尝试使用宋体作为回退


def generate_word_report(data):
    """
    生成 Word 诊断简报

    参数:
        data: 包含诊断信息的字典

    返回:
        str: 生成的 Word 文件路径
    """
    company_name = data['company_name']
    employee_name = data['employee_name']
    department = data['department']
    report_title = data['report_title']
    seven_s_scores = data['seven_s_scores']
    analysis = data['analysis']
    recommendations = data['recommendations']
    chart_path = data['chart_path']
    output_path = Path(data['output_path'])

    # 创建 Word 文档
    doc = Document()

    # 设置默认字体
    chinese_font = get_chinese_font_name()
    if chinese_font:
        doc.styles['Normal'].font.name = chinese_font
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), chinese_font)

    # ========== 封面 ==========
    # 标题
    title = doc.add_paragraph()
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title.add_run(report_title)
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 23, 42)
    add_chinese_font(title_run)

    # 公司名
    company = doc.add_paragraph()
    company.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    company_run = company.add_run(f"{company_name}")
    company_run.font.size = Pt(16)
    company_run.font.color.rgb = RGBColor(100, 116, 139)
    add_chinese_font(company_run)

    doc.add_paragraph().add_run()  # 空行

    # 员工信息
    info = doc.add_paragraph()
    info.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    info.add_run(f"员工姓名：{employee_name}").font.size = Pt(12)
    info.add_run(" | ")
    info.add_run(f"部门：{department}").font.size = Pt(12)

    doc.add_page_break()

    # ========== 诊断结果 ==========
    doc.add_heading('一、7S 模型诊断结果', level=1)

    # 评分表格
    table = doc.add_table(rows=8, cols=2)
    table.style = 'Light Grid Accent 1'

    # 表头
    header_cells = table.rows[0].cells
    header_cells[0].text = '维度'
    header_cells[1].text = '评分 (1-10)'
    for cell in header_cells:
        cell.paragraphs[0].runs[0].font.bold = True

    # 7S 维度名称映射
    dim_names = {
        'strategy': '战略',
        'structure': '结构',
        'systems': '制度',
        'style': '风格',
        'staff': '人员',
        'skills': '技能',
        'shared_values': '共享价值观'
    }

    # 填充数据
    for idx, (dim, name) in enumerate(dim_names.items(), 1):
        table.rows[idx].cells[0].text = name
        table.rows[idx].cells[1].text = str(seven_s_scores[dim])

    doc.add_paragraph().add_run()

    # ========== 雷达图 ==========
    if chart_path and Path(chart_path).exists():
        doc.add_heading('二、7S 雷达图', level=1)
        doc.add_picture(chart_path, width=Inches(5))
        doc.add_paragraph().add_run()

    # ========== 分析 ==========
    doc.add_heading('三、诊断分析', level=1)
    p = doc.add_paragraph(analysis)
    p.paragraph_format.line_spacing = 1.5

    # ========== 改进建议 ==========
    doc.add_heading('四、改进建议', level=1)
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            p = doc.add_paragraph(f"{idx}. {rec}", style='List Number')
    else:
        doc.add_paragraph("暂无具体改进建议")

    doc.add_paragraph().add_run()

    # ========== 免责申明 ==========
    doc.add_heading('免责申明', level=1)
    p_disclaimer = doc.add_paragraph()
    p_disclaimer.add_run('本工具由AI基于专业理论、行业实践、公开政府文件、权威机构白皮书及行业报告生成。所有生成报告、分析及建议均基于您提供的数据得出，仅供参考，不构成正式管理咨询、法律意见或商业决策依据，任何决策及后果由您自行承担。')
    p_disclaimer.paragraph_format.line_spacing = 1.8

    doc.add_paragraph().add_run()

    # ========== 页脚 ==========
    footer = doc.add_paragraph()
    footer.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    footer_run = footer.add_run('本报告由 OD 组织发展助手 生成')
    footer_run.font.size = Pt(10)
    footer_run.font.color.rgb = RGBColor(148, 163, 184)
    add_chinese_font(footer_run)

    # 保存文档
    doc.save(str(output_path))

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_word_report.py '<JSON数据>'")
        print("示例: python generate_word_report.py '{\"company_name\":\"XX公司\",\"employee_name\":\"张三\",\"seven_s_scores\":{\"strategy\":7,...}}'")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成 Word 报告
        result_path = generate_word_report(data)

        print(f"Word诊断简报已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
