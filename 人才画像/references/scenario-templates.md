# 场景模板文档

## 版本信息
- **版本**：v2.0
- **更新日期**：2026-05-28
- **状态**：正式发布

---

## 场景一：校园招聘（技术类岗位）

### 1.1 场景描述
针对应届本科/硕士毕业生，招聘AI算法工程师、数据分析师等岗位。

### 1.2 配置模板

```yaml
# 场景：校园招聘 - 技术类岗位

# 匹配目标
job_requirements:
  position: "AI算法工程师"
  department: "技术研发部"
  location: ["北京", "上海", "深圳"]
  remote_accepted: false

# 硬约束配置
hard_constraints:
  enabled: true
  rules:
    - field: "education"
      operator: "in"
      value: ["本科", "硕士"]
    - field: "total_experience"
      operator: "<="
      value: 2  # 应届或1-2年经验
    - field: "hard_skills"
      operator: "contains_any"
      value: ["Python", "机器学习", "深度学习"]

# 匹配权重
soft_constraints:
  weights:
    skill_match: 0.40      # 技能匹配 40%
    education_match: 0.25  # 学历匹配 25%
    experience_match: 0.15  # 经验匹配 15%
    location_match: 0.10   # 地域匹配 10%
    potential_score: 0.10  # 潜力评分 10%

# 潜力评分权重（针对应届生）
potential_scoring:
  factors:
    learning_ability: 0.35   # 学习能力 35%（看重学历和证书）
    growth_potential: 0.30   # 成长潜力 30%（看重专业对口）
    innovation_score: 0.20  # 创新评分 20%（看重项目经验）
    career_stability: 0.15  # 职业稳定性 15%

# 学历匹配特殊规则
education_rules:
  prefer_phd: false  # 不偏好博士（成本高）
  prefer_985_211: true  # 偏好985/211院校

# 输出格式
report_format:
  types: ["html", "excel"]
  include_charts: true
  chart_types: ["bar", "pie", "radar"]
```

### 1.3 预期候选人画像

```yaml
candidate_profile:
  education: "硕士"
  school: "清华大学"
  major: "计算机科学与技术"
  total_experience: 0  # 应届
  hard_skills:
    - Python: 高级
    - 机器学习: 中级
    - 深度学习: 中级
    - TensorFlow: 初级
  soft_skills:
    - 沟通能力
    - 学习能力
    - 团队协作
  certifications:
    - "英语CET-6"
    - "阿里云机器学习认证"
  potential_score: 85  # 高潜力
```

### 1.4 输出报告结构

```
人才Mapping报告 - 校园招聘
├── 执行摘要
│   └── 候选人概况：高潜力应届生23人，符合硬约束15人
├── 人才分布分析
│   ├── 学历分布（硕士占比78%）
│   ├── 院校分布（985/211占比65%）
│   └── 地域分布（北京、上海、深圳）
├── 技能图谱
│   ├── 硬技能分布
│   ├── 软技能分布
│   └── 技能标签云
├── 潜力评估
│   ├── 高潜力候选人（80-100分）
│   ├── 中等潜力（60-79分）
│   └── 潜力待提升（<60分）
└── 推荐候选人
    └── Top 10 推荐名单
```

---

## 场景二：社会招聘（高级管理岗）

### 2.1 场景描述
招聘AI研发总监、首席架构师等高级技术管理岗位。

### 2.2 配置模板

```yaml
# 场景：社会招聘 - 高级管理岗

# 匹配目标
job_requirements:
  position: "AI研发总监"
  department: "研发管理层"
  location: ["北京", "上海"]
  remote_accepted: true

# 硬约束配置
hard_constraints:
  enabled: true
  rules:
    - field: "education"
      operator: "in"
      value: ["硕士", "博士"]
    - field: "total_experience"
      operator: ">="
      value: 8  # 至少8年经验
    - field: "current_title"
      operator: "contains_any"
      value: ["总监", "VP", "首席", "负责人", "Head"]

# 匹配权重
soft_constraints:
  weights:
    skill_match: 0.25      # 技能匹配 25%
    education_match: 0.20  # 学历匹配 20%
    experience_match: 0.30  # 经验匹配 30%（加重）
    location_match: 0.10   # 地域匹配 10%
    potential_score: 0.15  # 潜力评分 15%

# 经验匹配特殊规则
experience_rules:
  leadership_exp_required: true  # 需要管理经验
  min_team_size: 10  # 至少管理10人团队
  industry_exp_bonus: true  # 同行经验加分

# 潜力评分权重（针对高管）
potential_scoring:
  factors:
    learning_ability: 0.20   # 学习能力 20%
    growth_potential: 0.25   # 成长潜力 25%
    innovation_score: 0.35  # 创新评分 35%（加重）
    career_stability: 0.20  # 职业稳定性 20%

# 输出格式
report_format:
  types: ["html", "excel"]
  include_charts: true
  chart_types: ["bar", "pie", "radar", "bubble"]
  executive_summary: true  # 包含高管摘要
```

