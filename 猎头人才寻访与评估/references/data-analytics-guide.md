# 数据能力建设指南

## 目录

- [招聘漏斗分析](#招聘漏斗分析)
- [渠道ROI分析](#渠道roi分析)
- [预测性分析](#预测性分析)

---

## 招聘漏斗分析

### 漏斗模型定义

招聘漏斗是将招聘流程各个阶段的候选人数量可视化，追踪每个环节的转化率。

### 标准招聘漏斗阶段

| 阶段 | 指标名称 | 说明 |
|------|----------|------|
| L1 | 简历获取 | 收到的简历总数 |
| L2 | 简历筛选 | 通过初筛的简历数 |
| L3 | 电话沟通 | 完成电话沟通的人数 |
| L4 | 面试邀请 | 发送面试邀请的人数 |
| L5 | 初试 | 完成初试的人数 |
| L6 | 复试 | 完成复试的人数 |
| L7 | Offer | 发放Offer的人数 |
| L8 | 入职 | 实际入职的人数 |

### 漏斗转化率计算

| 指标 | 计算公式 | 健康范围 |
|------|----------|----------|
| 初筛通过率 | L2/L1 | 30%-50% |
| 电话沟通率 | L3/L2 | 60%-80% |
| 面试邀请率 | L4/L3 | 40%-60% |
| 初试完成率 | L5/L4 | 70%-90% |
| 复试完成率 | L6/L5 | 80%-95% |
| Offer接受率 | L7/L6 | 60%-80% |
| 入职率 | L8/L7 | 80%-95% |
| 整体转化率 | L8/L1 | 1%-5% |

### 漏斗可视化HTML模板

```html
<div class="funnel-container">
  <h2>招聘漏斗分析</h2>
  <div class="funnel-chart">
    <!-- L1: 简历获取 -->
    <div class="funnel-stage" style="width: 100%; background: #4A90E2;">
      <span class="stage-label">简历获取</span>
      <span class="stage-value">1000人</span>
    </div>
    <!-- L2: 简历筛选 -->
    <div class="funnel-stage" style="width: 80%; background: #50C8A5;">
      <span class="stage-label">简历筛选</span>
      <span class="stage-value">400人 (40%)</span>
    </div>
    <!-- L3: 电话沟通 -->
    <div class="funnel-stage" style="width: 60%; background: #7B68EE;">
      <span class="stage-label">电话沟通</span>
      <span class="stage-value">240人 (60%)</span>
    </div>
    <!-- L4: 面试邀请 -->
    <div class="funnel-stage" style="width: 45%; background: #FF7F50;">
      <span class="stage-label">面试邀请</span>
      <span class="stage-value">108人 (45%)</span>
    </div>
    <!-- L5: 初试 -->
    <div class="funnel-stage" style="width: 35%; background: #FFD700;">
      <span class="stage-label">初试</span>
      <span class="stage-value">76人 (70%)</span>
    </div>
    <!-- L6: 复试 -->
    <div class="funnel-stage" style="width: 25%; background: #FF69B4;">
      <span class="stage-label">复试</span>
      <span class="stage-value">61人 (80%)</span>
    </div>
    <!-- L7: Offer -->
    <div class="funnel-stage" style="width: 15%; background: #9370DB;">
      <span class="stage-label">Offer</span>
      <span class="stage-value">37人 (61%)</span>
    </div>
    <!-- L8: 入职 -->
    <div class="funnel-stage" style="width: 12%; background: #32CD32;">
      <span class="stage-label">入职</span>
      <span class="stage-value">30人 (81%)</span>
    </div>
  </div>
  <div class="funnel-summary">
    <p>整体转化率: <strong>3.0%</strong></p>
    <p>平均每入职1人，需要获取 <strong>33份</strong> 简历</p>
  </div>
</div>
```

### 漏斗异常诊断

| 异常表现 | 可能原因 | 改进建议 |
|----------|----------|----------|
| 初筛通过率过低 | 职位要求过高/简历来源质量差 | 优化职位描述/拓宽渠道 |
| 电话沟通率低 | 沟通时间不当/话术问题 | 调整拨打时间/优化开场白 |
| Offer接受率低 | 薪资不具竞争力/候选人犹豫 | 优化薪酬方案/加强动机激发 |
| 入职率低 | 候选人反悔/CounterOffer | 做好入职跟进/提供过渡支持 |

---

## 渠道ROI分析

### 渠道ROI评估维度

| 维度 | 说明 |
|------|------|
| 候选人数量 | 各渠道获取的简历数量 |
| 候选人质量 | 各渠道候选人的匹配度评分 |
| 招聘周期 | 各渠道候选人的平均入职周期 |
| 招聘成本 | 各渠道的投入产出比 |
| 留存率 | 各渠道入职候选人的留存情况 |

### ROI计算公式

| 指标 | 计算公式 |
|------|----------|
| 渠道获取成本 | 渠道总花费 / 获取简历数 |
| 单个入职成本 | 渠道总花费 / 入职人数 |
| 渠道产出比 | 入职人数 / 渠道总花费 |
| 质量调整ROI | (入职人数 x 平均匹配度) / 渠道花费 |

### 渠道ROI对比表

| 渠道 | 简历数 | 入职数 | 总花费 | 入职成本 | 质量分 | ROI评分 |
|------|--------|--------|--------|----------|--------|---------|
| Boss直聘 | 500 | 15 | 5000 | 333 | 78 | 2.34 |
| 猎聘 | 200 | 12 | 8000 | 667 | 85 | 1.28 |
| 猎上网 | 50 | 8 | 15000 | 1875 | 92 | 0.49 |
| LinkedIn | 100 | 5 | 3000 | 600 | 90 | 1.50 |
| 内部推荐 | 30 | 6 | 3000 | 500 | 88 | 1.76 |

### 渠道ROI可视化HTML模板

```html
<div class="roi-analysis">
  <h2>招聘渠道ROI分析</h2>
  <table class="roi-table">
    <thead>
      <tr>
        <th>渠道</th>
        <th>简历数</th>
        <th>入职数</th>
        <th>花费</th>
        <th>入职成本</th>
        <th>质量分</th>
        <th>ROI</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Boss直聘</td>
        <td>500</td>
        <td>15</td>
        <td>5000</td>
        <td class="highlight">333</td>
        <td>78</td>
        <td class="highlight">2.34</td>
      </tr>
      <tr>
        <td>猎聘</td>
        <td>200</td>
        <td>12</td>
        <td>8000</td>
        <td>667</td>
        <td>85</td>
        <td>1.28</td>
      </tr>
      <tr>
        <td>内部推荐</td>
        <td>30</td>
        <td>6</td>
        <td>3000</td>
        <td>500</td>
        <td>88</td>
        <td>1.76</td>
      </tr>
    </tbody>
  </table>
  <div class="roi-chart">
    <!-- ROI柱状图占位 -->
  </div>
</div>
```

### 渠道优化建议

| 渠道类型 | 优化方向 |
|----------|----------|
| 高ROI渠道 | 增加投入、扩大覆盖 |
| 中ROI渠道 | 优化流程、提升转化 |
| 低ROI渠道 | 评估必要性、控制投入 |

---

## 预测性分析

### 留存概率预测模型

基于历史数据，预测候选人入职后的留存概率。

### 预测因素

| 因素类别 | 具体因素 | 影响方向 |
|----------|----------|----------|
| 候选人特征 | 工作经验年限 | 正向 |
| 候选人特征 | 学历水平 | 正向 |
| 候选人特征 | 薪资匹配度 | 正向 |
| 候选人特征 | 动机强度 | 正向 |
| 职位特征 | 职级匹配度 | 正向 |
| 职位特征 | 团队稳定性 | 正向 |
| 风险因素 | 通勤距离 | 负向 |
| 风险因素 | 家庭因素 | 负向 |
| 风险因素 | CounterOffer历史 | 负向 |

### 留存概率评分卡

| 评分区间 | 留存概率 | 风险等级 | 建议 |
|----------|----------|----------|------|
| 90-100分 | 95%+ | 极低 | 重点关注 |
| 80-89分 | 85%-95% | 低 | 正常跟进 |
| 70-79分 | 70%-85% | 中 | 加强沟通 |
| 60-69分 | 50%-70% | 高 | 重点跟进 |
| 60分以下 | <50% | 极高 | 谨慎推荐 |

### 留存预测Prompt模板

```
【候选人留存概率预测】

请根据以下信息，预测候选人入职后的留存概率：

【候选人信息】
- 姓名：[候选人姓名]
- 工作年限：[X]年
- 学历：[学历]
- 当前薪资：[X]K
- 期望薪资：[X]K
- 动机强度：[1-10分]
- 通勤距离：[X]公里

【职位信息】
- 职级匹配度：[完全匹配/基本匹配/略高/略低]
- 团队稳定性：[稳定/一般/不稳定]
- 上级管理风格：[详细型/授权型/民主型]

【历史数据】
- 同岗位历史留存率：[X]%
- 候选人所在公司CounterOffer历史：[有/无]

【预测要求】
1. 计算综合留存概率评分（0-100分）
2. 识别主要风险因素
3. 提供风险缓解建议
4. 给出是否推荐的建议

输出格式：
- 留存概率评分：[X]分
- 风险等级：[极低/低/中/高/极高]
- 主要风险因素：[列表]
- 风险缓解建议：[列表]
- 推荐建议：[强烈推荐/推荐/谨慎推荐/不推荐]
```

### 预测结果展示模板

```html
<div class="retention-prediction">
  <h2>候选人留存概率预测</h2>
  <div class="prediction-score">
    <div class="score-circle">85</div>
    <span class="score-label">留存概率评分</span>
  </div>
  <div class="risk-level">
    <span class="badge badge-low">风险等级：低</span>
  </div>
  <div class="risk-factors">
    <h3>主要风险因素</h3>
    <ul>
      <li>通勤距离较长（18公里）</li>
      <li>期望薪资略高于市场水平</li>
    </ul>
  </div>
  <div class="mitigation">
    <h3>风险缓解建议</h3>
    <ul>
      <li>建议提供交通补贴</li>
      <li>明确薪酬结构和发展空间</li>
    </ul>
  </div>
  <div class="recommendation">
    <span class="recommend-badge">建议：推荐</span>
    <p>综合评估后，留存概率较高，建议推进。</p>
  </div>
</div>
```

---

## 数据可视化最佳实践

### 图表设计原则

| 原则 | 说明 |
|------|------|
| 简洁明了 | 避免过多装饰元素 |
| 数据准确 | 确保数据来源可靠 |
| 色彩一致 | 使用统一的配色方案 |
| 标注清晰 | 图表元素标注完整 |
| 断网可用 | 图表必须内嵌，不依赖CDN |

### 合规检查清单

- [ ] 所有图表使用SVG或base64图片，不依赖CDN
- [ ] 数据来源标注清晰
- [ ] 脱敏信息检查通过
- [ ] 日期为真实系统时间
- [ ] 响应式布局适配移动端
