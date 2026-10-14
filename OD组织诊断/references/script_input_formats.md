# 脚本输入格式示例

本文档提供所有脚本的详细输入格式示例。

## 1. 组织健康度雷达图

### 输入格式
```json
{
  "strategy": 8,
  "structure": 6,
  "systems": 7,
  "style": 9,
  "staff": 5,
  "skills": 4,
  "shared_values": 7,
  "output_path": "./radar_chart.png"
}
```

### 字段说明
- 所有维度评分必须在1-10之间
- 必须包含全部7个维度
- output_path必须以.png或.jpg结尾

## 2. 人才九宫格

### 输入格式（纯列表）
```json
[
  {"name": "张三", "performance": 8, "potential": 9},
  {"name": "李四", "performance": 6, "potential": 5}
]
```

output_path作为命令行参数传入：`--output_path ./nine_box_grid.png`

### 字段说明
- performance和potential必须在1-10之间
- name字段不能为空
- 至少包含1条数据

## 3. 力场分析

### 输入格式
```json
{
  "driving_forces": [
    {
      "name": "高层支持",
      "score": 8
    }
  ],
  "restraining_forces": [
    {
      "name": "员工抵触",
      "score": 6
    }
  ],
  "output_path": "./force_field.png"
}
```

### 字段说明
- 驱动力和阻力列表至少各包含1个因素
- 所有分数必须在1-10之间
- 因素名称不能为空

## 4. 项目甘特图

### 输入格式（注意字段名）
```json
{
  "tasks": [
    {
      "task": "前期调研",
      "start": "2025-01-01",
      "end": "2025-01-15"
    }
  ],
  "output_path": "./gantt_chart.png"
}
```

### 字段说明
- **task**：任务名称（非name）
- **start**：开始日期（非start_date）
- **end**：结束日期（非end_date）
- 日期格式：YYYY-MM-DD
- 至少包含1个任务

## 5. ECharts交互式看板

### 输入格式（必填字段）
```json
{
  "company_name": "XX公司",
  "report_title": "组织健康度诊断报告",
  "seven_s_data": {
    "current": [75, 60, 65, 70, 68, 50, 72],
    "target": [90, 85, 80, 88, 90, 85, 90]
  },
  "key_success_factors": ["战略清晰", "组织优化", "人才发展"],
  "common_mistakes": ["急于求成", "缺乏沟通", "资源不足"],
  "phases": [
    {"name": "前期准备", "progress": 100, "status": "完成"},
    {"name": "全面诊断", "progress": 85, "status": "进行中"}
  ],
  "output_path": "./od_dashboard.html"
}
```

### 字段说明
- **report_title**（必填）：报告标题
- **seven_s_data**（必填）：0-100分数组格式，7个值对应7S维度
  - current: 当前得分数组
  - target: 目标得分数组
- **key_success_factors**（必填）：关键成功因素列表
- **common_mistakes**（必填）：常见误区列表

## 6. HTML概念卡

### 输入格式
```json
{
  "company_name": "XX公司",
  "title": "OD 组织发展入门概念卡",
  "content": {
    "definition": "OD是组织发展...",
    "difference": "传统HR关注个体绩效...",
    "key_models": ["麦肯锡7S模型", "BLM业务领先模型"]
  },
  "output_path": "./od_concept_card.html"
}
```

## 7. 诊断问卷

### 输入格式
```json
{
  "company_name": "XX公司",
  "title": "组织健康度诊断问卷",
  "questions": [
    {
      "id": 1,
      "dimension": "Strategy",
      "text": "公司有清晰的战略规划",
      "options": ["完全不同意", "不同意", "中立", "同意", "完全同意"]
    }
  ],
  "dimensions": {
    "Strategy": {"name": "战略", "weight": 1.0}
  },
  "questionnaire_type": "7s",
  "output_path": "./diagnostic_questionnaire.html"
}
```

### 字段说明
- **company_name**（必填）：公司名称
- **title**（必填）：问卷标题
- **questions**（必填）：题目列表
  - id: 题目编号
  - dimension: 所属维度
  - text: 题目内容
  - options: 选项列表