### 2.3 预期候选人画像

```yaml
candidate_profile:
  education: "博士"
  school: "中国科学院"
  major: "人工智能"
  total_experience: 12
  current_title: "AI研发总监"
  current_company: "某头部科技公司"
  team_size: 50  # 管理50人团队
  hard_skills:
    - Python: 专家
    - 深度学习: 专家
    - 架构设计: 高级
    - 团队管理: 高级
  achievements:
    - "带领团队完成3个AI项目落地"
    - "发表顶会论文5篇"
    - "申请专利8项"
  potential_score: 92  # 高潜力高管
```

---

## 场景三：跨界招聘（从传统行业转向AI）

### 3.1 场景描述
招聘具有传统行业经验但愿意转型AI的人才，如从金融、医疗、制造等行业。

### 3.2 配置模板

```yaml
# 场景：跨界招聘 - 传统行业转型AI

# 匹配目标
job_requirements:
  position: "AI产品经理"
  department: "产品部"
  location: ["北京", "杭州"]
  remote_accepted: false
  industry_background: ["金融", "医疗", "制造", "零售"]  # 优先行业背景

# 硬约束配置
hard_constraints:
  enabled: true
  rules:
    - field: "education"
      operator: "in"
      value: ["本科", "硕士", "博士"]
    - field: "total_experience"
      operator: ">="
      value: 3  # 至少3年行业经验
    - field: "hard_skills"
      operator: "contains_any"
      value: ["Python", "数据分析", "机器学习"]

# 跨界加分配置
cross_industry_bonus:
  enabled: true
  bonus_score: 15  # 跨界候选人额外加15分
  industries:
    - "金融科技"
    - "医疗健康"
    - "智能制造"
    - "新零售"

# 匹配权重
soft_constraints:
  weights:
    skill_match: 0.30      # 技能匹配 30%
    education_match: 0.15  # 学历匹配 15%
    experience_match: 0.20  # 经验匹配 20%
    location_match: 0.10   # 地域匹配 10%
    potential_score: 0.25  # 潜力评分 25%（加重）

# 潜力评分权重
potential_scoring:
  factors:
    learning_ability: 0.30   # 学习能力 30%
    growth_potential: 0.30   # 成长潜力 30%
    innovation_score: 0.25  # 创新评分 25%
    career_stability: 0.15  # 职业稳定性 15%
```

### 3.3 预期候选人画像

```yaml
candidate_profile:
  education: "硕士"
  school: "复旦大学"
  major: "金融学"
  total_experience: 5
  current_title: "高级产品经理"
  current_company: "某金融科技公司"
  industry_background: "金融科技"  # 跨界优势
  hard_skills:
    - Python: 中级
    - 数据分析: 高级
    - 机器学习: 初级
    - 产品设计: 专家
  cross_industry_bonus: 15  # 跨界加分
  potential_score: 88  # 高潜力跨界人才
```

---

## 场景四：海外人才招聘

### 4.1 场景描述
招聘海外留学或工作背景的AI人才。

### 4.2 配置模板

```yaml
# 场景：海外人才招聘

# 匹配目标
job_requirements:
  position: "AI研究员"
  department: "研究院"
  location: ["北京", "上海", "远程"]
  remote_accepted: true
  overseas_required: true  # 必须有海外背景

# 硬约束配置
hard_constraints:
  enabled: true
  rules:
    - field: "education"
      operator: "in"
      value: ["硕士", "博士"]
    - field: "overseas_exp"
      operator: "=="
      value: true  # 必须有海外经历
    - field: "language_skills"
      operator: "contains"
      value: "英语"

# 海外人才加分
overseas_bonus:
  enabled: true
  bonus_rules:
    - condition: "overseas_university_top100"
      bonus: 20  # 世界Top100院校毕业 +20分
    - condition: "overseas_work_exp"
      bonus: 15  # 海外工作经历 +15分
    - condition: "international_patent"
      bonus: 10  # 国际专利 +10分

# 匹配权重
soft_constraints:
  weights:
    skill_match: 0.30      # 技能匹配 30%
    education_match: 0.25  # 学历匹配 25%（加重）
    experience_match: 0.20  # 经验匹配 20%
    location_match: 0.10   # 地域匹配 10%
    potential_score: 0.15  # 潜力评分 15%

# 输出格式
report_format:
  types: ["html", "excel"]
  include_charts: true
  chart_types: ["bar", "pie", "radar", "heatmap"]
  language: "中英双语"
```

---

## 场景五：批量招聘（校招+社招）

### 5.1 场景描述
同时进行校园招聘和社会招聘，批量筛选候选人。

### 5.2 配置模板

