---
name: jd-candidate-matching
description: 基于JD解析与AI匹配评分的完整人才搜寻方案，支持多平台岗位解析、FABM推荐报告、可视化画像、智能评分卡、数据复盘看板、候选人库管理、全周期汇报复盘（金字塔+KISS+敏捷）；当用户需要进行JD解析、候选人匹配、简历筛选、FABM报告生成、候选人管理、数据复盘、招聘决策支持、日报/周报/月报生成或构建AI辅助人才搜寻体系时使用
---

# AI辅助人才搜寻工作流

## 任务目标
- 本Skill用于：从多平台JD解析到人才IPO模拟的完整AI辅助人才搜寻与评估流程
- 能力包含：多平台岗位解析、JD结构化解析、技能矩阵生成、人才搜寻策略、候选人匹配评分、优先级排序、FABM推荐报告（5套标准化模板）、可视化候选人画像、智能评分卡、虚假简历识别、候选人管理、入职护航、人才IPO模拟、猎头速查助手（20+场景）、数据复盘看板（招聘漏斗/渠道ROI/留存预测）、ATS简历通过率分析、候选人库管理（50+批量操作）、协作评审、简历解析优化、数据Marketplace、薪酬谈判支持、全周期汇报复盘（金字塔+KISS+敏捷）
- 触发条件：需要进行JD解析、候选人匹配、简历筛选、FABM报告、候选人管理、数据复盘、招聘决策支持、日报/周报/月报生成

## 架构概览

### 三大核心环节

| 环节 | 核心功能 | 效率提升 |
|------|---------|---------|
| 环节1：JD解析 | 多平台解析、技能矩阵 | 时间压缩80%+（基于行业AI辅助招聘基准估算） |
| 环节2：人才搜寻 | 关键词生成、人才地图 | 效率提升200%（基于行业基准估算） |
| 环节3：简历筛选 | 匹配评分、排序 | 人力减少70%（基于行业基准估算） |

### 三大增值模块

| 模块 | 核心功能 | 核心价值 |
|------|---------|---------|
| 环节4：FABM推荐报告 | 黄金公式、STAR成就 | 提升推荐说服力 |
| 环节5：虚假简历识别 | 三道防线、结构化验证 | 保护专业信誉 |
| 环节6：候选人管理 | SCARF模型、入职护航 | 提升留存率25%+（基于行业基准估算） |
| 环节7：人才IPO模拟 | 投资模型、成长评估 | 升级为价值发现者 |

## 前置准备

### 依赖说明
- 无特殊技术依赖，智能体可直接执行
- 用户需准备：JD文本、候选人信息
- Prompt模板：见 [assets/prompt-templates.md](assets/prompt-templates.md)

### 合规准备
- 阅读 [references/compliance-guide.md](references/compliance-guide.md) 了解合规红线
- 确认所有操作在主流招聘平台平台内完成
- 不进行自动化抓取、不存储未经授权的个人信息

## 操作步骤

### 环节1：JD解析

1. **获取JD文本**（人工）：从Boss直聘/智联/前程无忧/拉勾/猎聘/主流招聘平台/鱼泡/LinkedIn/脉脉复制
2. **AI解析JD**（智能体）：参考 [assets/prompt-templates.md](assets/prompt-templates.md)
   - 提取：核心职责、硬性条件、软性素质、技能矩阵、人才画像
   - 效率数据：15-20分钟->2-3分钟，时间压缩80%+（基于行业AI辅助招聘基准估算）
   - 详细标准：见 [references/jd-parsing-guide.md](references/jd-parsing-guide.md)
3. **人工审核微调**（人工）：检查准确性，调整不合理部分

### 环节2：人才搜寻

1. **生成搜索关键词**（智能体）：10-20组关键词组合
2. **生成人才地图**（智能体）：目标公司名单
   - 详细指南：见 [references/talent-search-guide.md](references/talent-search-guide.md)
3. **平台内搜索执行**（人工）：在主流招聘平台平台搜索
4. **外部信息辅助**（可选人工）：LinkedIn公开档案、X-ray搜索

### 环节3：简历筛选

1. **获取简历文本**（人工）：从主流招聘平台平台获取
2. **AI匹配评分**（智能体）：
   - 参考 [references/matching-criteria.md](references/matching-criteria.md)
   - 硬性指标60%+软性指标30%+优先条件10%
   - 匹配精度：匹配精度目标（设计值）：准确率>=85%、召回率>=80%
3. **优先级排序**（智能体）：按匹配度排序
4. **生成匹配报告**（智能体）：参考 [assets/report-template.md](assets/report-template.md)
5. **人工执行推荐**（人工）：在平台内推荐候选人

### 环节4：FABM推荐报告

1. **理解FABM模型**（智能体指导）：
   - F(Features)基础信息 -> A(Achievements)关键成就 -> B(Benefits)客户价值 -> M(Motivation)跳槽动机
   - 详细指南：见 [references/fabm-report-guide.md](references/fabm-report-guide.md)
2. **生成FABM报告**（智能体）：5套标准化模板（技术研发/销售/运营/管理/职能）
3. **人工审核优化**（人工）：验证真实性，优化说服力

### 环节5：虚假简历识别

1. **简历初筛**：三道防线检测
   - 详细指南：见 [references/resume-verification-guide.md](references/resume-verification-guide.md)
2. **面试追问**：深挖疑点
3. **背景调查**：第三方验证

### 环节6：候选人管理

