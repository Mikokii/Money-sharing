class User:
    def __init__(self, name, surname, username, email):
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.groups = []
class Group:
    def __init__(self, name):
        self.name = name
        list_groups.append(self)
        self.members = {}
        self.matrix = []
        self.list_expenses = []
    def AddMember(self, member):
        self.members[member] = 0
        member.groups.append(self)
        self.matrix.append([0]*len(self.members))
        for i in range(len(self.members)-1):
            self.matrix[i].append(0)
    def AddExpense(self, name, value, currency, payer, members, type):
        expense = Expense(name, value, currency, payer, members, type)
        self.list_expenses.append(expense)
        self.members[expense.payer] += expense.value
        index = list(self.members).index(expense.payer)
        for mem in expense.members:
            self.members[mem] -= expense.members[mem]
            if mem != expense.payer:
                index_member = list(self.members).index(mem)
                self.matrix[index][index_member] -= expense.members[mem]
                self.matrix[index_member][index] += expense.members[mem]

class Expense:
    def __init__(self, name, value, currency, payer, members, type):
        self.name = name
        self.value = value
        self.currency = currency
        self.payer = payer
        self.members = members
        self.type = type
        if type == "equally":
            _value_by_person = round(self.value/len(self.members),2)
            for i in self.members:
                self.members[i] = _value_by_person
    #equally
    #uneqally by percentage
    #uneqally by value

list_groups = []


################################################################
group1 = Group("test")
per1 = User("Mikołaj", "Kiszka", "Mikokii", "miko123@gmail.com")
group1.AddMember(per1)
per2 = User("Mikołaj", "Kiszka", "Mikokii", "miko123@gmail.com")
group1.AddMember(per2)
per3 = User("Mikołaj", "Kiszka", "Mikokii", "miko123@gmail.com")
group1.AddMember(per3)
group1.AddExpense("Zakupy", 120, "PLN", per2, {per1:0, per2:0, per3:0}, "equally")
group1.AddExpense("Samochod", 160, "PLN", per3, {per1:0, per2:0}, "equally")
print(group1.list_expenses)
print(group1.matrix)
print(group1.members)