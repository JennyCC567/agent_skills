# 文档输出格式指南（红线规则V6.2）

## 目录
1. [适用范围](#适用范围)
2. [核心要点](#核心要点)
3. [图表生成规范](#图表生成规范)
4. [PDF生成规范](#pdf生成规范)
5. [默认输出格式](#默认输出格式)
6. [HTML模板规范](#html模板规范)
7. [四阶验证流程](#四阶验证流程)
8. [日期防幻觉](#日期防幻觉)

---

## 适用范围

技能商店上架、用户订阅使用、精选案例展示，所有技能生成的HTML/PDF/Word/PPT/Excel等交付物，以及技能本身的所有文件。

**优先级**：强制执行，违反即视为交付不合格。

---

## 核心要点

| 序号 | 要点 | 说明 |
|------|------|------|
| 1 | 数据安全与防泄漏 | AES-256加密、动态脱敏、输出边界隔离、审计留痕 |
| 2 | 禁JS图表库 | 统一使用matplotlib base64 PNG |
| 3 | PDF导出标准 | 商务极简风，HTML内置一键导出 |
| 4 | PDF导出依赖 | 涉及PDF导出必须说明pdflatex依赖，提供降级方案 |
| 5 | 禁emoji | emoji用文本替代 |
| 6 | 日期要求 | 必须使用datetime.now()生成真实日期 |
| 7 | HTML规范 | 禁Flex/Grid |
| 8 | 视觉设计 | 渐变商务蓝、A4标准、850px宽度 |
| 9 | 四阶验证 | 在线->断网->下载->多浏览器 |
| 10 | 默认输出格式 | 数据分析类HTML+Excel，非数据分析类HTML内置PDF导出 |
| 11 | 脱敏处理 | 上传附件前必须脱敏 |

---

## 图表生成规范

### 禁止JS图表库

| 禁止项 | 问题 |
|--------|------|
| ECharts | 完整库约1MB，无法完整内嵌 |
| Chart.js | weasyprint无法渲染JS |
| D3.js / plotly | weasyprint不执行JavaScript |

**结论**：JS图表 = HTML里图表空白 + PDF里图表空白 = 双重失败

### 正确方案：matplotlib -> base64 PNG

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import base64, io

# 注册中文字体
fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

def fig_to_base64(fig):
    """matplotlib图表 -> base64字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
```

### HTML嵌入方式

```html
<!-- 正确 -->
<img src="data:image/png;base64,{base64字符串}" alt="图表说明" style="max-width:100%;height:auto;">

<!-- 错误：JS图表库 -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<div id="chart"></div>
```

### 图表质量标准

| 参数 | 要求 |
|------|------|
| DPI | >=150 |
| 格式 | PNG |
| 背景 | 白色（facecolor='white'） |
| 中文 | 必须注册WenQuanYi Micro Hei字体 |
| 色系 | 深蓝#1F4E79 / 浅蓝#4A90D9 / 青绿#2CA58D |

---

## PDF生成规范

### 禁止wkhtmltopdf和weasyprint

| 工具 | 问题 |
|------|------|
| wkhtmltopdf | 中文重复渲染、Unicode图标乱码 |
| weasyprint | PDF版本1.7兼容性差、文件头emoji字符 |

### 正确方案：reportlab直接生成PDF

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm

# 注册中文字体
pdfmetrics.registerFont(TTFont('WenQuanYi', '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))

# 创建文档
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        topMargin=2*cm, bottomMargin=2*cm,
                        leftMargin=2*cm, rightMargin=2*cm)

# 定义样式
title_style = ParagraphStyle('Title', fontName='WenQuanYi', fontSize=20,
                              textColor=HexColor('#1F4E79'), alignment=TA_CENTER)
```

### reportlab PDF规范

| 要求 | 说明 |
|------|------|
| 中文字体注册 | pdfmetrics.registerFont(TTFont(...)) |
| 所有字体 | fontName='WenQuanYi' |
| 图片嵌入 | RLImage(chart_path, width=16*cm, height=8*cm) |
| 表头样式 | 深蓝#1F4E79背景 + 白字 |
| 斑马纹 | ROWBACKGROUNDS 交替白色/#F2F2F2 |
| 页边距 | 上下左右各2cm |

---

## 默认输出格式

### 数据分析类技能

| 文件类型 | 格式 | 功能 |
|----------|------|------|
| HTML版 | .html | 在线查看 + 下载 + 一键导出PDF |
| Excel版 | .xlsx | 数据分析 + 离线使用 |

### 非数据分析类技能

| 文件类型 | 格式 | 功能 |
|----------|------|------|
| HTML版 | .html | 在线查看 + 下载 + 一键导出PDF |

### HTML内置一键导出PDF

```html
<!-- 导出按钮 -->
<div style="text-align:center; margin:20px 0;">
    <button onclick="window.print()" style="padding:10px 30px; background:#1F4E79; color:#fff; border:none; border-radius:4px; font-size:14px; cursor:pointer;">
        导出PDF
    </button>
</div>

<!-- 打印优化样式 -->
<style>
@media print {
    body { max-width: 100% !important; margin: 0 !important; padding: 0 !important; }
    .no-print { display: none !important; }
    img { max-width: 100% !important; page-break-inside: avoid; }
    table { page-break-inside: avoid; }
    h1, h2, h3 { page-break-after: avoid; }
}
</style>
```

### 文件命名规范

| 格式 | 命名规则 | 示例 |
|------|----------|------|
| HTML | {主题}报告.html | 招聘漏斗驾驶舱.html |
| Excel标准 | {主题}_分析报告_{YYYYMMDD}.xlsx | 招聘漏斗_分析报告_20260519.xlsx |
| Excel驾驶舱 | {主题}_驾驶舱_{YYYYMMDD}.xlsx | 招聘漏斗_驾驶舱_20260519.xlsx |

---

## HTML模板规范

### 必须满足

```css
body {
    font-family: 'WenQuanYi Micro Hei', 'Microsoft YaHei', sans-serif;
}
```

- 零JS依赖（图表用matplotlib base64 PNG）
- 零外部URL（图片/字体/脚本全部内嵌）
- 断网可正常打开
- 纯CSS布局（block + inline + table），避免flex/grid

### 禁止项清单

| 禁止项 | 替代方案 |
|--------|----------|
| ECharts / Chart.js / D3.js / plotly | matplotlib -> base64 PNG |
| 外部CDN链接 | 删除 |
| 外部图片URL | base64内嵌 |
| emoji / 特殊Unicode图标 | 纯文本（如 [OK] [!] [推荐]） |
| CSS Flex复杂布局 | 传统block / table布局 |
| CSS Grid布局 | 传统block / table布局 |
| CSS变量 var(--xxx) | 直接写颜色值 |
| JavaScript代码 | 删除（唯一例外：window.print()） |

---

## 四阶验证流程

| 序号 | 验证阶段 | 验证项 | 通过标准 |
|------|----------|--------|----------|
| 1 | 在线正常 | HTML在线打开 | 图表正常显示，无JS报错 |
| 2 | 在线正常 | HTML图表可见 | base64 PNG图片正常渲染 |
| 3 | 在线正常 | PDF在线打开 | 扣子平台可预览，中文无乱码 |
| 4 | 断网正常 | HTML断网打开 | 所有内容正常 |
| 5 | 下载正常 | PDF下载后打开 | Adobe Reader/WPS/浏览器均可打开 |
| 6 | 下载正常 | Excel下载后打开 | Excel/WPS/Google Sheets均可打开 |
| 7 | 多浏览器 | Chrome/Firefox/Edge | 纯HTML+CSS稳定显示 |
| 8 | 内容检查 | PDF无重复字符 | 无"优优化化"等重复 |
| 9 | 内容检查 | 无emoji残留 | HTML和PDF中无特殊Unicode图标 |
| 10 | 内容检查 | 日期真实 | 非硬编码，使用系统时间 |
| 11 | 内容检查 | 图表数据一致 | HTML/PDF/Excel图表数据一致 |

### 自动验证脚本

```python
import re

def validate_html(html_content):
    """验证HTML是否符合红线规则"""
    errors = []
    
    # 检查JS图表库
    if re.search(r'echarts|chart\.js|d3\.js', html_content, re.IGNORECASE):
        errors.append("发现JS图表库引用")
    
    # 检查script标签
    if re.search(r'<script', html_content, re.IGNORECASE):
        errors.append("发现<script>标签")
    
    # 检查外部URL
    if re.search(r'https?://', html_content):
        errors.append("发现外部URL引用")
    
    # 检查CSS Flex
    if re.search(r'display:\s*flex', html_content):
        errors.append("发现CSS Flex布局")
    
    return errors
```

---

## 日期防幻觉

**所有自动生成的评估报告，其日期字段必须自动填充为用户执行生成操作的真实系统时间，严禁预设、虚构任何日期数据。**

适用范围：
- 报告生成日期
- 数据分析截止日期
- 评估时间戳

```python
from datetime import datetime

# 正确：使用系统时间
report_date = datetime.now().strftime('%Y-%m-%d')

# 错误：硬编码日期
report_date = '2024-01-15'  # 禁止
```

---

## 合规检查清单

### 交付前必查

```
[ ] 无JS图表库引用
[ ] 无外部CDN链接
[ ] 无外部图片URL
[ ] 无emoji字符
[ ] 无CSS Flex/Grid布局
[ ] 无CSS变量
[ ] 日期使用系统时间
[ ] 图表base64内嵌
[ ] 四阶验证通过
```

### 数据脱敏检查

```
[ ] 上传附件前已脱敏
[ ] 姓名/手机号/邮箱/住址已处理
[ ] 敏感信息已替换为占位符
[ ] 输出内容不含原始数据
```
