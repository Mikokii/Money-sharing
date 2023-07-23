from collections import OrderedDict
import random

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

class User:
    def __init__(self, name, surname, username, email):
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        list_users.append(self)
        self.groups = []
        self.total = {}
    def CalculateBalance(self):
        self._balance = {}
        for group in self.groups:
            if not (group.currency in self._balance.keys()):
                self._balance[group.currency] = 0
            self._balance[group.currency] += round(group.members[self],2)
        return self._balance
class Group:
    def __init__(self, name, currency):
        self.name = name
        list_groups.append(self)
        self.members = OrderedDict()
        self.matrix = []
        self.list_expenses = []
        self.calculation_type = "normal"
        self.currency = currency
        self.total = {}
    def AddMember(self, member):
        self.members[member] = 0
        member.groups.append(self)
        self.matrix.append([0]*len(self.members))
        for i in range(len(self.members)-1):
            self.matrix[i].append(0)
    def AddExpense(self, name, value, currency, payer, members, category, type):
        expense = Expense(name, value, currency, payer, members, category, type)
        self.list_expenses.append(expense)
        if not (currency in self.total.keys()):
            self.total[currency] = 0
        self.total[currency] += round(value,2)
        self.members[payer] += round(value,2)
        index = list(self.members).index(payer)
        for mem in expense.members:
            self.members[mem] -= round(expense.members[mem],2)
            if not (currency in mem.total.keys()):
                mem.total[currency] = 0
            mem.total[currency] += round(expense.members[mem],2)
            if mem != expense.payer:
                index_member = list(self.members).index(mem)
                self.matrix[index][index_member] -= round(expense.members[mem],2)
                self.matrix[index_member][index] += round(expense.members[mem],2)
    def ChangeCalculationType(self):
        if self.calculation_type == "normal":
            self.calculation_type = "simplify"
        else:
            self.calculation_type = "normal"
    def IsSettled(self):
        for mem in self.members:
            if self.members[mem] != 0:
                return False
        return True
class Expense:
    def __init__(self, name, value, currency, payer, members, category, type):
        self.name = name
        self.value = value
        self.currency = currency
        self.payer = payer
        self.members = members
        self.category = category
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
            ShowGroupInfo(list_groups[inp])
        elif inp == "a":
            AddGroup()
        elif inp == "d":
            DeleteGroup()
        elif inp == "m":
            break
        elif inp == "e":
            exit()
        else:
            print("Wrong input. Try again")

def AddGroup():
    name = input("Name of group: ")
    currency = SelectCurrency()
    Group(name, currency)

def SelectCurrency():
    while True:
        print("Select currency:")
        print("(1) USD - $")
        print("(2) EUR - €")
        print("(3) GBP - £")
        print("(4) JPY - ¥")
        print("(5) CNY - 元")
        print("(6) PLN")
        print("(7) AUD")
        print("(8) CAD")
        print("(9) CHF")
        print("(0) Other")
        inp = input()
        try:
            inp = int(inp)
            match inp:
                case 1:
                    return "$"
                case 2:
                    return "€"
                case 3:
                    return "£"
                case 4:
                    return "¥"
                case 5:
                    return "元"
                case 6:
                    return "PLN"
                case 7:
                    return "AUD"
                case 8:
                    return "CAD"
                case 9:
                    return "CHF"
                case 0:
                    curr = input("Type currency: ")
                    return curr
                case _:
                    print("Wrong input. Try again")
        except:
            print("Wrong input. Try again")

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
            balance = user.CalculateBalance()
            if len(balance) == 0:
                print("No expenses")
            elif len(balance) == 1:
                print("Balance: {}{}".format(list(balance.values())[0], list(balance)[0]))
            else:
                print("Balance:")
                for currency, value in sorted(balance.items(), key = lambda item: item[1], reverse=True):
                    print(value, currency)
            if len(user.total) == 0:
                pass
            elif len(user.total) == 1:
                print("Total spendings: {}{}".format(list(user.total.values())[0], list(balance)[0]))
            else:
                print("Total spendings:")
                for currency, value in sorted(user.total.items(), key = lambda item: item[1], reverse=True):
                    print(value, currency)
            if len(user.groups) == 0:
                print("Not member of any groups")
            else:
                print("Groups: ")
                for group in user.groups:
                    print("\"{}\"".format(group.name))
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
            return False
        surname = input("Surname: ")
        if surname == "0":
            return False
        username = input("Username: ")
        if username == "0":
            return False
        email = input("Email: ")
        if email == "0":
            return False
        print("Confirm data: {0} {1}, {2}, {3}".format(name, surname, username, email))
        while True:
            inp = input("Type 1 if you want to confirm data, 2 if you want to enter it again or 0 if you want to cancel whole action: ")
            if inp == "1":
                User(name, surname, username, email)
                return True
            elif inp == "2":
                break
            elif inp == "0":
                return False
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

