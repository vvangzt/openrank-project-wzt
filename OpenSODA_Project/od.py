import requests
import pandas as pd
import datetime

# === 1. 配置 OpenDigger API  ===
#  https://oss.open-digger.cn/github/{org}/{repo}/{metric}.json
BASE_URL = "https://oss.open-digger.cn/github/{}/{}.json"

# 定义我们要验证的项目和指标
repo_name = "X-lab2017/open-digger"  # 以官方项目为例
metrics = {
    "openrank": "OpenRank",
    "activity": "Activity",
    "bus_factor": "BusFactor" # 风险指标
}

print(f"🚀 [Step 1] 开始验证数据链路: {repo_name} ...")

# === 2. 数据获取与 ETL 清洗 ===
dfs = []

for metric_key, metric_name in metrics.items():
    url = BASE_URL.format(repo_name, metric_key)
    print(f"   -> Requesting: {url}")
    
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            # 将 JSON 转换为 Pandas DataFrame
            df_temp = pd.DataFrame(list(data.items()), columns=['Date', metric_name])
            # 过滤非日期数据 (OpenDigger 有时包含 meta 数据)
            df_temp = df_temp[df_temp['Date'].str.match(r'^\d{4}-\d{2}$')]
            df_temp.set_index('Date', inplace=True)
            dfs.append(df_temp)
            print(f"      ✅ 获取成功: {len(df_temp)} 条记录")
        else:
            print(f"      ❌ 获取失败: Status {resp.status_code}")
    except Exception as e:
        print(f"      ❌ 异常: {e}")

# 合并所有指标
if dfs:
    df_final = pd.concat(dfs, axis=1).sort_index()
    # 填充缺失值 (假设早期没有数据为0)
    df_final = df_final.fillna(0)
    
    print("\n🚀 [Step 2] 验证 MFHM 算法计算...")
    
    # === 3. MFHM 算法原型实现 ===
    # 获取最近一个月的数据进行验证
    latest_data = df_final.iloc[-1].copy()
    
    openrank = float(latest_data['OpenRank'])
    activity = float(latest_data['Activity'])
    bus_factor = float(latest_data['BusFactor'])
    
    # 简单的归一化模拟 (0-100)
    # 假设 OpenRank 满分 100, Activity 满分 500
    norm_rank = min(openrank, 100) 
    norm_act = min(activity / 5, 100)
    
    # 核心公式：Score = 0.4*Rank + 0.4*Act - 惩罚项
    # 防止除以0
    bf_penalty = 20 * (1 / (bus_factor + 0.1))
    
    health_score = (0.4 * norm_rank) + (0.4 * norm_act) - bf_penalty
    
    print("-" * 40)
    print(f"📅 数据月份: {df_final.index[-1]}")
    print(f"📊 原始指标: OpenRank={openrank:.2f}, Activity={activity:.2f}, BusFactor={bus_factor}")
    print(f"🧮 算法过程: {0.4*norm_rank:.1f} (Rank) + {0.4*norm_act:.1f} (Act) - {bf_penalty:.1f} (Penalty)")
    print(f"🏆 最终健康分: {health_score:.2f}")
    print("-" * 40)
    
    # 保存验证结果
    df_final.tail(5).to_csv("mvp_verification_data.csv")
    print("✅ 验证通过！数据已保存至 mvp_verification_data.csv")

else:
    print("❌ 验证失败，未能获取数据")