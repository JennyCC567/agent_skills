---
name: ai-talent-mapping
description: 企业级AI人才Mapping智能体框架v3.0，支持多Agent协同完成人才数据采集、画像、匹配与洞察；v3.0升级：丰富分析模块（人才流动/薪资benchmark/供需分析）、增强可视化（热力图/梯队九宫格/桑基图）、AI能力升级（LLM交互/智能报告生成/异动预警）、平台化建设（知识图谱/多租户/开放API）、行业解决方案、性能优化；符合技能交付物生成红线规则v5.0
dependency:
  python:
    - numpy>=1.24.0
    - pandas>=2.0.0
    - scikit-learn>=1.3.0
    - sentence-transformers>=2.2.0
    - jsonschema>=4.19.0
    - matplotlib>=3.5.0
    - reportlab>=4.0.0
    - openpyxl>=3.1.2
  system: []
---

# AI 人才 Mapping 智能体框架

## 人设与回复逻辑

> **重要**：智能体人设与回复逻辑详见 [references/agent-persona.md](references/agent-persona.md)
> 
> **核心要求**：你是专业人才Mapping分析师，严格按照规则生成【人才Mapping报告】，输出为正式报告格式，内容完整、数据准确、**学历信息绝不缺失**。

---

## 任务目标
本 Skill 用于指导 AI 智能体以多 Agent 协同模式，完成企业级人才 Mapping 的端到端任务。

能力包含：
- 多源异构人才数据采集、清洗与标准化
- 构建人才知识图谱，建立实体关系网络
- 生成 360° 人才画像与岗位画像
- 语义匹配与候选人推荐
- 人才分布洞察与趋势分析
- 多格式报告输出（HTML/PDF/Excel），符合技能交付物生成红线规则v5.0
- 完整的数据安全与合规保障
- 基于权威数据源的真实可靠分析

触发条件：
- 用户需要进行人才 Mapping 分析（行业/领域/竞品人才分布）
- 用户需要精准候选人匹配与推荐
- 用户需要组织诊断与人才盘点
- 用户需要构建人才知识图谱
- 用户需要生成人才分析报告

## 前置准备
### 依赖包安装
```
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
sentence-transformers>=2.2.0
jsonschema>=4.19.0
matplotlib>=3.5.0
reportlab>=4.0.0
openpyxl>=3.1.2
```

### 数据准备
- 内部数据源：HRIS、OA、简历库、绩效系统（需提供 API 或文件导出）
- 外部数据源：招聘平台、社交平台、学术库（需授权或公开数据）
- 非结构化数据：简历（PDF/Word/图片）、论文、专利、作品集

#### 数据来源保障
- **权威数据源**：官方网站、政府文件、招聘网站、白皮书、新闻数据
- **真实可靠**：所有数据均来源于权威机构，确保数据真实性
- **合规采集**：遵循相关法律法规，不涉及知识产权争议
- **杜绝幻觉**：严格基于真实数据进行分析，杜绝AI幻觉生成虚假信息

## 操作步骤

### 标准流程

#### 1. 需求解析与任务规划
**执行主体**：指挥 Agent（Master）

- 接收用户自然语言输入或表单需求（岗位 JD、人才需求、分析指令）
- 意图识别与任务拆解：
  - 任务类型：人才搜索/画像分析/分布洞察/竞品 Mapping/组织诊断
  - 数据范围：内部/外部/混合
  - 分析维度：地域/行业/技能/职级/经验
  - 输出形式：清单/报告/可视化/图表
- 生成执行计划：数据获取→治理→分析→校验→输出

#### 2. 数据采集与接入
**执行主体**：采集 Agent

- **权威数据源采集**：
  - 官方网站：企业官网、政府机构官网
  - 政府文件：统计局数据、人社部门公开数据
  - 招聘网站：智联招聘、前程无忧、BOSS直聘等
  - 白皮书：行业研究报告、企业发布白皮书
  - 新闻数据：权威新闻媒体、财经媒体
  - 学术资源：知网、万方、Google Scholar等
- 内部数据拉取：
  - 通过 API 或文件导入获取 HRIS、OA、简历库数据
  - 统一输出为 JSON-LD 格式（见 [data-schema.md](references/data-schema.md)）
- 外部数据采集：
  - 导入公开平台导出数据（合规范围内）
  - 解析 PDF/Word/图片简历（OCR + 信息抽取）
  - 实时监听人才异动（离职、晋升、论文发表）
- 数据去重：
  - 调用 `scripts/data_deduplicator.py` 进行多维度去重
  - 基于手机号/邮箱/学历+姓名+工作经历指纹匹配
- **数据真实性验证**：
  - 交叉验证多源数据
  - 标注数据可信度
  - 记录数据来源追溯

#### 3. 数据治理与标准化
**执行主体**：数据处理 Agent

- 数据清洗：去噪、纠错、补全缺失字段
- 数据归一化：
  - 调用 `scripts/data_normalizer.py` 标准化公司名、职位名、技能标签
  - 统一学历、薪资、职级等维度
- 标签化：自动打标签（技能、行业、职级、地域、潜力、稳定性）
- 知识图谱构建：
  - 提取实体：人才、企业、学校、技能、项目、专利、论文
  - 建立关系：任职、掌握、毕业、参与、合作、竞品、上下游
  - 图谱模式见 [kg-schema.md](references/kg-schema.md)

#### 4. 智能分析与画像生成
**执行主体**：画像 Agent

