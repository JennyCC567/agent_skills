#!/usr/bin/env python3
"""
麦肯锡7S模型雷达图生成器
基于7S模型的6个维度评分生成组织健康度雷达图
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
        "strategy": 7,
        "structure": 5,
        "systems": 6,
        "shared_values": 8,
        "skills": 4,
        "staff": 6,
        "style": 7,
        "output_path": "./radar_chart.png"
    }

    验证规则:
    - 所有维度评分必须在1-10之间
    - 必须包含全部7个维度
    - output_path必须以.png或.jpg结尾
    """
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"输入格式错误：必须是有效的JSON字符串。错误信息：{e}")

    # 必需字段检查
    required_fields = [
        'strategy', 'structure', 'systems', 'shared_values',
        'skills', 'staff', 'style', 'output_path'
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")

    # 验证维度评分
    dimensions = ['strategy', 'structure', 'systems', 'shared_values', 'skills', 'staff', 'style']
    for dim in dimensions:
        score = data[dim]
        if not isinstance(score, (int, float)):
            raise ValueError(f"{dim} 必须是数字")
        if score < 1 or score > 10:
            raise ValueError(f"{dim} 评分必须在1-10之间，当前值：{score}")

    # 验证output_path
    output_path = data['output_path']
    if not output_path.endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError("output_path 必须以 .png、.jpg 或 .jpeg 结尾")

    return data


def generate_radar_chart(data):
    """
    生成7S模型雷达图

    参数:
        data: 包含7个维度评分和输出路径的字典

    返回:
        str: 生成的图片路径
    """
    # 维度标签和中文映射
    labels = ['Strategy\n战略', 'Structure\n结构', 'Systems\n制度',
              'Shared Values\n共同价值观', 'Skills\n技能', 'Staff\n人员', 'Style\n风格']

    # 提取评分数据
    scores = [
        data['strategy'],
        data['structure'],
        data['systems'],
        data['shared_values'],
        data['skills'],
        data['staff'],
        data['style']
    ]

    # 计算角度（7个维度）
    num_vars = len(labels)
    angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
    angles += angles[:1]  # 闭合图形

    # 闭合数据
    scores += scores[:1]

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    # 绘制评分数据
    ax.plot(angles, scores, 'o-', linewidth=2, color='#FF6B6B', label='当前评分')
    ax.fill(angles, scores, alpha=0.25, color='#FF6B6B')

    # 绘制参考线（满分10分）
    ax.plot(angles, [10] * len(angles), '--', linewidth=1, color='#CCCCCC', alpha=0.5, label='满分')

    # 添加5分基准线
    ax.plot(angles, [5] * len(angles), ':', linewidth=1, color='#999999', alpha=0.5, label='基准线')

    # 设置刻度和标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)

    # 添加标题
    ax.set_title('麦肯锡7S模型 - 组织健康度雷达图',
                 size=16, fontweight='bold', pad=20)

    # 添加图例
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    # 添加总分
    total_score = sum(scores[:-1])
    avg_score = total_score / 7
    plt.figtext(0.5, 0.02,
                f'总分: {total_score:.0f} / 70   平均分: {avg_score:.1f} / 10',
                ha='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 调整布局
    plt.tight_layout(rect=[0, 0.05, 0.85, 1])

    # 确保输出目录存在
    output_path = Path(data['output_path'])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存图片
    plt.savefig(str(output_path), dpi=300, bbox_inches='tight')
    plt.close()

    return str(output_path)


def main():
    """
    主函数：从命令行参数或标准输入读取数据，生成雷达图
    """
    # 检查参数
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
    else:
        # 从标准输入读取
        input_str = sys.stdin.read()

    # 解析输入
    data = parse_input(input_str)

    # 生成雷达图
    output_path = generate_radar_chart(data)

    # 输出结果
    print(f"雷达图已生成: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
