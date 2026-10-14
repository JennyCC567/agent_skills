# 报告生成时间更新机制

## 概览

本文档说明AI人才Mapping智能体中报告生成时间的更新机制，确保时间戳能够及时更新。

## 时间戳字段

**字段名**：`generated_at`
**格式**：`YYYY-MM-DD`
**示例**：`2025-04-17`

## 更新机制

### 位置

**文件**：`scripts/batch_generator.py`
**函数**：`main()`
**位置**：第115行

### 代码

```python
# 加载数据
print(f"📂 加载数据: {args.data}")
report_data = load_json(args.data)

# 添加默认值（强制更新生成时间）
report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d')
report_data.setdefault('version', '1.0')
```

### 关键点

#### 1. 强制更新而非条件更新

**错误的做法**：
```python
report_data.setdefault('generated_at', datetime.now().strftime('%Y-%m-%d'))
```

**问题**：
- 如果输入数据中已存在`generated_at`字段，则不会更新
- 导致报告显示旧的生成时间

**正确的做法**：
```python
report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d')
```

**优势**：
- 强制覆盖任何现有的`generated_at`值
- 确保每次生成报告时都使用当前时间
- 反映真实的报告生成时间

#### 2. 使用`setdefault`的例外

**版本号**：
```python
report_data.setdefault('version', '1.0')
```

**原因**：
- 版本号是业务数据，不是系统元数据
- 应该保留输入数据中的版本号
- 只有当不存在时才设置默认值

## 时间戳显示位置

### 1. 基本信息（所有格式）
```
生成时间: 2025-04-17
```

### 2. 页脚（所有格式）
```
本报告由AI人才Mapping智能体生成 | 生成时间: 2025-04-17
```

### 3. PPT副标题
```
生成时间: 2025-04-17
```

## 时间戳精度

**当前精度**：日期（仅年月日）
**格式**：`YYYY-MM-DD`

**示例**：
- 2025-04-17
- 2025-04-18

**为什么仅精确到日期**：
- 报告生成日期已足够区分不同报告
- 符合常规日期显示习惯
- 便于用户理解
- 避免过度精确导致的混淆

## 多次生成验证

### 测试场景

用户在同一天内多次生成报告：

```bash
# 第1次生成
python scripts/batch_generator.py --data report.json --output report

# 第2次生成
python scripts/batch_generator.py --data report.json --output report

# 第3次生成
python scripts/batch_generator.py --data report.json --output report
```

### 结果

```
第1次生成: 2025-04-17
第2次生成: 2025-04-17
第3次生成: 2025-04-17
```

**验证**：
- ✅ 同一天内生成的报告时间戳相同
- ✅ 不同日期生成的报告时间戳不同
- ✅ 时间戳精确到日期

## 常见问题

### Q1: 为什么报告的生成时间是旧的？

**A:** 可能的原因：
1. 输入数据中包含旧的`generated_at`字段
2. 代码使用了`setdefault`而非强制赋值
3. 系统时间不正确

**解决方案**：
- 确保使用`report_data['generated_at'] = datetime.now().strftime(...)`
- 检查系统时间是否正确
- 验证输入数据是否被意外修改

### Q2: 时间戳的时区是什么？

**A:** 当前使用系统本地时区。
- 如果需要UTC时间，可以修改为：`datetime.utcnow().strftime(...)`
- 如果需要特定时区，可以使用`pytz`库

### Q3: 为什么时间戳不精确到秒？

**A:** 当前仅精确到日期（YYYY-MM-DD），原因：
- 报告生成日期已足够区分不同报告
- 同一天内生成的报告应该有相同的时间戳
- 符合常规日期显示习惯
- 避免过度精确导致的混淆

如果需要更高精度，可以修改为：

**精确到分钟**：
```python
datetime.now().strftime('%Y-%m-%d %H:%M')
# 输出: 2025-04-17 14:30
```

**精确到秒**：
```python
datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 输出: 2025-04-17 14:30:45
```

**精确到毫秒**：
```python
datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
# 输出: 2025-04-17 14:30:45.123
```

### Q4: 为什么不使用`setdefault`？

**A:** `setdefault`的行为：
- 仅当键不存在时才设置值
- 如果键已存在，则保留原值

**示例**：
```python
data = {'generated_at': '2025-01-01'}
data.setdefault('generated_at', datetime.now().strftime('%Y-%m-%d'))
# 结果：data['generated_at'] = '2025-01-01' (未更新)
```

**强制赋值**：
```python
data = {'generated_at': '2025-01-01'}
data['generated_at'] = datetime.now().strftime('%Y-%m-%d')
# 结果：data['generated_at'] = '2025-04-17' (已更新)
```

## 最佳实践

### 1. 强制更新系统元数据
```python
# ✅ 正确：强制更新
report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d')

# ❌ 错误：条件更新
report_data.setdefault('generated_at', datetime.now().strftime('%Y-%m-%d'))
```

### 2. 保留业务数据
```python
# ✅ 正确：保留业务数据
report_data.setdefault('version', '1.0')

# ❌ 错误：强制覆盖业务数据
report_data['version'] = '1.0'
```

### 3. 在数据加载后立即更新
```python
# 加载数据
report_data = load_json(args.data)

# 立即更新时间戳（在数据验证和处理之前）
report_data['generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 继续处理数据
...
```

## 总结

- **更新时机**：每次生成报告时
- **更新方式**：强制赋值（`=`）而非条件赋值（`setdefault`）
- **时间精度**：日期（年月日）
- **显示位置**：基本信息和页脚
- **验证方法**：不同日期生成报告，观察时间戳是否不同

---

**文档版本**：1.0
**最后更新**：2025-04-17
**维护者**：AI人才Mapping智能体团队