def ShowGroupInfo(group):
    while True:
        print("\"{}\"".format(group.name))
        print("Group expense calculation type: {}".format(group.calculation_type))
        print("Group currency: {}".format(group.currency))
        print("Choose action:")
        print("(0) Add new expense")
        print("(1) Show balance of all members")
        print("(2) Show balance of certain member (in this group)")
        print("(3) Show all members")
        print("(4) Add new member")
        print("(5) Show expense history")
        print("(6) Show total spendings of group")
        print("(7) Change expense calculation type (to see diffrence between calculation types enter \"h\")")
        print("(8) Change currency of the group")
        print("(9) Go back to group list")
        inp = input()
        match inp:
            case "0":
                AddExpense(group)
            case "1":
                pass
            case "2":
                ShowBalanceMember(group)
            case "3":
                ShowMembers(group)
            case "4":
                AddMember(group)
            case "5":
                ShowExpensesHistory(group)
            case "6":
                if len(group.list_expenses) == 0:
                    print("There are no expenses")
                else:
                    print("Total spendings:")
                    for currency, value in sorted(group.total.items(), key = lambda item: item[1]):
                        print(value, currency)
            case "7":
                group.ChangeCalculationType()
            case "8":
                if group.IsSettled():
                    group.currency = SelectCurrency()
                else:
                    print("Group members are not settled!\
                        Changing currency will convert existing debts to new currency (it want affect currency of expenses in history)")
                    print("Type \"0\" to continue or anything else to cancel this action")
                    conf = input()
                    if conf == "0":
                        group.currency = SelectCurrency()
                    else:
                        pass
            case "9":
                return
            case "h":
                print("Normal type of expense calculation type is the intuitive way of calculating who owes who what amount of money.")
                print("Simplify type of expense calculation reduce the amount of needed transfers between users, but can be unintuitive.")
                print("Example: A owes B 5$ and B owes C 5$. Simplify type of expense calculation reduce trasfers number from 2 to 1 - A owes C 5$.")
            case _:
                print("Wrong input. Try again")

def ShowExpensesHistory(group):
    if len(group.list_expenses) == 0:
        print("There are no expenses")
        return
    while True:
        print("Type number to see more information about certain expense or \"e\" to go back to group menu")
        for i in range(len(group.list_expenses)-1, -1, -1):
            expense = group.list_expenses[i]
            print("({0}) \"{1}\" - {2}{3} - {4}".format(len(group.list_expenses)-i-1, expense.name, expense.value, expense.currency, expense.category))
        inp = input()
        try:
            inp = int(inp)
            if inp >= 0 and inp < len(group.list_expenses):
                ShowExpense(group.list_expenses[len(group.list_expenses)-inp-1])
            else:
                print("Wrong input. Try again")
        except:
            if inp == "e":
                return
            else:
                print("Wrong input. Try again")

def ShowExpense(expense):
    print("Type anything to exit")
    print("\"{0}\"   -   category: {1}".format(expense.name, expense.category))
    print("{0}{1}".format(expense.value,expense.currency))
    print("{0} {1} paid {2}{3}".format(expense.payer.name, expense.payer.surname, expense.value, expense.currency))
    for member in expense.members:
        print("{0} {1} owes {2}{3}".format(member.name, member.surname, expense.members[member], expense.currency))
    inp = input()
    return

def ShowMembers(group):
    if len(group.members) == 0:
        print("There are no members in this group")
        return
    for member in group.members:
        print("{0} {1}".format(member.name, member.surname))

def AddMember(group):
    while True:
        print("Choose existing user to be added or add new user")
        print("(c) Cancel action")
        print("(0) Add new user")
        list_not_in_group = []
        for user in list_users:
            if not (user in list(group.members)):
                list_not_in_group.append(user)
        for i in range(len(list_not_in_group)):
            user = list_not_in_group[i]
            print("({0}) {1} {2}".format(i+1, user.name, user.surname))
        inp = input()
        if inp == "c":
            return
        try:
            inp = int(inp)
            if inp == 0:
                if AddUser():
                    group.AddMember(list_users[-1])
                    print("Added {} {} to group".format(list_users[-1].name, list_users[-1].surname))
                    return
            elif inp >= 1 and inp <= len(list_not_in_group):
                group.AddMember(list_not_in_group[inp-1])
                print("Added {} {} to group".format(list_not_in_group[i-1].name, list_not_in_group[i-1].surname))
                return
            else:
                print("Wrong input. Try again")
        except:
            print("Wrong input. Try again")

