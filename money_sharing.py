from collections import OrderedDict
import random
class User:
    def __init__(self, name, surname, username, email):
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        list_users.append(self)
        self.groups = []
    def CalculateBalance(self):
        self._balance = 0
        for group in self.groups:
            self._balance += group.members[self]
        return self._balance
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
    #unequally by shares

def ShowGroups():
    while True:
        print("Type according number to access group or do another action")
        for i in range(len(list_groups)):
            group = list_groups[i]
            print("({0}) {1}".format(i, group.name))
        print("(a) Add new group")
        print("(d) Delete existing group")
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
        elif inp == "d":
            DeleteGroup()
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

def DeleteGroup():
    if len(list_groups) == 0:
        print("No groups to delete")
        return
    while True:
        print("Choose group to delete")
        for i in range(len(list_groups)):
            group = list_groups[i]
            print("({0}) {1}".format(i, group.name))
        print("(c) Cancel action")
        inp = input()
        try:
            inp = int(inp)
        except:
            pass
        if type(inp) == int and inp >= 0 and inp < len(list_groups):
            group = list_groups.pop(inp)
            print("Deleted group: \"{}\"".format(group.name))
            del group
            return
        elif inp == "c":
            return
        else:
            print("Wrong input. Try again")

def ShowUsers():
    while True:
        print("Type according number to access specific information about user")
        for i in range(len(list_users)):
            user = list_users[i]
            print("({0}) {1} {2}".format(i, user.name, user.surname))
        print("(a) Add new user")
        print("(d) Delete existing settled user")
        print("(m) Exit to main manu")
        print("(e) Exit app")
        inp = input()
        try:
            inp = int(inp)
        except:
            pass
        if type(inp) == int and inp >= 0 and inp < len(list_users):
            user = list_users[inp]
            print("Name: {0} {1}".format(user.name, user.surname))
            print("Username: {}".format(user.username))
            print("Email: {}".format(user.email))
            print("Balance: {}".format(user.CalculateBalance()))
            if len(user.groups) == 0:
                print("Not member of any groups")
            else:
                print("Groups: ")
                for group in user.groups:
                    print("\t{}".format(group))
        elif inp == "a":
            AddUser()
            continue
        elif inp == "d":
            DeleteUser()
            continue
        elif inp == "m":
            break
        elif inp == "e":
            exit()
        else:
            print("Wrong input. Try again")

def AddUser():
    while True:
        print("To cancel adding a user type 0 at any stage")
        name = input("Name: ")
        if name == "0":
            return
        surname = input("Surname: ")
        if surname == "0":
            return
        username = input("Username: ")
        if username == "0":
            return
        email = input("Email: ")
        if email == "0":
            return
        print("Confirm data: {0} {1}, {2}, {3}".format(name, surname, username, email))
        while True:
            inp = input("Type 1 if you want to confirm data, 2 if you want to enter it again or 0 if you want to cancel whole action")
            if inp == "1":
                User(name, surname, username, email)
                return
            elif inp == "2":
                break
            elif inp == "0":
                return
            else:
                print("Wrong input. Try again")
    
def DeleteUser():
    if len(list_users) == 0:
        print("No users to delete")
        return
    while True:
        print("Choose user to delete (showing only users settled in all groups): ")
        settled_users = []
        for i in range(len(list_users)):
            user = list_users[i]
            if user.CalculateBalance() == 0:
                settled_users.append(user)
        if len(settled_users) == 0:
            print("No settled users")
            return
        for i in range(len(settled_users)):
            user = settled_users[i]
            print("({0}) {1} {2}".format(i, user.name, user.surname))
        print("(c) Cancel action")
        inp = input()
        try:
            inp = int(inp)
        except:
            pass
        if type(inp) == int and inp >= 0 and inp < len(settled_users):
            user = list_users.pop(list_users.index(settled_users[inp]))
            print("Deleted user: \"{0} {1}\"".format(user.name, user.surname))
            del user
            return
        elif inp == "c":
            return
        else:
            print("Wrong input. Try again")

list_groups = []
list_users = []

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
        ShowUsers()
    elif inp == "3":
        exit()
    else:
        print("Wrong input. Try again")