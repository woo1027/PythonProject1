from flask import Flask, render_template, request

app = Flask(__name__)

def calc_RTP(fish_types, bullet_cost):
    expected_return = 0
    for fish in fish_types.values():
        fish_expect = fish["hit_prob"] * (fish["reward"] - bullet_cost) + (1 - fish["hit_prob"]) * (-bullet_cost)
        expected_return += fish["appearance_prob"] * fish_expect
    RTP = (expected_return + bullet_cost) / bullet_cost * 100
    return RTP

def adjust_boss_reward(fish_types, bullet_cost, target_RTP=90, step=1, max_iter=1000):
    boss_reward = fish_types["boss"]["reward"]
    for _ in range(max_iter):
        fish_types["boss"]["reward"] = boss_reward
        current_RTP = calc_RTP(fish_types, bullet_cost)
        if abs(current_RTP - target_RTP) < 0.1:
            break
        if current_RTP > target_RTP:
            boss_reward -= step
        else:
            boss_reward += step
    return boss_reward, current_RTP

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    adjusted = None
    if request.method == "POST":
        try:
            fish_types = {
                "small": {
                    "appearance_prob": float(request.form["small_appearance_prob"]),
                    "hit_prob": float(request.form["small_hit_prob"]),
                    "reward": float(request.form["small_reward"]),
                },
                "medium": {
                    "appearance_prob": float(request.form["medium_appearance_prob"]),
                    "hit_prob": float(request.form["medium_hit_prob"]),
                    "reward": float(request.form["medium_reward"]),
                },
                "boss": {
                    "appearance_prob": float(request.form["boss_appearance_prob"]),
                    "hit_prob": float(request.form["boss_hit_prob"]),
                    "reward": float(request.form["boss_reward"]),
                },
            }
            bullet_cost = float(request.form["bullet_cost"])
            target_RTP = float(request.form["target_RTP"])

            rtp = calc_RTP(fish_types, bullet_cost)
            result = f"目前RTP: {rtp:.2f}%"

            # 自動調整 boss 獎勵
            boss_reward, adjusted_rtp = adjust_boss_reward(
                fish_types, bullet_cost, target_RTP=target_RTP
            )
            adjusted = (
                f"調整後boss獎勵: {boss_reward:.2f}，達成目標RTP: {adjusted_rtp:.2f}%"
            )
        except Exception as e:
            result = f"輸入錯誤: {e}"

    return render_template("index.html", result=result, adjusted=adjusted)

if __name__ == "__main__":
    app.run(debug=True)
