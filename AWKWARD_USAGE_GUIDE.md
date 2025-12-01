# Awkward数组使用指南

## 概述

`data_loader.py` 现在提供了灵活的方式来处理awkward数组和DataFrames，满足不同的分析需求。

## 🎯 四种加载方式

### 1️⃣ 完整加载（默认）

**返回awkward数组 + DataFrames**

```python
from data_loader import load_and_process_data

data, df_hits, df_primaries, process_map, num_events = load_and_process_data(
    "data/res2.root"
)

# data 是 awkward.Array 类型
# df_hits 和 df_primaries 是 pandas.DataFrame
```

**适合场景：**
- ✅ 需要同时做事件级别和hit级别分析
- ✅ 需要保持数据的层次结构
- ✅ 需要灵活切换分析方式

**示例：**
```python
# 事件级别分析 (用awkward)
import awkward as ak
total_energy_per_event = data['TotalEdep']
mean_energy = ak.mean(total_energy_per_event)

# Hit级别分析 (用DataFrame)
hit_energy_dist = df_hits['edep'].hist()
```

---

### 2️⃣ 只返回DataFrames

**不返回awkward数组，节省内存**

```python
df_hits, df_primaries, process_map, num_events = load_and_process_data(
    "data/res2.root",
    return_awkward=False  # 关键参数
)
```

**适合场景：**
- ✅ 只需要hit级别统计分析
- ✅ 不需要事件层次结构
- ✅ 内存受限的环境

**示例：**
```python
# 统计分析
print(df_hits.groupby('pdg')['edep'].sum())

# 绘图
import matplotlib.pyplot as plt
df_hits['edep'].hist(bins=100)
plt.show()
```

---

### 3️⃣ 只加载awkward数组

**最快的加载方式，跳过DataFrame转换**

```python
from data_loader import load_awkward_only

data_ak, process_map, num_events = load_awkward_only("data/res2.root")
```

**适合场景：**
- ✅ 快速浏览数据
- ✅ 只做事件级别分析
- ✅ 需要最小内存占用
- ✅ 保持完整的ROOT数据结构

**示例：**
```python
# 访问事件级别数据
print(f"事件0的总能量: {data_ak['TotalEdep'][0]} MeV")
print(f"事件0的Hit数: {data_ak['HitCount'][0]}")

# 访问hit级别数据（保持层次结构）
print(f"事件0的所有hit能量: {data_ak['CrystalEdep'][0]}")

# 快速统计
import awkward as ak
total_energy = ak.sum(data_ak['TotalEdep'])
```

---

### 4️⃣ 提取子数组

**按类型分离awkward数组**

```python
from data_loader import get_awkward_arrays

event_data, hits_data, primary_data = get_awkward_arrays(data_ak)
```

**适合场景：**
- ✅ 需要分别处理不同类型的数据
- ✅ 代码结构更清晰
- ✅ 按需访问特定数据

**示例：**
```python
# 只处理事件级别数据
print(event_data.fields)  # ['EventID', 'TotalEdep', 'HitCount']

# 只处理hit数据
print(hits_data.fields)  # ['CrystalID', 'CrystalEdep', ...]

# 只处理primary数据
print(primary_data.fields)  # ['PrimaryPDG', 'PrimaryEnergy', ...]
```

---

## 📊 性能对比

| 方法 | 加载速度 | 内存占用 | 事件级分析 | Hit级分析 | 适用场景 |
|------|---------|---------|-----------|----------|---------|
| **完整加载** | ⭐⭐⭐ | 🔴🔴🔴 | ✅ | ✅ | 全面分析 |
| **只DataFrame** | ⭐⭐⭐ | 🟡🟡 | ❌ | ✅ | Hit统计 |
| **只awkward** | ⭐⭐⭐⭐⭐ | 🟢 | ✅ | ⚠️ | 快速浏览 |
| **提取子数组** | ⭐⭐⭐⭐ | 🟢🟡 | ✅ | ⚠️ | 分类处理 |

---

## 🔍 Awkward数组的优势

