#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OD图表生成工具 - matplotlib base64 PNG
遵循红线规则V6.2：禁止JS图表库，统一使用matplotlib
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import base64
import io
import os

# 中文字体配置
def setup_chinese_font():
    """设置中文字体，支持跨平台"""
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # Linux
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        'C:\\Windows\\Fonts\\msyh.ttc',  # Windows
        'C:\\Windows\\Fonts\\simhei.ttf',  # Windows备选
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                fm.fontManager.addfont(font_path)
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans']
                plt.rcParams['axes.unicode_minus'] = False
                return font_name
            except Exception as e:
                continue
    
    # 默认回退
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return 'DejaVu Sans'

# 初始化字体
FONT_NAME = setup_chinese_font()

# 颜色方案 - 商务蓝
COLORS = {
    'primary': '#1F4E79',      # 深蓝
    'secondary': '#4A90D9',    # 浅蓝
    'accent': '#2CA58D',       # 青绿
    'warning': '#E74C3C',      # 红色
    'success': '#27AE60',      # 绿色
    'gray': '#95A5A6',         # 灰色
    'light': '#ECF0F1',        # 浅灰
}

def fig_to_base64(fig, dpi=150):
    """matplotlib图表转换为base64字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def generate_radar_chart(dimensions, values, title='雷达图', max_value=10, figsize=(8, 6)):
    """
    生成雷达图
    dimensions: 维度名称列表
    values: 数值列表
    """
    N = len(dimensions)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values_plot = list(values) + [values[0]]
    
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    
    # 绘制雷达图
    ax.plot(angles, values_plot, 'o-', linewidth=2, color=COLORS['primary'])
    ax.fill(angles, values_plot, alpha=0.25, color=COLORS['secondary'])
    
    # 设置标签
    ax.set_thetagrids(np.degrees(angles[:-1]), dimensions, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=12)
    ax.set_ylim(0, max_value)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=10)
    ax.set_title(title, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=16, pad=20)
    
    # 网格样式
    ax.grid(color=COLORS['light'], linewidth=0.5)
    ax.spines['polar'].set_color(COLORS['light'])
    
    return fig_to_base64(fig)

def generate_bar_chart(categories, values, title='柱状图', xlabel='', ylabel='', figsize=(10, 6)):
    """
    生成柱状图
    categories: 类别列表
    values: 数值列表
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    bars = ax.bar(categories, values, color=COLORS['primary'], width=0.6)
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_title(title, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=16, pad=15)
    ax.set_xlabel(xlabel, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=12)
    ax.set_ylabel(ylabel, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=12)
    
    # 设置x轴标签
    ax.set_xticklabels(categories, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=10)
    
    # 样式
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['light'])
    ax.spines['bottom'].set_color(COLORS['light'])
    ax.tick_params(colors=COLORS['gray'])
    
    return fig_to_base64(fig)

def generate_line_chart(x_data, y_data, title='折线图', xlabel='', ylabel='', figsize=(10, 6)):
    """
    生成折线图
    x_data: X轴数据
    y_data: Y轴数据（可以是列表或字典用于多线）
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if isinstance(y_data, dict):
        colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning']]
        for i, (label, values) in enumerate(y_data.items()):
            color = colors[i % len(colors)]
            ax.plot(x_data, values, 'o-', linewidth=2, color=color, label=label)
        ax.legend(prop=fm.FontProperties(family=FONT_NAME), fontsize=10)
    else:
        ax.plot(x_data, y_data, 'o-', linewidth=2, color=COLORS['primary'])
    
    ax.set_title(title, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=16, pad=15)
    ax.set_xlabel(xlabel, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=12)
    ax.set_ylabel(ylabel, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=12)
    
    # 样式
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['light'])
    ax.spines['bottom'].set_color(COLORS['light'])
    ax.tick_params(colors=COLORS['gray'])
    ax.grid(axis='y', color=COLORS['light'], linewidth=0.5, alpha=0.5)
    
    return fig_to_base64(fig)

def generate_pie_chart(labels, values, title='饼图', figsize=(8, 8)):
    """
    生成饼图
    labels: 标签列表
    values: 数值列表
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
              COLORS['warning'], COLORS['success'], COLORS['gray']]
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                       colors=colors[:len(labels)],
                                       startangle=90)
    
    # 设置字体
    for text in texts:
        text.set_fontproperties(fm.FontProperties(family=FONT_NAME))
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
    ax.set_title(title, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=16, pad=20)
    
    return fig_to_base64(fig)

def generate_gauge_chart(value, max_value=100, title='仪表盘', figsize=(6, 4)):
    """
    生成仪表盘图
    value: 当前值
    max_value: 最大值
    """
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    
    # 设置角度范围（半圆）
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    
    # 绘制背景弧
    theta_bg = np.linspace(0, np.pi, 100)
    r_bg = np.ones_like(theta_bg)
    ax.plot(theta_bg, r_bg, color=COLORS['light'], linewidth=20, solid_capstyle='round')
    
    # 绘制值弧
    value_angle = (value / max_value) * np.pi
    theta_val = np.linspace(0, value_angle, 100)
    r_val = np.ones_like(theta_val)
    
    # 根据值选择颜色
    if value / max_value < 0.4:
        color = COLORS['warning']
    elif value / max_value < 0.7:
        color = COLORS['secondary']
    else:
        color = COLORS['success']
    
    ax.plot(theta_val, r_val, color=color, linewidth=20, solid_capstyle='round')
    
    # 添加数值文本
    ax.text(np.pi/2, 0.5, f'{value:.0f}', ha='center', va='center', 
            fontsize=36, fontweight='bold', color=color)
    ax.text(np.pi/2, 0.3, f'/ {max_value}', ha='center', va='center', 
            fontsize=14, color=COLORS['gray'])
    
    # 隐藏极坐标元素
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['polar'].set_visible(False)
    
    ax.set_title(title, fontproperties=fm.FontProperties(family=FONT_NAME), fontsize=14, pad=10)
    
    return fig_to_base64(fig)

if __name__ == '__main__':
    # 测试图表生成
    print("测试雷达图...")
    radar_b64 = generate_radar_chart(
        ['战略', '结构', '制度', '价值观', '技能', '领导力', '人才'],
        [8.5, 7.2, 6.8, 8.0, 7.5, 7.8, 7.0],
        title='组织健康度雷达图'
    )
    print(f"雷达图base64长度: {len(radar_b64)}")
    
    print("测试柱状图...")
    bar_b64 = generate_bar_chart(
        ['Q1', 'Q2', 'Q3', 'Q4'],
        [85, 92, 78, 95],
        title='季度业绩',
        xlabel='季度',
        ylabel='得分'
    )
    print(f"柱状图base64长度: {len(bar_b64)}")
    
    print("测试完成！")
