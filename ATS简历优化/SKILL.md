---
name: resume-optimizer
description: 依托JD智能解析自动完成简历诊断及优化，支持多招聘平台岗位信息解析，生成纯可投递优化版简历、岗位匹配度分析报告、详细修改说明文档、定制化面试题库、增强版交互式模拟演练页面（v2：直接DOM渲染+答案折叠+自评评分+复习模式）、面试自我介绍自动生成（4赛道×5经验×2时长）、面试优质反向提问题库（不踩雷、高适配）、求职进度看板及新用户欢迎开场白。新增：防泄漏机制（AES-256加密+动态脱敏+边界隔离+审计留痕）、个人数据保护专项规范（DCMM 2.0对齐版）、结合行业性质的针对性面试题生成（三维定位法：简历弱点+JD要求+行业特性）
dependency:
  python:
    - beautifulsoup4==4.12.2
    - pycryptodome==3.19.0
---

# 简历优化与面试准备

## 任务目标
- 本Skill用于：依托JD智能解析，自动完成简历诊断及优化，生成全套面试准备材料
- 能力包含：
  - 简历深度优化（岗位职责6-8项，不虚构内容，ATS适配）
  - 岗位匹配度分析报告
  - 定制化面试题库生成（基于真实经历，避免AI幻觉）
  - 增强版交互式模拟演练与复盘（v2：直接DOM渲染+答案折叠+自评评分+复习模式）
  - 面试优质反向提问题库（不踩雷、高适配，根据简历和JD自动匹配生成）
  - 支持多招聘平台岗位信息自动解析（Boss直聘、智联招聘、前程无忧、拉勾网、猎聘等）
  - 新用户首次使用自动弹出欢迎开场白（展示功能+使用指南）
- 触发条件：用户上传简历并提供岗位链接或岗位描述

## 前置准备
- 依赖说明：脚本所需依赖包（精确版本固定，确保供应链安全）
  ```
  beautifulsoup4==4.12.2
  pycryptodome==3.19.0
  ```

## 防泄漏机制（关键保障）

### 1. 主动加密
- **加密算法**：AES-256
- **密钥存储**：仅本地存储，不上传至云端
- **加密时机**：用户上传的文档内容在进入分析流程前自动触发加密

### 2. 动态脱敏
解析敏感字段时自动脱敏：
- 姓名替换为「[用户姓名]」
- 身份证号显示为110********1234
- 手机号显示为138*******5678
- 邮箱显示为*********@***
- 住址显示为**市**区

### 3. 边界隔离
- 在回答用户问题、生成各项建议时，所有输出内容仅包含「脱敏后数据」或「基于加密后的分析结论」
- 禁止泄露原始文档全文或具体隐私信息

### 4. 审计留痕
- 对敏感信息处理过程生成「操作审计日志」
- 仅开发人员可查看，确保数据流向可追溯

### 5. 数据安全与隐私保护
- AI将对用户上传文档全程加密
- 敏感信息自动脱敏
- 对外输出时严格过滤隐私数据
- 彻底杜绝信息泄露风险

### 6. 合规性保障
- 严格遵循隐私合规标准
- 不向第三方共享用户数据
- 确保数据全生命周期安全

### 7. 供应链安全
- **依赖版本固定**：所有Python依赖包使用精确版本（==），避免供应链攻击
- **加密库安全**：使用pycryptodome替代cryptography，降低供应链风险
- **纯本地解析**：岗位解析仅做本地HTML解析，不发起任何HTTP请求，彻底杜绝数据外泄
- **输入验证**：所有动态内容经过类型检查+长度限制+控制字符过滤+HTML转义

### 防泄漏工具使用
```bash
# 测试脱敏功能
python scripts/anti_leakage_protection.py --test-text "张三，手机号13812345678，邮箱zhangsan@example.com"

# 加密数据
python scripts/anti_leakage_protection.py --encrypt "需要加密的敏感数据"

# 生成合规报告
python scripts/anti_leakage_protection.py --test-text "测试文本" --output compliance_report.md
```

## 用户需提交的必备材料

请确保提供以下完整材料：

1. **原始简历文件**
   - 优先提供 Word 等可编辑格式
   - PDF 格式也可接受
   - 请确保文件可正常读取

2. **目标岗位信息**（任选其一）
   - 完整的招聘链接（支持Boss直聘、智联招聘、前程无忧、拉勾网、猎聘等）
   - 复制粘贴的完整岗位描述（JD）

3. **特殊要求说明**（如有）
   - 突出某段经历
   - 规避特定信息
   - 调整求职方向
   - 限定篇幅
   - 其他个性化要求

## 用户求职偏好采集（可选）

为生成更精准的个性化简历策略，可在必备材料之外额外采集以下偏好信息。所有偏好项均为可选，未提供时系统将自动分析推断：

