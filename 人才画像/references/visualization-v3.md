# v3.0高级可视化规范

## 一、桑基图（Sankey Diagram）

### 1.1 定义与用途
桑基图用于可视化人才流动路径，展示人才从源组织/岗位到目标组织/岗位的流动情况。

### 1.2 技术实现
使用分组条形图（Horizontal Bar Chart）模拟桑基图效果：

```python
def generate_sankey_chart(flow_data: Dict[str, Any]) -> str:
    """生成分组条形图模拟桑基图"""
    # 源节点数据
    source_data = flow_data['sources']
    # 目标节点数据
    target_data = flow_data['targets']
    # 流量数据
    flow_data_list = flow_data['flows']
    
    # 创建水平条形图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), 
                                     gridspec_kw={'width_ratios': [1, 1]})
    
    # 左图：源节点（流出）
    y_source = range(len(source_data))
    colors_source = plt.cm.Blues(np.linspace(0.3, 0.9, len(source_data)))
    ax1.barh(y_source, [s['value'] for s in source_data], 
             color=colors_source, height=0.6)
    ax1.set_yticks(y_source)
    ax1.set_yticklabels([s['name'] for s in source_data])
    ax1.set_xlabel('流出人数')
    ax1.set_title('人才流出来源分布')
    
    # 右图：目标节点（流入）
    y_target = range(len(target_data))
    colors_target = plt.cm.Greens(np.linspace(0.3, 0.9, len(target_data)))
    ax2.barh(y_target, [t['value'] for t in target_data], 
             color=colors_target, height=0.6)
    ax2.set_yticks(y_target)
    ax2.set_yticklabels([t['name'] for t in target_data])
    ax2.set_xlabel('流入人数')
    ax2.set_title('人才流入目标分布')
    
    # 添加连接线表示流量
    for i, (s, t, f) in enumerate(zip(source_data, target_data, flow_data_list)):
        # 绘制连接箭头
        ax1.annotate('', xy=(f['flow']*0.4, i), 
                    xytext=(s['value'], i),
                    arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))
    
    plt.tight_layout()
    return fig_to_base64(fig)
```

### 1.3 数据要求
```json
{
  "flow_type": "公司间流动",
  "sources": [
    {"name": "竞争对手A", "value": 150},
    {"name": "竞争对手B", "value": 120},
    {"name": "初创公司", "value": 80}
  ],
  "targets": [
    {"name": "目标企业", "value": 200},
    {"name": "其他企业", "value": 150}
  ],
  "flows": [
    {"from": "竞争对手A", "to": "目标企业", "flow": 80},
    {"from": "竞争对手B", "to": "目标企业", "flow": 70},
    {"from": "初创公司", "to": "目标企业", "flow": 50}
  ],
  "summary": {
    "total_outflow": 350,
    "total_inflow": 350,
    "net_flow": 0,
    "flow_rate": "12.5%"
  }
}
```

### 1.4 展示要求
- **必须展示**：流向占比、同比环比数据
- **必须标注**：关键流动路径（流量>20%）
- **必须说明**：流动原因分析

---

## 二、人才梯队九宫格（9-Box Grid）

### 2.1 定义与用途
九宫格矩阵用于人才盘点，展示人才的绩效与潜力分布。

### 2.2 技术实现
使用matplotlib创建3x3矩阵：

