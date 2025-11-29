"""
示例：使用配置文件加载和分析数据

这个脚本展示了如何：
1. 使用自定义配置文件
2. 修改配置而不改动代码
3. 访问配置中的粒子名称映射
"""

from data_loader import load_and_process_data, load_config

# 方式1：使用默认配置文件
print("=" * 60)
print("使用默认配置文件 (data_config.json)")
print("=" * 60)

data, df_hits, df_primaries, process_map, num_events = load_and_process_data("data/res2.root", cache=True)

print(f"\n加载完成:")
print(f"  事件数: {num_events}")
print(f"  Hit数: {len(df_hits)}")
print(f"  Primary数: {len(df_primaries)}")

# 方式2：访问配置信息
config = load_config()

print(f"\n配置信息:")
print(f"  Tree名称: {config['tree_name']}")
print(f"  Crystal分支数: {len(config['branches']['crystal_hits'])}")
print(f"  Primary分支数: {len(config['branches']['primary_particles'])}")

# 使用配置中的粒子名称映射
particle_names = config["particle_names"]
print(f"\n支持的粒子类型:")
for pdg_code, name in particle_names.items():
    print(f"  PDG {pdg_code:>5s}: {name}")

# 方式3：查看列名映射
print(f"\nHit列名映射:")
for old_name, new_name in config["column_mapping"]["hits"].items():
    print(f"  {old_name:25s} -> {new_name}")

print(f"\n数据预览:")
print(df_hits.head())
