fish_types = {
    "small": {"reward": 5, "appearance_prob": 0.7, "hit_prob": 0.8},
    "medium": {"reward": 20, "appearance_prob": 0.25, "hit_prob": 0.4},
    "boss": {"reward": 50, "appearance_prob": 0.05, "hit_prob": 0.05}
}

bullet_cost = 1
expected_return = 0
for fish in fish_types.values():
    # 期望淨收益 = 命中概率 * (獎勵 - 子彈成本) + 未命中概率 * (-子彈成本)
    fish_expect = fish["hit_prob"] * (fish["reward"] - bullet_cost) + (1 - fish["hit_prob"]) * (-bullet_cost)
    # 加權期望收益 = 出現機率 * 該魚期望淨收益
    expected_return += fish["appearance_prob"] * fish_expect

RTP = (expected_return + bullet_cost) / bullet_cost * 100

print(f"整體期望淨收益: {expected_return:.3f}")
print(f"整體RTP: {RTP:.2f}%")