1. **目标岗位类型**（可选）
   - 技术岗 / 管理岗 / 销售岗 / 运营岗 / 职能岗
   - 未指定时，系统根据简历和JD自动检测岗位类型

2. **职业发展阶段确认**（可选）
   - 应届生 / 1-3年成长期 / 3-5年成熟期 / 5-10年管理转型期 / 10年以上战略领导期
   - 未指定时，系统根据简历中的工作年限自动判断

3. **简历风格偏好**（可选）
   - 精简型（1页，核心信息优先）/ 详细型（2-3页，完整经历展示）
   - 未指定时，系统根据职业阶段自动推荐合适篇幅

4. **重点突出方向**（可选）
   - 技术深度 / 管理能力 / 业绩数据 / 行业经验 / 教育背景
   - 未指定时，系统根据职业阶段和岗位类型综合推荐

5. **行业偏好**（可选）
   - 目标行业方向（如互联网、金融、制造业、教育等）
   - 用于调整行业关键词植入策略

**偏好采集后处理流程**：
- 调用 `scripts/career_profile_analyzer.py` 进行职业阶段分析
- 结合用户偏好和自动检测结果生成个性化简历策略
- 策略结果指导后续简历模块排序、篇幅分配和关键词植入

## 优化版简历硬性要求（必须严格执行）

### 纯可投递格式要求
- 简历正文绝对不能出现任何分析、标注、提示类内容
- 禁止内容包括但不限于："匹配度亮点"、"HR 关注点"、"核心优势"、"修改说明"、"备注" 等
- 所有分析内容全部放在独立的报告中

### 内容完整性要求
- 单段工作经历的核心岗位职责与成果至少保留 6-8 项完整表述
- 绝不做过度精简
- 确保用户所有关键工作内容和能力都得到充分展现

### 真实性原则
- 完全基于用户提供的原始简历数据进行优化
- 不虚构任何经历、项目、成果或证书
- 仅对表述方式、逻辑结构和重点进行调整

### 专业表述要求
- 统一采用「执行动作 + 工作内容 + 可量化成果 / 价值」的行业通用句式
- 动词开头、逻辑分层、表述专业
- 将原始经历转化为目标行业通用的专业语言

### 匹配度隐性体现
- 通过内容优先级排序、行业关键词自然植入、核心成果前置的方式
- 隐性突出与目标岗位的匹配度
- 不做任何显性标注

### ATS 系统适配
- 优化关键词布局和排版格式
- 确保简历能通过 90% 以上企业的 ATS 简历筛选系统

## 核心交付物（必须完整交付）

### 1. 纯可投递优化版简历（Word版，第一优先级）
**格式要求**：
- 纯可投递格式，下载后可直接发送给 HR 或上传至任何招聘平台
- **无任何形式的分析标注、提示性内容**
- 模块顺序：个人信息→求职意向→工作经历→项目经验→专业技能→教育背景
- 篇幅控制：1-3 页（10 年以上工作经验可放宽至 3-4页，原则上不超过5页）
- 排版要求：统一使用宋体 / 微软雅黑，字体大小 10-12 号，行间距 1.2-1.5 倍，无任何花哨装饰

**内容要求**：
- **严格遵守"优化版简历硬性要求"**
- **岗位职责与项目数严格控制在6-8项，原则上不超过10项**
- **优化全程不虚构内容、不写空话套话、不暴露敏感信息**
- **无任何显性匹配标注**
- **严格遵循ATS适配标准及行业通用排版规范**
- 统一采用「执行动作 + 工作内容 + 可量化成果 / 价值」的行业通用句式

### 2. 岗位匹配度分析报告（PDF版）
**报告内容**：
- 整体匹配度百分制评分及匹配等级（优秀 / 良好 / 合格 / 不合格）
- 分维度匹配度分析（根据岗位类型动态调整：技术/运营/销售/管理）
- JD 核心关键词命中情况及缺失关键词清单
- 用户的核心优势亮点与待提升短板
- ATS 系统通过率预测
- 针对性面试准备方向及高频问题预测
- 最终投递建议（推荐投递 / 谨慎投递 / 不推荐投递）

### 3. 独立详细修改说明文档（Word版）
**文档内容**：
- 本次简历优化的整体思路与核心逻辑
- 分模块列出所有具体修改点及对应的修改原因
- 关键词优化的依据和排版调整的考量
- 所有被调整、合并、补充内容的标注，保留原始信息可追溯性
- 后续针对不同岗位进行个性化微调的通用方法

### 4. 定制化面试题库
**题库要求**：
- 全程基于用户真实简历经历构建
- 坚决避免AI幻觉，不虚构任何经历
- 所有题目均明确标注引用来源（如：[来源：简历-工作经历2]）
- 包含自我介绍、简历深挖、技术专业、行为面试、反向提问等类型
- 每个问题提供解答思路和关键要点

