from flask import Flask, render_template, session, jsonify, request
import random

app = Flask(__name__)
app.secret_key = "blackjack-secret"

def draw_card():
    card = random.randint(1, 13)
    return min(card, 10) if card > 10 else card

def calculate_score(hand):
    score = sum(hand)
    aces = hand.count(1)
    while score + 10 <= 21 and aces:
        score += 10
        aces -= 1
    return score

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    session['player'] = [draw_card(), draw_card()]
    session['dealer'] = [draw_card(), draw_card()]
    return jsonify({
        "player": session['player'],
        "dealer": [session['dealer'][0], "?"]
    })

@app.route("/hit", methods=["POST"])
def hit():
    player_hand = session.get("player", [])
    player_hand.append(draw_card())
    session["player"] = player_hand

    player_score = calculate_score(session['player'])
    result = ""
    if player_score > 21:
        result = "玩家爆牌，輸了！"
    return jsonify({
        "player": session['player'],
        "result": result
    })

@app.route("/stand", methods=["POST"])
def stand():
    dealer = session['dealer']
    while calculate_score(dealer) < 17:
        dealer.append(draw_card())
    session['dealer'] = dealer

    player_score = calculate_score(session['player'])
    dealer_score = calculate_score(dealer)

    if dealer_score > 21 or player_score > dealer_score:
        result = "玩家獲勝！"
    elif dealer_score == player_score:
        result = "平手！"
    else:
        result = "莊家獲勝！"

    return jsonify({
        "dealer": dealer,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)
