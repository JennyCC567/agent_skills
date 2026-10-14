# 数据结构规范

## 目录
- [JSON-LD 标准格式](#json-ld-标准格式)
- [人才记录结构](#人才记录结构)
- [岗位记录结构](#岗位记录结构)
- [字段定义与约束](#字段定义与约束)
- [数据示例](#数据示例)

## 概览
本文档定义 AI 人才 Mapping 系统中使用的数据结构规范，确保数据一致性和互操作性。

---

## JSON-LD 标准格式

### 基础结构
所有数据必须符合 JSON-LD 标准，包含 `@context` 和 `@type` 字段：

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "id": "uuid",
  "name": "张三",
  ...
}
```

### 上下文定义
```json
{
  "@context": {
    "schema": "https://schema.org/",
    "hris": "http://example.org/hris/",
    "talent": "http://example.org/talent/"
  }
}
```

---

## 人才记录结构

### 完整结构
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "id": "string (required, UUID)",
  "name": "string (required)",
  "phone": "string (optional, E.164格式)",
  "email": "string (optional, email格式)",
  "gender": "string (optional, enum: male|female|other)",
  "age": "integer (optional, >=18)",
  "education_level": "string (required, enum: high_school|college|bachelor|master|phd)",
  "education": [
    {
      "school": "string (required)",
      "degree": "string (required)",
      "major": "string (required)",
      "start_date": "string (required, YYYY-MM)",
      "end_date": "string (required, YYYY-MM)",
      "is_top_university": "boolean (optional)"
    }
  ],
  "experience_years": "integer (required, >=0)",
  "skills": [
    "string (required, 标准化技能标签)"
  ],
  "current_company": "string (optional, 标准化公司名)",
  "current_job_title": "string (optional, 标准化职位名)",
  "current_location": "string (optional, 城市)",
  "employment_status": "string (optional, enum: employed|unemployed|job_seeking)",
  "expected_salary": "integer (optional, 年薪，单位：元)",
  "work_experience": [
    {
      "company": "string (required, 标准化公司名)",
      "job_title": "string (required, 标准化职位名)",
      "department": "string (optional)",
      "industry": "string (optional, 标准化行业名)",
      "start_date": "string (required, YYYY-MM)",
      "end_date": "string (optional, YYYY-MM, null表示在职)",
      "skills": [
        "string (optional, 项目中使用的技能)"
      ],
      "achievements": [
        "string (optional, 业绩描述)"
      ],
      "promotion": "boolean (optional, 是否有晋升)"
    }
  ],
  "projects": [
    {
      "name": "string (required)",
      "role": "string (required)",
      "start_date": "string (required, YYYY-MM)",
      "end_date": "string (optional, YYYY-MM)",
      "description": "string (optional)",
      "skills": [
        "string (optional, 项目技能)"
      ],
      "achievements": [
        "string (optional)"
      ]
    }
  ],
  "certifications": [
    {
      "name": "string (required)",
      "issuer": "string (required)",
      "issue_date": "string (required, YYYY-MM)",
      "expiry_date": "string (optional, YYYY-MM)"
    }
  ],
  "publications": [
    {
      "title": "string (required)",
      "authors": [
        "string (required)"
      ],
      "venue": "string (optional)",
      "date": "string (required, YYYY-MM)",
      "url": "string (optional, URL)"
    }
  ],
  "patents": [
    {
      "title": "string (required)",
      "patent_number": "string (required)",
      "issue_date": "string (required, YYYY-MM)",
      "inventors": [
        "string (required)"
      ]
    }
  ],
  "soft_skills": [
    "string (optional, 标准化软技能标签)"
  ],
  "work_style": "string (optional, 工作风格描述)",
  "team_preference": "string (optional, 团队偏好描述)",
  "risk_score": "float (optional, 0-1, 离职风险)",
  "potential_score": "float (optional, 0-1, 潜力评分)",
  "source": "string (required, 数据来源)",
  "created_at": "string (required, ISO8601)",
  "updated_at": "string (required, ISO8601)"
}
```

---

## 岗位记录结构

### 完整结构
```json
{
  "@context": "https://schema.org",
  "@type": "JobPosting",
  "id": "string (required, UUID)",
  "title": "string (required, 标准化职位名)",
  "company": "string (required, 标准化公司名)",
  "department": "string (optional)",
  "industry": "string (optional, 标准化行业名)",
  "location": "string (required, 城市)",
  "employment_type": "string (optional, enum: full_time|part_time|contract|intern)",
  "required_education": "string (required, enum: high_school|college|bachelor|master|phd)",
  "required_years": "integer (required, >=0)",
  "required_skills": [
    "string (required, 必备技能标签)"
  ],
  "preferred_skills": [
    "string (optional, 加分技能标签)"
  ],
  "soft_skills": [
    "string (optional, 软技能要求)"
  ],
  "salary_min": "integer (optional, 年薪下限，单位：元)",
  "salary_max": "integer (optional, 年薪上限，单位：元)",
  "description": "string (optional, 岗位描述)",
  "responsibilities": [
    "string (optional, 职责描述)"
  ],
  "requirements": [
    "string (optional, 要求描述)"
  ],
  "benefits": [
    "string (optional, 福利描述)"
  ],
  "constraints": {
    "location": "string (optional, 地域约束)",
    "max_salary": "integer (optional, 薪资上限)",
    "employment_status": "string (optional, 在职状态约束)",
    "age_limit": "integer (optional, 年龄上限)"
  },
  "created_at": "string (required, ISO8601)",
  "updated_at": "string (required, ISO8601)"
}
```

---

## 字段定义与约束

### 通用约束
- **UUID**：符合 RFC 4122 标准的 UUID 字符串
- **日期格式**：ISO 8601 格式（YYYY-MM 或 YYYY-MM-DD）
- **枚举值**：严格使用预定义的枚举值
- **邮箱格式**：符合 RFC 5322 标准
- **电话号码**：E.164 格式（如：+8613800138000）

### 教育等级枚举
```json
{
  "education_level": {
    "high_school": "高中",
    "college": "大专",
    "bachelor": "本科",
    "master": "硕士",
    "phd": "博士"
  }
}
```

### 在职状态枚举
```json
{
  "employment_status": {
    "employed": "在职",
    "unemployed": "离职",
    "job_seeking": "求职中"
  }
}
```

### 就业类型枚举
```json
{
  "employment_type": {
    "full_time": "全职",
    "part_time": "兼职",
    "contract": "合同",
    "intern": "实习"
  }
}
```

---

## 数据示例

### 人才记录示例
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "李明",
  "phone": "+8613812345678",
  "email": "liming@example.com",
  "gender": "male",
  "age": 32,
  "education_level": "master",
  "education": [
    {
      "school": "清华大学",
      "degree": "硕士",
      "major": "计算机科学与技术",
      "start_date": "2012-09",
      "end_date": "2015-06",
      "is_top_university": true
    },
    {
      "school": "北京航空航天大学",
      "degree": "本科",
      "major": "软件工程",
      "start_date": "2008-09",
      "end_date": "2012-06",
      "is_top_university": true
    }
  ],
  "experience_years": 8,
  "skills": [
    "Python",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Data Analysis"
  ],
  "current_company": "字节跳动",
  "current_job_title": "高级算法工程师",
  "current_location": "北京",
  "employment_status": "employed",
  "expected_salary": 800000,
  "work_experience": [
    {
      "company": "字节跳动",
      "job_title": "高级算法工程师",
      "department": "AI Lab",
      "industry": "互联网",
      "start_date": "2020-03",
      "end_date": null,
      "skills": [
        "TensorFlow",
        "NLP",
        "Recommendation System"
      ],
      "achievements": [
        "主导推荐系统算法优化，CTR提升15%",
        "发表CVPR论文1篇"
      ],
      "promotion": true
    },
    {
      "company": "阿里巴巴",
      "job_title": "算法工程师",
      "department": "达摩院",
      "industry": "互联网",
      "start_date": "2017-07",
      "end_date": "2020-02",
      "skills": [
        "Python",
        "Machine Learning",
        "Data Mining"
      ],
      "achievements": [
        "参与搜索算法优化"
      ],
      "promotion": false
    }
  ],
  "projects": [
    {
      "name": "智能推荐系统",
      "role": "算法负责人",
      "start_date": "2021-01",
      "end_date": "2021-12",
      "description": "基于深度学习的电商推荐系统",
      "skills": [
        "Deep Learning",
        "Recommendation System"
      ],
      "achievements": [
        "系统上线后GMV提升20%"
      ]
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Machine Learning Specialty",
      "issuer": "Amazon Web Services",
      "issue_date": "2019-05",
      "expiry_date": "2022-05"
    }
  ],
  "publications": [
    {
      "title": "Deep Learning for Recommendation: A Survey",
      "authors": [
        "李明",
        "张三"
      ],
      "venue": "CVPR",
      "date": "2021-06",
      "url": "https://arxiv.org/abs/2106.12345"
    }
  ],
  "soft_skills": [
    "Team Leadership",
    "Problem Solving",
    "Communication"
  ],
  "work_style": "结果导向，善于团队协作",
  "team_preference": "扁平化管理，重视技术氛围",
  "risk_score": 0.3,
  "potential_score": 0.85,
  "source": "内部HRIS",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 岗位记录示例
```json
{
  "@context": "https://schema.org",
  "@type": "JobPosting",
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "AI算法专家",
  "company": "某科技公司",
  "department": "AI研究院",
  "industry": "互联网",
  "location": "北京",
  "employment_type": "full_time",
  "required_education": "master",
  "required_years": 5,
  "required_skills": [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch"
  ],
  "preferred_skills": [
    "NLP",
    "Computer Vision",
    "Reinforcement Learning"
  ],
  "soft_skills": [
    "Team Leadership",
    "Innovation",
    "Communication"
  ],
  "salary_min": 600000,
  "salary_max": 1000000,
  "description": "负责AI算法研发与应用落地",
  "responsibilities": [
    "设计并实现先进的AI算法",
    "带领团队完成技术攻关",
    "推动算法在业务场景的应用"
  ],
  "requirements": [
    "5年以上AI算法研发经验",
    "扎实的数学和编程基础",
    "有顶级会议论文发表者优先"
  ],
  "benefits": [
    "具有竞争力的薪酬",
    "股票期权",
    "弹性工作制"
  ],
  "constraints": {
    "location": "北京",
    "max_salary": 1000000,
    "employment_status": null
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-10T08:00:00Z"
}
```

---

## 数据验证规则

### 必填字段检查
- 人才记录：`id`, `name`, `education_level`, `experience_years`, `skills`, `source`, `created_at`, `updated_at`
- 岗位记录：`id`, `title`, `company`, `location`, `required_education`, `required_years`, `required_skills`, `created_at`, `updated_at`

### 格式验证
- UUID 格式：`^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
- 邮箱格式：`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- 日期格式：`^\d{4}-\d{2}$` 或 `^\d{4}-\d{2}-\d{2}$`

### 逻辑一致性
- `end_date` >= `start_date`
- `experience_years` 应与工作经历时间段大致一致
- `education_level` 应与教育经历最高学位一致

---

## 数据质量标准

### 完整性
- 必填字段完整率：>= 95%
- 关键信息完整率：>= 80%

### 准确性
- 联系方式有效验证率：>= 90%
- 技能标签准确率：>= 85%

### 一致性
- 公司名称标准化率：>= 90%
- 职位名称标准化率：>= 85%
- 技能标签标准化率：>= 80%

### 及时性
- 数据更新延迟：<= 7 天
- 实时数据延迟：<= 1 小时
