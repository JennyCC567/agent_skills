# 配置说明文档

## 版本信息
- **版本**：v2.0
- **更新日期**：2026-05-28
- **状态**：正式发布

## 一、配置文件结构

### 1.1 主配置文件（config.yaml）

```yaml
# AI人才Mapping智能体配置

# 基础配置
app:
  name: "AI人才Mapping智能体"
  version: "2.0.0"
  environment: "production"  # production/development/test

# 数据源配置
data_source:
  type: "multi"  # single/multi
  sources:
    - name: "招聘平台A"
      type: "api"
      endpoint: "https://api.example.com/v1"
      api_key: "${API_KEY_PLATFORM_A}"
    
    - name: "招聘平台B"
      type: "database"
      connection: "postgresql://user:pass@host:5432/db"
    
    - name: "简历库"
      type: "file"
      path: "./data/resumes/"

# 数据处理配置
data_processing:
  # 字段映射配置
  field_mapping:
    education:
      - "最高学历"
      - "学历"
      - "degree"
    school:
      - "毕业院校"
      - "学校"
      - "university"
    major:
      - "所学专业"
      - "专业"
      - "major"
    total_experience:
      - "工作年限"
      - "年限"
      - "experience_years"
    current_company:
      - "当前公司"
      - "公司"
      - "company"
    current_title:
      - "当前职位"
      - "职位"
      - "title"
    hard_skills:
      - "硬技能"
      - "技能"
      - "skills"
    soft_skills:
      - "软技能"
      - "soft_skills"

  # 数据清洗规则
  cleaning_rules:
    remove_duplicates: true
    duplicate_threshold: 0.85  # 相似度阈值
    normalize_phone: true
    normalize_email: true
    fill_missing_values: true

# 匹配算法配置
matching_algorithm:
  # 硬约束配置（必须满足）
  hard_constraints:
    enabled: true
    constraints:
      - field: "education"
        operator: ">="  # >=, <=, ==, in
        value: "本科"   # 最低学历要求
      - field: "total_experience"
        operator: ">="
        value: 3        # 最低工作年限
  
  # 软约束配置（加权评分）
  soft_constraints:
    weights:
      skill_match: 0.35       # 技能匹配权重 35%
      education_match: 0.20   # 学历匹配权重 20%
      experience_match: 0.20  # 经验匹配权重 20%
      location_match: 0.15   # 地域匹配权重 15%
      potential_score: 0.10   # 潜力评分权重 10%
    
    # 技能相似度计算配置
    skill_similarity:
      method: "cosine"  # cosine/tfidf/jaccard
      threshold: 0.60    # 最低相似度阈值
      weighting: "tfidf"  # tfidf/frequency/inverse
  
  # 潜力评分配置
  potential_scoring:
    enabled: true
    factors:
      learning_ability: 0.30   # 学习能力权重
      growth_potential: 0.30    # 成长潜力权重
      innovation_score: 0.25    # 创新评分权重
      career_stability: 0.15   # 职业稳定性权重
  
  # 地域匹配配置
  location_matching:
    enabled: true
    remote_bonus: true         # 是否考虑远程工作加分
    city_tiers:
      一线: 0
      新一线: 10
      二线: 15
      三线: 20
      其他: 25

# 报告生成配置
report_generation:
  # 默认输出格式
  default_formats:
    - "html"
    - "excel"
  
  # HTML报告配置
  html:
    template: "standard"  # standard/professional/minimal
    include_charts: true
    chart_types:
      - "bar"
      - "pie"
      - "radar"
      - "heatmap"
    color_scheme: "business"  # business/creative/minimal
  
  # Excel报告配置
  excel:
    template: "dashboard"  # standard/dashboard/compact
    include_charts: true
    conditional_formatting: true
  
  # PDF报告配置
  pdf:
    template: "professional"
    page_size: "A4"
    orientation: "portrait"  # portrait/landscape

# 性能配置
performance:
  max_candidates: 10000
  batch_size: 100
  cache_enabled: true
  cache_ttl: 3600  # 秒
  parallel_processing: true
  max_workers: 4

# 日志配置
logging:
  level: "INFO"  # DEBUG/INFO/WARNING/ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "./logs/app.log"
  max_size: "100MB"
  backup_count: 5

# 安全配置
security:
  encrypt_sensitive_data: true
  data_retention_days: 90
  anonymize_pii: true
```