```python
def generate_nine_box_grid(talent_data: Dict[str, Any]) -> str:
    """生成人才梯队九宫格"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 定义9个格子
    boxes = [
        # 第一行（高潜力低绩效）
        {"x": 0, "y": 2, "label": "待发展", "color": "#FFB74D", "talents": []},
        {"x": 1, "y": 2, "label": "新星", "color": "#4CAF50", "talents": []},
        {"x": 2, "y": 2, "label": "核心人才", "color": "#2196F3", "talents": []},
        # 第二行
        {"x": 0, "y": 1, "label": "评估中", "color": "#FFC107", "talents": []},
        {"x": 1, "y": 1, "label": "稳定贡献", "color": "#8BC34A", "talents": []},
        {"x": 2, "y": 1, "label": "高绩效", "color": "#03A9F4", "talents": []},
        # 第三行（低潜力）
        {"x": 0, "y": 0, "label": "调离", "color": "#F44336", "talents": []},
        {"x": 1, "y": 0, "label": "维持", "color": "#FF9800", "talents": []},
        {"x": 2, "y": 0, "label": "中坚力量", "color": "#9C27B0", "talents": []}
    ]
    
    # 绘制格子
    for box in boxes:
        rect = plt.Rectangle((box["x"], box["y"]), 1, 1, 
                             facecolor=box["color"], alpha=0.3, 
                             edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(box["x"] + 0.5, box["y"] + 0.7, box["label"], 
                ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(box["x"] + 0.5, box["y"] + 0.3, f"{len(box['talents'])}人", 
                ha='center', va='center', fontsize=10)
    
    # 设置坐标轴
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(['低绩效', '中绩效', '高绩效'], fontsize=10)
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(['低潜力', '中潜力', '高潜力'], fontsize=10)
    ax.set_xlabel('绩效维度', fontsize=12, fontweight='bold')
    ax.set_ylabel('潜力维度', fontsize=12, fontweight='bold')
    ax.set_title('人才梯队九宫格矩阵', fontsize=16, fontweight='bold', pad=20)
    
    # 添加图例
    legend_elements = [
        plt.Rectangle((0,0), 1, 1, facecolor='#4CAF50', alpha=0.3, label='战略接班人'),
        plt.Rectangle((0,0), 1, 1, facecolor='#2196F3', alpha=0.3, label='核心骨干'),
        plt.Rectangle((0,0), 1, 1, facecolor='#9C27B0', alpha=0.3, label='中坚力量')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    plt.tight_layout()
    return fig_to_base64(fig)
```

### 2.3 数据要求
```json
{
  "matrix": {
    "dimensions": {
      "x": "绩效评分 (1-5)",
      "y": "潜力评分 (1-5)"
    },
    "boxes": {
      "top_right": {"label": "战略接班人", "criteria": "绩效≥4, 潜力≥4", "count": 15},
      "middle_center": {"label": "核心骨干", "criteria": "绩效3-4, 潜力3-4", "count": 45},
      "bottom_left": {"label": "待发展", "criteria": "绩效<3, 潜力<3", "count": 8}
    },
    "summary": {
      "total_talents": 100,
      "high_potential": 25,
      "key_succession_candidates": 8
    }
  }
}
```

---

## 三、热力图（Heatmap）

### 3.1 定义与用途
热力图用于展示地域人才分布密度，直观显示不同地区的人才集中程度。

### 3.2 技术实现
使用matplotlib imshow实现：

```python
def generate_heatmap(data: Dict[str, Any]) -> str:
    """生成地域人才分布热力图"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 准备数据矩阵（省份x城市等级）
    regions = data['regions']  # ['北京', '上海', '深圳', '杭州', '成都', '武汉', ...]
    levels = ['一线城市', '新一线城市', '二线城市', '三线城市']
    
    # 创建数据矩阵
    matrix = np.array(data['matrix'])
    
    # 绘制热力图
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    # 设置坐标轴
    ax.set_xticks(np.arange(len(levels)))
    ax.set_yticks(np.arange(len(regions)))
    ax.set_xticklabels(levels)
    ax.set_yticklabels(regions)
    
    # 添加数值标签
    for i in range(len(regions)):
        for j in range(len(levels)):
            text = ax.text(j, i, f'{matrix[i, j]}%',
                          ha="center", va="center", color="black", fontsize=10)
    
    # 添加颜色条
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('人才密度 (%)', rotation=-90, va="bottom", fontsize=10)
    
    ax.set_title('地域人才分布热力图', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('城市等级', fontsize=12, fontweight='bold')
    ax.set_ylabel('地理区域', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    return fig_to_base64(fig)
```

