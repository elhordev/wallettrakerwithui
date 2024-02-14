class Stock:
    
    def __init__(self, stock, buyprice, qty, expense, index) -> None:
        
        self.stock = stock
        self.buyprice = buyprice
        self.qty = qty
        self.expense = expense
        self.index = index
        self.accountcharge = (buyprice * qty) + expense
        self.balance = 0

    