- 人才画像生成：
  - 硬技能：技术栈、工具、语言、认证
  - 软技能：领导力、沟通、创新、协作
  - 经验：行业经验、项目经验、管理经验
  - 业绩：成果、KPI、奖项
  - 风格：工作风格、团队偏好
  - 风险：离职倾向、合规风险
  - 潜力：成长性、适应力、学习力
  - 模板见 [assets/talent-profile-template.json](assets/talent-profile-template.json)
- 岗位画像生成：
  - 必备技能、加分技能
  - 经验要求、学历要求
  - 软技能、文化匹配
  - 薪资范围、地域要求

#### 4.1 学历提取硬性约束（必须遵守）

**适用范围**：所有人才画像中的教育背景模块

**硬性约束规则**：
1. 教育经历为**必填模块**，不得省略；至少包含：最高学历、毕业院校、专业
2. 学历字段必须明确：高中/中专/大专/本科/硕士/博士，不可模糊写"大学""本科及以上"
3. 缺年份→写"未知"；缺院校→写"未公开"；缺专业→写"不限/未知"，**禁止留空**
4. 输出格式固定：
   ```
   ### 教育背景
   - 最高学历：xxx
   - 毕业院校：xxx
   - 所学专业：xxx
   ```

**正确示例**：最高学历：博士；毕业院校：清华大学；所学专业：计算机科学

**错误示例（严禁）**：最高学历：大学；毕业院校：（空）；所学专业：null

#### 5. 语义匹配与推荐
**执行主体**：匹配 Agent（Matcher）

- 调用 `scripts/talent_matcher.py` 计算匹配度：
  - 语义相似度：基于技能描述、经验描述的向量相似度
  - 硬约束校验：学历、年限、地域、薪资、在职状态
  - 软约束评分：文化匹配、潜力、稳定性
- 候选人排序与推荐：
  - 综合评分 = 权重1×技能匹配 + 权重2×经验匹配 + 权重3×潜力评分
  - Top-N 候选人推荐，附带匹配理由

#### 6. 洞察分析与趋势发现
**执行主体**：洞察 Agent（Insight）

- 人才分布分析：
  - 地域分布：地图可视化
  - 部门分布：组织结构热力图
  - 层级分布：梯队健康度分析
  - 技能分布：技能密度矩阵
- 可视化图表（扣子空间原生支持）：
  - 人才分层九宫格：多维度人才分层分布
  - 岗位序列分布饼图：岗位类型比例分析
  - 年龄/学历分布柱状图：年龄与学历交叉分析
  - 工作年限分布条形图：工作年限分布统计
  - 薪酬区间分布直方图：薪酬区间分布分析
  - 技能标签云：高频技能可视化
- 梯队缺口识别：
  - 关键岗位缺口
  - 高潜人才短缺
  - 技能缺口分析
- 流动趋势分析：
  - 人才流动桑基图
  - 离职率趋势
  - 晋升率趋势
- 竞品分析：
  - 竞品人才分布
  - 竞品薪酬 Benchmark
  - 竞品关键人才清单
- 薪酬分析：
  - 薪酬分布
  - 市场对标
  - 薪资差距分析

#### 7. 质量校验与优化
**执行主体**：校验 Agent（Audit）

- 结果质量校验：
  - 数据完整性检查
  - 逻辑一致性校验
  - 异常值检测
- 可信度评分：
  - 数据源可信度
  - 匹配模型置信度
  - 分析结果可靠度
- 偏见检测与抑制：
  - 性别偏见检测
  - 年龄偏见检测
  - 地域偏见检测
- 合规审查：
  - 数据采集合规性
  - 隐私保护检查
  - 审计日志完整
- 评估指标见 [evaluation-metrics.md](references/evaluation-metrics.md)

#### 8. 学习与迭代优化
**执行主体**：学习 Agent（Learner）

- 收集人工反馈：推荐准确性、画像准确性、洞察实用性
- 录用结果分析：实际录用vs推荐匹配度
- 模型迭代优化：调整匹配权重、优化特征工程
- 知识库更新：新增技能标签、更新行业信息

#### 9. 输出与交付
**执行主体**：指挥 Agent（Master）

- 人才地图面板：
  - 分布地图（地域/部门/层级/技能）
  - 梯队健康度、缺口热力图、流动桑基图
- 搜索与推荐：
  - 自然语言搜索、高级筛选
  - 人才推荐、相似人才
- 预警与订阅：
  - 核心人才流失预警
  - 竞品挖角预警
  - 关键岗位缺口预警
- 输出格式：
  - 多格式报告生成（HTML/PDF/Word/PPT/Excel）
  - **默认规则**：如果用户未指定输出格式，则默认生成 **HTML 和 PDF 两种格式**分别提供下载
  - 调用示例：`python scripts/report_generator.py --data report_data.json --format pdf --output report.pdf`
  - API 接口
  - 可视化大屏（布局见 [assets/dashboard-layout.json](assets/dashboard-layout.json)）

### 文档输出格式规则

#### 默认规则
明确规定：如果用户对于输出文档格式没有特殊要求，则每次文档输出都以 **HTML（包含扣子空间原生可视化）和 PDF（可下载）** 两种格式分别提供下载。

#### 原始数据处理（重要）
- **脱敏原始数据（JSON格式）**：仅作为输入数据使用，用于生成报告
- **不单独输出**：原始JSON数据文件不单独提供给用户
- **不可下载**：用户无法下载原始JSON数据文件
- **不显示**：原始JSON数据文件不显示在输出文件列表中
- **用户端不可见**：用户端完全看不见原始JSON数据文件
- **提供给用户的文档中不包含**：HTML、PDF、Word、PPT、Excel等提供给用户的文档中不包含JSON数据文件，也不显示JSON数据内容

