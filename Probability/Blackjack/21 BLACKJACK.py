import random

def draw_card():
    card = random.randint(1, 13)
    return min(card, 10)  # J/Q/K 都算 10

def play_blackjack():
    player = draw_card() + draw_card()
    dealer = draw_card() + draw_card()

    while player < 17:
        player += draw_card()
    if player > 21:
        return -1  # 玩家爆掉

    while dealer < 17:
        dealer += draw_card()
    if dealer > 21 or player > dealer:
        return 1
    elif player == dealer:
        return 0
    else:
        return -1

results = [play_blackjack() for _ in range(10000)]
ev = sum(results) / len(results)
print("期望值：", ev)
