class Stock:
    tobin = False

    def __init__(self, stock, buyprice, qty, expense, index, ) -> None:
        self.stock = stock
        self.buyprice = buyprice
        self.qty = qty
        self.expense = expense
        self.index = index
        self.accountcharge = (buyprice * qty) + expense
        self.balance = 0

    def calcular_tobin(self):
        if self.tobin:
            self.tobin = self.accountcharge * 0.002



