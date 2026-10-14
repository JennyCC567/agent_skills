#!/usr/bin/env python3
"""
人才九宫格散点图生成器
基于绩效-潜力双维度生成人才盘点九宫格
"""

import json
import sys
import matplotlib.pyplot as plt
from pathlib import Path


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    [
        {"name": "张三", "performance": 8, "potential": 9},
        {"name": "李四", "performance": 6, "potential": 5}
    ]

    验证规则:
    - performance和potential必须在1-10之间
    - name字段不能为空
    - 至少包含1条数据
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查是否为列表
    if not isinstance(data, list):
        raise ValueError("输入必须是列表格式")

    # 检查是否至少包含1条数据
    if len(data) == 0:
        raise ValueError("至少需要包含1条员工数据")

    # 验证每条数据
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"第{idx+1}条数据必须是字典格式")

        if 'name' not in item:
            raise ValueError(f"第{idx+1}条数据缺少name字段")
        if not item['name']:
            raise ValueError(f"第{idx+1}条数据的name字段不能为空")

        if 'performance' not in item:
            raise ValueError(f"第{idx+1}条数据缺少performance字段")
        if not isinstance(item['performance'], (int, float)):
            raise ValueError(f"第{idx+1}条数据的performance必须是数字")
        if item['performance'] < 1 or item['performance'] > 10:
            raise ValueError(f"第{idx+1}条数据的performance必须在1-10之间")

        if 'potential' not in item:
            raise ValueError(f"第{idx+1}条数据缺少potential字段")
        if not isinstance(item['potential'], (int, float)):
            raise ValueError(f"第{idx+1}条数据的potential必须是数字")
        if item['potential'] < 1 or item['potential'] > 10:
            raise ValueError(f"第{idx+1}条数据的potential必须在1-10之间")

    return data