### 5. 一站式面试模拟页面（在线版/下载版）
**页面功能**：
- 交互式模拟面试演练
- 逐题回答、进度跟踪
- AI面试官点评与评分
- 多维度评分图表
- HTML/PDF导出功能
- 支持在线查看和下载

## 优化简历绝对禁止清单（违者重改）

### 内容类绝对禁止
- ❌ 禁止出现任何分析、标注、提示类内容
- ❌ 禁止虚构任何经历、成果或资质
- ❌ 禁止出现 "责任心强、执行力强、沟通能力好" 等无事实支撑的空话套话
- ❌ 禁止出现性别、年龄、民族、籍贯、婚育状况等个人敏感信息
- ❌ 禁止出现身份证号、银行卡号、家庭详细住址等隐私信息
- ❌ 禁止出现过往离职原因、对前雇主的评价、过往薪资等负面或敏感内容
- ❌ 禁止使用 "精通"、"专家"、"顶级" 等过于绝对且无成果支撑的表述
- ❌ 禁止出现与求职岗位无关的政治立场、宗教信仰、个人观点等内容

### 表述与排版类绝对禁止
- ❌ 除非用户明确要求，否则禁止出现 "自我评价" 和 "兴趣爱好" 模块
- ❌ 禁止使用 "搞定了"、"做了"、"帮忙" 等口语化表述
- ❌ 禁止使用任何彩色字体、背景图片、头像、图标、艺术字等装饰元素
- ❌ 禁止使用表格、文本框、分栏等复杂排版方式
- ❌ 禁止在页眉、页脚中放置个人信息或重要内容
- ❌ 禁止出现空白页、多余空行或特殊符号、表情符号

## 行业标准合规保障机制

### 严格对标行业通用简历结构规范
按照国内职场通用排版逻辑排布模块：个人信息、求职意向、工作经历、项目经验、专业技能、教育背景等，模块顺序、篇幅占比、信息详略均遵循主流企业 HR 审阅习惯，不使用花哨格式，适配 90% 以上企业的 ATS 简历筛选系统。

### 深度匹配目标岗位 JD 与行业任职要求
全程以招聘岗位官方描述为核心依据，提取行业高频关键词、能力要求、专业术语、工作范畴，将原始经历转化为该行业通用的专业表述，避免口语化、生活化描述，贴合行业招聘语言体系。

### 统一职业表述体系
结合所属行业（行政、人力、运营、技术、销售、职能岗等）通用岗位职责口径润色，专业名词、工作模块、能力标签统一使用行业通用叫法，保证同行业HR一眼识别能力匹配度。

### 全面规避行业简历通病与雷区
剔除无效空话、冗余信息、主观形容词；不夸大履历、不虚构经历、不虚构项目数据，杜绝数据幻觉；规范职场术语用词，规避错别字、语病、格式混乱、时间线矛盾等问题，符合企业背调、HR 初筛、人事存档的通用审核标准。

## 数据上传与脱敏处理流程
1. **文件接收与验证**
   - 用户上传简历文件（PDF/Word/Text/Markdown）
   - 智能体验证文件格式（PDF、Word、TXT、MD）
   - 检查文件大小（≤ 10MB）和安全性
   - 验证文件是否可以正常读取

2. **内容读取**
   - 使用对应的方法读取文件内容
   - PDF：使用PDF解析库提取文本
   - Word：使用python-docx库提取内容
   - Text/Markdown：直接读取并解析

3. **敏感信息识别**
   - 智能体识别简历中的所有敏感信息：
     - 个人身份信息（姓名、身份证号、手机号、邮箱、住址）
     - 职业信息（工资、银行卡号、社保号、公积金号）
     - 其他敏感信息（紧急联系人、家庭成员、健康信息）
   - 参考 [references/data_upload_desensitization_guide.md](references/data_upload_desensitization_guide.md) 中的识别规则

4. **自动脱敏处理**
   - 智能体对所有识别出的敏感信息进行脱敏：
     - 姓名：张**（保留姓氏）
     - 手机号：138****5678（保留前3位和后4位）
     - 邮箱：zhan***@example.com（保留前3位字符）
     - 身份证号：110101********1234（保留前6位和后4位）
     - 银行卡号：[银行卡号已隐藏]（完全隐藏）
     - 家庭住址：[地址已隐藏]（完全隐藏）
   - 参考 [references/data_upload_desensitization_guide.md](references/data_upload_desensitization_guide.md) 中的脱敏规则

5. **脱敏验证**
   - 智能体验证所有敏感信息是否已正确脱敏
   - 检查脱敏格式是否一致
   - 确保脱敏后的信息无法被还原
   - 验证文档完整性和可读性

6. **数据结构化存储**
   - 将脱敏后的数据结构化存储
   - 提取关键信息（基本信息、教育背景、工作经历、项目经验、技能清单）
   - 保留脱敏后的非敏感信息