### 3.3 数据要求
```json
{
  "regions": ["华北地区", "华东地区", "华南地区", "华中地区", "西南地区", "西北地区", "东北地区"],
  "levels": ["一线城市", "新一线城市", "二线城市", "三线城市"],
  "matrix": [
    [85, 92, 78, 65],
    [88, 95, 82, 70],
    [90, 88, 75, 68],
    [72, 80, 70, 55],
    [65, 75, 68, 50],
    [55, 62, 58, 45],
    [50, 58, 52, 40]
  ],
  "summary": {
    "total_talent": 50000,
    "top_region": "华东地区",
    "top_level": "一线城市",
    "density_avg": 68.5
  }
}
```

---

## 四、雷达图（Radar Chart）

### 4.1 定义与用途
雷达图用于多维度能力分析，直观展示人才的能力结构。

### 4.2 技术实现
使用matplotlib极坐标投影：

```python
def generate_radar_chart(data: Dict[str, Any]) -> str:
    """生成多维度能力雷达图"""
    # 能力维度
    categories = data['categories']
    # 能力评分
    values = data['values']
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values = values + [values[0]]  # 闭合图形
    angles = angles + [angles[0]]
    
    # 创建极坐标图
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # 绘制雷达图
    ax.plot(angles, values, 'o-', linewidth=2, color='#1F4E79')
    ax.fill(angles, values, alpha=0.25, color='#4A90D9')
    
    # 设置维度标签
    ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=11)
    
    # 设置径向范围
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9)
    
    ax.set_title('能力素质雷达图', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    return fig_to_base64(fig)
```

### 4.3 数据要求
```json
{
  "categories": ["技术能力", "业务理解", "沟通协作", "创新能力", "领导力", "学习能力"],
  "values": [85, 78, 82, 75, 68, 90],
  "benchmark": [75, 70, 75, 70, 65, 80],
  "summary": {
    "overall_score": 79.7,
    "strengths": ["学习能力", "技术能力"],
    "development_areas": ["领导力"]
  }
}
```

---

## 五、流动趋势分析（增强版）

### 5.1 必须包含的数据

#### 同比数据
```json
{
  "year_over_year": {
    "inflow_rate": "+15.3%",
    "outflow_rate": "-8.2%",
    "net_flow": "+23.5%",
    "turnover_rate": "12.5% → 9.8%"
  }
}
```

#### 环比数据
```json
{
  "quarter_over_quarter": {
    "q1_inflow": 120,
    "q2_inflow": 135,
    "q3_inflow": 142,
    "q4_inflow": 158,
    "trend": "上升趋势 +31.7%"
  }
}
```

#### 流向占比
```json
{
  "flow_distribution": {
    "intra_industry": 45.5,
    "inter_industry": 32.3,
    "inter_region": 15.2,
    "retirees": 7.0
  },
  "流向说明": {
    "intra_industry": "同行业竞争对手间流动",
    "inter_industry": "跨行业流动（如互联网→金融）",
    "inter_region": "跨地区流动（如北京→上海）",
    "retirees": "退休/离职"
  }
}
```

### 5.2 流动路径数据
```json
{
  "flow_paths": [
    {"from": "字节跳动", "to": "本公司", "count": 45, "percentage": 22.5, "avg_level": "P6"},
    {"from": "腾讯", "to": "本公司", "count": 38, "percentage": 19.0, "avg_level": "P7"},
    {"from": "阿里巴巴", "to": "本公司", "count": 32, "percentage": 16.0, "avg_level": "P6"},
    {"from": "百度", "to": "本公司", "count": 25, "percentage": 12.5, "avg_level": "P5"},
    {"from": "其他", "to": "本公司", "count": 60, "percentage": 30.0, "avg_level": "P5"}
  ],
  "关键洞察": [
    "字节跳动流入人才最多，占比22.5%",
    "腾讯流入人才平均职级最高（P7）",
    "头部互联网公司流入占比超过50%"
  ]
}
```

---

## 六、候选人360°画像（增强版）

