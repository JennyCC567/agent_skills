# 交互式可视化HTML报告功能说明

## 功能概述

交互式可视化HTML报告提供以下功能：
1. **在线查看**：直接在浏览器中查看报告
2. **一键下载HTML**：下载HTML文件到本地
3. **PDF一键导出下载**：通过浏览器打印功能导出PDF

## 下载按钮

### 1. 下载HTML按钮
- **按钮文字**：📄 下载HTML
- **功能**：下载当前HTML文件到本地
- **文件名**：`{报告名称}.html`
- **文件格式**：HTML文件，包含所有内容和样式

### 2. 导出PDF按钮
- **按钮文字**：📄 导出PDF
- **功能**：调用浏览器打印对话框，用户可选择"另存为PDF"
- **文件名**：用户自定义
- **文件格式**：PDF文件

## 使用方法

### 下载HTML文件
1. 打开交互式可视化HTML报告
2. 点击"📄 下载HTML"按钮
3. HTML文件将自动下载到本地

### 导出PDF文件
1. 打开交互式可视化HTML报告
2. 点击"📄 导出PDF"按钮
3. 浏览器打印对话框打开
4. 在打印对话框中：
   - 选择"目标"或"打印机"为"另存为PDF"
   - 调整页面设置（可选）
   - 点击"保存"
5. 选择保存位置和文件名
6. 点击"保存"完成导出

## 浏览器支持

### Chrome/Edge
1. 点击"导出PDF"按钮
2. 在打印对话框中，目标选择"另存为PDF"
3. 点击"保存"

### Firefox
1. 点击"导出PDF"按钮
2. 在打印对话框中，目标选择"另存为PDF"
3. 点击"保存"

### Safari
1. 点击"导出PDF"按钮
2. 在打印对话框中，点击"PDF"下拉菜单
3. 选择"存储为PDF"
4. 点击"保存"

## 打印优化

交互式可视化HTML报告已针对PDF导出进行优化：

### CSS打印样式
```css
@media print {
    body { background: white; }
    .container { box-shadow: none; padding: 0; }
    .download-buttons { display: none; }  /* 隐藏下载按钮 */
    .chart-wrapper { page-break-inside: avoid; }  /* 避免图表分页 */
    .candidate-card { page-break-inside: avoid; }  /* 避免候选人卡片分页 */
    h1, h2, h3 { page-break-after: avoid; }  /* 避免标题分页 */
}
```

### 打印效果
- ✅ 下载按钮自动隐藏
- ✅ 图表完整显示，避免分页截断
- ✅ 候选人卡片完整显示，避免分页截断
- ✅ 标题与内容在同一页，避免分页
- ✅ 移除阴影和背景，提高打印质量

## 功能对比

| 功能 | 下载HTML | 导出PDF |
|------|---------|---------|
| 交互式图表 | ✅ 保留 | ❌ 静态 |
| 样式完整性 | ✅ 100% | ✅ 100% |
| 打印友好 | ✅ 支持 | ✅ 优化 |
| 离线查看 | ✅ 支持 | ✅ 支持 |
| 文件大小 | 较小 | 较大 |
| 兼容性 | 所有浏览器 | 所有浏览器 |

## 常见问题

### Q1: 为什么导出PDF按钮点击后没有直接下载PDF？
**A:** "导出PDF"功能使用浏览器的打印对话框，用户需要在对话框中选择"另存为PDF"选项。这是最可靠、兼容性最好的PDF生成方式。

### Q2: 导出的PDF中图表是交互式的吗？
**A:** 不，PDF中的图表是静态的图片，不具备交互功能。如果需要交互式图表，请使用HTML格式。

### Q3: 如何调整PDF的页面大小和边距？
**A:** 在打印对话框中，可以调整"页面设置"选项，包括：
- 页面大小（A4、Letter等）
- 边距（默认、无、最小、自定义）
- 缩放（默认、自定义）

### Q4: 为什么PDF中的图表有时会被截断？
**A:** 系统已添加`page-break-inside: avoid`样式来避免图表分页截断。如果仍然出现截断，可以尝试：
- 调整浏览器缩放比例
- 调整PDF页面方向（横向/纵向）
- 减少打印边距

### Q5: PDF文件太大怎么办？
**A:** 可以尝试：
- 减少报告中的图片数量
- 降低图表分辨率
- 使用PDF压缩工具

## 技术实现

### 下载HTML功能
```javascript
function downloadAsHTML() {
    const htmlContent = document.documentElement.outerHTML;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '{{report_name}}.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
```

### 导出PDF功能
```javascript
function exportAsPDF() {
    // 使用浏览器的打印功能，用户可以选择"另存为PDF"
    window.print();
}
```

## 总结

交互式可视化HTML报告提供两种下载方式：
1. **下载HTML**：保留所有交互功能，适合在线查看和分享
2. **导出PDF**：生成静态PDF文档，适合打印和归档

两种方式都完全由浏览器原生支持，无需额外插件或库。

---

**文档版本**：1.0
**最后更新**：2025-04-17
**维护者**：AI人才Mapping智能体团队