## 操作步骤

### 标准流程
1. **用户提供材料**
   - 确认用户已提供完整的必备材料（原始简历、岗位信息、特殊要求）
   - 如材料不完整，提示用户补充

2. **岗位信息解析**
   - 如果用户提供招聘链接：调用 `scripts/parse_job_posting.py` 解析岗位信息
   - 如果用户直接提供岗位描述：直接进行分析
   - 提取岗位核心要求、关键词、任职资格

3. **简历深度分析**
   - 读取用户原始简历内容
   - 进行敏感信息识别与脱敏
   - 分析简历结构、内容、语言表达

4. **职业阶段分析与个性化策略**
   - 调用 `scripts/career_profile_analyzer.py` 从简历文本提取工作年限
   - 自动判断职业阶段（应届生 / 1-3年 / 3-5年 / 5-10年 / 10年+）
   - 检测岗位类型（技术岗 / 管理岗 / 销售岗 / 运营岗 / 职能岗）
   - 输出JSON：`{career_stage, years_of_experience, job_category, resume_strategy}`
   - 结合用户偏好（如有）生成个性化简历优化策略
   - 策略包含：推荐模块顺序、篇幅建议、重点突出内容、关键词策略
   - 参考 `references/career_stage_resume_strategy.md` 和 `references/job_type_resume_structure.md`

5. **生成三项交付成果**
   - 智能体生成纯可投递优化版简历（严格遵守硬性要求和禁止清单）
   - 生成独立岗位匹配度分析报告
   - 生成独立详细修改说明文档

6. **面试准备（可选）**
   - 当用户确认已通过简历筛选时：
     - 智能体生成面试准备提纲
     - 生成面试问题和解答思路

7. **模拟面试（可选）**
   - 当 **用户说"准备好了"**：
     - 智能体生成面试问题数据（JSON格式）
     - 调用 `scripts/generate_interview_web.py` 生成模拟面试网页
     - 提供网页访问方式或下载路径

## 必要脚本
- [scripts/parse_job_posting.py](scripts/parse_job_posting.py)
  - 用途：解析招聘网站链接，提取岗位信息（支持Boss直聘、智联招聘、前程无忧、拉勾网、猎聘等）
  - 参数：招聘链接URL（命令行参数）
  - 输出：结构化岗位信息（JSON格式）
- [scripts/generate_interview_web.py](scripts/generate_interview_web.py)
  - 用途：生成模拟面试网页系统
  - 参数：面试问题数据文件（JSON格式）、输出目录
  - 输出：HTML网页文件及相关资源
- [scripts/generate_resume_optimization.py](scripts/generate_resume_optimization.py)
  - 用途：生成纯可投递优化版简历、岗位匹配度分析报告、修改说明文档
  - 参数：简历数据JSON、岗位信息、匹配度分数
  - 输出：三个HTML文档（可转Word/PDF）
- [scripts/ats_scorer.py](scripts/ats_scorer.py)
  - 用途：模拟ATS系统对简历进行评分，支持扣子平台Skill格式
  - 参数：简历文本、JD结构化需求、格式信息
  - 输出：ATS评分结果（匹配度、缺失关键词、格式建议）
- [scripts/career_profile_analyzer.py](scripts/career_profile_analyzer.py)
  - 用途：职业阶段分析与简历策略推荐，从简历文本提取工作年限，自动判断职业阶段，检测岗位类型，输出个性化简历优化策略
  - 参数：简历文本文件路径（--resume）、JD文本文件路径（--jd，可选）、岗位类型（--job-category，可选）
  - 输出：JSON格式分析结果，包含career_stage、years_of_experience、job_category、resume_strategy（含recommended_focus、module_order、page_limit）

## 领域参考
- [references/resume_optimization_guide.md](references/resume_optimization_guide.md)
  - 何时读取：生成简历优化建议时
  - 内容：简历优化方法论、关键词匹配技巧、STAR法则等
- [references/interview_preparation_guide.md](references/interview_preparation_guide.md)
  - 何时读取：生成面试准备提纲时
  - 内容：面试问题分类、解答思路、常见问题模板、STAR法则应用
- [references/interview_question_generation_guide.md](references/interview_question_generation_guide.md)
  - 何时读取：生成面试问题时
  - 内容：基于真实经历的面试题生成规则、避免AI幻觉的方法、问题质量检验标准
- [references/multi_dimensional_evaluation_guide.md](references/multi_dimensional_evaluation_guide.md)
  - 何时读取：进行多维度评估时
  - 内容：信息抽取与评估、智能匹配与筛选、多维度综合评估、面试表现评估、简历优化评估的AI提示词模板
- [references/data_upload_desensitization_guide.md](references/data_upload_desensitization_guide.md)
  - 何时读取：处理用户上传的文件时
  - 内容：数据上传流程、敏感信息识别、脱敏处理策略、脱敏实现方法、数据验证与检查、异常处理