## 二、匹配算法参数配置

### 2.1 硬约束过滤器配置

```yaml
hard_constraints:
  # 是否启用硬约束过滤
  enabled: true
  
  # 硬约束规则列表
  rules:
    # 学历硬约束
    - name: "学历要求"
      field: "education"
      operator: "in"
      value: ["本科", "硕士", "博士"]  # 必须在此列表中
      
    # 工作年限硬约束
    - name: "工作年限"
      field: "total_experience"
      operator: ">="
      value: 3  # 至少3年
      
    # 地点硬约束（可选）
    - name: "工作地点"
      field: "location"
      operator: "in"
      value: ["北京", "上海", "深圳", "远程"]
      required: false  # 非强制
      
    # 薪资硬约束
    - name: "薪资上限"
      field: "current_salary"
      operator: "<="
      value: 50000  # 月薪不超过5万
      required: false
```

### 2.2 技能相似度配置

```yaml
skill_similarity:
  # 计算方法
  method: "cosine"  # 余弦相似度
  
  # 权重方案
  weighting: "tfidf"  # TF-IDF权重
  
  # 技能级别权重
  level_weights:
    专家: 1.0
    高级: 0.8
    中级: 0.6
    初级: 0.4
  
  # 同义词映射
  synonyms:
    Python:
      - "python"
      - "Python3"
      - "py"
    机器学习:
      - "机器学习"
      - "ML"
      - "Machine Learning"
    深度学习:
      - "深度学习"
      - "DL"
      - "Deep Learning"
    前端:
      - "前端"
      - "前端开发"
      - "Front-end"
      - "FE"
```

### 2.3 潜力评分配置

```yaml
potential_scoring:
  # 是否启用潜力评分
  enabled: true
  
  # 评分因子
  factors:
    # 学习能力评估
    learning_ability:
      weight: 0.30
      indicators:
        - field: "overseas_exp"
          weight: 0.3
        - field: "certifications"
          weight: 0.4
        - field: "education"
          weight: 0.3
    
    # 成长潜力评估
    growth_potential:
      weight: 0.30
      indicators:
        - field: "age"
          weight: 0.3
        - field: "total_experience"
          weight: 0.3
        - field: "career_changes"
          weight: 0.4
    
    # 创新评分
    innovation_score:
      weight: 0.25
      indicators:
        - field: "innovation_projects"
          weight: 0.5
        - field: "patents"
          weight: 0.3
        - field: "publications"
          weight: 0.2
    
    # 职业稳定性
    career_stability:
      weight: 0.15
      indicators:
        - field: "avg_job_duration"
          weight: 0.6
        - field: "job_changes"
          weight: 0.4
```

## 三、地域匹配配置

```yaml
location_matching:
  # 是否启用地域匹配
  enabled: true
  
  # 城市等级划分
  city_tiers:
    一线:
      - "北京"
      - "上海"
      - "广州"
      - "深圳"
      score: 0
    
    新一线:
      - "成都"
      - "杭州"
      - "重庆"
      - "武汉"
      - "西安"
      - "苏州"
      - "天津"
      - "南京"
      - "长沙"
      - "郑州"
      - "东莞"
      - "青岛"
      - "沈阳"
      - "宁波"
      - "昆明"
      score: 10
    
    二线:
      - "大连"
      - "厦门"
      - "泉州"
      - "无锡"
      - "合肥"
      - "昆明"
      - "哈尔滨"
      - "济南"
      - "温州"
      - "南宁"
      - "长春"
      - "常州"
      - "南通"
      - "嘉兴"
      - "太原"
      score: 15
    
    三线:
      - "珠海"
      - "镇江"
      - "海口"
      - "中山"
      - "咸阳"
      - "石家庄"
      - "潍坊"
      - "临沂"
      - "台州"
      - "漳州"
      score: 20
  
  # 远程工作配置
  remote_work:
    # 是否接受远程工作的加分
    remote_accepted_bonus: 25
    # 远程工作匹配规则
    remote_matching:
      - target_accepts_remote: true
        candidate_remote: true
        score_bonus: 25
      - target_accepts_remote: true
        candidate_remote: false
        score_bonus: 0
      - target_accepts_remote: false
        candidate_remote: true
        score_bonus: -10
```

## 四、输出格式配置

### 4.1 HTML报告配置

