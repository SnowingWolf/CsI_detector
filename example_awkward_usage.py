"""
示例：灵活使用awkward数组和DataFrames

展示不同的数据加载方式，适应不同的分析需求
"""

from data_loader import get_awkward_arrays, load_and_process_data, load_awkward_only, load_config

print("=" * 80)
print("方式1: 完整加载 (包含awkward数组和DataFrames)")
print("=" * 80)

data, df_hits, df_primaries, process_map, num_events = load_and_process_data("data/res2.root", cache=True)

print(f"\n加载完成:")
print(f"  事件数: {num_events}")
print(f"  Awkward数组类型: {type(data)}")
print(f"  Hit DataFrame: {len(df_hits)} 行")
print(f"  Primary DataFrame: {len(df_primaries)} 行")

# 使用awkward数组进行事件级别分析
print(f"\n事件级别数据 (来自awkward数组):")
print(f"  前5个事件的总能量: {data['TotalEdep'][:5]}")
print(f"  前5个事件的Hit数: {data['HitCount'][:5]}")

print("\n" + "=" * 80)
print("方式2: 只加载DataFrames (不返回awkward数组)")
print("=" * 80)

df_hits_only, df_primaries_only, process_map, num_events = load_and_process_data(
    "data/res2.root",
    cache=True,
    return_awkward=False,  # 不返回awkward数组，节省内存
)

print(f"返回值数量: 4 (无awkward数组)")
print(f"适合场景: 只做hit级别分析，不需要保持事件层次结构")

print("\n" + "=" * 80)
print("方式3: 只加载awkward数组 (最快，适合事件级别分析)")
print("=" * 80)

data_ak, process_map, num_events = load_awkward_only("data/res2.root")

print(f"Awkward数组字段: {data_ak.fields}")
print(f"\n事件级别数据访问示例:")
print(f"  第1个事件总能量: {data_ak['TotalEdep'][0]:.4f} MeV")
print(f"  第1个事件Hit数: {data_ak['HitCount'][0]}")
print(f"  第1个事件的Crystal能量: {data_ak['CrystalEdep'][0]}")

print(f"\n优势: 跳过DataFrame转换，更快，内存占用更小")

print("\n" + "=" * 80)
print("方式4: 从awkward数组中提取子数组")
print("=" * 80)

event_data, hits_data, primary_data = get_awkward_arrays(data_ak)

print(f"分离后的数组:")
print(f"  事件级别数组字段: {event_data.fields}")
print(f"  Hit数组字段: {hits_data.fields}")
print(f"  Primary数组字段: {primary_data.fields}")

print(f"\n使用示例:")
print(f"  事件0的总能量: {event_data['TotalEdep'][0]:.4f} MeV")
print(f"  事件0的第1个hit能量: {hits_data['CrystalEdep'][0][0]:.4f} MeV")
print(f"  事件0的第1个primary粒子PDG: {primary_data['PrimaryPDG'][0][0]}")

print("\n" + "=" * 80)
print("性能对比和使用建议")
print("=" * 80)
print("""
1. 完整加载 (默认) - 适合需要多种分析的场景:
   data, df_hits, df_primaries, ... = load_and_process_data(file)
   ✓ 可以做事件级别分析 (用awkward)
   ✓ 可以做hit级别分析 (用DataFrame)
   ✗ 内存占用较大
   
2. 只要DataFrame - 适合只做hit级别统计:
   df_hits, df_primaries, ... = load_and_process_data(file, return_awkward=False)
   ✓ 方便的统计和绘图
   ✓ 节省awkward数组的内存
   ✗ 失去事件层次结构
   
3. 只要awkward - 适合快速浏览和事件级别分析:
   data_ak, ... = load_awkward_only(file)
   ✓ 加载最快 (不需要转DataFrame)
   ✓ 保持完整的层次结构
   ✓ 内存占用最小
   ✗ 不如DataFrame方便做统计
   
4. 分离子数组 - 适合按类型分别处理:
   event_data, hits_data, primary_data = get_awkward_arrays(data_ak)
   ✓ 按需访问不同类型的数据
   ✓ 代码更清晰
""")

print("\n" + "=" * 80)
print("实际分析示例")
print("=" * 80)

# 示例1: 用awkward数组快速统计
import awkward as ak

total_energy = ak.sum(data_ak["TotalEdep"])
print(f"\n所有事件的总能量 (awkward): {total_energy:.2f} MeV")

# 示例2: 用DataFrame做统计
mean_edep_per_hit = df_hits["edep"].mean()
print(f"每个hit的平均能量 (DataFrame): {mean_edep_per_hit:.4f} MeV")

# 示例3: 结合两者
print(f"\n结合分析:")
print(f"  事件数 (awkward): {len(data_ak)}")
print(f"  总Hit数 (DataFrame): {len(df_hits)}")
print(f"  平均每事件Hit数: {len(df_hits) / len(data_ak):.2f}")