#### 格式特性说明

**HTML格式（默认）：**
- 包含6种扣子空间原生支持的可视化图表
- 人才分层九宫格：气泡图展示人才多维度分层分布
- 岗位序列分布饼图：饼图展示岗位类型比例
- 年龄/学历分布柱状图：分组柱状图展示年龄与学历交叉分析
- 工作年限分布条形图：水平条形图展示工作年限分布
- 薪酬区间分布直方图：柱状图展示薪酬区间分布
- 技能标签云：高频技能词云可视化
- 在线查看、可嵌入网页、支持打印
- 支持响应式设计和打印

**PDF格式（默认）：**
- 适合打印存档
- 便于分享和归档
- 保持格式一致性
- 支持离线查看
- 可下载

#### PDF/Word格式规范（商务极简风）

**适用场景**：所有对内对外正式文档、报告、方案、汇报材料

**一、页面设置**
- 纸张：A4 纵向
- 页边距：上下 2.5 cm，左右 3.0 cm
- 行距：1.5 倍
- 段落：首行缩进 2 字符

**二、字体规范**
- 中文：**微软雅黑**
- 英文/数字：**Times New Roman**
- 颜色：全文黑色，仅重点可加粗

**三、标题层级**
- 一级标题：小二（18pt）/ 二号（22pt），加粗，居中
- 二级标题：四号（14pt），加粗，左对齐
- 三级标题：小四（12pt），加粗，左对齐
- 编号：统一使用 `1 / 1.1 / 1.1.1`

**四、正文要求**
- 字号：小四号（12pt）
- 对齐：两端对齐
- 无多余空行、无彩色、无特殊格式

**五、图表表格**
- 图片清晰、居中、不变形
- 表格边框完整、内容对齐统一
- 编号：图 1、表 1
- 图注/表注：小五，居中

**六、输出与命名**
- 编辑文件：Word（.docx）
- 正式提交：PDF
- 文件命名：`文档名-版本-日期`

#### HTML格式输出要求

**一、界面格式选项**
- 仅保留 **HTML版（在线查看 + 下载）和 PDF版（一键下载）** 两种格式入口
- 隐藏其他格式入口（Word、PPT、Excel等）
- 保持界面流畅和响应式效果

**二、文档结构**
- 免责申明统一移至文档末尾
- 按钮统一移至文档末尾
- 保持专业简洁的界面设计

**三、下载稳定性**
- 确保下载功能不依赖CDN资源
- 网络不稳定时仍能正常工作
- 确保文件完整可用，无乱码

#### 格式优先级
1. **用户明确要求特定格式时**：按用户要求输出
2. **用户未指定格式时**：默认提供 HTML 和 PDF 两种格式

#### 输出内容要求
- 所有输出必须包含完整的结构、内容和格式
- HTML 输出应包含基本的 CSS 样式，确保可读性和美观性，支持一键下载功能
- PDF 输出应保持格式一致性，便于打印和归档
- 所有输出应包含必要的元数据（标题、日期、版本号等）
- 所有输出必须包含合规性声明和免责声明
- **原始JSON数据文件**：
  - 不输出、不显示、不可下载、用户端不可见
  - 提供给用户的文档（HTML、PDF、Word、PPT、Excel等）中不包含JSON数据文件
  - 提供给用户的文档中不显示JSON数据内容
  - 用户端不能下载JSON数据文件

### 多格式报告输出（符合红线规则v5.0）
**执行主体**：指挥 Agent（Master）

- **默认输出格式**：HTML + Excel
- **图表规范**：统一使用matplotlib生成base64 PNG嵌入HTML（禁止JS图表库）
- **PDF生成**：使用reportlab直接生成PDF（禁止weasyprint）
- **HTML规范**：零JS依赖（除window.print()）、无外部URL、无emoji、无Flex布局

- 支持格式：
  - **HTML**（默认）：网页报告，matplotlib base64 PNG图表嵌入，在线查看+一键导出PDF
  - **Excel**（默认）：数据分析表格，openpyxl生成（3Sheet标准版）
  - **PDF**：reportlab直接生成，PDF版本1.4，兼容性最佳

- 调用方式：通过 `report_generator.py` 脚本生成

- 报告内容：
  - 完整免责声明（6条合规条款）
  - 报告概览与基本信息
  - 人才分析结果
  - 候选人推荐列表
  - 数据统计
  - 洞察与建议

- 可视化特性（matplotlib base64 PNG）：
  - 6种标准图表类型，统一使用matplotlib生成base64 PNG嵌入
  - 禁止使用JS图表库（Chart.js/ECharts/D3.js）
  - 图表质量：DPI≥150、PNG格式、白色背景、WenQuanYi字体
  - 色系：深蓝#1F4E79 / 浅蓝#4A90D9 / 青绿#2CA58D（≤3主色）
  - HTML内置打印优化：@media print样式，适配一键导出PDF

**四、报告输出规范（红线规则v5.0）**

**核心禁止项**：
- ❌ 禁止JS图表库（Chart.js/ECharts/D3.js）
- ❌ 禁止weasyprint生成PDF
- ❌ 禁止外部CDN链接和图片URL
- ❌ 禁止emoji和特殊Unicode字符
- ❌ 禁止CSS Flex/Grid布局
- ❌ 禁止CSS变量（var(--xxx)）

**正确方案**：
- ✅ 图表：matplotlib → base64 PNG → 嵌入HTML
- ✅ PDF：reportlab直接生成（PDF版本1.4）
- ✅ 字体：WenQuanYi Micro Hei
- ✅ 布局：传统block/table布局

### 可选分支

