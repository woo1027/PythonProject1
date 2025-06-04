import random

symbols = ["A", "B", "C", "D", "Jackpot", "Wild", "FreeSpin"]
weights = [0.35, 0.25, 0.15, 0.1, 0.01, 0.08, 0.06]  # 總和為 1

cost_per_spin = 10  # 每次投注

def spin():
    return [random.choices(symbols, weights)[0] for _ in range(3)]

def calculate_reward(result):
    reward = 0
    free_spins = 0

    # 免轉判定
    free_spins += result.count("FreeSpin")

    # Wild 替代：把除了 FreeSpin、Wild 的符號抓出來
    symbols_only = [s for s in result if s not in ["FreeSpin", "Wild"]]

    if len(symbols_only) == 0:
        # 全部是 Wild 或 FreeSpin，視為 Wild 中獎
        reward = 300
    elif len(set(symbols_only)) == 1 and len(symbols_only) + result.count("Wild") == 3:
        # 組成三個相同符號（考慮 Wild）
        symbol = symbols_only[0]
        if symbol == "Jackpot":
            reward = 1000
        else:
            reward = 100
    elif result.count("Wild") == 3:
        reward = 300

    return reward, free_spins


# 模擬
total_spins = 10000
spin_count = total_spins
free_spin_pool = 0
total_reward = 0

while spin_count > 0:
    result = spin()
    reward, free_spins = calculate_reward(result)
    total_reward += reward
    free_spin_pool += free_spins
    spin_count -= 1
    while free_spin_pool > 0:
        result = spin()
        reward, extra_fs = calculate_reward(result)
        total_reward += reward
        free_spin_pool += extra_fs - 1

expected_reward = total_reward / total_spins
net_gain = expected_reward - cost_per_spin
roi = net_gain / cost_per_spin

print("🎰 模擬預期收益：", expected_reward)
print("💸 模擬淨收益（收益 - 成本）：", net_gain)
print("📈 模擬報酬率 (ROI)：", f"{roi * 100:.2f}%")