def ShowBalanceMember(group):
    if len(group.members) == 0:
        print("There are no members in this group")
        return
    while True:
        print("Type corresponding number of member to see his/her balance or anything else to quit")
        for i in range(len(group.members)):
            member = list(group.members)[i]
            print("({}) {} {}".format(i+1, member.name, member.surname))
        inp = input()
        try:
            inp = int(inp)
            if inp >= 1 and inp <= len(group.members):
                member = list(group.members)[inp-1]
                value = group.members[member]
                if value == 0:
                    print("{} {} is settled".format(member.name, member.surname))
                elif value < 0:
                    print("{} {} owes {}{}".format(member.name, member.surname, -value, group.currency))
                    #
                    #
                    #
                    #
                else:
                    print("{} {} is owed {}{}".format(member.name, member.surname, value, group.currency))
                    #
                    #
                    #
                    #
                    #
                print(("Type \"0\" to see another member's balance or anything else to go back to group menu"))
                inp = input()
                if inp == "0":
                    continue
                else:
                    return
            else:
                return
        except:
            return

def AddExpense(group):
    if len(group.members) == 0:
        print("There are no members in group")
        return
    while True:
        print("Follow instructions or type \"0\" at any point to cancel the action")
        name = input("Name of expense: ")
        if name == "0":
            return
        categories = ["General", "Food and drink", "Entertainment", "Home", "Life", "Transport", "Utilities", "Business", "Custom category"]
        while True:
            for i in range(len(categories)):
                print("({}) {}".format(i+1, categories[i]))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return
                elif inp >= 1 and inp < len(categories):
                    category = categories[inp-1]
                    break
                elif inp == len(categories):
                    category = input("Category: ")
                    break
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
        while True:
            value = input("Value ({}): ".format(group.currency))
            try:
                value = round(float(value),2)
                if value == 0:
                    return
                elif value < 0:
                    print("Wrong input. Try again")
                else:
                    break
            except:
                print("Wrong input. Try again")
        while True:
            print("Choose payer: ")
            for i in range(len(group.members)):
                member = list(group.members)[i]
                print("({}) {} {}".format(i+1, member.name, member.surname))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return
                elif inp >= 1 and inp <= len(group.members):
                    payer = list(group.members)[inp-1]
                    break
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
        chosen_members = {mem:0 for mem in list(group.members)}
        while True:
            print("Choose who is involved in this expense (green - chosen, red - not chosen):")
            print("Press enter to confirm selection")
            print("(a) Select/Discard everybody")
            for i in range(len(group.members)):
                member = list(group.members)[i]
                if chosen_members[member] == 0:
                    prRed("({}) {} {}".format(i+1, member.name, member.surname))
                else:
                    prGreen("({}) {} {}".format(i+1, member.name, member.surname))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return
                elif inp >= 1 and inp <= len(group.members):
                    chosen_members[list(group.members)[inp-1]] = abs(chosen_members[list(group.members)[inp-1]]-1)
                else:
                    print("Wrong input. Try again")
            except:
                if inp == "a":
                    if 0 in list(chosen_members.values()):
                        for chosen in chosen_members:
                            chosen_members[chosen] = 1
                    else:
                        for chosen in chosen_members:
                            chosen_members[chosen] = 0
                elif inp == "":
                    members = {user:0 for user in list(chosen_members) if chosen_members[user] == 1}
                    break
                else:
                    print("Wrong input. Try again")
        types = ["equally", "unequally"] ############ ADD TYPES
        while True:
            print("Choose a way to split expense")
            for i in range(len(types)):
                print("({}) {}".format(i+1, types[i]))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return
                elif inp >= 1 and inp <= len(types):
                    type = types[inp - 1]
                    break
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
        while True:
            print("Type \"1\" to confirm expense or \"2\" to enter it again")
            print("{} - {} - {}{}".format(name, category, value, group.currency))
            print("Paid by {} {}".format(payer.name, payer.surname))
            print("Split across:")
            for mem in members:
                print("{} {}".format(mem.name, mem.surname))
            print("Divided {}".format(type))
            inp = input()
            match inp:
                case "0":
                    return
                case "1":
                    group.AddExpense(name, value, group.currency, payer, members, category, type)
                    return
                case "2":
                    break
                case _:
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

# Someone needs to be picked in expense
# Add remaining options to group info
# Add another type of expenses
# Add calculating transfers in both ways (also not finished showing balance)
# Add option to settle up two users
# Add specific ownings in Show balance member
# ... 
# Clean up (Change some separate functions to class functions ??????)