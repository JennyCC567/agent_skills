#!/usr/bin/env python3
"""
PPT方案建议书生成器
生成 PowerPoint 格式的团队 OD 干预方案建议书
"""

import json
import sys
import platform
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "company_name": "XX公司",
        "title": "团队OD干预方案建议书",
        "subtitle": "组织能力提升项目",
        "author": "OD顾问",
        "slides": [
            {
                "type": "background",
                "title": "项目背景",
                "content": ["当前面临的挑战...", "战略目标..."]
            },
            {
                "type": "solution",
                "title": "解决方案",
                "content": ["方案1...", "方案2..."]
            }
        ],
        "output_path": "./od_proposal.pptx"
    }

    验证规则:
    - company_name 和 title 不能为空
    - slides 必须至少包含 1 页
    - output_path 必须以 .pptx 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'title' not in data or not data['title']:
        data['title'] = "团队OD干预方案建议书"

    if 'subtitle' not in data:
        data['subtitle'] = "组织能力提升项目"

    if 'author' not in data:
        data['author'] = "OD顾问"

    if 'slides' not in data or not isinstance(data['slides'], list):
        raise ValueError("缺少必需字段: slides 或slides格式错误")

    if len(data['slides']) == 0:
        raise ValueError("slides 必须至少包含 1 页")

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./od_proposal.pptx"
    else:
        if not data['output_path'].endswith('.pptx'):
            raise ValueError("output_path 必须以 .pptx 结尾")

    return data


def get_chinese_font_name():
    """
    获取可用的中文字体名称（跨平台支持）

    返回:
        str: 可用的中文字体名称
    """
    system = platform.system()

    # 按优先级检测中文字体
    if system == 'Windows':
        font_candidates = ['微软雅黑', '宋体', '黑体', 'SimSun', 'Microsoft YaHei']
    elif system == 'Darwin':  # macOS
        font_candidates = ['PingFang SC', 'STHeiti', 'STSong', 'Heiti SC']
    else:  # Linux
        font_candidates = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans', 'Liberation Sans']

    return font_candidates[0] if font_candidates else 'Arial'


def set_chinese_font(paragraph):
    """为段落设置中文字体"""
    font_name = get_chinese_font_name()
    if font_name:
        paragraph.font.name = font_name


def create_title_slide(prs, company_name, title, subtitle, author):
    """创建封面页"""
    slide_layout = prs.slide_layouts[6]  # 空白布局
    slide = prs.slides.add_slide(slide_layout)

    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.alignment = PP_ALIGN.CENTER
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = RGBColor(15, 23, 42)
    set_chinese_font(title_para)

    # 添加副标题
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.2), Inches(9), Inches(0.5))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.alignment = PP_ALIGN.CENTER
    subtitle_para.font.size = Pt(20)
    subtitle_para.font.color.rgb = RGBColor(59, 130, 246)
    set_chinese_font(subtitle_para)

    # 添加公司名
    company_box = slide.shapes.add_textbox(Inches(0.5), Inches(5), Inches(9), Inches(0.5))
    company_frame = company_box.text_frame
    company_frame.text = company_name
    company_para = company_frame.paragraphs[0]
    company_para.alignment = PP_ALIGN.CENTER
    company_para.font.size = Pt(16)
    company_para.font.color.rgb = RGBColor(100, 116, 139)
    set_chinese_font(company_para)

    # 添加作者
    author_box = slide.shapes.add_textbox(Inches(0.5), Inches(6), Inches(9), Inches(0.5))
    author_frame = author_box.text_frame
    author_frame.text = f"汇报人：{author}"
    author_para = author_frame.paragraphs[0]
    author_para.alignment = PP_ALIGN.CENTER
    author_para.font.size = Pt(14)
    author_para.font.color.rgb = RGBColor(148, 163, 184)