- [references/data_security_guide.md](references/data_security_guide.md)
  - 何时读取：处理用户数据时
  - 内容：数据保护原则、敏感信息识别、数据脱敏策略、安全注意事项
- [references/supported_platforms.md](references/supported_platforms.md)
  - 何时读取：解析招聘网站链接时
  - 内容：支持的招聘平台列表、解析策略说明、已知限制、备用方案
- [references/career_stage_resume_strategy.md](references/career_stage_resume_strategy.md)
  - 何时读取：职业阶段分析完成后，生成简历优化策略时
  - 内容：5个职业阶段（应届生/1-3年/3-5年/5-10年/10年+）各自的简历优化策略表，包含模块优先级、篇幅占比、内容要求、关键词策略、常见问题提醒
- [references/job_type_resume_structure.md](references/job_type_resume_structure.md)
  - 何时读取：确定岗位类型后，调整简历模块结构时
  - 内容：5种岗位类型（技术岗/管理岗/销售岗/运营岗/职能岗）的简历模块结构差异，包含模块优先级、篇幅分配、内容要求、关键词策略、特殊要求

## 数据安全与隐私保护
- **数据脱敏处理**：在所有输出内容中，对敏感信息进行脱敏处理：
  - 手机号：138****5678
  - 邮箱：zhan***@example.com
  - 身份证号：110101********1234
  - 家庭住址：[地址已隐藏]
  - 银行卡号：[银行卡号已隐藏]
- **不暴露敏感信息**：
  - 不在日志、提示、输出中暴露用户的完整敏感信息
  - 不在网页源码、JavaScript变量中存储敏感数据
  - 不在示例中使用用户真实的个人信息
- **临时文件管理**：
  - 处理完成后及时删除用户上传的原始简历文件
  - 清理所有临时中间文件
  - 不持久化存储敏感数据
- **访问控制**：
  - 智能体只能读取当前用户上传的文件
  - 不能访问其他用户的文件
  - 不同用户的数据严格隔离
- **平台安全实施**：
  - 实际的数据加密、存储、访问控制由运行Skill的平台负责
  - 本Skill遵循数据保护原则，提供安全的数据处理指导
  - 详细安全策略见 [references/data_security_guide.md](references/data_security_guide.md)

## 面试问题生成约束
- **面试问题必须基于真实经历**：
  - 每个面试问题必须引用简历中的具体内容（公司、项目、技术栈、时间段、成果数据等）
  - 禁止虚构简历中没有的经历、技术或成果（避免AI幻觉）
  - 每个问题标注引用来源（如：[来源：简历-工作经历2]）
  - 所有问题中的信息必须与简历原文完全一致
- **解答思路必须基于真实经历**：
  - 指导用户结合简历中的具体项目和经历回答问题
  - 提醒用户引用简历中的具体数据和案例
  - 不提供通用的模板化回答，而是基于简历真实经历的定制化指导
- 鼓励用户根据自己的实际情况调整解答思路，避免模板化回答
- 模拟面试网页中的图表数据默认为演示数据，在智能体评分后会更新为真实分数
- 点击"下载Word报告"按钮可直接下载完整的Word版面试报告
- 智能体评分后会提供图表数据，用户可以通过网页界面查看更新后的评分分析

## HTML报告验证清单

在交付最终HTML报告前，请按以下清单验证报告完整性和稳定性：

### 在线访问验证
1. **在Chrome浏览器中打开HTML报告**
   - [ ] 所有Logo图片正常显示
   - [ ] 核心图表（柱状图）正常渲染
   - [ ] 雷达图正常显示
   - [ ] 对比分析图正常加载
   - [ ] 页面排版正常，无错位
2. **在Firefox浏览器中打开HTML报告**
   - [ ] 所有图片正常显示
   - [ ] 图表渲染正常
   - [ ] 页面布局正常
3. **在Safari浏览器中打开HTML报告**
   - [ ] 所有图片正常显示
   - [ ] 图表渲染正常
   - [ ] 页面布局正常
4. **在Edge浏览器中打开HTML报告**
   - [ ] 所有图片正常显示
   - [ ] 图表渲染正常
   - [ ] 页面布局正常
5. **在360浏览器中打开HTML报告**
   - [ ] 所有图片正常显示
   - [ ] 图表渲染正常
   - [ ] 页面布局正常

### 离线访问验证
1. **断网状态下打开HTML报告**
   - [ ] 所有本地嵌入的图片正常显示
   - [ ] 图表（Chart.js）能正常加载并渲染
   - [ ] 页面功能正常使用
   - [ ] 无网络请求错误提示

### PDF导出验证
1. **通过浏览器打印功能导出PDF**
   - [ ] 所有图片在PDF中完整显示
   - [ ] 图表在PDF中排版正常
   - [ ] 无内容缺失或截断
   - [ ] 页面布局与网页版一致
