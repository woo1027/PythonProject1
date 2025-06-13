function calculate() {
    const revenue = parseFloat(document.getElementById('revenue').value);
    const salaryCost = parseFloat(document.getElementById('salaryCost').value);
    const foodCost = parseFloat(document.getElementById('foodCost').value);
    const rent = parseFloat(document.getElementById('rent').value);
    const phoneCost = parseFloat(document.getElementById('phoneCost').value);
    const gasCost = parseFloat(document.getElementById('gasCost').value);
    const utilityCost = parseFloat(document.getElementById('utilityCost').value);

    // 計算
    const salaryPercentage = (salaryCost / revenue) * 100;
    const foodPercentage = (foodCost / revenue) * 100;
    const totalCosts = salaryCost + foodCost + rent + phoneCost + gasCost + utilityCost;
    const netProfit = revenue - totalCosts;

    // 顯示結果
    document.getElementById('salaryPercentage').textContent = `人事占比：${salaryPercentage.toFixed(2)}%`;
    document.getElementById('foodPercentage').textContent = `食材占比：${foodPercentage.toFixed(2)}%`;
    document.getElementById('netProfit').textContent = `淨利：${netProfit.toFixed(2)}`;

    // 警示顯示紅字
    document.getElementById('salaryPercentage').classList.toggle('red-text', salaryPercentage > 24);
    document.getElementById('foodPercentage').classList.toggle('red-text', foodPercentage > 44);

    // 更新圓餅圖
    updateChart(salaryPercentage, foodPercentage, netProfit);
}

function updateChart(salaryPercentage, foodPercentage, netProfit) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['人事占比', '食材占比', '其他費用'],
            datasets: [{
                label: '成本占比',
                data: [salaryPercentage, foodPercentage, 100 - salaryPercentage - foodPercentage],
                backgroundColor: ['#ff9999', '#66b3ff', '#99ff99'],
                borderColor: ['#ffffff', '#ffffff', '#ffffff'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}