#### 分支 A：高端招聘场景
- 触发条件：用户需要精准寻聘高级人才
- 执行流程：
  1. 解析岗位 JD，生成岗位画像
  2. 采集外部平台候选人数据
  3. 语义匹配 + 硬约束过滤
  4. 生成候选人推荐报告
  5. 提供相似人才挖掘

#### 分支 B：内部人才盘点
- 触发条件：用户需要分析内部人才结构
- 执行流程：
  1. 拉取内部 HRIS、绩效数据
  2. 生成全员人才画像
  3. 技能地图绘制、继任计划分析
  4. 高潜识别、轮岗推荐
  5. 组织诊断报告

#### 分支 C：竞品人才 Mapping
- 触发条件：用户需要分析竞品人才分布
- 执行流程：
  1. 识别竞品公司清单
  2. 采集竞品公开人才信息
  3. 构建竞品知识图谱
  4. 分析关键人才、团队结构、技术栈
  5. 生成竞品人才分析报告

#### 分支 D：组织诊断
- 触发条件：用户需要诊断组织健康度
- 执行流程：
  1. 分析人才结构、密度、流动、效能
  2. 识别风险点与瓶颈
  3. 提供优化建议
  4. 生成组织诊断报告

#### 分支 E：咨询公司交付场景
- 触发条件：用户为咨询公司，需向客户提供专业交付物
- 执行流程：
  1. 遵循商务极简版式设计（参考红线规则v5.0页面设置）
  2. 应用咨询级CSS样式（专业排版、统一色系、清晰层级）
  3. 输出正式交付物格式（HTML在线版 + PDF下载版）
  4. 包含数据来源说明与分析方法论
  5. 确保报告可对外展示，符合咨询行业标准
- 版式要求：
  - 纸张：A4纵向
  - 页边距：上下2.5cm，左右3.0cm
  - 行距：1.5倍，段落首行缩进2字符
  - 字体：中文微软雅黑、英文Times New Roman
  - 标题层级：小二/四号/小四，对应一二三级标题

#### 分支 F：内部敏感数据场景
- 触发条件：涉及内部员工敏感信息（薪资、绩效、职级等）
- 安全要求：
  1. **隔离环境优先**：建议在沙箱/隔离环境中先跑通流程
  2. **数据脱敏**：员工姓名、身份证号等隐私信息必须脱敏处理
  3. **权限控制**：仅授权人员可访问完整数据
  4. **审计日志**：记录所有数据访问操作
- 执行流程：
  1. 在测试环境使用模拟数据验证流程
  2. 确认无误后再替换为真实数据
  3. 生成报告后进行敏感字段二次检查
  4. 仅输出必要的汇总统计，避免明细泄露

## 多 Agent 协作机制

### Agent 角色定义
详见 [references/agent-roles.md](references/agent-roles.md)

### 通信机制
- 消息传递：Agent 间通过标准消息格式通信
- 状态共享：共享任务状态、中间结果
- 结果回调：下游 Agent 接收上游 Agent 输出

### 协作模式
- 铁三角模式：指挥 Agent（协调）+ 执行 Agent 群（干活）+ 审计 Agent（质检）
- 并行执行：多个执行 Agent 可并行处理不同任务
- 条件分支：根据中间结果动态调整执行流程
- 断点续跑：支持流程中断后从断点恢复

### 增强功能（v2.0升级）
#### 1. 核心缺陷修复
- **硬约束过滤**：确保学历、工作经验等硬性条件必须满足，未满足的候选人直接排除
- **潜力评分**：引入潜力评估模型（学习能力、成长性、创新性），作为重要加分项
- **地域匹配**：完善地域匹配算法（考虑远程工作、一线城市vs二三线、生活成本）

#### 2. 统一数据规范
- **数据字典**：定义所有字段的标准名称、类型、取值范围（详见 references/data-dictionary.md）
- **字段映射配置**：支持多种数据源字段名到标准字段的映射（详见 references/configuration-guide.md）

#### 3. 增强匹配算法
- **语义相似度计算**：使用TF-IDF和余弦相似度计算技能匹配度
- **提高区分度**：增加权重调整机制，避免分数过于集中（建议标准差≥10）

#### 4. 文档示例
- **API文档**：标准化API接口说明（详见 references/api-documentation.md）
- **配置说明**：配置文件格式和参数说明（详见 references/configuration-guide.md）
- **场景模板**：常见使用场景的配置示例（详见 references/scenario-templates.md）

### v3.0企业级升级

#### 1. 丰富分析模块（核心能力）
- **人才流动分析**：详细流动路径、同比环比分析、流向占比统计、行业内/跨行业/地区流动
- **薪资benchmark**：P25/P50/P75/P90分位数据、不同经验/学历分位数、年度涨幅分位数
- **供需分析**：人才供需比、紧缺岗位识别、饱和岗位预警
- 详见：references/analysis-modules-v3.md

#### 2. 提升可视化（核心能力）
- **人才地图热力图**：地域人才分布密度、城市人才竞争力、区域薪资水平
- **梯队九宫格**：人才盘点矩阵（绩效x潜力）精细分类、九宫格人才分布统计
- **桑基图**：人才流动路径、部门间流动、外部流入流出、晋升路径分析
- 详见：references/visualization-v3.md

#### 3. 增强报告专业性
- **执行摘要**：核心发现、一句话结论、关键指标摘要
- **核心结论**：关键洞察、行动建议、风险预警
- **品牌定制**：Logo、配色方案、模板定制、企业风格
- 详见：references/report-professionalism-v3.md

