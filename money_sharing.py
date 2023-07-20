from collections import OrderedDict
import random

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
        self.members = OrderedDict()
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
        self.members[expense.payer] += round(expense.value,2)
        index = list(self.members).index(expense.payer)
        for mem in expense.members:
            self.members[mem] -= round(expense.members[mem],2)
            if mem != expense.payer:
                index_member = list(self.members).index(mem)
                self.matrix[index][index_member] -= round(expense.members[mem],2)
                self.matrix[index_member][index] += round(expense.members[mem],2)

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
            if _value_by_person*len(self.members) != value:
                self.members[list(self.members)[random.randint(0, len(self.members)-1)]] += round((value - _value_by_person*len(self.members)), 2)
        if type == "unequally":
            pass
    #equally
    #uneqally by percentage
    #uneqally by value

list_groups = []

def ShowGroups():
    while True:
        print("Type according number to acces group or do another action")
        for i in range(len(list_groups)):
            group = list_groups[i]
            print("({0}) {1}".format(i, group.name))
        print("(a) Add new group")
        print("(m) Exit to main manu")
        print("(e) Exit app")
        inp = input()
        try:
            inp = int(inp)
        except:
            pass
        if type(inp) == int and inp >= 0 and inp < len(list_groups):
            print(list_groups[inp].name)
            #
            #
            #
        elif inp == "a":
            AddGroup()
            continue
        elif inp == "m":
            break
        elif inp == "e":
            exit()
        else:
            print("Wrong input. Try again")

def AddGroup():
    name = input("Name of group: ")
    Group(name)



while True:
    print("----------------------------------------------------------------")
    print("Type according number")
    print("(1) Show list of groups")
    print("(2) Show all users")
    print("(3) Quit app")
    inp = input()
    if inp == "1":
        ShowGroups()
    elif inp == "2":
        pass
        #ShowUsers()
    elif inp == "3":
        exit()
    else:
        print("Wrong input. Try again")