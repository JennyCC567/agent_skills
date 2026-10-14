# 图片使用规范与合规底线

## 重要提示

> ⚠️ **【强制要求】所有技能生成报告时必须严格遵守以下合规底线：**
> - HTML图表：CDN禁止，ECharts等库必须内嵌
> - 所有图片：base64内嵌，不引用外部URL
> - PDF/Word/PPT/Excel：图片完整嵌入，不依赖外部链接
> - 交付前验证：在线正常 → 断网正常 → 各种格式文档下载/导出正常 → 多浏览器兼容
> - **后续生成报告都会按这个标准执行！**

---

## 目录

1. [合规底线概述](#合规底线概述)
2. [HTML图表规范](#html图表规范)
3. [图片内嵌规范](#图片内嵌规范)
4. [多格式导出规范](#多格式导出规范)
5. [交付前验证流程](#交付前验证流程)
6. [常见问题与解决方案](#常见问题与解决方案)

---

## 合规底线概述

### 三条合规底线（绝对禁止）

| 合规底线 | 规则 | 违规后果 |
|------|------|---------|
| **合规底线1** | HTML图表库禁止使用CDN，必须内嵌 | ❌ 违反将导致断网后图表无法显示 |
| **合规底线2** | 所有图片禁止外部URL引用，必须base64内嵌 | ❌ 违反将导致图片丢失或显示异常 |
| **合规底线3** | PDF/Word/Excel导出时禁止外部链接依赖 | ❌ 违反将导致导出文档图片缺失 |

### 正确做法示例

```html
<!-- ✅ 正确：ECharts库内嵌到HTML -->
<script>
  // ECharts完整库代码内嵌
  (function(){
    // ... ECharts完整代码（约1万行） ...
  })();
</script>

<!-- ✅ 正确：图片base64内嵌 -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEA..." />

<!-- ❌ 错误：使用CDN -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

<!-- ❌ 错误：外部图片URL -->
<img src="https://example.com/image.png" />
```

---

## HTML图表规范

### 规则要求

| 图表类型 | 规范要求 | 内嵌方式 |
|---------|---------|---------|
| **ECharts** | 必须内嵌完整库代码 | 直接将库代码粘贴到HTML中 |
| **Chart.js** | 必须内嵌完整库代码 | 直接将库代码粘贴到HTML中 |
| **D3.js** | 必须内嵌完整库代码 | 直接将库代码粘贴到HTML中 |
| **其他图表库** | 必须内嵌完整库代码 | 同上 |

### 内嵌示例

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>报告</title>
  <style>
    /* 内嵌必要样式 */
    .chart-container { width: 100%; height: 400px; }
  </style>
</head>
<body>
  <div id="chart" class="chart-container"></div>
  
  <!-- ✅ 正确：内嵌ECharts库 -->
  <script>
    // ECharts 5.x 完整库代码（必须内嵌完整版，不要使用精简版）
    !function(e,t){"object"==typeof module&&"object"==typeof module.exports?module.exports=e.document?t(e,!0):function(e){if(!e.document)throw new Error("...");
    // ... 完整ECharts代码（约1万行） ...
    }:"function"==typeof define&&define.amd?define("echarts",function(){return t(e)}):(e.echarts||(e.echarts={})).module=e.document?t(e):t(e)}
  </script>
  
  <script>
    // 使用内嵌的ECharts
    var chart = echarts.init(document.getElementById('chart'));
    chart.setOption({/* 图表配置 */});
  </script>
</body>
</html>
```

### 常见错误

```html
<!-- ❌ 错误1：使用CDN -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

<!-- ❌ 错误2：使用本地文件（网络环境不可用时失效） -->
<script src="./libs/echarts.min.js"></script>

<!-- ❌ 错误3：使用npm包引用 -->
<script>
  import * as echarts from 'echarts';
</script>
```

---

## 图片内嵌规范

### 规则要求

| 图片类型 | 规范要求 | 脱敏要求 |
|---------|---------|---------|
| **个人照片** | base64内嵌，可选脱敏 | 建议移除或模糊化 |
| **图表图片** | base64内嵌 | 必须内嵌 |
| **图标图片** | base64内嵌或SVG内联 | 必须内嵌 |
| **装饰图片** | base64内嵌 | 必须内嵌 |

### base64内嵌方法

#### 方法1：手动转换

```javascript
// 使用Python将图片转为base64
import base64

with open('image.png', 'rb') as f:
    data = base64.b64encode(f.read()).decode('utf-8')
    
print(f'data:image/png;base64,{data}')
```

#### 方法2：在线工具转换

1. 访问在线图片转Base64工具（如 https://www.base64-image.de/）
2. 上传图片
3. 复制生成的base64代码
4. 粘贴到HTML中

#### 方法3：JavaScript转换（仅用于用户上传图片）

```javascript
// 处理用户上传的图片
function convertToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = function(e) {
      resolve(e.target.result);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
```

### base64使用示例

```html
<!-- ✅ 正确：PNG图片内嵌 -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="图标" />

<!-- ✅ 正确：JPG图片内嵌 -->
<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..." alt="照片" />

<!-- ✅ 正确：SVG内联 -->
<svg width="24" height="24" viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="10" fill="#3498db"/>
</svg>

<!-- ❌ 错误：外部图片URL -->
<img src="https://example.com/photo.jpg" alt="照片" />

<!-- ❌ 错误：CSS外部图片 -->
<div style="background-image: url('https://example.com/bg.png')">
</div>
```

### CSS图片内嵌方法

```css
/* ✅ 正确：CSS中使用base64内嵌 */
.icon {
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==');
}

/* ✅ 正确：CSS中使用SVG内联 */
.icon-svg {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='12' cy='12' r='10' fill='%233498db'/%3E%3C/svg%3E");
}

/* ❌ 错误：CSS中使用外部URL */
.icon {
  background-image: url('https://example.com/icon.png');
}
```

---

## 多格式导出规范

### PDF导出规范

| 要求 | 说明 |
|------|------|
| **图片嵌入** | 所有图片必须完整嵌入PDF，不依赖外部链接 |
| **图表嵌入** | 图表必须转为图片后嵌入（使用canvas截图） |
| **字体嵌入** | 中文字体必须嵌入，确保跨平台显示一致 |
| **断网验证** | 断网后打开PDF，所有内容完整显示 |

### Word导出规范

| 要求 | 说明 |
|------|------|
| **图片嵌入** | 所有图片必须完整嵌入Word文档 |
| **格式保留** | 保留原始排版、字体、颜色 |
| **兼容性** | 支持Office和WPS双打开 |

### Excel导出规范

| 要求 | 说明 |
|------|------|
| **图片嵌入** | 图表必须转为图片后嵌入 |
| **数据完整** | 所有数据完整导出，无截断 |

### 导出代码示例

```javascript
// PDF导出：使用window.print()
function downloadPDF() {
  // 触发浏览器打印对话框，用户可选择"保存为PDF"
  window.print();
}

// Word导出：使用Blob下载
function downloadWord() {
  const element = document.getElementById('report');
  
  // 添加Word兼容样式
  const wordStyles = `
    <style>
      body { font-family: 'Microsoft YaHei', sans-serif; }
      table { border-collapse: collapse; width: 100%; }
      th, td { border: 1px solid #ddd; padding: 8px; }
    </style>
  `;
  
  const content = wordStyles + element.innerHTML;
  const blob = new Blob([content], { type: 'application/msword' });
  
  // 创建下载链接
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'report.docx';
  link.click();
  
  // 清理
  URL.revokeObjectURL(link.href);
}

// HTML导出：完整保存
function downloadHTML() {
  const html = document.documentElement.outerHTML;
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  
  // 创建下载链接
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'report.html';
  link.click();
  
  // 清理
  URL.revokeObjectURL(link.href);
}
```

---

## 交付前验证流程

> ⚠️ **【强制要求】所有交付物在正式发布前必须完成以下四项验证！**

### 验证1：在线正常

| 步骤 | 操作 | 通过标准 |
|------|------|---------|
| 1 | 打开HTML报告 | 页面正常加载 |
| 2 | 检查所有图表 | 图表正常渲染 |
| 3 | 检查所有图片 | 图片正常显示 |
| 4 | 检查控制台 | 无404错误、无跨域错误 |

### 验证2：断网正常

| 步骤 | 操作 | 通过标准 |
|------|------|---------|
| 1 | 断开网络连接 | - |
| 2 | 刷新页面 | 页面正常加载 |
| 3 | 检查所有图表 | 图表正常显示 |
| 4 | 检查所有图片 | 图片正常显示 |
| 5 | 打开开发者工具 | 无外部资源请求错误 |

**断网测试方法：**

- **Chrome**: 打开开发者工具 → Network → 勾选"Offline"
- **Firefox**: 打开开发者工具 → Network → 勾选"Offline"
- **或者**：直接拔掉网线或关闭WiFi

### 验证3：格式导出正常

| 步骤 | 操作 | 通过标准 |
|------|------|---------|
| 1 | 点击"下载PDF" | PDF下载成功 |
| 2 | 打开PDF | 所有图表、图片完整显示 |
| 3 | 点击"下载Word" | Word下载成功 |
| 4 | 打开Word | 所有图片完整显示 |
| 5 | 点击"下载HTML" | HTML下载成功 |
| 6 | 打开HTML | 所有内容完整显示 |

### 验证4：多浏览器兼容

| 浏览器 | 版本要求 | 验证内容 |
|--------|---------|---------|
| **Chrome** | 最新版 | 页面显示、图表渲染、导出功能 |
| **Firefox** | 最新版 | 页面显示、图表渲染、导出功能 |
| **Edge** | 最新版 | 页面显示、图表渲染、导出功能 |
| **Safari** | 最新版 | 页面显示、图表渲染、导出功能 |

### 验证清单

```
【交付前必检清单】

□ 代码规范检查
  □ 无CDN引用（html-docx-js、FileSaver、html2pdf等第三方库全部禁止）
  □ 所有图表库必须内嵌
  □ 所有图片必须base64内嵌
  □ PDF导出必须使用window.print()

□ 在线验证
  □ HTML页面正常加载
  □ 所有图表正常渲染
  □ 所有图片正常显示
  □ 控制台无错误

□ 断网验证
  □ 页面正常加载
  □ 图表正常显示
  □ 图片正常显示
  □ PDF打印功能正常
  □ 无外部资源请求

□ 导出验证
  □ HTML下载成功，内容完整
  □ PDF打印成功，内容完整

□ 浏览器兼容验证
  □ Chrome测试通过
  □ Firefox测试通过
  □ Edge测试通过
  □ Safari测试通过

□ 报告内容验证
  □ 数据准确无误
  □ 格式排版正确
  □ 无隐私信息泄露
```

---

## 常见问题与解决方案

### 问题1：图表库太大，内嵌后HTML文件过大

**解决方案：**

```javascript
// 按需引入ECharts模块（推荐）
// 只引入使用到的组件，减少代码体积
import * as echarts from 'echarts/core';
import { BarChart, LineChart, PieChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 注册必要的组件
echarts.use([
  BarChart, LineChart, PieChart,
  TitleComponent, TooltipComponent, GridComponent,
  CanvasRenderer
]);

// 使用
var chart = echarts.init(document.getElementById('chart'));
chart.setOption({/* 配置 */});
```

### 问题2：图片base64字符串太长

**解决方案：**

1. **压缩图片尺寸**：使用较小尺寸的图片
2. **选择合适格式**：PNG（图标/透明图）、JPG（照片）、WebP（推荐）
3. **使用SVG**：简单图形使用SVG内联，体积更小

```html
<!-- 推荐：使用SVG替代小图标 -->
<svg width="24" height="24" viewBox="0 0 24 24">
  <path fill="#3498db" d="M12 2L2 7l10 5 10-5-10-5z"/>
</svg>

<!-- 不推荐：小图标也用base64 -->
<img src="data:image/png;base64,iVBORw0..." width="24" height="24" />
```

### 问题3：断网后图表无法显示

**原因：** 使用了CDN链接

**解决方案：** 严格按照合规底线，所有图表库必须内嵌

### 问题4：打印样式优化

**原因：** 打印时样式不理想，需要添加专门的打印样式

**解决方案：**

```css
/* 添加打印样式 */
@media print {
  body { font-size: 12pt; }
  .no-print { display: none; } /* 隐藏不需要打印的元素 */
  @page { margin: 1cm; }
}
```

### 问题5：导出Word后格式错乱

**原因：** CSS样式不兼容Word

**解决方案：**

```javascript
// 添加Word兼容样式
const wordStyles = `
  <style>
    body { font-family: 'Microsoft YaHei', sans-serif; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; }
  </style>
`;

// 导出时包含样式
const content = wordStyles + element.innerHTML;
const blob = new Blob([content], { type: 'application/msword' });

// 创建下载链接
const link = document.createElement('a');
link.href = URL.createObjectURL(blob);
link.download = 'report.docx';
link.click();

// 清理
URL.revokeObjectURL(link.href);
```

---

## 总结

| 规则类型 | 强制要求 | 违规后果 |
|---------|---------|---------|
| **HTML图表** | 必须内嵌，禁止CDN | 断网后无法使用 |
| **图片引用** | 必须base64内嵌，禁止外部URL | 图片无法显示 |
| **PDF导出** | 必须使用window.print()，禁止html2pdf/jsPDF | 断网后无法使用 |
| **下载功能** | 禁止使用第三方库，使用原生API | 断网后无法使用 |
| **导出文档** | 图片必须完整嵌入 | 文档内容缺失 |
| **交付验证** | 必须完成四项验证 | 可能导致用户投诉 |

> ⚠️ **【重要】违反合规底线将导致报告在断网环境或导出后无法正常使用，请务必严格遵守！**
