#!/usr/bin/env python3
"""
图表生成工具 - 使用matplotlib生成base64 PNG图片
符合技能交付物生成红线规则V6.2
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import base64
import io
import numpy as np

# 必须先注册中文字体
try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False
except:
    # 如果找不到中文字体，使用系统默认字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

# 配色方案（深蓝#1F4E79 / 浅蓝#4A90D9 / 青绿#2CA58D）
COLORS = {
    'primary': '#1F4E79',
    'secondary': '#4A90D9',
    'accent': '#2CA58D',
    'success': '#2CA58D',
    'warning': '#E9B948',
    'danger': '#E94B35',
    'neutral': '#909399'
}

def fig_to_base64(fig):
    """
    matplotlib图表 --> base64字符串
    符合规则：DPI≥150，PNG格式，白色背景
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def generate_matching_score_chart(score, dimensions, scores):
    """
    生成匹配度评分柱状图
    score: 总分
    dimensions: 维度名称列表
    scores: 对应分数列表
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制柱状图
    bars = ax.bar(dimensions, scores, color=[COLORS['primary'] if s >= 70 
                                               else COLORS['accent'] if s >= 50 
                                               else COLORS['danger'] 
                                               for s in scores])
    
    # 在柱子上标注分数
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}分',
                ha='center', va='bottom', fontsize=11)
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('得分', fontsize=12)
    ax.set_title(f'整体匹配度：{int(score)}分', fontsize=14, pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    return fig_to_base64(fig)

def generate_radar_chart(dimensions, scores, title='能力评估雷达图'):
    """
    生成雷达图
    dimensions: 维度名称列表
    scores: 对应分数列表
    title: 图表标题
    """
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # 设置角度
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    scores += scores[:1]  # 闭合
    angles += angles[:1]
    
    # 绘制雷达图
    ax.fill(angles, scores, color=COLORS['secondary'], alpha=0.4)
    ax.plot(angles, scores, color=COLORS['primary'], linewidth=2)
    
    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8)
    ax.set_title(title, fontsize=14, pad=20)
    ax.grid(True)
    
    return fig_to_base64(fig)

def generate_funnel_chart(stages, values, title='求职进度漏斗'):
    """
    生成漏斗图
    stages: 阶段名称列表
    values: 对应数值列表
    title: 图表标题
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 计算宽度
    max_value = max(values)
    widths = [v / max_value for v in values]
    
    # 绘制漏斗
    y_pos = np.arange(len(stages))
    bars = ax.barh(y_pos, widths, color=[COLORS['primary'], COLORS['secondary'], 
                                          COLORS['accent'], COLORS['success']])
    
    # 添加数值标注
    for i, (bar, value, stage) in enumerate(zip(bars, values, stages)):
        width = bar.get_width()
        ax.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                f'{stage}: {value}',
                va='center', fontsize=11)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=11)
    ax.set_xlim(0, 1.1)
    ax.set_xlabel('相对规模', fontsize=12)
    ax.set_title(title, fontsize=14, pad=20)
    ax.invert_yaxis()  # 倒序显示
    ax.grid(axis='x', alpha=0.3)
    
    return fig_to_base64(fig)

def generate_pie_chart(labels, values, title='分布饼图'):
    """
    生成饼图
    labels: 标签列表
    values: 对应数值列表
    title: 图表标题
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
              COLORS['success'], COLORS['warning']]
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                        colors=colors[:len(labels)], startangle=90)
    ax.set_title(title, fontsize=14, pad=20)
    
    # 设置字体
    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_fontsize(10)
    
    return fig_to_base64(fig)

def generate_trend_chart(dates, values, title='趋势图'):
    """
    生成趋势图
    dates: 日期列表
    values: 对应数值列表
    title: 图表标题
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(dates, values, color=COLORS['primary'], linewidth=2, marker='o', 
            markersize=6)
    ax.fill_between(dates, values, color=COLORS['secondary'], alpha=0.3)
    
    ax.set_xlabel('时间', fontsize=12)
    ax.set_ylabel('数值', fontsize=12)
    ax.set_title(title, fontsize=14, pad=20)
    ax.grid(True, alpha=0.3)
    
    return fig_to_base64(fig)
