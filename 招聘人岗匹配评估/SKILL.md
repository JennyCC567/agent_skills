---
name: resume-job-matching
description: 简历智能分析与岗位匹配工具，5大差异化能力：①Word/PDF简历自动解析+脱敏；②多维度人岗匹配度评分（硬性条件+必备技能+软性素质+ATS通过率）；③FABM猎头推荐报告；④4行业适配模板（互联网/跨境电商/国内电商/医疗）；⑤批量分析+候选人库+协作评审。HTML报告（本地内嵌禁止CDN）+Excel汇总
category: 办公与效率
tags: 简历,人岗匹配,FABM,ATS,猎头
eval_strategy: developer
dependency:
  python:
    - python-docx>=0.8.11
    - pdfplumber>=0.9.0
---

# 简历智能分析与岗位匹配 Skill

## 执行规则（强制）

1. **收到简历分析需求后，先判断**：单份/批量 → 是否有JD → 输出格式
2. **解析前必须脱敏**：身份证/护照/社保/住址/银行账号→掩码，期望薪资保留
3. **直接输出匹配分析结果**，不要解释框架、不要展示系统说明
4. **每个维度必须给评分**，0-100分制，匹配度分级：A(≥85%) B(70-84%) C(50-69%) D(<50%)
5. **问题必须配建议**，建议必须含面试考察点
6. **日期必须用系统真实时间**，禁止虚构

## 重要提示

> 本工具仅提供参考建议，所有决策请结合企业实际情况并经人工审核确认。
> 数据安全：AES-256加密+动态脱敏+边界隔离。上传前务必预处理隐私信息。
> 需遵守《个人信息保护法》，确保已获候选人授权。

## 合规底线

| 类型 | 规则 | 禁止 |
|------|------|------|
| HTML图表 | 本地内嵌 | 外部CDN链接 |
| 图片 | base64内嵌 | 外部URL引用 |
| 第三方库 | 严禁html-docx-js/FileSaver | 断网失效 |
| PDF导出 | window.print()原生方法 | PDF生成库 |

## 流程选择

| 场景 | 推荐流程 | 耗时 |
|------|---------|------|
| 单份简历 | 标准5步流程 | 25-45s |
| 批量处理 | 传统完整版 | 50-90s |
| 快速筛选 | 快速评分 | 8-15s |

### 标准5步要点

| 步骤 | 内容 | 关键输出 |
|------|------|---------|
| 1.解析 | parse_resume.py→mask_sensitive_info.py | 脱敏文本 |
| 2.扫描 | 硬性条件初判 | 概览+条件满足情况 |
| 3.技能匹配 | 逐项分析必备技能 | 每项匹配等级+小结 |
| 4.软性素质 | 加分技能+软性素质 | 加分项+素质评分 |
| 5.综合评分 | 评分+决策建议+面试考察点 | 综合分+推荐等级 |

每步完成输出 `✓ [步骤X/5] 已完成`。

## 可选分支

| 分支 | 触发条件 | 参考 |
|------|---------|------|
| 批量处理 | 多份简历 | [references/batch-analysis-format.md](references/batch-analysis-format.md) |
| FABM猎头报告 | 生成推荐报告 | [references/fabm-model-guide.md](references/fabm-model-guide.md) + [assets/recommendation-report-template.html](assets/recommendation-report-template.html) |
| 虚假简历识别 | 验证真实性 | [references/resume-verification-guide.md](references/resume-verification-guide.md) |
| JD生成 | 生成标准JD | [references/jd-generation-prompt.md](references/jd-generation-prompt.md) |
| ATS通过率 | 含ATS分析 | [references/prompt-templates.md](references/prompt-templates.md) §2 |
| 面试题库 | 面试准备 | [references/interview-question-guide.md](references/interview-question-guide.md) |
| offer决策 | 录用决策 | [references/offer-decision-guide.md](references/offer-decision-guide.md) |

## 输入校验

| 校验项 | 要求 | 异常处理 |
|-------|------|---------|
| 简历文件 | 存在+格式正确(docx/doc/pdf) | 不存在/格式错→报错停止 |
| 岗位JD | 内容完整含必要字段 | 缺失→提示补充 |
| 评分结果 | 分数0-100 | 超范围→归一化 |

## 输出格式

**默认**：交互式HTML（本地内嵌禁止CDN）+ Excel汇总

