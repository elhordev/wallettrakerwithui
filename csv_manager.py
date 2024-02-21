class Stock:

    def __init__(self, stock, buyprice, qty, expense, index, tobin) -> None:
        self.stock = stock
        self.buyprice = buyprice
        self.qty = qty
        self.expense = expense
        self.index = index
        self.accountcharge = (buyprice * qty) + expense
        self.balance = 0
        self.tobin = tobin

    def calcular_tobin(self):
        if self.tobin:
            self.tobin = self.accountcharge * 0.002


'''santander = Stock('Santander', 3.72, 2000, 3.6, 1, False)
santander.calcular_tobin()

santander2 = Stock('BBVA', 9, 500, 3.6, 4, True)
santander2.calcular_tobin()

print(santander.stock, santander.buyprice, santander.balance, santander.tobin)
print(santander2.stock, santander2.buyprice, santander2.balance, round(santander2.tobin, 2))
'''