- **dimensions**（可选）：维度定义
- **questionnaire_type**（可选）：问卷类型，默认7s_model

## 8. Word诊断报告

### 输入格式
```json
{
  "company_name": "XX公司",
  "employee_name": "张三",
  "department": "销售部",
  "seven_s_scores": {
    "strategy": 7,
    "structure": 5,
    "systems": 6,
    "style": 7,
    "staff": 6,
    "skills": 4,
    "shared_values": 8
  },
  "analysis": "整体组织能力良好，战略清晰，但结构和制度需要优化...",
  "recommendations": [
    "建议优化组织结构，明确各部门职责边界",
    "建议完善激励机制，提升员工积极性"
  ],
  "chart_path": "./radar_chart.png",
  "output_path": "./diagnosis_report.docx"
}
```

## 9. PPT方案建议书

### 输入格式
```json
{
  "company_name": "XX公司",
  "project_name": "组织能力提升项目",
  "slides": [
    {
      "type": "cover",
      "title": "OD变革方案建议书",
      "subtitle": "XX公司组织能力提升项目"
    },
    {
      "type": "content",
      "title": "诊断结果",
      "content": "基于7S模型的诊断分析..."
    }
  ],
  "output_path": "./proposal.pptx"
}
```

## 10. Excel人才盘点底表

### 输入格式
```json
{
  "company_name": "XX公司",
  "employees": [
    {
      "name": "张三",
      "department": "销售部",
      "position": "销售经理",
      "performance": 8,
      "potential": 7
    }
  ],
  "output_path": "./talent_matrix.xlsx"
}
```

### 字段说明
- **company_name**（必填）：公司名称
- **employees**（必填）：员工列表
  - name: 姓名
  - department: 部门
  - position: 职位
  - performance: 绩效评分
  - potential: 潜力评分

## 11. 项目驾驶舱

### 输入格式
```json
{
  "company_name": "XX公司",
  "project_name": "组织能力提升项目",
  "project_period": "2025-01 至 2025-06",
  "phases": [
    {
      "name": "前期准备",
      "start": "2025-01",
      "end": "2025-01",
      "progress": 100,
      "status": "完成"
    }
  ],
  "resources": [
    {
      "name": "张三",
      "role": "OD顾问",
      "allocation": "100%"
    }
  ],
  "risks": [
    {
      "name": "高层支持不足",
      "impact": "高",
      "probability": "中",
      "mitigation": "加强沟通汇报"
    }
  ],
  "key_metrics": [
    {
      "name": "员工参与度",
      "current": 85,
      "target": 90,
      "unit": "%"
    }
  ],
  "output_path": "./project_cockpit.html"
}
```

## 12. HTML诊断报告

### 输入格式
```json
{
  "title": "XX公司组织健康度诊断报告",
  "sections": [
    {
      "heading": "诊断背景",
      "content": "本次诊断基于麦肯锡7S模型..."
    },
    {
      "heading": "7S模型分析",
      "content": "从雷达图可以看出...",
      "chart_path": "./radar_chart.png"
    }
  ],
  "output_path": "./od_report.html"
}
```

## 13. 战略解码卡（阶段1）

### 输入格式
```json
{
  "company_name": "XX公司",
  "project_name": "OD能力提升项目",
  "vision": "成为行业领先的创新型企业",
  "mission": "为客户创造价值，为员工创造机会",
  "values": ["创新", "协作", "客户导向"],
  "strategic_goals": [
    {
      "goal": "提升组织效能",
      "kpis": ["人均产出提升15%", "流程周期缩短20%"],
      "owner": "HR总监"
    }
  ],
  "blm_model": {
    "leadership": "领导力描述...",
    "vision": "战略愿景描述...",
    "Market_Insight": "市场洞察描述...",
    "Innovation_Offer": "创新焦点描述...",
    "Strategy": "策略描述...",
    "alignment": "组织对齐描述...",
    "teams": "团队描述...",
    "work_plan": "工作计划描述..."
  },
  "output_path": "./strategy_card.html"
}
```

