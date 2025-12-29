import easygraph as eg
import matplotlib.pyplot as plt
import math
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# === 1. 数据准备 ===
repo_contributors = {
    'Vue': ['Evan You', 'Sodatea', 'Posva', 'HcySunYang', 'DevA', 'DevB'],
    'Vite': ['Evan You', 'Patak', 'Antfu', 'Sheremet', 'DevC'],
    'Nuxt': ['Pooya', 'Daniel', 'Antfu', 'DevD'],
    'Vitest': ['Antfu', 'Sheremet', 'Patak', 'DevE'],
    'Unjs': ['Pooya', 'Pi0', 'DevF'],
    'Core-js': ['Zloirock'] 
}

print("🕸️ [Pure EasyGraph] 正在构建开发者协作网络...")

# === 2. 构建图 ===
G = eg.Graph()

for repo, contributors in repo_contributors.items():
    G.add_node(repo, type='repo')
    for dev in contributors:
        if not G.nodes.get(dev):
             G.add_node(dev, type='dev')
        G.add_edge(dev, repo)

print(f"✅ 网络构建完成: {len(G.nodes)} 个节点, {len(G.edges)} 条边")

# === 3. 核心算法: 介数中心性 ===
print("🧮 正在计算风险传播路径 (Betweenness Centrality)...")
betweenness = eg.betweenness_centrality(G)

if isinstance(betweenness, list):
    betweenness = dict(zip(G.nodes, betweenness))

top_bridges = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3]
print("\n🏆 生态关键桥梁 (Key Bridges):")
for dev, score in top_bridges:
    print(f"   - {dev}: {score:.4f}")

# === 4. 可视化绘图  ===
print("🎨 正在绘制图谱...")

plt.figure(figsize=(12, 10))

# 手动生成一个简单的布局 (同心圆布局)
# 项目在内圈，开发者在外圈，这样画出来很整齐
pos = {}
repos = [n for n in G.nodes if G.nodes[n].get('type') == 'repo']
devs = [n for n in G.nodes if G.nodes[n].get('type') == 'dev']

# 内圈布局 (Repo)
for i, node in enumerate(repos):
    angle = 2 * math.pi * i / len(repos)
    pos[node] = (0.3 * math.cos(angle), 0.3 * math.sin(angle))

# 外圈布局 (Dev)
for i, node in enumerate(devs):
    angle = 2 * math.pi * i / len(devs)
    r = 0.8 + random.uniform(-0.1, 0.1)
    pos[node] = (r * math.cos(angle), r * math.sin(angle))

for edge in G.edges:
    u, v = edge[0], edge[1]
    x_values = [pos[u][0], pos[v][0]]
    y_values = [pos[u][1], pos[v][1]]
    plt.plot(x_values, y_values, color='gray', alpha=0.2, zorder=1)

for node, (x, y) in pos.items():
    if G.nodes[node].get('type') == 'repo':
        plt.scatter(x, y, s=1500, c='#FF6B6B', zorder=2, edgecolors='white') # 红点
    else:
        plt.scatter(x, y, s=300, c='#4D96FF', zorder=2, edgecolors='white')  # 蓝点
    
    # 绘制标签
    # 只显示 Repo 和 核心开发者
    if node in repos or node in [x[0] for x in top_bridges]:
        plt.text(x, y-0.05, node, fontsize=10, ha='center', fontweight='bold', zorder=3)

plt.title("Open Source Ecosystem Risk Graph (Pure EasyGraph Logic)", fontsize=16)
plt.axis('off')

save_path = 'Final_Risk__Manual.png'
plt.savefig(save_path, dpi=300)
print(f"\n✅ 成功！图谱已保存为: {save_path}")
plt.show()