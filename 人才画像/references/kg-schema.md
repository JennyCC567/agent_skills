# 知识图谱模式

## 目录
- [实体类型定义](#实体类型定义)
- [关系类型定义](#关系类型定义)
- [属性定义](#属性定义)
- [图数据库模式](#图数据库模式)
- [图谱构建流程](#图谱构建流程)

## 概览
本文档定义 AI 人才 Mapping 知识图谱的模式，包括实体类型、关系类型和属性规范。

---

## 实体类型定义

### Person（人才）
人才节点，表示一个具体的个人。

**属性**：
- `id`: string (required, UUID)
- `name`: string (required)
- `gender`: string (optional, enum: male|female|other)
- `age`: integer (optional)
- `education_level`: string (optional)
- `experience_years`: integer (optional)
- `skills`: array<string> (optional)
- `current_location`: string (optional)
- `employment_status`: string (optional)
- `risk_score`: float (optional, 0-1)
- `potential_score`: float (optional, 0-1)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `name`, `current_location`

### Company（企业）
企业节点，表示一个公司或组织。

**属性**：
- `id`: string (required, UUID)
- `name`: string (required)
- `industry`: string (optional)
- `location`: string (optional)
- `size`: string (optional, enum: startup|small|medium|large|enterprise)
- `funding_stage`: string (optional)
- `website`: string (optional)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `name`, `industry`, `location`

### School（学校）
学校节点，表示教育机构。

**属性**：
- `id`: string (required, UUID)
- `name`: string (required)
- `type`: string (optional, enum: university|college|high_school)
- `level`: string (optional, enum: 985|211|double_first_class|ordinary)
- `location`: string (optional)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `name`, `location`

### Skill（技能）
技能节点，表示一项技术能力或软技能。

**属性**：
- `id`: string (required, UUID)
- `name`: string (required)
- `category`: string (required, enum: technical|soft|language|certification)
- `subcategory`: string (optional)
- `popularity`: integer (optional, 技能热度)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `name`, `category`

### Project（项目）
项目节点，表示一个具体的项目或产品。

**属性**：
- `id`: string (required, UUID)
- `name`: string (required)
- `description`: string (optional)
- `domain`: string (optional)
- `start_date`: string (optional, YYYY-MM)
- `end_date`: string (optional, YYYY-MM)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `name`

### Publication（论文）
论文节点，表示学术出版物。

**属性**：
- `id`: string (required, UUID)
- `title`: string (required)
- `venue`: string (optional)
- `type`: string (optional, enum: journal|conference|preprint)
- `date`: string (optional, YYYY-MM)
- `url`: string (optional)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `title`, `venue`

### Patent（专利）
专利节点，表示知识产权。

**属性**：
- `id`: string (required, UUID)
- `title`: string (required)
- `patent_number`: string (required)
- `type`: string (optional, enum: invention|utility|design)
- `issue_date`: string (optional, YYYY-MM)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `patent_number`

### Position（职位）
职位节点，表示一个工作岗位。

**属性**：
- `id`: string (required, UUID)
- `title`: string (required)
- `level`: string (optional, enum: junior|middle|senior|expert|executive)
- `function`: string (optional)

**索引**：
- PRIMARY KEY: `id`
- INDEX: `title`

---

## 关系类型定义

### EMPLOYED_AT（任职）
Person -> Company

表示一个人在某个公司工作。

**属性**：
- `start_date`: string (YYYY-MM)
- `end_date`: string (YYYY-MM, null表示在职)
- `job_title`: string
- `department`: string
- `is_current`: boolean

### WORKS_WITH（合作）
Person -> Person

表示两个人之间存在合作关系。

**属性**：
- `context`: string (合作场景)
- `start_date`: string (YYYY-MM)
- `end_date`: string (YYYY-MM)

### EDUCATED_AT（毕业）
Person -> School

表示一个人在某所学校接受教育。

**属性**：
- `start_date`: string (YYYY-MM)
- `end_date`: string (YYYY-MM)
- `degree`: string
- `major`: string

### SKILLED_IN（掌握）
Person -> Skill

表示一个人掌握某项技能。

**属性**：
- `proficiency`: string (enum: beginner|intermediate|advanced|expert)
- `years`: integer (掌握年限)

### REQUIRES（需要）
Position -> Skill

表示某个职位需要某项技能。

**属性**：
- `level`: string (enum: required|preferred)
- `proficiency`: string (enum: intermediate|advanced|expert)

### PARTICIPATED_IN（参与）
Person -> Project

表示一个人参与某个项目。

**属性**：
- `role`: string
- `start_date`: string (YYYY-MM)
- `end_date`: string (YYYY-MM)
- `contribution`: string

### AUTHORED（发表）
Person -> Publication

表示一个人发表论文。

**属性**：
- `author_order`: integer (作者排序)
- `contribution_type`: string

### INVENTED（发明）
Person -> Patent

表示一个人参与发明专利。

**属性**：
- `inventor_order`: integer (发明人排序)

### OFFERS（提供）
Company -> Position

表示公司提供某个职位。

**属性**：
- `department`: string
- `location`: string
- `salary_min`: integer
- `salary_max`: integer

### COMPETITOR_OF（竞争）
Company -> Company

表示两个公司是竞争对手。

**属性**：
- `competition_level`: string (enum: direct|indirect)
- `market_overlap`: float (0-1)

### SUPPLIER_OF（供应商）
Company -> Company

表示两个公司是上下游关系。

**属性**：
- `relationship_type`: string (enum: supplier|customer|partner)

### USED_IN（应用于）
Project -> Skill

表示项目中使用了某项技能。

**属性**：
- `usage_level`: string (enum: core|auxiliary)

---

## 属性定义

### 通用属性
- `created_at`: string (ISO8601, 记录创建时间)
- `updated_at`: string (ISO8601, 记录更新时间)
- `data_source`: string (数据来源)

### 权重属性
- `relevance_score`: float (0-1, 相关性分数)
- `confidence`: float (0-1, 置信度)

---

## 图数据库模式

### Neo4j CQL 示例

#### 创建索引
```cypher
CREATE INDEX person_name_index FOR (p:Person) ON (p.name);
CREATE INDEX company_name_index FOR (c:Company) ON (c.name);
CREATE INDEX skill_name_index FOR (s:Skill) ON (s.name);
```

#### 创建约束
```cypher
CREATE CONSTRAINT person_id_unique FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT company_id_unique FOR (c:Company) REQUIRE c.id IS UNIQUE;
```

#### 创建节点
```cypher
CREATE (p:Person {
  id: "550e8400-e29b-41d4-a716-446655440000",
  name: "张三",
  gender: "male",
  age: 32,
  education_level: "master",
  experience_years: 8,
  skills: ["Python", "Machine Learning"],
  current_location: "北京",
  employment_status: "employed",
  risk_score: 0.3,
  potential_score: 0.85
})
```

#### 创建关系
```cypher
MATCH (p:Person {id: "550e8400-e29b-41d4-a716-446655440000"})
MATCH (c:Company {name: "字节跳动"})
CREATE (p)-[:EMPLOYED_AT {
  start_date: "2020-03",
  end_date: null,
  job_title: "高级算法工程师",
  department: "AI Lab",
  is_current: true
}]->(c)
```

### 常用查询

#### 查询某公司的所有员工
```cypher
MATCH (p:Person)-[e:EMPLOYED_AT]->(c:Company {name: "字节跳动"})
WHERE e.is_current = true
RETURN p, e
```

#### 查询掌握特定技能的人才
```cypher
MATCH (p:Person)-[s:SKILLED_IN]->(sk:Skill {name: "Python"})
WHERE s.proficiency IN ["advanced", "expert"]
RETURN p, s
ORDER BY s.years DESC
```

#### 查询人才的社会关系网络
```cypher
MATCH path = (p:Person {name: "张三"})-[:WORKS_WITH*1..2]-(other:Person)
RETURN path
```

#### 查询竞品公司的人才流动
```cypher
MATCH (c1:Company)-[:COMPETITOR_OF]->(c2:Company)
MATCH (p:Person)-[e1:EMPLOYED_AT]->(c1)
MATCH (p)-[e2:EMPLOYED_AT]->(c2)
WHERE e1.end_date IS NOT NULL
  AND e2.start_date > e1.end_date
RETURN p, e1, e2
ORDER BY e2.start_date DESC
```

#### 查询技能相关性
```cypher
MATCH (s1:Skill)<-[:SKILLED_IN]-(p:Person)-[:SKILLED_IN]->(s2:Skill)
WHERE s1.name = "Python" AND s1 <> s2
WITH s2, count(p) AS co_occurrence
RETURN s2.name, co_occurrence
ORDER BY co_occurrence DESC
LIMIT 10
```

---

## 图谱构建流程

### 1. 数据抽取
从结构化数据和非结构化数据中提取实体和关系。

### 2. 实体链接
- 确定实体唯一标识
- 消除歧义（同义词、多义词）
- 实体归一（公司名、技能名等）

### 3. 关系抽取
- 显式关系：直接从数据中提取
- 隐式关系：通过推理和规则生成

### 4. 质量校验
- 检查数据一致性
- 验证关系合理性
- 去除噪声和异常

### 5. 图谱更新
- 增量更新新数据
- 修正错误数据
- 维护图谱时效性

---

## 图谱应用场景

### 人才推荐
基于知识图谱的路径和关系进行候选人推荐。

### 技能匹配
通过技能节点和关系计算技能相似度和匹配度。

### 竞品分析
通过公司关系和人才流动分析竞品情况。

### 团队构建
基于人员合作关系推荐互补团队成员。

### 风险预警
通过关系网络识别潜在的离职风险和合规风险。