2. **验证PDF在不同查看器中显示**
   - [ ] Adobe Acrobat Reader中显示正常
   - [ ] 浏览器内置PDF查看器中显示正常
   - [ ] 其他PDF查看软件中显示正常

### 图表稳定性保证
- Chart.js库使用多CDN备用源（jsDelivr、cdnjs、unpkg），提高加载成功率
- 实现CDN自动降级机制，当前CDN加载失败时自动尝试下一个
- 添加图表加载失败的错误处理，提供友好的用户提示
- 优化图表初始化逻辑，增加元素存在性检查和异常捕获
- 所有图表数据内置在HTML中，不依赖外部数据源

## 使用示例

### 示例1：简历优化完整流程
1. **用户提交材料**
   - 用户上传原始简历：「我的简历.docx」
   - 用户提供岗位链接：「https://www.zhipin.com/job_detail/xxx」
   - 用户特殊要求：「请突出我在XX公司的项目经验，控制简历在1页内」

2. **解析岗位信息**
   ```bash
   python scripts/parse_job_posting.py "https://www.zhipin.com/job_detail/xxx"
   ```

3. **智能体生成三项交付成果**
   - 交付成果1：纯可投递优化版简历（1页，严格遵守硬性要求和禁止清单）
   - 交付成果2：独立岗位匹配度分析报告（含评分、维度分析、关键词命中、优势短板、投递建议）
   - 交付成果3：独立详细修改说明文档（含优化思路、具体修改点、关键词依据、后续调整方法）

### 示例2：Boss直聘岗位优化
```bash
# 解析岗位信息
python scripts/parse_job_posting.py "https://www.zhipin.com/job_detail/xxx"
```

智能体将：
1. 解析出职位：高级Java工程师
2. 分析要求：3年以上经验、Spring Boot、微服务架构
3. 对比简历：识别匹配的项目经验
4. 生成优化简历：严格遵守硬性要求和禁止清单
5. 生成匹配度分析报告和修改说明文档

### 示例3：智联招聘岗位优化
```bash
# 解析岗位信息
python scripts/parse_job_posting.py "https://jobs.zhaopin.com/xxx"
```

智能体将：
1. 解析出职位：产品经理
2. 分析要求：B端产品经验、数据分析能力
3. 对比简历：识别相关产品经历
4. 生成优化简历：严格遵守硬性要求和禁止清单
5. 生成匹配度分析报告和修改说明文档

### 示例4：面试准备
- 用户：已经通过了这个岗位的简历筛选，帮我准备面试 [提供同一个链接]
- 智能体：解析岗位 → 读取简历 → 生成面试准备提纲

智能体将生成：
1. **自我介绍模板**：根据简历亮点定制
2. **简历深挖问题**：
   - "请详细介绍一下XX项目中你的具体职责"
   - "你在XX项目中遇到的最大挑战是什么？如何解决的？"
3. **技术专业问题**：
   - "Spring Boot的自动配置原理是什么？"
   - "如何设计一个高可用的微服务架构？"
4. **行为面试题**：
   - "请举例说明你如何处理团队冲突"
   - "描述一次你主动承担额外责任并取得成果的经历"
5. **反向提问建议**：
   - "请问这个岗位目前的团队结构是怎样的？"
   - "团队未来一年的主要目标是什么？"

### 示例5：模拟面试
```bash
# 1. 智能体先生成面试问题数据（JSON格式）
# 2. 生成模拟面试网页
python scripts/generate_interview_web.py questions.json --job-name "高级Java工程师" --company "XX科技"
```

智能体将：
1. 基于岗位要求和用户简历生成面试问题数据
2. 调用脚本生成互动式模拟面试网页
3. 网页包含AI面试官功能，用户可以逐题回答
4. 用户完成后，将回答提交给智能体

**网页功能特性**：
- 互动式面试体验：逐题回答、进度跟踪
- **数据可视化**：使用Chart.js生成评分图表
  - 柱状图：展示各维度得分（相关性、完整性、清晰度、具体性、专业度）
  - 雷达图：展示综合能力评估（沟通能力、逻辑思维、专业知识等）
- 响应式设计：适配不同屏幕尺寸
- **报告下载**：提供Word下载按钮，一键下载完整的Word版面试报告

智能体评分与点评：
- 评分维度：
  - 回答相关性（是否切中问题核心）
  - 内容完整性（是否有STAR结构）
  - 逻辑清晰度（表达是否条理清晰）
  - 具体性（是否有具体案例和数据）
  - 专业深度（是否体现专业水平）

- 评分结果（总分100分）：
  - 90-100分：优秀，面试表现极佳
  - 80-89分：良好，面试表现良好
  - 70-79分：中等，需要改进
  - 60-69分：及格，有明显不足
  - 60分以下：不及格，需要大幅提升