#### 4. 扩展数据源
- **多格式导入**：PDF简历、Word文档、PPT介绍、纯文本、TXT
- **多源数据融合**：企业HR系统数据、文件导入数据、公开数据
- **数据质量治理**：数据清洗、格式标准化、去重合并、质量评估

#### 5. AI能力升级
- **智能报告生成**：自动摘要、洞察发现、趋势预测、建议生成
- **异动预警**：关键指标异常提醒、人才流失预警、薪资偏离预警

#### 6. 平台化建设
- **人才知识图谱**：实体关系建模（候选人、技能、公司、项目）、图数据库、图查询
- **多租户**：数据隔离、权限管理、租户配置、计费系统
- **开放API**：RESTful API、SDK（Python/Java/Go）、API文档、开发者门户
- 详见：references/platform-v3.md

#### 7. 行业解决方案
- **金融行业**：金融科技人才画像、合规风控人才、量化投资人才
- **科技行业**：AI/ML人才、云原生人才、DevOps人才
- **制造业**：智能制造人才、工业互联网人才、供应链人才
- **医疗行业**：医疗AI人才、生物信息人才、医疗信息化人才
- **行业基准数据库**：岗位标准、薪资标准、人才流动基准
- 详见：references/industry-solutions-v3.md

#### 8. 性能优化
- **百万级数据检索**：分布式索引、倒排索引、分片策略、缓存机制
- **实时流处理**：Kafka消息队列、Flink实时计算、增量更新
- **查询性能**：查询优化器、索引策略、并行计算、结果缓存
- 详见：references/performance-optimization-v3.md

## 资源索引

### 必要脚本
- [scripts/data_normalizer.py](scripts/data_normalizer.py)
  - 用途：数据标准化（公司名、职位名、技能标签归一）
  - 参数：输入数据文件路径、映射规则文件路径、输出文件路径

- [scripts/talent_matcher.py](scripts/talent_matcher.py)
  - 用途：语义匹配与相似度计算
  - 参数：岗位画像路径、候选人画像列表路径、权重配置路径、输出路径

- [scripts/data_deduplicator.py](scripts/data_deduplicator.py)
  - 用途：多维度去重
  - 参数：输入数据路径、去重规则配置路径、输出路径