def generate_nine_box_grid(data, output_path="./nine_box_grid.png"):
    """
    生成人才九宫格散点图

    参数:
        data: 员工数据列表
        output_path: 输出图片路径

    返回:
        str: 生成的图片路径
    """
    # 提取数据
    names = [item['name'] for item in data]
    performances = [item['performance'] for item in data]
    potentials = [item['potential'] for item in data]

    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 10))

    # 绘制九宫格背景（3x3）
    # 绘制网格线
    ax.axvline(x=6.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(y=6.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=3.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axhline(y=3.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # 绘制九宫格区域
    # Q1: 高绩效高潜力（超级明星）
    ax.fill_between([6.5, 10], 6.5, 10, color='#2E8B57', alpha=0.1)
    ax.text(8.25, 8.25, 'Q1\n超级明星\n(高绩效/高潜力)',
            ha='center', va='center', fontsize=10, fontweight='bold', color='#2E8B57')

    # Q2: 中绩效高潜力（明日之星）
    ax.fill_between([3.5, 6.5], 6.5, 10, color='#3CB371', alpha=0.1)
    ax.text(5, 8.25, 'Q2\n明日之星\n(中绩效/高潜力)',
            ha='center', va='center', fontsize=9, color='#3CB371')

    # Q3: 高绩效中潜力（中坚力量）
    ax.fill_between([6.5, 10], 3.5, 6.5, color='#66CDAA', alpha=0.1)
    ax.text(8.25, 5, 'Q3\n中坚力量\n(高绩效/中潜力)',
            ha='center', va='center', fontsize=9, color='#66CDAA')

    # Q4: 高绩效低潜力（金牛人才）
    ax.fill_between([6.5, 10], 1, 3.5, color='#F0E68C', alpha=0.1)
    ax.text(8.25, 2.25, 'Q4\n金牛人才\n(高绩效/低潜力)',
            ha='center', va='center', fontsize=9, color='#DAA520')

    # Q5: 中绩效中潜力（潜力人才）
    ax.fill_between([3.5, 6.5], 3.5, 6.5, color='#FFD700', alpha=0.1)
    ax.text(5, 5, 'Q5\n潜力人才\n(中绩效/中潜力)',
            ha='center', va='center', fontsize=9, color='#FF8C00')

    # Q6: 低绩效高潜力（可培养）
    ax.fill_between([1, 3.5], 6.5, 10, color='#FFA07A', alpha=0.1)
    ax.text(2.25, 8.25, 'Q6\n可培养\n(低绩效/高潜力)',
            ha='center', va='center', fontsize=9, color='#FF6347')

    # Q7: 中绩效低潜力（稳定人才）
    ax.fill_between([3.5, 6.5], 1, 3.5, color='#FFA500', alpha=0.1)
    ax.text(5, 2.25, 'Q7\n稳定人才\n(中绩效/低潜力)',
            ha='center', va='center', fontsize=9, color='#FFA500')

    # Q8: 低绩效中潜力（基础人才）
    ax.fill_between([1, 3.5], 3.5, 6.5, color='#FF7F50', alpha=0.1)
    ax.text(2.25, 5, 'Q8\n基础人才\n(低绩效/中潜力)',
            ha='center', va='center', fontsize=9, color='#FF7F50')

    # Q9: 低绩效低潜力（待优化）
    ax.fill_between([1, 3.5], 1, 3.5, color='#FF4500', alpha=0.1)
    ax.text(2.25, 2.25, 'Q9\n待优化\n(低绩效/低潜力)',
            ha='center', va='center', fontsize=9, color='#FF4500')

    # 绘制散点
    scatter = ax.scatter(performances, potentials, c=potentials, s=200,
                        cmap='RdYlGn', edgecolors='black', linewidth=1.5,
                        alpha=0.8)

    # 添加姓名标签（避免重叠）
    for i, name in enumerate(names):
        ax.annotate(name, (performances[i], potentials[i]),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

    # 设置坐标轴范围
    ax.set_xlim(0.5, 10.5)
    ax.set_ylim(0.5, 10.5)

    # 设置坐标轴标签
    ax.set_xlabel('绩效分数 (Performance)', fontsize=12, fontweight='bold')
    ax.set_ylabel('潜力分数 (Potential)', fontsize=12, fontweight='bold')

    # 设置刻度
    ax.set_xticks(range(1, 11))
    ax.set_yticks(range(1, 11))
    ax.set_xticklabels(range(1, 11), fontsize=9)
    ax.set_yticklabels(range(1, 11), fontsize=9)

    # 添加网格
    ax.grid(True, linestyle=':', alpha=0.3)

    # 添加标题
    ax.set_title('人才盘点九宫格', size=16, fontweight='bold', pad=20)

    # 添加统计信息
    total_count = len(data)
    high_potential = sum(1 for p in potentials if p >= 7)
    high_performance = sum(1 for p in performances if p >= 7)
    star_count = sum(1 for i in range(len(data)) if performances[i] >= 7 and potentials[i] >= 7)

    stats_text = f'总人数: {total_count}  高潜人才: {high_potential}  高绩效: {high_performance}  超级明星: {star_count}'
    plt.figtext(0.5, 0.02, stats_text, ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    # 调整布局
    plt.tight_layout(rect=[0, 0.05, 1, 1])

    # 确保输出目录存在
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存图片
    plt.savefig(str(output_path), dpi=300, bbox_inches='tight')
    plt.close()

    return str(output_path)


def main():
    """
    主函数
    """
    # 解析命令行参数
    if len(sys.argv) < 2:
        print("用法: python generate_nine_box_grid.py '<JSON数据>' [--output_path <路径>]")
        print("示例: python generate_nine_box_grid.py '[{\"name\":\"张三\",\"performance\":8,\"potential\":9}]' --output_path ./nine_box.png")
        return 1

    input_str = sys.argv[1]
    output_path = "./nine_box_grid.png"

    # 解析可选参数
    if len(sys.argv) >= 4 and sys.argv[2] == "--output_path":
        output_path = sys.argv[3]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成九宫格
        result_path = generate_nine_box_grid(data, output_path)

        print(f"九宫格已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