- 点评内容：
  - 优点：指出回答中的亮点
  - 不足：指出需要改进的地方
  - 建议：提供具体的改进建议
  - 示例：给出优化后的回答示例
  - 图表数据更新：提供各维度和能力评估的分数，用于更新网页图表

### 示例6：直接提供岗位描述
- 用户：无法解析链接，直接粘贴岗位描述
- 智能体：分析岗位文本 → 对比简历 → 生成优化简历（严格遵守硬性要求）、匹配度分析报告、修改说明文档
- 用户：已经通过了这个岗位的简历筛选，帮我准备面试
- 智能体：解析岗位 → 读取简历 → 生成面试准备提纲

智能体将生成三项交付成果和面试准备材料。

## ATS评分模拟器使用说明（V2.0）

### V2.0升级内容
- 8维度评分体系（原4维度），参考Jobscan/ResumeWorded等成熟产品
- 30+类技能同义词库（原10类），覆盖全行业
- 7平台ATS模拟器（Workday/Taleo/iCIMS/Greenhouse/北森/BOSS直聘/猎聘）
- 简历结构完整性检测（5模块+顺序评估）
- 量化成果密度分析
- 可读性与专业度评估（弱动词/专业术语/行动导向）
- 多层级报告输出（评级A-F+维度得分+优先级建议）
- 完全兼容V1接口

### 评分维度
| 维度 | 权重 | 说明 |
|------|------|------|
| 关键词匹配 | 30% | JD技能覆盖率+同义词/模糊/部分匹配 |
| 格式兼容性 | 12% | 15+项检查（表格/图片/特殊字符/编码/分栏等） |
| 结构完整性 | 13% | 必备模块检测+模块顺序合理性 |
| 量化成果 | 15% | 数字/百分比/指标密度评估 |
| 可读性与专业度 | 10% | 动词强度/专业术语密度/行动导向 |
| 经验相关性 | 10% | 年限达标+JD关键词密度 |
| 学历匹配 | 5% | 学历是否满足岗位最低要求 |
| ATS平台兼容 | 5% | 7个主流ATS系统解析兼容度均值 |

### 评级体系
| 评级 | 分数区间 | 含义 |
|------|---------|------|
| A | 90-100 | 优秀，ATS友好度极高，大概率通过筛选 |
| B | 75-89 | 良好，较高通过率 |
| C | 60-74 | 合格，建议优化后投递 |
| D | 40-59 | 待优化，需重点改进 |
| F | 0-39 | 不合格，几乎无法通过ATS筛选 |

### ATS平台模拟
支持7个主流ATS系统解析模拟，每个系统有独立的解析规则：
- **Workday**: 全球最大ATS，500强首选，对多栏布局敏感
- **Taleo**: 传统企业常用，仅支持精确关键词匹配
- **iCIMS**: 中型企业主流，词干匹配
- **Greenhouse**: 科技公司首选，支持语义匹配
- **北森**: 国内最大ATS，中文解析优秀
- **BOSS直聘**: 国内最大招聘平台
- **猎聘**: 中高端人才招聘

### 使用方式

**扣子平台Skill调用：**
```yaml
name: ats_score_simulator
input:
  resume_text: "简历纯文本内容"
  jd_requirements:
    required_skills: ["Java", "Spring Boot"]
    preferred_skills: ["Kafka", "Redis"]
    min_experience_years: 5
    education_level: "本科"
  resume_format_info:
    has_table: false
    has_image: false
    has_text_box: false
    has_column: false
    has_header_footer: false
    has_contact_masked: true
    file_format: "pdf"
  target_platform: "workday"  # 可选，指定ATS平台模拟
```

**本地测试（命令行）：**
```bash
python scripts/ats_scorer.py \
  --resume-file resume.txt \
  --jd-file jd_requirements.json \
  --format-file format_info.json \
  --platform workday \
  --output result.json
```

### 技能同义词库（30+类）
- 编程语言：Java/Python/JavaScript/C++/Go/Rust/PHP/Ruby/Swift/Kotlin/Scala/R
- 数据：数据分析/机器学习/数据工程/关系数据库/NoSQL
- 云与基础设施：云服务/DevOps
- 开发：前端开发/移动开发/后端开发/中间件/测试/网络安全
- 行业：项目管理/产品管理/UI-UX设计/运营/销售/财务/人力资源

### 输出示例（V2.0增强）
```json
{
  "ats_score": 94,
  "score_level": {"level": "A", "label": "优秀", "color": "green", "desc": "ATS友好度极高"},
  "keyword_match_rate": 1.0,
  "missing_skills": [],
  "format_score": 100,
  "suggestions": ["使用强动词替代弱动词"],
  "dimension_scores": {
    "keyword_match": {"name": "关键词匹配", "score": 100, "weight": 0.3, "weighted": 30.0},
    "format_compat": {"name": "格式兼容性", "score": 100, "weight": 0.12, "weighted": 12.0}
  },
  "detailed_suggestions": [
    {"priority": "medium", "dimension": "可读性与专业度", "issue": "发现弱动词", "action": "使用强动词", "impact": ""}
  ],
  "platform_simulation": {"platform": "Workday", "compat_score": 100, "parse_success": true},
  "scoring_version": "2.0",
  "evaluated_at": "2026-06-09 12:30:00"
}
```

