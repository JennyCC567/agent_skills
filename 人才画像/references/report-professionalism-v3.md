# 报告专业性增强 v3.0

> **版本**：v3.0
> **更新日期**：2026-06-08
> **适用范围**：所有报告模板与生成规范

---

## 目录

1. [执行摘要](#1-执行摘要)
2. [核心结论](#2-核心结论)
3. [品牌定制](#3-品牌定制)
4. [报告模板](#4-报告模板)

---

## 1. 执行摘要

### 1.1 执行摘要定义

执行摘要是报告的"电梯演讲"，用1-2页篇幅呈现最核心的发现和结论，让决策者快速把握要点。

### 1.2 执行摘要结构

```markdown
# 执行摘要

## 一句话结论
{用一句话概括报告的核心发现，通常15-25个字}

## 核心数据
| 指标 | 数值 | 同比变化 | 趋势 |
|------|------|----------|------|
| 人才总量 | XX人 | +XX% | ↑↓ |
| 平均薪资 | XX元/月 | +XX% | ↑↓ |
| 供需比 | X.X | -XX% | ↓↑ |
| 平均匹配度 | XX% | +XX% | ↑ |

## 关键发现（3-5条）
1. **{发现标题}**：{1-2句话说明发现内容}
2. **{发现标题}**：{1-2句话说明发现内容}
3. **{发现标题}**：{1-2句话说明发现内容}

## 行动建议（Top 3）
1. **{建议标题}**：{具体建议内容}
2. **{建议标题}**：{具体建议内容}
3. **{建议标题}**：{具体建议内容}
```

### 1.3 执行摘要示例

```markdown
# 执行摘要

## 一句话结论
2026年AI人才市场竞争加剧，技术类岗位供需比降至0.35，建议企业提前布局校园招聘并优化薪酬结构。

## 核心数据
| 指标 | 数值 | 同比变化 | 趋势 |
|------|------|----------|------|
| 技术人才总量 | 45,200人 | +18.5% | ↑ |
| 算法工程师薪资 | 42,000元/月 | +12.3% | ↑ |
| 技术岗供需比 | 0.35 | -28.6% | ↓ |
| 平均入职周期 | 32天 | +5天 | ↑ |

## 关键发现
1. **算法工程师严重紧缺**：供需比0.15，招聘周期延长至45天，需提前储备
2. **薪资涨幅超预期**：技术岗薪资平均涨幅12.3%，高于市场预测的8%
3. **学历门槛提升**：硕士及以上占比达68%，博士需求增长35%
4. **地域集中度高**：北京、上海、深圳占总量65%，二三线城市人才匮乏

## 行动建议
1. **加快技术人才储备**：启动秋季校园招聘，提前锁定优秀毕业生
2. **优化薪酬竞争力**：技术岗薪资对标75分位，确保薪酬吸引力
3. **拓展远程招聘**：针对紧缺岗位开放远程工作，拓宽人才来源
```

---

## 2. 核心结论

### 2.1 核心结论结构

```python
# 核心结论数据结构
core_conclusions = {
    "conclusion_group": [
        {
            "group_id": "T001",
            "group_title": "人才供需",
            "conclusions": [
                {
                    "id": "T001-01",
                    "title": "技术人才严重紧缺",
                    "level": "high",  # high/medium/low
                    "evidence": [
                        "供需比0.15",
                        "招聘周期45天",
                        "薪资溢价25%"
                    ],
                    "impact": "影响企业技术布局和项目交付",
                    "recommendation": "加快储备，优化渠道"
                }
            ]
        }
    ],
    "priority_matrix": {
        "high_impact_high_urgency": ["T001-01", "T002-03"],
        "high_impact_low_urgency": ["T001-02"],
        "low_impact_high_urgency": ["T002-01"],
        "low_impact_low_urgency": ["T003-01"]
    }
}
```

### 2.2 结论分级标准

| 等级 | 定义 | 影响范围 | 响应时效 |
|------|------|----------|----------|
| 高（High） | 战略级影响 | 全局/长期 | 立即行动 |
| 中（Medium） | 战术级影响 | 局部/中期 | 本季度内 |
| 低（Low） | 运营级影响 | 短期 | 下季度关注 |

### 2.3 结论撰写规范

```markdown
## 结论编号：{ID}

### {结论标题}
**等级**：{High/Medium/Low}

**核心发现**：
{用2-3句话说明核心发现，包含具体数据和对比}

**支撑证据**：
- {证据1}：{数据或事实}
- {证据2}：{数据或事实}
- {证据3}：{数据或事实}

**影响分析**：
{分析该发现对企业/业务的影响，包括：
- 短期影响（1-3个月）
- 中期影响（3-12个月）
- 长期影响（1年以上）
}

**建议行动**：
1. **{行动1}**：{具体行动内容}
2. **{行动2}**：{具体行动内容}
3. **{行动3}**：{具体行动内容}

**责任部门**：{建议负责部门}
**完成时限**：{建议完成时间}
```

### 2.4 结论示例

```markdown
## 结论编号：T001-01

### 算法工程师供需比创历史新低
**等级**：High

**核心发现**：
2026Q1算法工程师供需比降至0.15，创近5年历史新低。招聘周期从28天延长至45天，薪资溢价达25%仍难以快速填补岗位空缺。

**支撑证据**：
- 供需比：0.15（同比-42%）
- 平均招聘周期：45天（同比+60%）
- 薪资溢价：25%（同比+8pp）
- 职位空缺：2,800个
- 有效候选：420人

**影响分析**：
- **短期**：AI产品研发进度延迟2-3个月
- **中期**：核心技术竞争力下降
- **长期**：市场份额可能被竞争对手蚕食

**建议行动**：
1. **启动紧急招聘**：开辟猎头渠道，提高薪资竞争力
2. **校园提前储备**：与高校合作，提前锁定优秀毕业生
3. **远程招聘开放**：开放算法岗位远程工作，吸引外地域人才
4. **外包补充**：短期通过技术外包弥补人力缺口

**责任部门**：人力资源部 + 技术部
**完成时限**：2026年Q2末
```

---

## 3. 品牌定制

### 3.1 品牌定制配置

```python
# 品牌定制配置
brand_customization = {
    "brand_info": {
        "company_name": "示例科技",
        "logo_url": "data:image/png;base64,{logo_base64}",
        "brand_color": {
            "primary": "#1F4E79",      # 主色（深蓝）
            "secondary": "#4A90D9",    # 辅助色（浅蓝）
            "accent": "#2CA58D",       # 强调色（青绿）
            "warning": "#FFA000",      # 警示色（橙色）
            "danger": "#C62828",       # 危险色（红色）
            "success": "#2E7D32"      # 成功色（绿色）
        },
        "font_family": "WenQuanYi Micro Hei, Microsoft YaHei",
        "font_size_base": "12pt"
    },
    "report_style": {
        "layout": "A4",
        "orientation": "portrait",
        "margins": {
            "top": 2.5,
            "bottom": 2.5,
            "left": 3.0,
            "right": 2.5
        },
        "header": {
            "show": True,
            "height": 1.5,
            "logo_position": "left",
            "title_position": "center"
        },
        "footer": {
            "show": True,
            "height": 1.0,
            "page_number": True,
            "confidential": True
        }
    },
    "chart_style": {
        "colors": ["#1F4E79", "#4A90D9", "#2CA58D", "#FFA000", 
                  "#C62828", "#2E7D32", "#7B1FA2", "#455A64"],
        "title_font": "WenQuanYi Micro Hei",
        "title_size": 14,
        "label_font": "WenQuanYi Micro Hei",
        "label_size": 10
    }
}
```

### 3.2 Logo设计规范

| 规范项 | 要求 | 说明 |
|--------|------|------|
| 格式 | PNG/SVG | 优先SVG，支持透明背景 |
| 尺寸 | 宽度80-120px | 等比缩放，高度自适应 |
| 文件大小 | ≤50KB | 压缩后嵌入 |
| 颜色模式 | RGB | 确保屏幕显示正确 |
| 最小分辨率 | 150DPI | 确保打印清晰 |

### 3.3 品牌定制HTML模板

```html
<!-- 品牌定制报告头部 -->
<div class="report-header">
    <div class="header-left">
        <img src="data:image/png;base64,{logo_base64}" 
             alt="公司Logo" 
             class="brand-logo"
             style="height:60px;max-width:120px;">
    </div>
    <div class="header-center">
        <h1 class="report-title" 
            style="color:#1F4E79;font-family:'WenQuanYi Micro Hei';font-size:24pt;">
            人才Mapping分析报告
        </h1>
    </div>
    <div class="header-right">
        <p class="report-meta" style="font-size:10pt;color:#666;">
            {report_date}<br>
            <span style="color:#1F4E79;font-weight:bold;">{company_name}</span>
        </p>
    </div>
</div>

<style>
.report-header {
    display: table;
    width: 100%;
    border-bottom: 2px solid #1F4E79;
    padding-bottom: 15px;
    margin-bottom: 20px;
}
.header-left, .header-center, .header-right {
    display: table-cell;
    vertical-align: middle;
}
.header-left { width: 15%; text-align: left; }
.header-center { width: 70%; text-align: center; }
.header-right { width: 15%; text-align: right; }
</style>
```

### 3.4 品牌定制Word模板

```python
# Word品牌定制模板
def create_brand_word_template(config: Dict):
    from docx import Document
    from docx.shared import Inches, Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    
    doc = Document()
    
    # 设置页面布局
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        section.left_margin = Inches(1.18)  # 3cm
        section.right_margin = Inches(0.98)  # 2.5cm
        section.top_margin = Inches(0.98)  # 2.5cm
        section.bottom_margin = Inches(0.98)
    
    # 添加品牌头部
    header = section.header
    header.is_linked_to_previous = False
    
    # 添加Logo
    logo_para = header.paragraphs[0]
    logo_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = logo_para.add_run()
    run.add_picture(config['brand_info']['logo_url'], 
                   width=Inches(1.2))
    
    # 添加报告标题
    title_para = header.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_para.add_run('人才Mapping分析报告')
    title_run.font.name = 'WenQuanYi Micro Hei'
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.color.rgb = config['brand_info']['brand_color']['primary']
    
    # 添加分隔线
    p = header.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p_pr = p._p.get_or_add_ppr()
    p_bdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F4E79')
    p_bdr.append(bottom)
    p_pr.append(p_bdr)
    
    return doc
```

---

## 4. 报告模板

### 4.1 标准报告结构

```markdown
# {报告标题}

## 报告信息
| 项目 | 内容 |
|------|------|
| 报告名称 | {报告名称} |
| 分析周期 | {开始日期} - {结束日期} |
| 报告类型 | {报告类型} |
| 数据口径 | {数据来源说明} |
| 生成时间 | {生成时间} |
| 报告版本 | v{版本号} |

---

## 一、执行摘要

{执行摘要内容}

---

## 二、人才概况

### 2.1 人才总量与分布

{数据表格和分析}

### 2.2 人才结构分析

{学历分布、工作年限、技能分布等}

---

## 三、教育背景分析

### 3.1 学历分布

{学历分布图表和分析}

### 3.2 院校背景

{毕业院校分布}

### 3.3 专业分布

{所学专业分布}

---

## 四、技能图谱

### 4.1 核心技能

{技能标签云/柱状图}

### 4.2 技能组合分析

{技能关联分析}

---

## 五、薪资分析

### 5.1 薪资分布

{薪资分布图表}

### 5.2 薪资Benchmark

{与市场对比}

---

## 六、地域分布

### 6.1 地域分布热力图

{热力图}

### 6.2 地域流动性分析

{流动分析}

---

## 七、核心结论

{核心结论内容}

---

## 八、行动建议

{建议内容}

---

## 附录

### 附录A 数据说明
{数据来源、质量说明}

### 附录B 方法论
{分析方法、模型说明}

### 附录C 术语表
{专业术语解释}

---

## 免责声明

{免责声明内容}

---

**报告制作**：{公司名称}
**联系方式**：{联系方式}
**版权声明**：{版权说明}
```

### 4.2 报告生成配置

```python
# 报告生成配置
report_generation_config = {
    "report_type": "standard",  # standard/comprehensive/executive
    
    "sections": {
        "executive_summary": {
            "include": True,
            "position": 1,
            "template": "executive_summary_v1"
        },
        "talent_overview": {
            "include": True,
            "position": 2,
            "charts": ["bar", "pie"]
        },
        "education_analysis": {
            "include": True,
            "position": 3,
            "charts": ["bar", "pie"],
            "education_constraint": True  # 硬性约束
        },
        "skill_analysis": {
            "include": True,
            "position": 4,
            "charts": ["wordcloud", "bar"]
        },
        "salary_analysis": {
            "include": True,
            "position": 5,
            "charts": ["histogram", "benchmark"]
        },
        "geo_distribution": {
            "include": True,
            "position": 6,
            "charts": ["heatmap", "sankey"]
        },
        "conclusions": {
            "include": True,
            "position": 7,
            "template": "conclusions_v1"
        },
        "recommendations": {
            "include": True,
            "position": 8,
            "priority_limit": 5
        }
    },
    
    "brand": {
        "customize": True,
        "logo_required": True,
        "color_scheme": "default"  # default/custom
    },
    
    "output": {
        "formats": ["html", "pdf", "excel"],
        "default_format": "html",
        "filename_pattern": "{report_name}_{date}"
    }
}
```

### 4.3 报告质量检查清单

```python
# 报告质量检查清单
quality_checklist = {
    "完整性检查": {
        "必含章节": [
            "执行摘要",
            "人才概况",
            "教育背景分析（学历必填）",
            "核心结论",
            "行动建议"
        ],
        "检查项": [
            "所有章节标题完整",
            "所有数据表格有数据",
            "所有图表有图注",
            "所有引用有来源标注"
        ]
    },
    "准确性检查": {
        "数据验证": [
            "数据求和一致",
            "百分比相加=100%",
            "同比/环比计算正确",
            "日期格式统一"
        ],
        "逻辑验证": [
            "结论与数据一致",
            "建议有数据支撑",
            "图表与文字一致"
        ]
    },
    "规范性检查": {
        "格式规范": [
            "字体统一（WenQuanYi）",
            "字号符合规范",
            "对齐方式统一",
            "行距1.5倍"
        ],
        "内容规范": [
            "学历字段不缺失",
            "日期使用真实时间",
            "无硬编码数据",
            "无emoji字符"
        ]
    },
    "专业性检查": {
        "语言规范": [
            "专业术语准确",
            "避免口语化表达",
            "逻辑清晰连贯",
            "结论明确具体"
        ],
        "视觉规范": [
            "图表清晰可读",
            "配色协调统一",
            "排版专业美观",
            "留白合理适当"
        ]
    }
}

def run_quality_check(report_data: Dict) -> Dict:
    """执行报告质量检查"""
    results = {
        "passed": True,
        "errors": [],
        "warnings": [],
        "check_items": {}
    }
    
    # 检查学历字段
    if 'education_analysis' in report_data:
        education = report_data['education_analysis']
        if not education.get('highest_education'):
            results['errors'].append("学历字段缺失，违反硬性约束")
            results['passed'] = False
    
    # 检查日期
    if not report_data.get('generated_at'):
        results['errors'].append("生成日期缺失")
        results['passed'] = False
    elif report_data['generated_at'] == '2026-01-01':
        results['warnings'].append("日期可能为硬编码，请确认")
    
    # 检查图表数量
    chart_count = len(report_data.get('charts', []))
    if chart_count < 3:
        results['warnings'].append(f"图表数量偏少（{chart_count}个），建议增加")
    
    return results
```

---

## 5. 输出格式规范

### 5.1 HTML报告规范

```html
<!-- HTML报告头部 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{报告标题} - {公司名称}</title>
    <style>
        body {
            font-family: 'WenQuanYi Micro Hei', 'Microsoft YaHei', sans-serif;
            font-size: 12pt;
            line-height: 1.5;
            color: #333;
            max-width: 850px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { font-size: 20pt; color: #1F4E79; text-align: center; }
        h2 { font-size: 16pt; color: #1F4E79; border-bottom: 2px solid #1F4E79; }
        h3 { font-size: 14pt; color: #333; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th { background: #1F4E79; color: white; padding: 10px; }
        td { border: 1px solid #ddd; padding: 8px; }
        .chart-wrapper { margin: 20px 0; text-align: center; }
        .chart-caption { font-size: 10pt; color: #666; text-align: center; }
        @media print {
            body { max-width: none; }
            .page-break { page-break-before: always; }
        }
    </style>
</head>
<body>
    <!-- 报告内容 -->
</body>
</html>
```

### 5.2 PDF报告规范

```python
# PDF报告生成规范
def generate_pdf_report(data: Dict, config: Dict) -> str:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
    from reportlab.lib.colors import HexColor
    
    # 注册中文字体
    pdfmetrics.registerFont(TTFont('WenQuanYi', '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))
    
    # 创建文档
    doc = SimpleDocTemplate(
        config['output_path'],
        pagesize=A4,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        leftMargin=3*cm,
        rightMargin=2.5*cm
    )
    
    # 定义样式
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        fontName='WenQuanYi',
        fontSize=20,
        textColor=HexColor('#1F4E79'),
        alignment=1,  # 居中
        spaceAfter=20
    )
    
    # 构建内容
    story = []
    
    # 添加标题
    story.append(Paragraph(data['report_title'], title_style))
    story.append(Spacer(1, 20))
    
    # 添加执行摘要
    story.append(Paragraph('一、执行摘要', styles['Heading1']))
    story.append(Paragraph(data['executive_summary'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # 添加图表
    for chart in data['charts']:
        img = Image(chart['path'], width=16*cm, height=8*cm)
        story.append(img)
        story.append(Paragraph(chart['caption'], styles['Normal']))
        story.append(Spacer(1, 15))
    
    # 生成PDF
    doc.build(story)
    
    return config['output_path']
```

### 5.3 Excel报告规范

```python
# Excel报告生成规范
def generate_excel_report(data: Dict, config: Dict) -> str:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    
    wb = Workbook()
    
    # 定义样式
    header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
    header_font = Font(name='WenQuanYi Micro Hei', size=11, color='FFFFFF', bold=True)
    data_font = Font(name='WenQuanYi Micro Hei', size=10)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Sheet 1: 数据概览
    ws1 = wb.active
    ws1.title = '数据概览'
    
    # 添加标题
    ws1['A1'] = '人才Mapping分析报告'
    ws1['A1'].font = Font(name='WenQuanYi Micro Hei', size=16, bold=True, color='1F4E79')
    
    # 添加数据
    for row_idx, row_data in enumerate(data['overview'], start=3):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=value)
            cell.font = data_font
            cell.border = thin_border
    
    # 设置列宽
    ws1.column_dimensions['A'].width = 20
    ws1.column_dimensions['B'].width = 15
    
    # Sheet 2: 教育背景（学历必填）
    ws2 = wb.create_sheet('教育背景')
    ws2['A1'] = '教育背景分析'
    ws2['A1'].font = Font(name='WenQuanYi Micro Hei', size=14, bold=True, color='1F4E79')
    
    # 添加表头（学历必填）
    headers = ['姓名', '最高学历', '毕业院校', '所学专业', '毕业年份']
    for col_idx, header in enumerate(headers, start=1):
        cell = ws2.cell(row=3, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    
    # 添加数据
    for row_idx, candidate in enumerate(data['candidates'], start=4):
        ws2.cell(row=row_idx, column=1, value=candidate['name']).font = data_font
        ws2.cell(row=row_idx, column=2, value=candidate['education']).font = data_font  # 学历必填
        ws2.cell(row=row_idx, column=3, value=candidate['school']).font = data_font
        ws2.cell(row=row_idx, column=4, value=candidate['major']).font = data_font
        ws2.cell(row=row_idx, column=5, value=candidate['graduation_year']).font = data_font
    
    wb.save(config['output_path'])
    return config['output_path']
```