### 6.1 项目经历时间轴
```json
{
  "project_timeline": [
    {
      "period": "2023.03 - 2024.02",
      "project": "AI平台重构项目",
      "role": "技术负责人",
      "achievement": "平台性能提升200%，支撑日活1亿用户",
      "tech_stack": ["Python", "Kubernetes", "TensorFlow"]
    },
    {
      "period": "2021.06 - 2023.02",
      "project": "智能推荐系统",
      "role": "核心开发",
      "achievement": "推荐准确率提升35%，带来收入增长2亿",
      "tech_stack": ["Spark", "Flink", "Redis"]
    }
  ]
}
```

### 6.2 专利与论文
```json
{
  "patents": [
    {
      "name": "一种基于深度学习的推荐方法",
      "status": "已授权",
      "date": "2023-05",
      "patent_no": "CN202310123456.7"
    }
  ],
  "papers": [
    {
      "title": "Deep Learning for Recommender Systems",
      "conference": "KDD 2022",
      "date": "2022-08",
      "citation": 128
    }
  ]
}
```

### 6.3 软技能量化
```json
{
  "soft_skills": {
    "沟通能力": {
      "score": 85,
      "evidence": ["跨部门项目协调", "技术方案汇报"]
    },
    "领导力": {
      "score": 72,
      "evidence": ["团队规模10人", "年度优秀团队"]
    },
    "创新能力": {
      "score": 88,
      "evidence": ["专利2项", "技术创新奖"]
    }
  }
}
```

### 6.4 职业成长轨迹
```json
{
  "career_progression": [
    {"year": 2018, "company": "A公司", "title": "初级工程师", "salary": "15K", "level": "L3"},
    {"year": 2020, "company": "A公司", "title": "高级工程师", "salary": "28K", "level": "L5"},
    {"year": 2022, "company": "B公司", "title": "技术专家", "salary": "45K", "level": "L7"},
    {"year": 2024, "company": "C公司", "title": "技术总监", "salary": "70K", "level": "L8"}
  ],
  "growth_metrics": {
    "salary_growth_rate": "46.7% (年化)",
    "level_up_speed": "1级/2年",
    "company_stay_avg": "2.5年"
  }
}
```

---

## 七、薪资Benchmark精细化（增强版）

### 7.1 分位数数据
```json
{
  "salary_percentiles": {
    "P25": 25000,
    "P50": 35000,
    "P75": 50000,
    "P90": 72000,
    "P95": 90000
  },
  "by_experience": {
    "1-3年": {"P25": 15000, "P50": 20000, "P75": 30000, "P90": 40000},
    "3-5年": {"P25": 25000, "P50": 35000, "P75": 50000, "P90": 65000},
    "5-8年": {"P25": 40000, "P50": 55000, "P75": 75000, "P90": 95000},
    "8年以上": {"P25": 60000, "P50": 80000, "P75": 110000, "P90": 150000}
  },
  "by_education": {
    "本科": {"P25": 18000, "P50": 28000, "P75": 45000, "P90": 65000},
    "硕士": {"P25": 25000, "P50": 40000, "P75": 60000, "P90": 85000},
    "博士": {"P25": 40000, "P50": 60000, "P75": 90000, "P90": 130000}
  }
}
```

### 7.2 年度涨幅数据
```json
{
  "salary_growth": {
    "market_avg": "+8.5%",
    "high_performer": "+15.2%",
    "promotion_avg": "+12.0%",
    "counter_offer_avg": "+18.5%"
  },
  "by_industry": {
    "互联网": "+12.3%",
    "金融": "+8.7%",
    "咨询": "+7.2%",
    "制造": "+6.5%"
  }
}
```

---

## 八、实现优先级

| 图表类型 | 优先级 | 实现难度 | 说明 |
|---------|--------|---------|------|
| 雷达图 | P0 | 低 | 立即实现 |
| 热力图 | P0 | 低 | 立即实现 |
| 九宫格 | P0 | 中 | 立即实现 |
| 桑基图 | P1 | 中 | 分组条形图模拟 |
| 流动趋势 | P1 | 中 | 添加同比环比 |
| 360°画像 | P2 | 高 | 分阶段实现 |
| 薪资分位数 | P0 | 低 | 立即实现 |
