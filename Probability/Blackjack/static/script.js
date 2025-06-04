document.addEventListener("DOMContentLoaded", function () {
  const startBtn = document.getElementById("startBtn");
  const hitBtn = document.getElementById("hitBtn");
  const standBtn = document.getElementById("standBtn");
  const playerCards = document.getElementById("playerCards");
  const dealerCards = document.getElementById("dealerCards");
  const resultText = document.getElementById("result");

  // 開始新遊戲
  startBtn.addEventListener("click", () => {
    fetch("/start", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        playerCards.textContent = data.player.join(", ");
        dealerCards.textContent = data.dealer[0] + ", ?";
        resultText.textContent = "";
        hitBtn.disabled = false;
        standBtn.disabled = false;
      });
  });

  // 抽牌
  hitBtn.addEventListener("click", () => {
    fetch("/hit", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        playerCards.textContent = data.player.join(", ");
        if (data.result) {
          resultText.textContent = data.result;
          hitBtn.disabled = true;
          standBtn.disabled = true;
        }
      });
  });

  // 停牌
  standBtn.addEventListener("click", () => {
    fetch("/stand", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        dealerCards.textContent = data.dealer.join(", ");
        resultText.textContent = data.result;
        hitBtn.disabled = true;
        standBtn.disabled = true;
      });
  });
});
