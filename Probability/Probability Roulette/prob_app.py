from flask import Flask, jsonify, render_template
import random, time

app = Flask(__name__)

wheel = [
    {"label": "1", "reward": 100, "prob": 0.05},
    {"label": "2", "reward": 20, "prob": 0.1},
    {"label": "3", "reward": 5, "prob": 0.2},
    {"label": "4", "reward": 1, "prob": 0.13},
    {"label": "5", "reward": 1, "prob": 0.13},
    {"label": "6", "reward": 1, "prob": 0.13},
    {"label": "7", "reward": 1, "prob": 0.13},
    {"label": "8", "reward": 1, "prob": 0.13},
]

history = []

def spin_roulette():
    r = random.random()
    cumulative = 0
    for i, segment in enumerate(wheel):
        cumulative += segment["prob"]
        if r < cumulative:
            return {"index": i, "label": segment["label"], "reward": segment["reward"]}
    return {"index": -1, "label": "None", "reward": 0}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin')
def spin():
    result = spin_roulette()
    result['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    history.append(result)
    return jsonify(result)

@app.route('/history')
def get_history():
    return jsonify(history[::-1])

if __name__ == '__main__':
    app.run(debug=True)
