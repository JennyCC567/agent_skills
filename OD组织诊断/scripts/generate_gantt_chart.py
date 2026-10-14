#!/usr/bin/env python3
"""
OD项目甘特图生成器
基于任务时间规划生成项目甘特图
"""

import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    [
        {"task": "战略诊断", "start": "2025-01-01", "end": "2025-01-15"},
        {"task": "方案设计", "start": "2025-01-16", "end": "2025-02-15"}
    ]

    验证规则:
    - 至少包含1条任务
    - start和end格式必须为YYYY-MM-DD
    - end必须晚于start
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查是否为列表
    if not isinstance(data, list):
        raise ValueError("输入必须是列表格式")

    # 检查是否至少包含1条任务
    if len(data) == 0:
        raise ValueError("至少需要包含1条任务")

    # 验证每条任务
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"第{idx+1}条任务必须是字典格式")

        if 'task' not in item or not item['task']:
            raise ValueError(f"第{idx+1}条任务缺少task字段或task为空")

        if 'start' not in item:
            raise ValueError(f"第{idx+1}条任务缺少start字段")
        if 'end' not in item:
            raise ValueError(f"第{idx+1}条任务缺少end字段")

        # 验证日期格式
        try:
            start_date = datetime.strptime(item['start'], '%Y-%m-%d')
            end_date = datetime.strptime(item['end'], '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"第{idx+1}条任务的日期格式必须为YYYY-MM-DD")

        # 验证end必须晚于start
        if end_date <= start_date:
            raise ValueError(f"第{idx+1}条任务的结束日期必须晚于开始日期")

    return data


def generate_gantt_chart(data, output_path="./gantt_chart.png"):
    """
    生成甘特图

    参数:
        data: 任务列表
        output_path: 输出图片路径

    返回:
        str: 生成的图片路径
    """
    # 提取数据
    tasks = [item['task'] for item in data]
    start_dates = [datetime.strptime(item['start'], '%Y-%m-%d') for item in data]
    end_dates = [datetime.strptime(item['end'], '%Y-%m-%d') for item in data]

    # 计算持续时间
    durations = [(end - start).days for start, end in zip(start_dates, end_dates)]

    # 创建图形
    fig, ax = plt.subplots(figsize=(14, 8))

    # 为每个任务生成不同颜色
    colors = plt.cm.Set3(np.linspace(0, 1, len(tasks)))

    # 绘制甘特条
    y_pos = range(len(tasks))
    for i, (task, start, duration, color) in enumerate(zip(tasks, start_dates, durations, colors)):
        ax.barh(i, duration, left=start, height=0.6, color=color,
                edgecolor='black', linewidth=1.5, label=task)

        # 添加任务标签
        ax.text(start, i, task, va='center', ha='right', fontsize=10,
                fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        # 添加持续时间标签
        mid_date = start + (end_dates[i] - start) / 2
        ax.text(mid_date, i, f'{duration}天', va='center', ha='center',
                fontsize=9, color='black', fontweight='bold')

    # 设置Y轴
    ax.set_yticks(y_pos)
    ax.set_yticklabels([''] * len(tasks))  # 隐藏Y轴标签
    ax.set_ylim(-0.5, len(tasks) - 0.5)

    # 设置X轴（日期格式）
    min_date = min(start_dates)
    max_date = max(end_dates)
    ax.set_xlim(min_date, max_date + (max_date - min_date) * 0.05)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, int((max_date - min_date).days / 10))))
    plt.xticks(rotation=45, ha='right', fontsize=9)

    # 添加网格
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # 设置标题和标签
    ax.set_title('OD项目甘特图', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('时间线', fontsize=12, fontweight='bold')

    # 添加关键里程碑线（可选：当前日期线）
    # current_date = datetime.now()
    # ax.axvline(x=current_date, color='red', linestyle='--', linewidth=2, label='当前日期')
    # ax.text(current_date, len(tasks)-0.3, '今天', rotation=90, va='top', ha='right',
    #         fontsize=10, fontweight='bold', color='red')

    # 添加项目统计信息
    total_duration = (max_date - min_date).days
    total_tasks = len(tasks)
    active_tasks = sum(1 for start, end in zip(start_dates, end_dates)
                       if start <= datetime.now() <= end) if datetime.now() >= min_date else 0

    stats_text = f'项目周期: {total_duration}天  任务总数: {total_tasks}'
    plt.figtext(0.5, 0.02, stats_text, ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    # 调整布局
    plt.tight_layout(rect=[0, 0.05, 1, 0.97])

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
    if len(sys.argv) < 2:
        print("用法: python generate_gantt_chart.py '<JSON数据>' [--output_path <路径>]")
        print("示例: python generate_gantt_chart.py '[{\"task\":\"诊断\",\"start\":\"2025-01-01\",\"end\":\"2025-01-15\"}]' --output_path ./gantt.png")
        return 1

    input_str = sys.argv[1]
    output_path = "./gantt_chart.png"

    # 解析可选参数
    if len(sys.argv) >= 4 and sys.argv[2] == "--output_path":
        output_path = sys.argv[3]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成甘特图
        result_path = generate_gantt_chart(data, output_path)

        print(f"甘特图已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
