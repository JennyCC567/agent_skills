#!/usr/bin/env python3
"""
Excel人才盘点底表生成器
生成带公式和颜色标识的 Excel 人才盘点底表
"""

import json
import sys
import platform
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "company_name": "XX公司",
        "title": "人才盘点底表",
        "employees": [
            {"name": "张三", "department": "销售部", "position": "销售经理", "performance": 8, "potential": 9}
        ],
        "output_path": "./talent_matrix.xlsx"
    }

    验证规则:
    - company_name 不能为空
    - employees 必须至少包含 1 人
    - 每个员工必须有 name, performance, potential
    - performance 和 potential 必须是 1-10 的数字
    - output_path 必须以 .xlsx 结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    if 'company_name' not in data or not data['company_name']:
        raise ValueError("缺少必需字段: company_name 或company_name为空")

    if 'title' not in data:
        data['title'] = "人才盘点底表"

    if 'employees' not in data or not isinstance(data['employees'], list):
        raise ValueError("缺少必需字段: employees 或employees格式错误")

    if len(data['employees']) == 0:
        raise ValueError("employees 必须至少包含 1 人")

    # 验证员工数据
    for idx, emp in enumerate(data['employees']):
        if 'name' not in emp or not emp['name']:
            raise ValueError(f"第{idx+1}个员工缺少name字段")

        if 'performance' not in emp:
            data['employees'][idx]['performance'] = 5
        else:
            perf = emp['performance']
            if not isinstance(perf, (int, float)) or perf < 1 or perf > 10:
                raise ValueError(f"第{idx+1}个员工的performance必须在1-10之间")

        if 'potential' not in emp:
            data['employees'][idx]['potential'] = 5
        else:
            pot = emp['potential']
            if not isinstance(pot, (int, float)) or pot < 1 or pot > 10:
                raise ValueError(f"第{idx+1}个员工的potential必须在1-10之间")

        if 'department' not in emp:
            data['employees'][idx]['department'] = "未指定"

        if 'position' not in emp:
            data['employees'][idx]['position'] = "未指定"

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./talent_matrix.xlsx"
    else:
        if not data['output_path'].endswith('.xlsx'):
            raise ValueError("output_path 必须以 .xlsx 结尾")

    return data


def get_nine_box_category(performance, potential):
    """
    根据绩效和潜力确定九宫格分类

    参数:
        performance: 绩效分数 (1-10)
        potential: 潜力分数 (1-10)

    返回:
        tuple: (分类名称, 颜色代码)
    """
    if performance >= 7 and potential >= 7:
        return ("超级明星", "00FF00")  # 绿色
    elif performance >= 7 and potential >= 5:
        return ("中坚力量", "90EE90")  # 浅绿
    elif performance >= 7:
        return ("金牛人才", "FFD700")  # 金色
    elif performance >= 5 and potential >= 7:
        return ("潜力人才", "00BFFF")  # 深天蓝
    elif performance >= 5 and potential >= 5:
        return ("稳定人才", "87CEEB")  # 天蓝
    elif performance >= 5:
        return ("待提升", "FFA07A")  # 浅红
    elif potential >= 7:
        return ("可培养", "FFA500")  # 橙色
    elif performance >= 3 or potential >= 3:
        return ("观察中", "FFD700")  # 金色
    else:
        return ("待优化", "FF0000")  # 红色


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


def generate_excel_talent_matrix(data):
    """
    生成 Excel 人才盘点底表

    参数:
        data: 包含员工信息的字典

    返回:
        str: 生成的 Excel 文件路径
    """
    company_name = data['company_name']
    title = data['title']
    employees = data['employees']
    output_path = Path(data['output_path'])

    # 创建工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = "人才盘点"

    # 获取中文字体
    chinese_font = get_chinese_font_name()

    # 定义样式
    header_font = Font(name=chinese_font, size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # 设置列标题
    headers = ['姓名', '部门', '职位', '绩效分数(1-10)', '潜力分数(1-10)', '九宫格分类', '平均分', '备注']
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border

    # 设置列宽
    column_widths = [10, 15, 15, 12, 12, 12, 10, 20]
    for col_idx, width in enumerate(column_widths, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # 填充员工数据
    for row_idx, emp in enumerate(employees, 2):
        name = emp['name']
        department = emp['department']
        position = emp['position']
        performance = emp['performance']
        potential = emp['potential']

        # 计算九宫格分类
        category, color_code = get_nine_box_category(performance, potential)

        # 计算平均分
        avg_score = (performance + potential) / 2

        # 填充数据
        ws.cell(row=row_idx, column=1, value=name).border = border
        ws.cell(row=row_idx, column=2, value=department).border = border
        ws.cell(row=row_idx, column=3, value=position).border = border
        ws.cell(row=row_idx, column=4, value=performance).border = border
        ws.cell(row=row_idx, column=5, value=potential).border = border

        # 九宫格分类单元格（带颜色）
        category_cell = ws.cell(row=row_idx, column=6, value=category)
        category_cell.border = border
        category_cell.fill = PatternFill(
            start_color=color_code,
            end_color=color_code,
            fill_type='solid'
        )
        category_cell.font = Font(bold=True, color='000000')

        ws.cell(row=row_idx, column=7, value=round(avg_score, 1)).border = border
        ws.cell(row=row_idx, column=8, value="").border = border

        # 添加公式（平均分）
        ws.cell(row=row_idx, column=7).value = f"=AVERAGE(D{row_idx}:E{row_idx})"

    # 添加统计信息
    stats_row = len(employees) + 3
    ws.cell(row=stats_row, column=1, value="统计信息").font = Font(bold=True)

    # 统计人数
    ws.cell(row=stats_row + 1, column=1, value="总人数:")
    ws.cell(row=stats_row + 1, column=2, value=len(employees))

    # 统计高潜人才（潜力 >= 7）
    high_potential_count = sum(1 for emp in employees if emp['potential'] >= 7)
    ws.cell(row=stats_row + 2, column=1, value="高潜人才数:")
    ws.cell(row=stats_row + 2, column=2, value=high_potential_count)

    # 统计高绩效（绩效 >= 7）
    high_performance_count = sum(1 for emp in employees if emp['performance'] >= 7)
    ws.cell(row=stats_row + 3, column=1, value="高绩效人数:")
    ws.cell(row=stats_row + 3, column=2, value=high_performance_count)

    # 冻结首行
    ws.freeze_panes = 'A2'

    # 保存工作簿
    wb.save(str(output_path))

    return str(output_path)


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法: python generate_excel_talent_matrix.py '<JSON数据>'")
        print("示例: python generate_excel_talent_matrix.py '{\"company_name\":\"XX公司\",\"employees\":[{\"name\":\"张三\",\"performance\":8,\"potential\":9}]}'")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成 Excel
        result_path = generate_excel_talent_matrix(data)

        print(f"Excel人才盘点底表已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
