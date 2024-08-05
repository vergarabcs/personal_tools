function change(amount: number, coins: number[]): number {
    coins.sort((a: number, b: number) => (a-b))
    const change2 = (amount2: number, endI: number) => {
        if(amount2 === 0){
            return 1;
        }
        if(endI < 0) return 0;

        const iCoin = coins[endI]
        let total = 0;
        let remainingAmount = amount
        while(remainingAmount >= 0){
            total += change2(remainingAmount, endI-1)
            remainingAmount -= iCoin
        }
        return total;
    }

    return change2(amount, coins.length - 1)
};

console.log(change(5, [1, 2, 5]))