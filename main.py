class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description = ""):
        self.ledger.append( {"amount": amount, "description": description} )

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.ledger.append( {"amount":-amount, "description": description} )
            return True
        return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False


    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)
    
    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        ret_str = self.name.center(30,'*') + '\n'
        for item in self.ledger:
            ret_str += item['description'].ljust(23)[:23] + ('{:.2f}'.format(item['amount']) + '\n').rjust(8)
        
        ret_str += "Total: " + '{:.2f}'.format(self.get_balance())

        return ret_str

def create_spend_chart(categories):
    spends = []

    for category in categories:
        spends.append( -round(sum( [ val['amount'] for val in category.ledger if val['amount'] < 0 ] ),2) )
    
    total_spends = sum(spends)
    
    print(spends, total_spends)

    chart = "Percentage spent by category\n"

    for i in range(100,-1,-10):
        chart += f"{str(i).rjust(3)}|"
        for spend in spends:
            if spend/total_spends*100 > i:
                chart += ' o '
            else:
                chart += '   '
        chart+=' \n'

    chart += f"    {'---'*len(spends)}-\n"

    for letter_index in range( max( map( lambda category : len(category.name), categories ) ) ):
        chart += '    '
        for category in categories:
            if letter_index < len(category.name):
                chart += f' {category.name[letter_index]} '
            else:
                chart += '   '
        chart += ' \n' 

    return chart.strip('\n')

if __name__ == "__main__":
    food = Category("Food")
    food.deposit(1000, "deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(15.89, "restaurant and more food for dessert")
    
    clothing = Category("Clothing")
    food.transfer(200, clothing)
    clothing.withdraw(100, "new clothes")

    auto = Category("Auto")
    food.transfer(50,auto)
    auto.withdraw(20, "wheels")

    print(food,'\n')
    print(clothing,'\n')
    print(auto,"\n")    

    categories = [food, clothing, auto]
    chart = create_spend_chart(categories)

    print(chart)
    f = open("test.txt", 'a')
    f.write( chart)
    f.close()