### 1. 保持层次结构

```python
# DataFrame会展平数据
df_hits['EventID']  # [0, 0, 0, 1, 1, 2, ...]  每个hit一行

# Awkward保持事件结构
data_ak['CrystalEdep']  # [[hit1, hit2, hit3], [hit1, hit2], ...]  每个事件一个列表
```

### 2. 高效的向量化操作

```python
import awkward as ak

# 计算每个事件的总能量（一行代码）
total_per_event = ak.sum(data_ak['CrystalEdep'], axis=1)

# 筛选有超过5个hit的事件
mask = data_ak['HitCount'] > 5
filtered_data = data_ak[mask]

# 计算统计量
mean_energy = ak.mean(data_ak['TotalEdep'])
std_energy = ak.std(data_ak['TotalEdep'])
```

### 3. 原生支持嵌套结构

```python
# 访问事件0的所有hit
event_0_hits = data_ak[0]['CrystalEdep']

# 找到每个事件中能量最大的hit
max_edep_per_event = ak.max(data_ak['CrystalEdep'], axis=1)

# 统计每个事件的hit数
hit_counts = ak.num(data_ak['CrystalEdep'])
```

---

## 💡 使用建议

### 场景1: 初步探索数据

```python
# 使用最快的方式
data_ak, process_map, num_events = load_awkward_only("data/res2.root")

# 快速查看
print(f"事件数: {len(data_ak)}")
print(f"字段: {data_ak.fields}")
print(f"第一个事件: {data_ak[0]}")
```

### 场景2: 详细统计分析

```python
# 加载DataFrame
df_hits, df_primaries, process_map, num_events = load_and_process_data(
    "data/res2.root", 
    return_awkward=False
)

# 使用pandas的强大功能
stats = df_hits.groupby(['pdg', 'processID']).agg({
    'edep': ['sum', 'mean', 'std'],
    'trackLength': 'sum'
})
```

### 场景3: 混合分析

```python
# 同时获取两种格式
data, df_hits, df_primaries, process_map, num_events = load_and_process_data(
    "data/res2.root"
)

# 事件级别用awkward
import awkward as ak
high_energy_events = data[data['TotalEdep'] > 5.0]

# Hit级别用DataFrame
import matplotlib.pyplot as plt
df_hits[df_hits['EventID'].isin([0, 1, 2])]['edep'].hist()
```

---

## 🔧 实用函数

### 常用awkward操作

```python
import awkward as ak

# 数组长度（每个事件的hit数）
hit_counts = ak.num(data_ak['CrystalEdep'])

# 求和
total_energy = ak.sum(data_ak['TotalEdep'])
energy_per_event = ak.sum(data_ak['CrystalEdep'], axis=1)

# 最大/最小值
max_edep = ak.max(data_ak['CrystalEdep'])
max_per_event = ak.max(data_ak['CrystalEdep'], axis=1)

# 筛选
mask = data_ak['HitCount'] > 3
filtered = data_ak[mask]

# 展平（类似DataFrame）
flat_edep = ak.flatten(data_ak['CrystalEdep'])

# 统计
mean = ak.mean(data_ak['TotalEdep'])
std = ak.std(data_ak['TotalEdep'])
```

---

## 📚 更多资源

- **Awkward Array文档**: https://awkward-array.org/
- **示例代码**: `example_awkward_usage.py`
- **配置指南**: `DATA_CONFIG_README.md`

---

## ⚠️ 注意事项

1. **内存管理**: 
   - 完整加载会同时保留awkward和DataFrame，内存占用大
   - 对于大数据集，考虑只加载需要的格式

2. **缓存机制**:
   - 只有DataFrame会被缓存（parquet格式）
   - Awkward数组每次都从ROOT文件读取
   - 首次运行较慢，后续运行DataFrame会很快

3. **数据一致性**:
   - awkward和DataFrame来自同一份数据
   - 修改一个不会影响另一个（已经是独立的拷贝）

4. **向后兼容**:
   - 默认行为保持不变（返回所有内容）
   - 旧代码无需修改