def create_content_slide(prs, slide_data):
    """创建内容页"""
    slide_layout = prs.slide_layouts[6]  # 空白布局
    slide = prs.slides.add_slide(slide_layout)

    title = slide_data.get('title', '')
    content = slide_data.get('content', [])
    slide_type = slide_data.get('type', 'content')

    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(28)
    title_para.font.bold = True
    title_para.font.color.rgb = RGBColor(15, 23, 42)
    set_chinese_font(title_para)

    # 添加内容
    if content:
        content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
        content_frame = content_box.text_frame
        content_frame.word_wrap = True

        for idx, item in enumerate(content):
            if idx == 0:
                p = content_frame.paragraphs[0]
            else:
                p = content_frame.add_paragraph()

            p.text = item
            p.font.size = Pt(16)
            set_chinese_font(p)
            p.level = 0
            p.space_after = Pt(12)

            # 根据类型设置不同颜色
            if slide_type == 'solution':
                p.font.color.rgb = RGBColor(59, 130, 246)
            elif slide_type == 'background':
                p.font.color.rgb = RGBColor(239, 68, 68)
            else:
                p.font.color.rgb = RGBColor(30, 41, 59)


def create_timeline_slide(prs, timeline_data):
    """创建时间线页"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 添加标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "项目实施时间线"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(28)
    title_para.font.bold = True
    title_para.font.color.rgb = RGBColor(15, 23, 42)
    set_chinese_font(title_para)

    # 添加时间线内容
    timeline_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
    timeline_frame = timeline_box.text_frame
    timeline_frame.word_wrap = True

    for idx, item in enumerate(timeline_data):
        if idx == 0:
            p = timeline_frame.paragraphs[0]
        else:
            p = timeline_frame.add_paragraph()

        phase = item.get('phase', '')
        duration = item.get('duration', '')
        tasks = item.get('tasks', [])

        p.text = f"阶段{idx + 1}：{phase} ({duration})"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = RGBColor(59, 130, 246)
        set_chinese_font(p)
        p.space_after = Pt(8)

        # 添加任务列表
        for task in tasks:
            task_p = timeline_frame.add_paragraph()
            task_p.text = f"  • {task}"
            task_p.font.size = Pt(14)
            task_p.font.color.rgb = RGBColor(71, 85, 105)
            set_chinese_font(task_p)
            task_p.space_after = Pt(4)


def generate_ppt_proposal(data):
    """
    生成 PPT 方案建议书

    参数:
        data: 包含PPT信息的字典

    返回:
        str: 生成的 PPT 文件路径
    """
    company_name = data['company_name']
    title = data['title']
    subtitle = data['subtitle']
    author = data['author']
    slides = data['slides']
    output_path = Path(data['output_path'])

    # 创建演示文稿
    prs = Presentation()

    # 设置幻灯片尺寸（16:9）
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # 1. 封面页
    create_title_slide(prs, company_name, title, subtitle, author)

    # 2. 内容页
    for slide_data in slides:
        slide_type = slide_data.get('type', 'content')

        if slide_type == 'timeline':
            # 时间线页（特殊处理）
            timeline_data = slide_data.get('timeline', [])
            if timeline_data:
                create_timeline_slide(prs, timeline_data)
        else:
            # 普通内容页
            create_content_slide(prs, slide_data)

    # 3. 结束页
    end_layout = prs.slide_layouts[6]
    end_slide = prs.slides.add_slide(end_layout)

    end_box = end_slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(0.5))
    end_frame = end_box.text_frame
    end_frame.text = "谢谢！"
    end_para = end_frame.paragraphs[0]
    end_para.alignment = PP_ALIGN.CENTER
    end_para.font.size = Pt(36)
    end_para.font.bold = True
    end_para.font.color.rgb = RGBColor(59, 130, 246)
    set_chinese_font(end_para)

    # 保存PPT
    prs.save(str(output_path))

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_ppt_proposal.py '<JSON数据>'")
        print("示例: python generate_ppt_proposal.py '{\"company_name\":\"XX公司\",\"title\":\"方案书\",\"slides\":[{\"title\":\"背景\",\"content\":[...\"]}]}")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成 PPT
        result_path = generate_ppt_proposal(data)

        print(f"PPT方案建议书已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