1. **候选人识别**：3分钟读懂简历、SCARF心理模型
   - 详细指南：见 [references/candidate-management-guide.md](references/candidate-management-guide.md)
2. **离职期防反水**：CounterOffer应对、交接清单
3. **入职护航**：第一周陪伴、30/60/90天复盘
4. **保证期深绑定**：终身关系经营

### 环节7：人才IPO模拟

1. **四大维度评估**：赛道/团队/壁垒/增速
2. **结构化提问**：获取成长性证据
3. **人才投资价值报告**：为客户构建成长叙事
   - 详细指南：见 [references/talent-ipo-guide.md](references/talent-ipo-guide.md)

## 使用示例

### 示例1：JD解析与候选人匹配
- 场景：用户上传技术岗位JD，需要匹配合适候选人
- 预期产出：结构化JD摘要、技能矩阵、候选人匹配评分报告
- 关键点：多平台支持、合规操作、人工执行搜索和推荐

### 示例2：FABM推荐报告生成
- 场景：用户提供候选人简历，需要生成推荐报告
- 预期产出：FABM格式推荐报告，含STAR成就、客户价值
- 关键点：选择对应岗位类型模板、验证信息真实性

### 示例3：数据复盘看板
- 场景：用户需要分析招聘漏斗和渠道ROI
- 预期产出：可视化看板、三张表数据、改进建议
- 关键点：ATS简历通过率追踪、渠道效率对比

## 资源索引

### 核心参考文档
- [references/jd-parsing-guide.md](references/jd-parsing-guide.md) - JD解析标准与指南
- [references/matching-criteria.md](references/matching-criteria.md) - 候选人匹配评分标准（含验证案例）
- [references/fabm-report-guide.md](references/fabm-report-guide.md) - FABM报告完整指南（5套模板）
- [references/resume-verification-guide.md](references/resume-verification-guide.md) - 虚假简历识别指南
- [references/candidate-management-guide.md](references/candidate-management-guide.md) - 候选人全流程管理指南
- [references/talent-ipo-guide.md](references/talent-ipo-guide.md) - 人才IPO模拟方法论
- [references/headhunter-quick-ref-guide.md](references/headhunter-quick-ref-guide.md) - 猎头速查助手（20+场景）
- [references/headhunter-data-review-guide.md](references/headhunter-data-review-guide.md) - 数据复盘看板（含招聘漏斗/渠道ROI/留存预测）
- [references/ats-resume-throughput-guide.md](references/ats-resume-throughput-guide.md) - ATS简历通过率分析（本地）
- [references/candidate-database-guide.md](references/candidate-database-guide.md) - 候选人库管理
- [references/collaborative-review-guide.md](references/collaborative-review-guide.md) - 协作评审
- [references/salary-reference-guide.md](references/salary-reference-guide.md) - 薪资参考与Marketplace
- [references/candidate-profile-guide.md](references/candidate-profile-guide.md) - 可视化画像与智能评分卡
- [references/user-experience-guide.md](references/user-experience-guide.md) - 用户体验优化
- [references/compliance-guide.md](references/compliance-guide.md) - 合规指南（红线规范+个人数据保护DCMM 2.0）
- [references/periodic-report-guide.md](references/periodic-report-guide.md) - 全周期汇报复盘标准化模板（金字塔+KISS+敏捷）
- [references/document-output-guide.md](references/document-output-guide.md) - 文档输出格式指南
- [references/salary-reference-guide.md](references/salary-reference-guide.md) - 薪资参考指南
- [references/multi-platform-jd-guide.md](references/multi-platform-jd-guide.md) - 多平台JD解析
- [references/output-template.md](references/output-template.md) - 输出模板
- [references/talent-search-guide.md](references/talent-search-guide.md) - 人才搜寻指南

### Prompt模板
- [assets/prompt-templates.md](assets/prompt-templates.md) - 完整Prompt模板库

### 报告模板
- [assets/report-template.md](assets/report-template.md) - 报告模板（含多候选人对比模板）

### Python脚本
- [scripts/cleanup_unicode.py](scripts/cleanup_unicode.py) - Unicode清理脚本

## 合规要求

### 三条红线
1. **反爬虫条款**：禁止自动化抓取
2. **数据隐私**：禁止未经授权存储
3. **知识产权**：禁止大规模复制

### 技术安全标准
- HTML图表：CDN禁止，ECharts等库必须内嵌
- 所有图片：base64内嵌，不引用外部URL
- PDF/Word/PPT/Excel：图片完整嵌入，不依赖外部链接

### 数据规范
- 日期字段：必须使用真实系统时间
- 脱敏处理：上传附件前必须完成脱敏
- 交付格式：默认统一输出HTML版（交互式HTML + PDF）

### 匹配精度目标
- 准确率：>=85%
- 召回率：>=80%
- F1分数：>=82%

### 效率提升目标
- JD解析：时间压缩80%+（基于行业AI辅助招聘基准估算）（15-20分钟->2-3分钟）
- 人才搜寻：效率提升200%（基于行业基准估算）
- 简历筛选：人力减少70%（基于行业基准估算）（2.4分钟->0.7分钟）

## 注意事项
- 详细内容请阅读各参考文档
- 合规红线必须严格遵守
- 所有操作优先人工执行，智能体提供辅助
- 报告输出前验证：在线正常->断网正常->下载正常->多浏览器兼容

## 版权声明

本技能为HR×AI Agent 实战派（hr_aiagent）原创，版权所有，严禁盗用、二次改编及商用。一经查实侵权行为，将依法开展维权处理。