**Excel 16项必填字段**：姓名、性别、年龄、电话(脱敏)、邮箱(脱敏)、所在地、意向岗位、工作年限、最高学历、毕业院校、专业、技能标签、核心经历摘要、项目亮点、匹配度(%)、备注

**文件命名**：`简历批量分析_{类型}_{YYYYMMDD}_{人数}人.{扩展名}`

## 完整范例

### 范例：单份简历匹配分析

> 候选人张XX应聘互联网产品经理，匹配度78%（B级），核心优势是5年B端产品经验+支付领域深耕，短板是缺乏AI产品经验。

**硬性条件**：本科及以上学历✓、3年以上产品经验✓（5年）、有支付/金融领域经验✓

**必备技能匹配**：
| 技能 | 匹配等级 | 说明 |
|------|---------|------|
| 需求分析 | A(90%) | 5年B端需求分析经验，有完整方法论 |
| 数据驱动 | B(75%) | 会用SQL+埋点分析，深度一般 |
| 项目管理 | B(80%) | 敏捷开发经验丰富，跨部门协调偏弱 |
| AI产品 | D(30%) | 无AI产品经验，仅了解概念 |

**软性素质**：逻辑清晰(A)、表达流畅(A)、团队协作(B)、创新思维(C)

**综合评分**：78分，B级推荐。建议重点考察AI学习意愿和跨部门协调案例。

## 资源索引

### 脚本
| 脚本 | 用途 |
|------|------|
| [scripts/parse_resume.py](scripts/parse_resume.py) | 解析Word/PDF简历 |
| [scripts/mask_sensitive_info.py](scripts/mask_sensitive_info.py) | 隐私脱敏 |
| [scripts/candidate-database.py](scripts/candidate-database.py) | 候选人库 |

### 参考文档
| 文档 | 何时读取 |
|------|---------|
| [references/prompt-templates.md](references/prompt-templates.md) | 匹配分析/快速评分/分步思考 |
| [references/assessment-standards.md](references/assessment-standards.md) | 综合评估+薪资标准 |
| [references/fabm-model-guide.md](references/fabm-model-guide.md) | FABM推荐报告 |
| [references/star-method-template.md](references/star-method-template.md) | STAR法则 |
| [references/resume-verification-guide.md](references/resume-verification-guide.md) | 虚假简历识别 |
| [references/data-security-guide.md](references/data-security-guide.md) | 数据安全合规 |
| [references/image-usage-guide.md](references/image-usage-guide.md) | HTML图片规范 |
| [references/batch-analysis-format.md](references/batch-analysis-format.md) | 批量分析规范 |
| [references/industry-adaptation-templates.md](references/industry-adaptation-templates.md) | 4行业适配模板 |
| [references/job-spec-template.md](references/job-spec-template.md) | 岗位说明书模板 |
| [references/jd-generation-prompt.md](references/jd-generation-prompt.md) | JD生成 |
| [references/collab-review-guide.md](references/collab-review-guide.md) | 协作评审 |
| [references/ats-integration-guide.md](references/ats-integration-guide.md) | ATS对接 |
| [references/history-data-guide.md](references/history-data-guide.md) | 历史数据 |
| [references/interview-question-guide.md](references/interview-question-guide.md) | 面试题库 |
| [references/offer-decision-guide.md](references/offer-decision-guide.md) | offer决策 |

### 输出资产
| 资产 | 用途 |
|------|------|
| [assets/report-template.html](assets/report-template.html) | 分析报告HTML模板 |
| [assets/recommendation-report-template.html](assets/recommendation-report-template.html) | FABM推荐报告模板 |
| [assets/batch-summary-template.md](assets/batch-summary-template.md) | Excel汇总模板 |

---

## 版权声明与使用协议
**版权所有 @HR×AI Agent实战派**

### 知识产权声明
- 本技能的核心算法、业务逻辑、数据模型及可视化方案均为原创知识产权
- HTML模板、图表配色方案、报告结构为独家设计，受著作权保护
- 禁止未经授权的二次分发、逆向工程、商业转售

### 授权使用范围
- 个人学习、内部使用、非商业用途可自由使用
- 禁止本技能进行二次开发和改进
- 虾评平台内的下载、安装、评测等正常使用行为
- 禁止剥离版权声明后重新发布为"原创"技能
- 禁止用于商业产品或收费服务（需单独授权）

### 商业合作
- 如需商业授权或定制开发，请通过虾评平台联系开发者。
