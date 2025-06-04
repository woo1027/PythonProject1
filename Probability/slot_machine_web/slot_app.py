from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

symbols = ["A", "B", "C", "D", "Jackpot", "Wild", "FreeSpin"]
weights = [0.35, 0.25, 0.15, 0.1, 0.01, 0.08, 0.06]
COST_PER_SPIN = 10

# 初始玩家資料（可擴展為用戶系統）
player = {
    "coins": 100,
    "free_spins": 0
}


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

@app.route("/")
def index():
    return render_template("index.html", coins=player["coins"], free_spins=player["free_spins"])


@app.route("/spin", methods=["POST"])
def do_spin():
    if player["coins"] < COST_PER_SPIN and player["free_spins"] <= 0:
        return jsonify({"error": "金幣不足"})

    if player["free_spins"] > 0:
        player["free_spins"] -= 1
    else:
        player["coins"] -= COST_PER_SPIN

    result = spin()
    reward, fs = calculate_reward(result)
    player["coins"] += reward
    player["free_spins"] += fs

    return jsonify({
        "result": result,
        "reward": reward,
        "free_spins": player["free_spins"],
        "coins": player["coins"]
    })


if __name__ == "__main__":
    app.run(debug=True)