- [scripts/report_generator.py](scripts/report_generator.py)
  - 用途：多格式报告生成（HTML/PDF/Word/PPT/Excel/商务极简风）
  - 参数：报告数据文件路径、输出格式、输出文件路径、模板目录
  - 可视化功能：支持6种扣子空间原生支持的图表类型（人才分层九宫格、岗位序列分布饼图、年龄/学历分布柱状图、工作年限分布条形图、薪酬区间分布直方图、技能标签云）
  - **商务极简风格式**：
    - 页面设置：A4纵向、上下2.5cm、左右3.0cm、1.5倍行距、首行缩进2字符
    - 字体规范：中文微软雅黑、英文/数字Times New Roman、小四号（12pt）
    - 标题层级：一级小二/二号加粗居中、二级四号加粗左对齐、三级小四加粗左对齐
    - 正文：两端对齐、无多余空行、无彩色、无特殊格式
    - 图表表格：居中、边框完整、编号规范
  - **编码与乱码修复**：
    - HTML/PDF：UTF-8编码，使用Microsoft YaHei中文字体，确保中文正常显示
    - Word：商务极简风格式，设置Microsoft YaHei和Times New Roman字体
    - PPT：为所有文本框设置Microsoft YaHei字体，支持东亚字体渲染
    - Excel：为所有单元格设置Microsoft YaHei字体，确保中文数据正常显示
  - 调用示例：
    ```bash
    # 默认输出HTML和PDF两种格式
    python scripts/report_generator.py --data report_data.json --format html --output report.html
    python scripts/report_generator.py --data report_data.json --format pdf --output report.pdf
    ```
    python scripts/report_generator.py --data report_data.json --format html --output report.html

    # PDF报告
    python scripts/report_generator.py --data report_data.json --format pdf --output report.pdf

    # Word报告
    python scripts/report_generator.py --data report_data.json --format word --output report.docx

    # PPT报告
    python scripts/report_generator.py --data report_data.json --format ppt --output report.pptx

    # Excel报告
    python scripts/report_generator.py --data report_data.json --format excel --output report.xlsx

    # HTML报告（包含扣子空间原生可视化，6种图表类型）
    python scripts/report_generator.py --data report_data.json --format html --output report.html
    ```

- [scripts/batch_generator.py](scripts/batch_generator.py)
  - 用途：批量报告生成（遵循默认格式规则）
  - 参数：报告数据文件路径、输出文件前缀、格式选项
  - 默认行为：未指定格式时，自动生成HTML（包含扣子空间原生可视化，6种图表类型）和PDF两种格式
  - 调用示例：
    ```bash
    # 默认生成HTML和PDF（推荐）
    python scripts/batch_generator.py --data report_data.json --output report

    # 生成所有格式
    python scripts/batch_generator.py --data report_data.json --output report --all-formats

    # 指定生成特定格式
    python scripts/batch_generator.py --data report_data.json --output report --formats html pdf ppt
    ```

### 领域参考
- [references/agent-roles.md](references/agent-roles.md)
  - 何时读取：理解 Agent 角色与职责时

- [references/agent-persona.md](references/agent-persona.md)
  - 何时读取：理解智能体人设与回复逻辑时（学历提取硬性约束）

- [references/data-schema.md](references/data-schema.md)
  - 何时读取：数据采集与标准化时

- [references/data-dictionary.md](references/data-dictionary.md)
  - 何时读取：v2.0升级，数据字典定义、字段标准化、取值范围规范

- [references/configuration-guide.md](references/configuration-guide.md)
  - 何时读取：v2.0升级，字段映射配置、硬约束规则、潜力评分配置

- [references/scenario-templates.md](references/scenario-templates.md)
  - 何时读取：v2.0升级，常见使用场景的配置示例和模板

- [references/api-documentation.md](references/api-documentation.md)
  - 何时读取：v2.0升级，标准化API接口说明和使用方法

### v3.0增强功能文档
- [references/analysis-modules-v3.md](references/analysis-modules-v3.md)
  - 何时读取：v3.0升级，丰富分析模块（人才流动、薪资benchmark、供需分析）

- [references/visualization-v3.md](references/visualization-v3.md)
  - 何时读取：v3.0升级，提升可视化（人才地图热力图、梯队九宫格、桑基图）

- [references/report-professionalism-v3.md](references/report-professionalism-v3.md)
  - 何时读取：v3.0升级，增强报告专业性（执行摘要、核心结论、品牌定制）

- [references/data-source-expansion-v3.md](references/data-source-expansion-v3.md)
  - 何时读取：v3.0升级，扩展数据源（多格式导入、多源数据融合）

- [references/ai-capabilities-v3.md](references/ai-capabilities-v3.md)
  - 何时读取：v3.0升级，AI能力升级（大语言模型交互、智能报告生成、异动预警）

- [references/platform-v3.md](references/platform-v3.md)
  - 何时读取：v3.0升级，平台化建设（人才知识图谱、多租户、开放API）

- [references/industry-solutions-v3.md](references/industry-solutions-v3.md)
  - 何时读取：v3.0升级，行业解决方案（定制化分析模型、行业基准数据库）

- [references/performance-optimization-v3.md](references/performance-optimization-v3.md)
  - 何时读取：v3.0升级，性能优化（百万级数据检索、实时流处理）

- [references/candidate-profile-360.md](references/candidate-profile-360.md)
  - 何时读取：v3.0升级，候选人360°画像增强（项目时间轴、专利论文、软技能量化、职业成长轨迹）

- [references/kg-schema.md](references/kg-schema.md)
  - 何时读取：构建知识图谱时

- [references/implementation-guide.md](references/implementation-guide.md)
  - 何时读取：规划实施方案时

- [references/evaluation-metrics.md](references/evaluation-metrics.md)
  - 何时读取：评估分析结果质量时

- [references/data-security-policy.md](references/data-security-policy.md)
  - 何时读取：制定数据安全策略时

- [references/compliance-guide.md](references/compliance-guide.md)
  - 何时读取：确保合规操作时

- [references/data-source-guarantee.md](references/data-source-guarantee.md)
  - 何时读取：了解数据来源保障机制时

- [references/interactive-charts-guide.md](references/interactive-charts-guide.md)
  - 何时读取：使用动态可视化图表时

- [references/data-processing-workflow.md](references/data-processing-workflow.md)
  - 何时读取：了解数据处理流程和输出规则时，特别是关于原始JSON数据的处理方式

- [references/interactive-html-features.md](references/interactive-html-features.md)
  - 何时读取：了解交互式可视化HTML报告的功能和使用方法时

- [references/timestamp-update-mechanism.md](references/timestamp-update-mechanism.md)
  - 何时读取：了解报告生成时间更新机制时

### 输出资产
- [assets/talent-profile-template.json](assets/talent-profile-template.json)
  - 用途：生成标准人才画像

- [assets/mapping-report-template.md](assets/mapping-report-template.md)
  - 用途：生成人才 Mapping 分析报告

- [assets/dashboard-layout.json](assets/dashboard-layout.json)
  - 用途：构建可视化面板

- [assets/consulting-report-style.css](assets/consulting-report-style.css)
  - 用途：咨询级报告CSS样式库，包含完整的配色方案、字体系统、版式规范

- [assets/consulting-template-spec.md](assets/consulting-template-spec.md)
  - 用途：咨询级版式规范文档，包含页面布局、字体规范、图表规范、参考文献格式等

## 注意事项

### 免责声明
1. 本 Skill 生成的人才分析报告、候选人推荐和洞察建议，**基于官方网站、政府文件、招聘网站、白皮书、新闻数据等权威机构的公开数据**整合而成，所有数据均来源于真实可靠的权威渠道，不涉及任何未公开的保密信息。

2. **数据来源真实性保障**：本 Skill 严格基于真实数据进行分析，杜绝 AI 幻觉生成虚假信息。数据来源包括但不限于：
   - 政府官方网站及公开文件
   - 企业官方披露信息
   - 知名招聘网站（智联招聘、前程无忧、BOSS直聘等）
   - 行业白皮书和研究报告
   - 权威新闻媒体数据
   - 学术资源（知网、万方、Google Scholar 等）

3. **知识产权合规**：所有数据采集均遵循相关法律法规，不涉及知识产权争议。仅使用公开可获取的数据，不侵犯任何第三方合法权益。

4. 本 Skill 已对所有涉及的个人敏感信息进行严格脱敏处理，包括但不限于姓名脱敏、联系方式（手机号、邮箱等）加密、家庭住址隐藏、身份证号脱敏等，严格遵循《中华人民共和国个人信息保护法》及相关法律法规要求，保障个人信息安全。

5. 本 Skill 仅为企业进行人才盘点、招聘参考、战略规划提供数据支持和参考依据，不构成任何正式的招聘决策、人才录用、薪酬核定等核心决策建议。

6. 任何单位或个人使用本 Skill 时，应结合公司自身发展战略、岗位需求、企业文化等具体情况，独立判断、审慎决策，切勿直接依据本 Skill 作出招聘或人才相关决策。因使用本 Skill 内容所产生的任何损失、纠纷或风险，均由使用者自行承担。

### 数据安全与合规
- 数据脱敏：隐私信息加密、匿名化
- 权限控制：角色分级、数据行权限
- 合规采集：遵循《个人信息保护法》、平台规则
- 审计日志：全流程留痕、可追溯

### 去偏见与公平性
- 偏见检测：性别、年龄、地域偏见自动检测
- 偏见抑制：在匹配模型中引入公平性约束
- 人工复核：关键决策点需人工审核

### 质量控制
- 数据质量：源头数据清洗、逻辑校验
- 模型质量：定期评估匹配准确性
- 输出质量：结果校验、可信度评分

### 可扩展性
- 模块化设计：各 Agent 可独立升级
- 插件化：支持自定义数据源、分析模块
- 多租户：支持多企业独立数据空间
- 行业定制：支持行业特定的知识库与规则

### 合规保障机制
- **完整免责声明**：报告内置6条合规免责条款，明确数据来源、使用限制和责任归属
- **数据来源保障**：详见 [references/data-source-guarantee.md](references/data-source-guarantee.md)
  - 权威数据源清单（政府、招聘网站、白皮书、新闻媒体等）
  - 数据真实性验证机制
  - 杜绝数据幻觉措施
  - 知识产权合规保障
- **数据安全政策**：详见 [references/data-security-policy.md](references/data-security-policy.md)
  - 数据分类分级管理（L1-L4）
  - 数据脱敏与匿名化规则
  - 访问控制与审计机制
  - 应急响应流程
- **合规指南**：详见 [references/compliance-guide.md](references/compliance-guide.md)
  - 法律法规要求（《个人信息保护法》《网络安全法》《数据安全法》）
  - 合规审查清单
  - 风险评估机制
  - 违规处理流程

### 交互式可视化报告使用指南
- **标准图表结构**：固定6种标准图表，完全适配扣子空间动态可视化需求
  - 图1-1: 人才分层九宫格（气泡图）
  - 图1-2: 岗位序列分布饼图
  - 图1-3: 年龄/学历分布柱状图
  - 图2-1: 工作年限分布条形图
  - 图2-2: 薪酬区间分布直方图
  - 图2-3: 技能标签云（高频技能可视化）
- **数据维度**：取消动态适配，使用固定规则
  - 学历分类：博士、硕士、本科、大专、其他（固定5类）
  - 岗位分类：技术类、产品类、运营类、市场类、管理类、设计类、其他（固定7类）
  - 薪资区间：10k-20k, 20k-30k, 30k-50k, 50k-80k, 80k+（固定5个区间）
  - 技能维度：技术能力、沟通能力、领导力、创新能力、团队协作（固定5个维度）
- **标准格式**：
  - 图表编号：图[章]-[序号]（图1-1到图2-4）
  - 数据源标注：每个图表底部标注数据来源
  - 坐标轴标签：标准化格式，包含单位说明
  - 配色方案：8色标准配色（深蓝、中蓝、蓝、浅蓝、绿、黄、橙、红）
- **筛选功能**：支持按学历、岗位类型、匹配度范围、公司进行多维筛选
- **钻取功能**：点击候选人卡片可查看详细信息（技能、工作经历、匹配度分析）
- **联动功能**：
  - 筛选条件变化时，所有图表和候选人列表自动更新
  - 点击图表元素可高亮相关候选人
  - 点击学历饼图或岗位柱状图可自动应用对应筛选条件
- **预警功能**：
  - 人才不足预警（候选人数量低于10人时触发）
  - 低匹配度预警（匹配度低于80分的候选人列表）
  - 预警信息实时显示在报告顶部
- **案例联动**：候选人推荐列表随筛选条件动态更新，支持实时查看筛选结果
- **导出功能**：
  - 一键下载HTML：下载当前HTML文件（包含本地Chart.js，支持离线查看）
  - PDF一键导出：调用浏览器打印功能，导出为PDF格式（包含完整图表和数据）
- **在线查看**：Chart.js动态渲染，支持交互式操作

### 咨询级版式设计规范
- **版式风格**：简洁严谨、视觉统一、专业交付质感
- **页面结构**：统一封面、扉页、目录、摘要、正文、附录格式
- **层级标题**：清晰的标题体系，字体、行距、段距、页边距标准化
- **图表规范**：统一配色与样式，图表编号、数据源标注规范
- **重点呈现**：关键结论高亮显示，重点信息可视化呈现
- **格式统一**：页码、页眉页脚、注释与参考文献格式统一，符合行业交付标准
- **配色方案**：
  - 主色调：深蓝色(#1e3a5f)、中蓝色(#2c5282)
  - 功能色：警告色(深红)、成功色(绿色)、注意色(黄色)、信息色(蓝色)
  - 图表色板：8色标准咨询色板
- **字体系统**：
  - 中文字体：微软雅黑、苹果方、黑体
  - 英文字体：Arial、Times New Roman、Consolas
  - 字号标准：封面标题42pt、章节标题26pt、正文14pt
- **版式规范**：详见 [assets/consulting-template-spec.md](assets/consulting-template-spec.md)
- **样式库**：完整CSS样式库见 [assets/consulting-report-style.css](assets/consulting-report-style.css)

## 使用示例

### 示例 1：高端算法人才寻聘
**功能说明**：为算法岗位精准推荐候选人
**执行方式**：指挥 Agent + 采集 Agent + 画像 Agent + 匹配 Agent

**关键步骤**：
1. 指挥 Agent 解析岗位需求："北京，大模型算法专家，3年以上经验"
2. 采集 Agent 从内部简历库 + 外部平台采集候选人数据
3. 画像 Agent 生成候选人 360° 画像
4. 匹配 Agent 调用 `talent_matcher.py` 计算匹配度，输出 Top-10 候选人
5. 指挥 Agent 调用 `batch_generator.py` 生成报告

**报告生成**：
```bash
# 默认生成交互式可视化HTML和PDF两种格式（推荐）
python scripts/batch_generator.py --data candidates.json --output 候选人推荐报告