### 字段说明
- **company_name**（必填）：公司名称
- **project_name**（必填）：项目名称
- **vision**（可选）：企业愿景
- **mission**（可选）：企业使命
- **values**（可选）：核心价值观列表
- **strategic_goals**（可选）：战略目标列表
- **blm_model**（可选）：BLM模型数据

## 14. 试点追踪表（阶段4）

### 输入格式
```json
{
  "company_name": "XX公司",
  "project_name": "OD能力提升项目",
  "pilot_scope": "选取华东区3家门店作为首批试点",
  "start_date": "2025-01-01",
  "end_date": "2025-03-31",
  "milestones": [
    {"name": "试点启动", "date": "2025-01-15", "status": "completed", "notes": "已完成"},
    {"name": "方案部署", "date": "2025-02-01", "status": "in_progress", "notes": "进行中"}
  ],
  "risks": [
    {"name": "人员抵触", "impact": "high", "mitigation": "加强沟通与培训"}
  ],
  "learnings": ["试点初期需要更多时间进行人员培训"],
  "recommendations": ["推广前完善培训体系"],
  "output_path": "./pilot_tracker.html"
}
```

### 字段说明
- **company_name**（必填）：公司名称
- **project_name**（必填）：项目名称
- **pilot_scope**（可选）：试点范围描述
- **start_date/end_date**（可选）：开始/结束日期
- **milestones**（可选）：里程碑列表，status可选值：pending/in_progress/completed
- **risks**（可选）：风险列表，impact可选值：high/medium/low
- **learnings**（可选）：试点学习点列表
- **recommendations**（可选）：建议列表

## 15. 推广检查单（阶段5）

### 输入格式
```json
{
  "company_name": "XX公司",
  "project_name": "OD能力提升项目",
  "kotter_steps": [
    {"step": "1. 创造紧迫感", "description": "...", "check_items": ["..."], "status": "completed"},
    {"step": "2. 建立指导联盟", "description": "...", "check_items": ["..."], "status": "in_progress"}
  ],
  "rollout_plan": [
    {"phase": "第一阶段", "timeline": "Q1", "scope": "华东区", "owner": "张总", "status": "completed"}
  ],
  "success_criteria": ["全员覆盖率达到95%以上", "核心指标提升10%以上"],
  "output_path": "./promotion_checklist.html"
}
```

### 字段说明
- **company_name**（必填）：公司名称
- **project_name**（必填）：项目名称
- **kotter_steps**（可选）：Kotter八步法检查项，默认包含8个步骤
- **rollout_plan**（可选）：推广计划列表
- **success_criteria**（可选）：成功标准列表

## 16. 固化复盘卡（阶段6）

### 输入格式
```json
{
  "company_name": "XX公司",
  "project_name": "OD能力提升项目",
  "project_duration": "2025-01-01 至 2025-12-31",
  "key_achievements": [
    {"metric": "组织效能提升", "value": "+25%"},
    {"metric": "员工满意度", "value": "92%"}
  ],
  "success_factors": ["高层领导持续支持", "充分的资源投入"],
  "lessons_learned": ["试点阶段需要更多时间"],
  "institutionalized_changes": [
    {"area": "组织架构", "change": "优化部门设置", "owner": "HR总监", "timeline": "2025-12"}
  ],
  "continuous_improvements": [
    {"title": "文化建设深化", "description": "...", "owner": "...", "timeline": "2026-Q1"}
  ],
  "metrics_summary": {
    "项目周期": "12个月",
    "参与人数": "500+"
  },
  "output_path": "./solidification_card.html"
}
```

### 字段说明
- **company_name**（必填）：公司名称
- **project_name**（必填）：项目名称
- **project_duration**（可选）：项目周期
- **key_achievements**（可选）：关键成果列表
- **success_factors**（可选）：成功要素列表
- **lessons_learned**（可选）：经验教训列表
- **institutionalized_changes**（可选）：制度化变革列表
- **continuous_improvements**（可选）：持续改进计划列表
- **metrics_summary**（可选）：指标总结字典
