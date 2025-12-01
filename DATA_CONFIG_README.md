# Data Loader 配置系统

## 概述

数据加载器现在支持通过 JSON 配置文件管理所有硬编码内容，使得修改数据结构更加灵活。

## 配置文件: `data_config.json`

### 结构说明

```json
{
  "branches": {
    "event_level": [...],      // 事件级别的分支
    "crystal_hits": [...],     // Crystal Hit的分支
    "primary_particles": [...]  // Primary粒子的分支
  },
  "column_mapping": {
    "hits": {...},             // Hit列名映射
    "primaries": {...}         // Primary列名映射
  },
  "particle_names": {...},     // PDG代码到粒子名称的映射
  "tree_name": "CsI",          // ROOT Tree名称
  "cache_suffix": {...}        // 缓存文件后缀
}
```

## 使用方法

### 1. 基本使用（使用默认配置）

```python
from data_loader import load_and_process_data

data, df_hits, df_primaries, process_map, num_events = load_and_process_data(
    "data/res2.root",
    cache=True
)
```

### 2. 使用自定义配置文件

```python
data, df_hits, df_primaries, process_map, num_events = load_and_process_data(
    "data/res2.root",
    cache=True,
    config_file="my_custom_config.json"  # 使用自定义配置
)
```

### 3. 访问配置信息

```python
from data_loader import load_config

config = load_config()  # 或 load_config("my_config.json")

# 获取分支列表
crystal_branches = config["branches"]["crystal_hits"]

# 获取列名映射
column_mapping = config["column_mapping"]["hits"]

# 获取粒子名称
particle_names = config["particle_names"]
```

## 添加新的数据分支

### 步骤：

1. **在Geant4中添加新分支** (例如：`CrystalNewField`)

2. **更新 `data_config.json`**:

```json
{
  "branches": {
    "crystal_hits": [
      ...,
      "CrystalNewField"  // 添加新分支
    ]
  },
  "column_mapping": {
    "hits": {
      ...,
      "CrystalNewField": "newField"  // 添加映射
    }
  }
}
```

3. **重新运行** - 无需修改代码！

```python
# 代码保持不变
data, df_hits, df_primaries, process_map, num_events = load_and_process_data("data/res2.root")

# df_hits 会自动包含新的 "newField" 列
print(df_hits["newField"])
```

## 优势

✅ **无需修改代码** - 只需编辑JSON文件  
✅ **易于维护** - 所有配置集中管理  
✅ **版本控制友好** - 配置变更清晰可见  
✅ **支持多套配置** - 不同分析使用不同配置  
✅ **减少错误** - 避免硬编码带来的拼写错误  

## 示例场景

### 场景1: 添加了 Track Length 分支

在 `data_config.json` 中已包含:
```json
"crystal_hits": [
  ...,
  "CrystalTrackLength"
],
"hits": {
  ...,
  "CrystalTrackLength": "trackLength"
}
```

现在 `df_hits` 会自动包含 `trackLength` 列。

### 场景2: 添加新粒子类型

```json
"particle_names": {
  ...,
  "1000020040": "Alpha"  // 添加Alpha粒子
}
```

### 场景3: 不同的分析需求

创建 `minimal_config.json` 只加载必需的分支：
```json
{
  "branches": {
    "event_level": ["EventID", "TotalEdep"],
    "crystal_hits": ["CrystalID", "CrystalEdep"],
    "primary_particles": []
  }
}
```

使用：
```python
data, df_hits, _, _, _ = load_and_process_data(
    "data/res2.root",
    config_file="minimal_config.json"
)
# 只加载最少的数据，更快！
```

## 配置文件字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `branches.event_level` | Array | 事件级别的标量分支 |
| `branches.crystal_hits` | Array | Hit级别的向量分支（每个事件多个值） |
| `branches.primary_particles` | Array | Primary粒子的向量分支 |
| `column_mapping.hits` | Object | Crystal分支名到DataFrame列名的映射 |
| `column_mapping.primaries` | Object | Primary分支名到DataFrame列名的映射 |
| `particle_names` | Object | PDG代码(字符串)到粒子名称的映射 |
| `tree_name` | String | ROOT文件中的TTree名称 |
| `cache_suffix` | Object | 各种缓存文件的后缀 |

## 兼容性

现有代码完全兼容，无需修改：

```python
# 旧代码仍然可以工作
from data_loader import load_and_process_data
data, df_hits, df_primaries, process_map, num_events = load_and_process_data("data/res2.root")
```

默认会使用 `data_config.json`。