# 输出文件：
# - 候选人推荐报告.html (交互式可视化动态报告 - 默认)
# - 候选人推荐报告.pdf (默认)
```

### 示例 2：AI 行业人才分布分析
**功能说明**：分析 AI 行业人才地域与技能分布
**执行方式**：指挥 Agent + 洞察 Agent + 校验 Agent

**关键步骤**：
1. 指挥 Agent 定义分析范围：AI 行业、全国范围
2. 洞察 Agent 分析人才地域分布、技能密度、梯队结构
3. 校验 Agent 验证分析结果可信度
4. 指挥 Agent 调用 `batch_generator.py` 生成可视化报告

**报告生成**：
```bash
# 生成动态可视化报告（包含交互式图表）
python scripts/batch_generator.py --data analysis.json --output 人才分布分析 --formats interactive

# 输出文件：
# - 人才分布分析_interactive.html
```

### 示例 3：竞品人才 Mapping
**功能说明**：分析竞品公司人才结构
**执行方式**：指挥 Agent + 采集 Agent + 洞察 Agent

**关键步骤**：
1. 指挥 Agent 识别竞品公司清单
2. 采集 Agent 采集竞品公开人才信息
3. 洞察 Agent 分析竞品人才分布、技术栈、团队结构
4. 指挥 Agent 调用 `batch_generator.py` 生成竞品分析报告

**报告生成**：
```bash
# 生成所有格式（完整报告包）
python scripts/batch_generator.py --data competitor.json --output 竞品人才分析 --all-formats

