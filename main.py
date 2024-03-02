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
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

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