```yaml
html_report:
  # 模板选择
  template: "standard"
  
  # 图表配置
  charts:
    enabled: true
    types:
      - type: "bar"
        title: "企业人才规模与招聘热度对比"
        id: "company-comparison"
      - type: "pie"
        title: "岗位序列分布"
        id: "position-distribution"
      - type: "radar"
        title: "核心能力维度分析"
        id: "ability-radar"
      - type: "heatmap"
        title: "年龄/学历分布"
        id: "demographics-heatmap"
      - type: "bar"
        title: "工作年限分布"
        id: "experience-distribution"
      - type: "histogram"
        title: "薪酬区间分布"
        id: "salary-distribution"
      - type: "wordcloud"
        title: "技能标签云"
        id: "skill-wordcloud"
      - type: "bubble"
        title: "人才分层九宫格"
        id: "talent-stratification"
  
  # 样式配置
  styles:
    theme: "business"
    primary_color: "#1F4E79"
    secondary_color: "#4A90D9"
    accent_color: "#2CA58D"
    font_family: "WenQuanYi Micro Hei"
    font_size_base: "14px"
    line_height: "1.6"
  
  # 打印配置
  print:
    page_size: "A4"
    orientation: "portrait"
    margins:
      top: "2.5cm"
      bottom: "2.5cm"
      left: "3.0cm"
      right: "3.0cm"
    print_background: true
```

### 4.2 Excel报告配置

```yaml
excel_report:
  # 模板选择
  template: "dashboard"
  
  # 工作表配置
  sheets:
    - name: "总览"
      type: "overview"
      include_charts: true
    - name: "候选人明细"
      type: "detail"
      columns:
        - "姓名"
        - "当前公司"
        - "当前职位"
        - "匹配度"
        - "潜力评分"
        - "学历"
        - "工作年限"
        - "薪资范围"
    - name: "数据分析"
      type: "analysis"
      include_charts: true
    - name: "结论与建议"
      type: "conclusion"
  
  # 样式配置
  styles:
    header_bg: "#1F4E79"
    header_font_color: "#FFFFFF"
    zebra_stripe: true
    zebra_color: "#F2F2F2"
    border_color: "#E0E0E0"
  
  # 条件格式
  conditional_formatting:
    match_score:
      - condition: ">=90"
        color: "#2CA58D"  # 绿色
      - condition: ">=70"
        color: "#4A90D9"  # 蓝色
      - condition: ">=50"
        color: "#F5A623"  # 橙色
      - condition: "<50"
        color: "#D0021B"  # 红色
```

## 五、环境变量配置

### 5.1 必需的环境变量

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@host:5432/db

# API密钥
API_KEY_PLATFORM_A=your_api_key_here
API_KEY_PLATFORM_B=your_api_key_here

# 安全配置
ENCRYPTION_KEY=your_encryption_key_here
JWT_SECRET=your_jwt_secret_here

# 文件存储
STORAGE_PATH=/data/talent-mapping/
```

### 5.2 可选的环境变量

```bash
# 性能配置
MAX_WORKERS=4
CACHE_TTL=3600
BATCH_SIZE=100

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/var/log/talent-mapping/app.log

# 第三方服务
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=https://xxx@sentry.io/xxx
```

## 六、配置验证规则

### 6.1 必填配置项

| 配置路径 | 类型 | 说明 |
|----------|------|------|
| app.name | STRING | 应用名称 |
| data_source.type | STRING | 数据源类型 |
| matching_algorithm.hard_constraints.enabled | BOOLEAN | 硬约束开关 |
| matching_algorithm.soft_constraints.weights | OBJECT | 匹配权重 |
| report_generation.default_formats | LIST | 默认输出格式 |

### 6.2 配置校验规则

```yaml
validation_rules:
  # 权重必须之和为1
  weights_sum:
    path: "matching_algorithm.soft_constraints.weights"
    rule: "sum_equals_1"
    tolerance: 0.01
  
  # 相似度阈值范围
  similarity_threshold:
    path: "matching_algorithm.soft_constraints.skill_similarity.threshold"
    rule: "range"
    min: 0.0
    max: 1.0
  
  # 数值必须为正
  positive_values:
    - path: "performance.max_candidates"
      min: 1
    - path: "performance.batch_size"
      min: 1
```

## 七、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-10 | 初始配置版本 |
| v2.0 | 2026-05-28 | 新增潜力评分配置、地域匹配配置、硬约束过滤配置 |