# 输出文件：
# - 竞品人才分析.html
# - 竞品人才分析.pdf
# - 竞品人才分析.docx
# - 竞品人才分析.pptx
# - 竞品人才分析.xlsx
# - 竞品人才分析_interactive.html
```

### 报告生成流程说明

**步骤 1：数据准备**
将分析结果整理为 JSON 格式，包含：
- 基本信息（报告名称、类型、范围、周期等）
- 执行摘要
- 分析结果（候选人列表、统计数据等）

**步骤 2：选择生成方式**

**方式 A：默认格式（推荐）**
```bash
# 用户未指定格式时，自动生成交互式可视化HTML和PDF
python scripts/batch_generator.py --data report.json --output report
```

**方式 B：指定格式**
```bash
# 用户明确要求特定格式
python scripts/batch_generator.py --data report.json --output report --formats html ppt
```

**方式 C：全部格式**
```bash
# 需要完整报告包时
python scripts/batch_generator.py --data report.json --output report --all-formats
```

**步骤 3：输出交付**
- 交互式可视化HTML格式：交互式动态报告，在线查看、一键下载，包含6种图表
- PDF格式：适合打印存档、正式归档、保持格式一致，可下载
- 其他格式：根据需求选择

### 输出格式选择指南

| 场景 | 推荐格式 | 说明 |
|------|---------|------|
| 常规交付 | 交互式可视化HTML + PDF | 默认组合，覆盖在线和归档需求 |
| 领导汇报 | PPT | 幻灯片演示 |
| 数据分析 | Excel | 表格化数据，便于二次分析 |
| 需要编辑 | Word | 可编辑文档格式 |
| 在线展示 | Interactive | 交互式图表，用户体验最佳 |

## 实施路径

### 阶段 1（0-3 月）：基础能力搭建
- 数据源对接：HRIS、OA、简历库
- 基础采集清洗：数据去重、标准化
- 简单搜索匹配：关键词搜索、基础筛选

### 阶段 2（3-6 月）：智能化升级
- 知识图谱构建：实体识别、关系抽取
- 智能画像：360° 人才画像
- 语义匹配：基于向量相似度的精准匹配
- 基础可视化：人才地图、分布图

### 阶段 3（6-12 月）：深度分析
- 洞察分析：趋势、缺口、竞品、风险
- 预警系统：流失预警、挖角预警
- 多 Agent 协同：自动化流程
- 深度定制：行业特定分析

### 阶段 4（持续）：迭代优化
- 模型迭代：基于反馈持续优化
- 场景扩展：新增应用场景
- 生态集成：与第三方系统集成

详见 [references/implementation-guide.md](references/implementation-guide.md)


---

## 📜 版权声明与使用协议

**版权所有 @MikiMiko**

### 🔒 知识产权声明
- 本技能的核心算法、业务逻辑、数据模型及可视化方案均为原创知识产权
- HTML模板、图表配色方案、报告结构为独家设计，受著作权保护
- 禁止未经授权的二次分发、逆向工程、商业转售

### ✅ 授权使用范围
- ✅ 个人学习、内部使用、非商业用途可自由使用
- ❌ 禁止对本技能进行二次开发和改进
- ✅ 虾评平台内的下载、安装、评测等正常使用行为
- ❌ 禁止剥离版权声明后重新发布为"原创"技能
- ❌ 禁止用于商业产品或收费服务（需单独授权）

### 🤝 商业合作
- 如需商业授权或定制开发，请通过虾评平台联系开发者。
