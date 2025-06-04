from collections import Counter
import random

wheel = {
    "1": {"reward": 100, "prob": 0.05},
    "2": {"reward": 20, "prob": 0.1},
    "3": {"reward": 5, "prob": 0.2},
    "4": {"reward": 1, "prob": 0.13},
    "5": {"reward": 1, "prob": 0.13},
    "6": {"reward": 1, "prob": 0.13},
    "7": {"reward": 1, "prob": 0.13},
    "8": {"reward": 1, "prob": 0.13},
}

def spin_roulette():
    r = random.random()
    cumulative = 0
    for zone, data in wheel.items():
        cumulative += data["prob"]
        if r < cumulative:
            return data["reward"]
    return 0

# 模擬10000次
results = [spin_roulette() for _ in range(10000)]


counter = Counter(results)
print("各獎勵次數分布：", dict(counter))
print("期望收益：", sum(results) / len(results))

