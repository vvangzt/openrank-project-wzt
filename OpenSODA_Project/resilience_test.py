import easygraph as eg
import matplotlib.pyplot as plt
import random

# === 0. 设置绘图风格 ===
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')

print("🚀 启动 EasyGraph 生态韧性破坏性测试 (Resilience Simulation)...")

# === 1. 构建两个典型的对照组网络 ===

# 【模型 A】健壮生态 (Vue Mode)
G_robust = eg.Graph()
devs_a = ['Evan', 'Sodatea', 'Posva', 'Jin', 'Antfu', 'Patak']
repos_a = ['Vue', 'Vite', 'Nuxt']
# 构建健壮的网状结构
for d in devs_a:
    for r in repos_a:
        if random.random() > 0.4: 
            G_robust.add_edge(d, r)

# 【模型 B】脆弱生态 (Core-js Mode)
G_fragile = eg.Graph()
repos_b = ['Core-js', 'Lib-X', 'Lib-Y']
# 构建脆弱的星型结构
for r in repos_b:
    G_fragile.add_edge('Zloirock', r)
for d in ['User1', 'User2', 'User3']:
    G_fragile.add_edge(d, 'Core-js')

print(f"✅ 网络模型构建完成")

# === 2. 定义核心模拟函数 (修复版) ===

def calculate_connectivity(G):
    """
    【修复】使用“最大连通分量占比”代替“效率”
    这能更直观地反映网络是否“散架”了，且不会报除以零错误。
    """
    if len(G.nodes) == 0:
        return 0
    
    # 获取所有连通分量
    components = eg.connected_components(G)
    
    # 找到最大的那一团
    if not components:
        return 0
    max_component_size = len(max(components, key=len))
    
    # 计算占比 (0.0 ~ 1.0)
    # 如果是 1.0，说明网络是完整的；如果是 0.1，说明网络碎成渣了
    return max_component_size / len(G.nodes)

def simulate_attack(G, name):
    history = []
    G_temp = G.copy()
    
    # 1. 初始状态
    score_initial = calculate_connectivity(G_temp)
    history.append(score_initial)
    
    # 2. 寻找 Top 1 核心节点 (度中心性)
    if len(G_temp.nodes) > 0:
        degrees = G_temp.degree()
        # 排序找到连接最多的节点
        top_node = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[0][0]
        
        print(f"🔥 [{name}] 移除核心: {top_node}")
        G_temp.remove_node(top_node) # 模拟核心离职
        
        # 3. 攻击后状态
        score_after = calculate_connectivity(G_temp)
        history.append(score_after)
        
        drop_rate = (score_initial - score_after) / score_initial * 100
        print(f"   -> 连通性从 {score_initial:.2%} 跌至 {score_after:.2%} (崩塌率: {drop_rate:.1f}%)")
    
    return history

# === 3. 执行模拟实验 ===
print("-" * 30)
history_a = simulate_attack(G_robust, "健壮生态")
print("-" * 30)
history_b = simulate_attack(G_fragile, "脆弱生态")

# === 4. 可视化结果 ===
plt.figure(figsize=(10, 6))

# 绘制折线
plt.plot(['Initial', 'After Attack'], history_a, marker='o', markersize=15, linewidth=4, label='Robust (Vue)', color='#00E396')
plt.plot(['Initial', 'After Attack'], history_b, marker='x', markersize=15, linewidth=4, label='Fragile (Core-js)', color='#FF4560', linestyle='--')

# 装饰
plt.title('Ecosystem Resilience Test: Network Connectivity Drop', fontsize=14, fontweight='bold')
plt.ylabel('Max Connected Component Ratio', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.ylim(-0.1, 1.1) # 固定Y轴范围

# 标注
drop_b = (history_b[0] - history_b[1]) / history_b[0] * 100
plt.text(0.55, history_a[1] + 0.05, "Safe Drop\n(Still Connected)", color='#00E396', fontweight='bold')
plt.text(0.55, history_b[1] + 0.05, f"COLLAPSE\n(-{drop_b:.0f}%)", color='#FF4560', fontweight='bold')

save_path = 'Resilience_Test_Fixed.png'
plt.savefig(save_path, dpi=300)
print(f"\n✅ 修复完成！结果图已保存为: {save_path}")
plt.show()