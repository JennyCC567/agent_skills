# 候选人画像与智能评分卡指南

## 目录
1. [概览](#概览)
2. [候选人画像模型](#候选人画像模型)
3. [可视化画像生成](#可视化画像生成)
4. [智能评分卡](#智能评分卡)
5. [权重配置](#权重配置)
6. [使用流程](#使用流程)

## 概览

候选人画像是对候选人的全方位数字化呈现，通过多维度数据整合，形成直观的人才价值视图。

**核心价值**：
- 快速识别候选人核心优势
- 精准匹配岗位需求
- 提升推荐说服力
- 支持数据化决策

## 候选人画像模型

### 基础属性维度

| 维度 | 指标 | 说明 |
|------|------|------|
| 基本信息 | 姓名、年龄、学历、工作年限 | 基础标签 |
| 职业背景 | 职位、公司、行业、职级 | 履历标签 |
| 薪酬预期 | 当前薪资、期望薪资、薪资结构 | 薪酬标签 |
| 地域偏好 | 期望工作地、通勤范围、搬迁意愿 | 地域标签 |

### 能力属性维度

| 维度 | 指标 | 说明 |
|------|------|------|
| 硬技能 | 技术栈、专业能力、资质认证 | 专业技术能力 |
| 软技能 | 沟通能力、团队协作、问题解决 | 通用软技能 |
| 管理能力 | 团队规模、管理风格、领导力 | 管理潜质 |
| 行业认知 | 行业经验、业务理解、前瞻性 | 行业积累 |

### 发展属性维度

| 维度 | 指标 | 说明 |
|------|------|------|
| 成长轨迹 | 晋升速度、技能跃迁、职责扩展 | 历史成长 |
| 学习能力 | 学习速度、知识更新、方法论 | 学习潜质 |
| 发展意愿 | 职业规划、成长诉求、发展目标 | 发展动力 |

### 匹配属性维度

| 维度 | 指标 | 说明 |
|------|------|------|
| 岗位匹配 | 技能匹配度、经验匹配度 | 岗位适合度 |
| 团队匹配 | 风格匹配、文化认同 | 融入度 |
| 发展匹配 | 成长空间、晋升路径 | 发展空间 |

## 可视化画像生成

### 画像雷达图

使用SVG生成候选人能力雷达图，支持断网查看：

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>候选人能力雷达图</title>
<style>
body {font-family: Arial, sans-serif; margin: 20px;}
.radar-container {text-align: center;}
h2 {color: #333;}
table {margin: 20px auto; border-collapse: collapse; width: 80%;}
th, td {border: 1px solid #ddd; padding: 12px; text-align: center;}
th {background-color: #4a90d9; color: white;}
.avatar {
  width: 80px; height: 80px; border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 24px; font-weight: bold; margin: 0 auto;
}
.avatar-container {text-align: center;}
.score-high {color: #52c41a; font-weight: bold;}
.score-mid {color: #faad14; font-weight: bold;}
.score-low {color: #f5222d; font-weight: bold;}
</style>
</head>
<body>
<div class="radar-container">
<h2>候选人能力画像</h2>

<div class="avatar-container">
<div class="avatar">[姓]</div>
<p><strong>候选人代号</strong><br/>[候选人姓名]</p>
</div>

<h3>能力雷达图</h3>
<svg width="400" height="400" viewBox="-220 -220 440 440" style="display:block;margin:0 auto;">
<!-- 背景网格 -->
<circle cx="0" cy="0" r="50" fill="none" stroke="#e8e8e8" stroke-width="1"/>
<circle cx="0" cy="0" r="100" fill="none" stroke="#e8e8e8" stroke-width="1"/>
<circle cx="0" cy="0" r="150" fill="none" stroke="#e8e8e8" stroke-width="1"/>
<circle cx="0" cy="0" r="200" fill="none" stroke="#e8e8e8" stroke-width="1"/>

<!-- 轴线 -->
<line x1="0" y1="-200" x2="0" y2="200" stroke="#e8e8e8" stroke-width="1"/>
<line x1="-200" y1="0" x2="200" y2="0" stroke="#e8e8e8" stroke-width="1"/>
<line x1="-141" y1="-141" x2="141" y2="141" stroke="#e8e8e8" stroke-width="1"/>
<line x1="141" y1="-141" x2="-141" y2="141" stroke="#e8e8e8" stroke-width="1"/>

<!-- 数据区域 -->
<polygon
  points="[技能1分数*cos(0),技能1分数*sin(0)]"
  fill="rgba(74,144,217,0.3)"
  stroke="#4a90d9"
  stroke-width="2"
  transform="rotate(-90)"/>

<!-- 刻度标签 -->
<text x="0" y="-210" text-anchor="middle" font-size="12">技能能力</text>
<text x="0" y="220" text-anchor="middle" font-size="12">项目经验</text>
<text x="-210" y="0" text-anchor="end" font-size="12">沟通能力</text>
<text x="210" y="0" text-anchor="start" font-size="12">管理能力</text>
</svg>

<h3>详细评分</h3>
<table>
<tr>
<th>评估维度</th>
<th>评分</th>
<th>说明</th>
</tr>
<tr>
<td>技术能力</td>
<td class="score-high">[8.5]/10</td>
<td>掌握主流技术栈</td>
</tr>
<tr>
<td>项目经验</td>
<td class="score-high">[9.0]/10</td>
<td>大型项目主导经验</td>
</tr>
<tr>
<td>沟通能力</td>
<td class="score-mid">[7.0]/10</td>
<td>表达清晰有条理</td>
</tr>
<tr>
<td>管理能力</td>
<td class="score-mid">[6.5]/10</td>
<td>有带团队经验</td>
</tr>
<tr>
<td>学习能力</td>
<td class="score-high">[8.0]/10</td>
<td>持续学习意愿强</td>
</tr>
<tr>
<td>文化契合</td>
<td class="score-high">[8.5]/10</td>
<td>价值观匹配度高</td>
</tr>
</table>

<p style="color:#666;font-size:12px;">生成时间：[填入真实系统时间]</p>
</div>
</body>
</html>
```

### 画像JSON结构

```json
{
  "candidate_id": "[候选人ID]",
  "basic_info": {
    "name": "[姓名]",
    "age": "[年龄]",
    "education": "[学历]",
    "work_years": [工作年限],
    "current_title": "[当前职位]",
    "current_company": "[当前公司]"
  },
  "skill_radar": {
    "technical": [技术能力分数],
    "experience": [项目经验分数],
    "communication": [沟通能力分数],
    "management": [管理能力分数],
    "learning": [学习能力分数],
    "culture_fit": [文化契合分数]
  },
  "salary": {
    "current": "[当前薪资]",
    "expected": "[期望薪资]",
    "negotiable": [是否可谈]
  },
  "matching_score": {
    "overall": [综合匹配度],
    "hard_skills": [硬技能匹配],
    "soft_skills": [软技能匹配],
    "experience": [经验匹配]
  },
  "tags": ["[标签1]", "[标签2]", "[标签3]"],
  "generated_at": "[填入真实系统时间]"
}
```

## 智能评分卡

### 评分卡结构

```
+--------------------------------------------------+
|              候选人智能评分卡                     |
+--------------------------------------------------+
| 候选人：[姓名]          生成时间：[填入真实系统时间] |
+--------------------------------------------------+
| 一、硬性指标评分（必须满足）                       |
+--------------------------------------------------+
| [ ] 学历要求：本科及以上    [满足/不满足]         |
| [ ] 工作年限：5年以上       [满足/不满足]         |
| [ ] 核心技术栈：Python      [满足/不满足]         |
+--------------------------------------------------+
| 二、软性指标评分（权重可调整）                     |
+--------------------------------------------------+
| 评估维度          权重    得分    加权得分         |
| ------------------------------------------------ |
| 技术能力           30%     8.5      2.55         |
| 项目经验           25%     9.0      2.25         |
| 沟通能力           15%     7.0      1.05         |
| 管理能力           15%     6.5      0.98         |
| 学习能力           10%     8.0      0.80         |
| 文化契合            5%     8.5      0.43         |
+--------------------------------------------------+
| 三、综合评分                                          |
+--------------------------------------------------+
| 硬性指标通过：[是/否]                               |
| 软性指标得分：[X]分（满分10分）                     |
| 综合匹配度：[X]分                                    |
| 人才评级：[A/B/C/D]                                 |
+--------------------------------------------------+
| 四、决策建议                                        |
+--------------------------------------------------+
| [根据评分给出决策建议]                              |
+--------------------------------------------------+
```

### 技术研发类评分卡

| 评估维度 | 权重 | 评分标准 | 得分范围 |
|----------|------|----------|----------|
| 技术深度 | 25% | 掌握技术栈数量、源码阅读能力、架构设计能力 | 1-10 |
| 项目经验 | 25% | 项目规模、复杂度、主导/参与角色 | 1-10 |
| 学习能力 | 20% | 新技术学习速度、知识体系更新频率 | 1-10 |
| 沟通协作 | 15% | 技术沟通清晰度、跨团队协作能力 | 1-10 |
| 文化契合 | 15% | 价值观匹配、抗压能力、职业素养 | 1-10 |

### 销售类评分卡

| 评估维度 | 权重 | 评分标准 | 得分范围 |
|----------|------|----------|----------|
| 业绩达成 | 30% | 连续业绩完成率、增长率 | 1-10 |
| 客户资源 | 25% | 客户数量、质量、持续贡献 | 1-10 |
| 谈判能力 | 20% | 成交率、谈判技巧、异议处理 | 1-10 |
| 客情关系 | 15% | 客户满意度、转介绍率 | 1-10 |
| 抗压能力 | 10% | 目标压力、周期压力 | 1-10 |

### 管理类评分卡

| 评估维度 | 权重 | 评分标准 | 得分范围 |
|----------|------|----------|----------|
| 战略思维 | 25% | 战略理解、规划能力、全局视角 | 1-10 |
| 团队建设 | 25% | 团队规模、培养人才、梯队建设 | 1-10 |
| 业务突破 | 20% | 业绩增长、创新突破、问题解决 | 1-10 |
| 变革推动 | 15% | 变革意愿、推动能力、执行力 | 1-10 |
| 文化传承 | 15% | 价值观传递、氛围营造 | 1-10 |

## 权重配置

### 默认权重模板

```json
{
  "technical": {
    "weights": {
      "technical_depth": 0.25,
      "project_experience": 0.25,
      "learning_ability": 0.20,
      "communication": 0.15,
      "culture_fit": 0.15
    },
    "pass_threshold": 6.0,
    "overall_threshold": 7.0
  },
  "sales": {
    "weights": {
      "performance": 0.30,
      "customer_resource": 0.25,
      "negotiation": 0.20,
      "relationship": 0.15,
      "pressure": 0.10
    },
    "pass_threshold": 6.5,
    "overall_threshold": 7.5
  },
  "management": {
    "weights": {
      "strategy": 0.25,
      "team_building": 0.25,
      "business_impact": 0.20,
      "change_management": 0.15,
      "culture": 0.15
    },
    "pass_threshold": 6.0,
    "overall_threshold": 7.0
  },
  "operations": {
    "weights": {
      "operation_ability": 0.30,
      "data_analysis": 0.25,
      "execution": 0.20,
      "innovation": 0.15,
      "collaboration": 0.10
    },
    "pass_threshold": 6.0,
    "overall_threshold": 7.0
  }
}
```

### 自定义权重配置

用户可根据具体需求调整权重：

```markdown
## 权重调整规则

1. **岗位优先级**：根据JD核心需求调整权重
2. **企业阶段**：初创期重视执行，成长期重视管理
3. **团队现状**：补短板型招聘调整相关权重
4. **预算限制**：预算有限时适当降低薪资期望权重

## 调整建议

| 场景 | 权重调整建议 |
|------|--------------|
| 技术专家招聘 | 技术深度权重提升至30%+ |
| 销售负责人 | 业绩达成权重提升至35%+ |
| 管理培训生 | 学习能力权重提升至25%+ |
| 跨行业招聘 | 文化契合权重提升至20%+ |
```

## 使用流程

### 标准流程

```
Step 1: 收集候选人信息
        ↓
Step 2: 生成候选人画像（JSON）
        ↓
Step 3: 生成可视化雷达图
        ↓
Step 4: 选择评分卡模板
        ↓
Step 5: 根据候选人信息评分
        ↓
Step 6: 自动计算加权得分
        ↓
Step 7: 生成综合评价和建议
```

### 快速流程（已有画像数据）

```
Step 1: 导入候选人画像数据
        ↓
Step 2: 选择评分维度
        ↓
Step 3: 一键生成评分卡
        ↓
Step 4: 输出PDF/HTML报告
```

### 批量流程（多候选人对比）

```
Step 1: 批量导入候选人画像
        ↓
Step 2: 统一评分维度
        ↓
Step 3: 自动批量评分
        ↓
Step 4: 生成对比报告
        ↓
Step 5: 输出排名和推荐
```

## 合规检查清单

- [是] 所有日期使用真实系统时间
- [是] 图片使用base64内嵌，不引用外部URL
- [是] HTML报告支持断网查看
- [是] 敏感数据已脱敏处理
- [是] 不包含任何CDN引用