## 资源索引
- 脚本: [scripts/generate_resume_optimization.py](scripts/generate_resume_optimization.py)（简历优化主脚本）
- 脚本: [scripts/generate_interview_web.py](scripts/generate_interview_web.py)（面试页面生成脚本）
- 脚本: [scripts/generate_enhanced_interview_web.py](scripts/generate_enhanced_interview_web.py)（增强版交互式面试模拟页面v2：直接DOM渲染+答案折叠+自评评分+复习模式）
- 脚本: [scripts/parse_job_posting.py](scripts/parse_job_posting.py)（岗位解析脚本：支持Boss直聘、智联招聘、前程无忧、拉勾网、猎聘等）
- 脚本: [scripts/ats_scorer.py](scripts/ats_scorer.py)（ATS评分模拟器）
- 脚本: [scripts/generate_job_search_dashboard.py](scripts/generate_job_search_dashboard.py)（求职进度看板生成脚本：漏斗式展示ATS分→面试通过率→offer拿到率）
- 脚本: [scripts/data_protection.py](scripts/data_protection.py)（个人数据保护工具：PII四级分类、自动脱敏、合规报告生成）
- 脚本: [scripts/anti_leakage_protection.py](scripts/anti_leakage_protection.py)（防泄漏机制工具：AES-256加密+动态脱敏+边界隔离+审计留痕）
- 脚本: [scripts/chart_utils.py](scripts/chart_utils.py)（图表生成工具：符合红线规则的matplotlib base64 PNG图表）
- 脚本: [scripts/industry_specific_interview.py](scripts/industry_specific_interview.py)（结合行业性质的针对性面试题生成：三维定位法-简历弱点+JD要求+行业特性）
- 脚本: [scripts/intro_generator.py](scripts/intro_generator.py)（面试自我介绍自动生成：4赛道×5经验×2时长，支持通用/技术/市场运营/职能赛道）
- 脚本: [scripts/reverse_question_generator.py](scripts/reverse_question_generator.py)（面试优质反向提问题库：不踩雷、高适配，根据简历和JD自动匹配生成，包含5个通用优质提问+行业特定提问+个性化提问）
- 脚本: [scripts/generate_welcome_page.py](scripts/generate_welcome_page.py)（新用户首次使用自动弹出欢迎开场白：展示功能+使用指南）
- 脚本: [scripts/career_profile_analyzer.py](scripts/career_profile_analyzer.py)（职业阶段分析与简历策略推荐：工作年限提取+职业阶段判断+岗位类型检测+个性化策略输出）
- 配置: [skill.yaml](skill.yaml)（扣子平台Skill配置）
- 参考: [references/supported_platforms.md](references/supported_platforms.md)（支持的招聘平台列表）
- 参考: [references/data_upload_desensitization_guide.md](references/data_upload_desensitization_guide.md)（数据上传与脱敏处理指南）
- 参考: [references/data_security_guide.md](references/data_security_guide.md)（数据安全指南）
- 参考: [references/interview_question_generation_guide.md](references/interview_question_generation_guide.md)（面试问题生成指南）
- 参考: [references/multi_dimensional_evaluation_guide.md](references/multi_dimensional_evaluation_guide.md)（多维度评估指南）
- 参考: [references/resume_optimization_guide.md](references/resume_optimization_guide.md)（简历优化指南）
- 参考: [references/interview_preparation_guide.md](references/interview_preparation_guide.md)（面试准备指南）
- 参考: [references/delivery_redline_rules_v6.2.md](references/delivery_redline_rules_v6.2.md)（技能交付物生成红线规则v6.2）
- 参考: [references/data_protection_specification.md](references/data_protection_specification.md)（个人数据保护专项规范DCMM 2.0对齐版）
- 参考: [references/career_stage_resume_strategy.md](references/career_stage_resume_strategy.md)（职业阶段简历优化策略手册：5阶段×策略表+模块优先级+关键词策略）
- 参考: [references/job_type_resume_structure.md](references/job_type_resume_structure.md)（岗位类型简历模块结构指南：5种岗位×模块差异+篇幅分配+特殊要求）

## 注意事项
- 仅在需要时读取参考，保持上下文简洁。
- 操作脆弱时优先调用脚本并校验结果。
- 充分利用智能体能力，避免为简单任务编写脚本。
- 解析招聘链接时，如遇反爬虫限制，请使用备用方案（手动提供岗位描述）。
