#!/usr/bin/env python3
"""
变革阻力力场分析图生成器
基于Lewin的力场分析模型，生成驱动力与阻力的对比分析图
"""

import json
import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def parse_input(input_str):
    """
    解析输入的JSON字符串

    输入格式:
    {
        "driving_forces": [
            {"name": "市场竞争压力", "score": 8},
            {"name": "高层支持", "score": 7}
        ],
        "restraining_forces": [
            {"name": "员工抵触", "score": 6},
            {"name": "资源不足", "score": 5}
        ],
        "output_path": "./force_field.png"
    }

    验证规则:
    - 驱动力和阻力列表至少各包含1个因素
    - 所有分数必须在1-10之间
    - 因素名称不能为空
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 检查必需字段
    required_fields = ['driving_forces', 'restraining_forces']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")

    # 检查列表是否为空
    if len(data['driving_forces']) == 0:
        raise ValueError("driving_forces 必须至少包含1个因素")
    if len(data['restraining_forces']) == 0:
        raise ValueError("restraining_forces 必须至少包含1个因素")

    # 验证驱动力
    for idx, item in enumerate(data['driving_forces']):
        if 'name' not in item or not item['name']:
            raise ValueError(f"驱动力第{idx+1}项缺少name字段或name为空")
        if 'score' not in item:
            raise ValueError(f"驱动力第{idx+1}项缺少score字段")
        if not isinstance(item['score'], (int, float)):
            raise ValueError(f"驱动力第{idx+1}项的score必须是数字")
        if item['score'] < 1 or item['score'] > 10:
            raise ValueError(f"驱动力第{idx+1}项的score必须在1-10之间")

    # 验证阻力
    for idx, item in enumerate(data['restraining_forces']):
        if 'name' not in item or not item['name']:
            raise ValueError(f"阻力第{idx+1}项缺少name字段或name为空")
        if 'score' not in item:
            raise ValueError(f"阻力第{idx+1}项缺少score字段")
        if not isinstance(item['score'], (int, float)):
            raise ValueError(f"阻力第{idx+1}项的score必须是数字")
        if item['score'] < 1 or item['score'] > 10:
            raise ValueError(f"阻力第{idx+1}项的score必须在1-10之间")

    # 设置默认output_path
    if 'output_path' not in data:
        data['output_path'] = "./force_field.png"

    return data


def generate_force_field(data):
    """
    生成力场分析图

    参数:
        data: 包含驱动力、阻力和输出路径的字典

    返回:
        str: 生成的图片路径
    """
    driving_forces = data['driving_forces']
    restraining_forces = data['restraining_forces']
    output_path = data['output_path']

    # 提取数据
    driving_names = [item['name'] for item in driving_forces]
    driving_scores = [item['score'] for item in driving_forces]
    restraining_names = [item['name'] for item in restraining_forces]
    restraining_scores = [item['score'] for item in restraining_forces]

    # 计算总分
    total_driving = sum(driving_scores)
    total_restraining = sum(restraining_scores)
    net_force = total_driving - total_restraining

    # 创建图形
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 8))

    # 图1: 驱动力柱状图
    y_pos = np.arange(len(driving_names))
    colors1 = plt.cm.Greens(np.linspace(0.4, 0.8, len(driving_scores)))
    bars1 = ax1.barh(y_pos, driving_scores, align='center', color=colors1, edgecolor='black', linewidth=1.5)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(driving_names, fontsize=11)
    ax1.invert_yaxis()
    ax1.set_xlabel('影响力分数', fontsize=12, fontweight='bold')
    ax1.set_title(f'驱动力\n(总分: {total_driving})', fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 11)
    ax1.grid(True, axis='x', linestyle='--', alpha=0.3)

    # 添加分数标签
    for i, (bar, score) in enumerate(zip(bars1, driving_scores)):
        ax1.text(score + 0.1, bar.get_y() + bar.get_height()/2, str(score),
                va='center', fontsize=10, fontweight='bold')

    # 图2: 阻力柱状图
    y_pos = np.arange(len(restraining_names))
    colors2 = plt.cm.Reds(np.linspace(0.4, 0.8, len(restraining_scores)))
    bars2 = ax2.barh(y_pos, restraining_scores, align='center', color=colors2, edgecolor='black', linewidth=1.5)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(restraining_names, fontsize=11)
    ax2.invert_yaxis()
    ax2.set_xlabel('影响力分数', fontsize=12, fontweight='bold')
    ax2.set_title(f'阻力\n(总分: {total_restraining})', fontsize=13, fontweight='bold')
    ax2.set_xlim(0, 11)
    ax2.grid(True, axis='x', linestyle='--', alpha=0.3)

    # 添加分数标签
    for i, (bar, score) in enumerate(zip(bars2, restraining_scores)):
        ax2.text(score + 0.1, bar.get_y() + bar.get_height()/2, str(score),
                va='center', fontsize=10, fontweight='bold')

    # 图3: 力场平衡图
    # 绘制驱动力和阻力的对比
    ax3.bar(['驱动力', '阻力'], [total_driving, total_restraining],
            color=['#2E8B57', '#DC143C'], edgecolor='black', linewidth=2, width=0.6)
    ax3.set_ylabel('总分', fontsize=12, fontweight='bold')
    ax3.set_title('力场平衡分析', fontsize=13, fontweight='bold')
    ax3.set_ylim(0, max(total_driving, total_restraining) * 1.2)
    ax3.grid(True, axis='y', linestyle='--', alpha=0.3)

    # 添加净力量指示
    if net_force > 0:
        status = "驱动力占优"
        status_color = "#2E8B57"
    elif net_force < 0:
        status = "阻力占优"
        status_color = "#DC143C"
    else:
        status = "力场平衡"
        status_color = "#FFA500"

    ax3.text(0.5, max(total_driving, total_restraining) * 1.05,
             f'净力量: {net_force:+}\n{status}',
             ha='center', va='bottom', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor=status_color, alpha=0.3, edgecolor='black'))

    # 添加分数标签
    for i, (name, score) in enumerate([('驱动力', total_driving), ('阻力', total_restraining)]):
        ax3.text(i, score + max(total_driving, total_restraining) * 0.02, str(score),
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    # 总标题
    fig.suptitle('变革阻力力场分析 (Lewin Force Field Analysis)',
                 fontsize=16, fontweight='bold', y=0.98)

    # 添加策略建议
    if net_force > 2:
        strategy = "建议：驱动力较强，可以加速变革推进，同时关注阻力管理"
    elif net_force < -2:
        strategy = "建议：阻力较强，需优先解决关键阻力因素，增强驱动力"
    else:
        strategy = "建议：力场基本平衡，建议增强驱动力或减弱阻力以突破僵局"

    plt.figtext(0.5, 0.02, strategy, ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7, edgecolor='black'))

    # 调整布局
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])

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
        print("用法: python generate_force_field.py '<JSON数据>'")
        print("示例: python generate_force_field.py '{\"driving_forces\":[{\"name\":\"压力\",\"score\":8}],\"restraining_forces\":[{\"name\":\"抵触\",\"score\":6}]}'")
        return 1

    input_str = sys.argv[1]

    try:
        # 解析输入
        data = parse_input(input_str)

        # 生成力场分析图
        result_path = generate_force_field(data)

        print(f"力场分析图已生成: {result_path}")
        return 0

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