```yaml
# 场景：批量招聘

# 招聘批次配置
recruitment_batches:
  - name: "校招批次"
    priority: 1
    config:
      hard_constraints:
        rules:
          - field: "total_experience"
            operator: "<="
            value: 2
      target_count: 30
  
  - name: "社招批次"
    priority: 2
    config:
      hard_constraints:
        rules:
          - field: "total_experience"
            operator: ">="
            value: 3
      target_count: 20

# 批量处理配置
batch_processing:
  enabled: true
  batch_size: 100
  parallel_workers: 4
  cache_enabled: true

# 输出格式
report_format:
  types: ["html", "excel"]
  include_charts: true
  separate_reports: true  # 分开生成报告
```

---

## 场景六：竞品人才Mapping

### 6.1 场景描述
对竞品公司人才进行全面分析和Mapping。

### 6.2 配置模板

```yaml
# 场景：竞品人才Mapping

# 竞品公司列表
target_companies:
  - name: "竞品A公司"
    employees: 5000
    ai_team_size: 300
  - name: "竞品B公司"
    employees: 3000
    ai_team_size: 200
  - name: "竞品C公司"
    employees: 8000
    ai_team_size: 500

# 分析维度
analysis_dimensions:
  - "人才规模"
  - "人才结构"
  - "学历分布"
  - "薪资水平"
  - "核心人才流动"

# 匹配配置（宽松，用于分析）
matching_config:
  hard_constraints:
    enabled: false  # 关闭硬约束
  weights:
    skill_match: 0.35
    education_match: 0.20
    experience_match: 0.25
    location_match: 0.10
    potential_score: 0.10

# 输出格式
report_format:
  types: ["html", "excel"]
  include_charts: true
  chart_types: ["bar", "pie", "radar", "heatmap", "bubble"]
  comparison_mode: true  # 竞品对比模式
```

---

## 场景七：内部人才盘点

### 7.1 场景描述
对公司内部人才进行全面盘点，识别高潜力人才。

### 7.2 配置模板

```yaml
# 场景：内部人才盘点

# 盘点范围
scope:
  include_departments: ["*"]  # 全公司
  include_levels: ["P5", "P6", "P7", "P8"]  # 中高管理层级

# 盘点维度
dimensions:
  - name: "绩效表现"
    weight: 0.30
    data_source: "绩效系统"
  - name: "能力评估"
    weight: 0.30
    data_source: "360评估"
  - name: "发展潜力"
    weight: 0.20
    data_source: "潜力评估"
  - name: "离职风险"
    weight: 0.20
    data_source: "敬业度调查"

# 九宫格配置
talent_grid:
  dimensions:
    x: "绩效表现"  # X轴：绩效
    y: "发展潜力"  # Y轴：潜力
  zones:
    - name: "明星人才"
      x_range: [80, 100]
      y_range: [80, 100]
      action: "重点培养，赋予重要项目"
    - name: "高绩效稳定人才"
      x_range: [80, 100]
      y_range: [60, 80]
      action: "保持激励，防止人才流失"
    - name: "高潜力人才"
      x_range: [60, 80]
      y_range: [80, 100]
      action: "加强绩效辅导"
    - name: "待提升人才"
      x_range: [60, 80]
      y_range: [60, 80]
      action: "绩效改进计划"
    - name: "问题人才"
      x_range: [0, 60]
      y_range: [0, 60]
      action: "绩效警告或调岗"

# 输出格式
report_format:
  types: ["html", "excel"]
  include_charts: true
  chart_types: ["bubble", "pie", "bar"]  # 九宫格用气泡图
  include_talent_grid: true  # 人才九宫格
```

---

## 附录：配置快速参考

### A.1 权重配置速查表

| 场景 | 技能 | 学历 | 经验 | 地域 | 潜力 |
|------|------|------|------|------|------|
| 校园招聘 | 40% | 25% | 15% | 10% | 10% |
| 社会招聘(高级) | 25% | 20% | 30% | 10% | 15% |
| 跨界招聘 | 30% | 15% | 20% | 10% | 25% |
| 海外招聘 | 30% | 25% | 20% | 10% | 15% |
| 竞品Mapping | 35% | 20% | 25% | 10% | 10% |

### A.2 硬约束字段速查表

| 约束字段 | 操作符 | 说明 |
|----------|--------|------|
| education | in | 学历必须在列表中 |
| total_experience | >=, <= | 工作年限范围 |
| hard_skills | contains_any | 必须包含至少一个技能 |
| location | in | 工作地点匹配 |
| salary_range | <= | 薪资上限 |

### A.3 潜力评分因子速查表

| 因子 | 权重范围 | 主要指标 |
|------|----------|----------|
| 学习能力 | 20-35% | 学历、证书、海外经历 |
| 成长潜力 | 25-30% | 年龄、经验、行业前景 |
| 创新评分 | 20-35% | 专利、论文、项目 |
| 职业稳定性 | 15-20% | 在职时长、换工作频率 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-10 | 初始场景模板 |
| v2.0 | 2026-05-28 | 新增潜力评分配置、地域匹配配置、内部人才盘点场景 |
