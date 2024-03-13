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
            self.tobin = round(self.accountcharge * 0.002, 2)


'''compra = Stock('pepe',3.2,3000,3.6,2,False)
compra.tobin = True

compra2 = Stock('pepe',3.2,3000,3.6,2,False)
compra2.tobin = True
compra.calcular_tobin()
compra2.calcular_tobin()
print(compra.tobin)
print(compra2.tobin)'''
