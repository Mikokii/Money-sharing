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
        self.total = {}     #{currency:value, ...}
        self._balance = {}  #{currency:value, ...}
    def CalculateBalance(self):
        for curr in self._balance:
            self._balance[curr] = 0
        for group in self.groups:
            if not (group.currency in self._balance.keys()):
                self._balance[group.currency] = 0
            self._balance[group.currency] += round(group.members[self],2)
        return self._balance
    def IsSettled(self):
        for group in self.groups:
            if group.calculation_type == "normal":
                for i in range(len(group.expense_matrix)):
                    if group.expense_matrix[i][list(group.members).index(self)] != 0:
                        return False
            if group.calculation_type == "simplify":
                if group.members[self] != 0:
                    return False
        return True
    def ShowInfo(self):
        print("Name: {0} {1}".format(self.name, self.surname))
        print("Username: {}".format(self.username))
        print("Email: {}".format(self.email))
        balance = self.CalculateBalance()
        if len(balance) == 0:
            print("No expenses")
        elif len(balance) == 1:
            print("Balance: {}{}".format(list(balance.values())[0], list(balance)[0]))
        else:
            print("Balance:")
            for currency, value in sorted(balance.items(), key = lambda item: item[1], reverse=True):
                print(value, currency)
        if len(self.total) == 0:
            pass
        elif len(self.total) == 1:
            print("Total spendings: {}{}".format(list(self.total.values())[0], list(balance)[0]))
        else:
            print("Total spendings:")
            for currency, value in sorted(self.total.items(), key = lambda item: item[1], reverse=True):
                print(value, currency)
        if len(self.groups) == 0:
            print("Not member of any groups")
        else:
            print("Groups: ")
            for group in self.groups:
                print("\"{}\"".format(group.name))
class Group:
    def __init__(self, name):
        self.name = name
        list_groups.append(self)
        self.members = OrderedDict()
        self.expense_matrix = []
        self.list_expenses = []
        self.calculation_type = "normal"    #normal or simplify
        self.currency = None
        self.SelectCurrency()
        self.total = {}     #{currency:value, ...}
    def AddMember(self, member):
        self.members[member] = 0
        member.groups.append(self)
        self.expense_matrix.append([0]*len(self.members))
        for i in range(len(self.members)-1):
            self.expense_matrix[i].append(0)
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
                self.expense_matrix[index][index_member] -= round(expense.members[mem],2)
                self.expense_matrix[index_member][index] += round(expense.members[mem],2)
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
    def ShowGroupInfo(self):
         while True:
            print("\"{}\"".format(self.name))
            print("Group expense calculation type: {}".format(self.calculation_type))
            print("Group currency: {}".format(self.currency))
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
                    self.AddExpenseMenu()
                case "1":
                    pass # ADD !!!!!!
                case "2":
                    self.ShowBalanceMember() # Check !!!!!!
                case "3":
                    self.ShowMembers()
                case "4":
                    self.AddMemberMenu()
                case "5":
                    self.ShowExpensesHistory()
                case "6":
                    self.ShowTotalSpendings()
                case "7":
                    self.ChangeCalculationType()
                case "8":
                    self.ChangeCurrency()
                case "9":
                    return
                case "h":
                    print("Normal type of expense calculation type is the intuitive way of calculating who owes who what amount of money.")
                    print("Simplify type of expense calculation reduce the amount of needed transfers between users, but can be unintuitive.")
                    print("Example: A owes B 5$ and B owes C 5$. Simplify type of expense calculation reduce trasfers number from 2 to 1 - A owes C 5$.")
                case _:
                    print("Wrong input. Try again")
    def ChangeCurrency(self):
        if self.IsSettled():
            self.SelectCurrency()
        else:
            print("Group members are not settled!")
            print("Changing currency will convert existing debts to new currency (it want affect currency of expenses in history)")
            print("Type \"0\" to continue or anything else to cancel this action")
            conf = input()
            if conf == "0":
                self.SelectCurrency()
            else:
                pass
    def ShowTotalSpendings(self):
        if len(self.list_expenses) == 0:
            print("There are no expenses")
        else:
            print("Total spendings:")
            for currency, value in sorted(self.total.items(), key = lambda item: item[1]):
                print(value, currency)
    def ShowExpensesHistory(self):
        if len(self.list_expenses) == 0:
            print("There are no expenses")
            return
        while True:
            print("Type number to see more information about certain expense or \"e\" to go back to group menu")
            for i in range(len(self.list_expenses)-1, -1, -1):
                expense = self.list_expenses[i]
                print("({0}) \"{1}\" - {2}{3} - {4}".format(len(self.list_expenses)-i-1, expense.name, expense.value, expense.currency, expense.category))
            inp = input()
            try:
                inp = int(inp)
                if inp >= 0 and inp < len(self.list_expenses):
                    self.list_expenses[len(self.list_expenses)-inp-1].ShowExpense()
                else:
                    print("Wrong input. Try again")
            except:
                if inp == "e":
                    return
                else:
                    print("Wrong input. Try again")
    def ShowMembers(self):
        if len(self.members) == 0:
            print("There are no members in this group")
            return
        for member in self.members:
            print("{0} {1}".format(member.name, member.surname))
    def AddMemberMenu(self):
        while True:
            print("Choose existing user to be added or add new user")
            print("(c) Cancel action")
            print("(0) Add new user")
            list_not_in_group = []
            for user in list_users:
                if not (user in list(self.members)):
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
                        self.AddMember(list_users[-1])
                        print("Added {} {} to group".format(list_users[-1].name, list_users[-1].surname))
                        return
                elif inp >= 1 and inp <= len(list_not_in_group):
                    self.AddMember(list_not_in_group[inp-1])
                    print("Added {} {} to group".format(list_not_in_group[i-1].name, list_not_in_group[i-1].surname))
                    return
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
    def ShowBalanceMember(self):
        if len(self.members) == 0:
            print("There are no members in this group")
            return
        while True:
            print("Type corresponding number of member to see his/her balance or anything else to quit")
            for i in range(len(self.members)):
                member = list(self.members)[i]
                print("({}) {} {}".format(i+1, member.name, member.surname))
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(self.members):
                    member = list(self.members)[inp-1]
                    value = self.members[member]
                    if value == 0:
                        print("{} {} is settled".format(member.name, member.surname))
                    elif value < 0:
                        print("{} {} owes {}{}".format(member.name, member.surname, -value, self.currency))
                        #
                        #
                        #
                        #
                    else:
                        print("{} {} is owed {}{}".format(member.name, member.surname, value, self.currency))
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
    def AddExpenseMenu(self):  
        if len(self.members) == 0:
            print("There are no members in group")
            return
        while True:
            print("Follow instructions or type \"0\" at any point to cancel the action")
            name = input("Name of expense: ")
            if name == "0":
                return
            category = self.SelectCategory()
            if category == "0":
                return
            value = self.SelectValue()
            if value == 0:
                return
            payer = self.SelectPayer()
            if payer == "0":
                return 
            members = self.SelectMembers()
            if members == "0":
                return
            type = self.SelectType()
            if type == "0":
                return
            members = self.SplitingMenu(type, members, value)
            while True:
                print("Type \"1\" to confirm expense or \"2\" to enter it again")
                print("{} - {} - {}{}".format(name, category, value, self.currency))
                print("Paid by {} {}".format(payer.name, payer.surname))
                print("Split across:")
                for mem in members:
                    print("{} {}: {}{}".format(mem.name, mem.surname, members[mem], self.currency))
                inp = input()
                match inp:
                    case "0":
                        return
                    case "1":
                        self.AddExpense(name, value, self.currency, payer, members, category, type)
                        return
                    case "2":
                        break
                    case _:
                        print("Wrong input. Try again")
    def SelectCategory(self):
        categories = ["General", "Food and drink", "Entertainment", "Home", "Life", "Transport", "Utilities", "Business", "Custom category"]
        while True:
            for i in range(len(categories)):
                print("({}) {}".format(i+1, categories[i]))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return "0"
                elif inp >= 1 and inp < len(categories):
                    return categories[inp-1]
                elif inp == len(categories):
                    return input("Category: ")
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
    def SelectValue(self):
        while True:
            value = input("Value ({}): ".format(self.currency))
            try:
                value = round(float(value),2)
                if value < 0:
                    print("Wrong input. Try again")
                else:
                    return value
            except:
                print("Wrong input. Try again")
    def SelectPayer(self):
        while True:
            print("Choose payer: ")
            for i in range(len(self.members)):
                member = list(self.members)[i]
                print("({}) {} {}".format(i+1, member.name, member.surname))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return "0"
                elif inp >= 1 and inp <= len(self.members):
                    return list(self.members)[inp-1]
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
    def SelectMembers(self):
        chosen_members = {mem:0 for mem in list(self.members)}
        while True:
            print("Choose who is involved in this expense (green - chosen, red - not chosen):")
            print("Press enter to confirm selection")
            print("(a) Select/Discard everybody")
            for i in range(len(self.members)):
                member = list(self.members)[i]
                if chosen_members[member] == 0:
                    prRed("({}) {} {}".format(i+1, member.name, member.surname))
                else:
                    prGreen("({}) {} {}".format(i+1, member.name, member.surname))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return "0"
                elif inp >= 1 and inp <= len(self.members):
                    chosen_members[list(self.members)[inp-1]] = abs(chosen_members[list(self.members)[inp-1]]-1)
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
                    if all(num == 0 for num in list(chosen_members.values())):
                        print("Someone needs to be picked")
                    else:
                        return {user:0 for user in list(chosen_members) if chosen_members[user] == 1}
                else:
                    print("Wrong input. Try again")
    def SelectType(self):
        types = ["equally", "unequally by value", "unequally by percentage", "unequally by shares"]
        while True:
            print("Choose a way to split expense")
            for i in range(len(types)):
                print("({}) {}".format(i+1, types[i]))
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return "0"
                elif inp >= 1 and inp <= len(types):
                    return types[inp - 1]
                else:
                    print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
    def SplitingMenu(self, type, members, value):
        match type:
            case "equally":
                return self.CalculateEqually(members, value)
            case "unequally by value":
                return self.CalculateUnequallyValue(members, value)
            case "unequally by percentage":
                return self.CalculateUnequallyPercentage(members, value)
            case "unequally by shares":
                return self.CalculateUnequallyShares(members, value)
    def CalculateEqually(self, members, value):
        _value_by_person = round(value/len(members),2)
        for mem in members:
            members[mem] = _value_by_person
        if sum(members.values()) != value:
            members[list(self.members)[random.randint(0, len(members)-1)]] += round((value - sum(members.values())), 2)
        return members
    def CalculateUnequallyValue(self, members, value):
        while True:
            print("Choose person to change value or type enter to confirm selection")
            remaining = round(value - sum(members.values()),2)
            print("Remaining amount: {}{}".format(remaining, self.currency))
            for i in range(len(members)):
                mem = list(members.keys())[i]
                print("({}) {} {}: {}{}".format(i+1, mem.name, mem.surname, members[mem], self.currency))
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(members):
                    while True:
                        inp1 = input("Enter value or \"0\" to cancel: ")
                        try:
                            inp1 = round(float(inp1),2)
                            if inp1 == 0:
                                break
                            elif inp1 > 0 and inp1 <= (remaining + members[list(members.keys())[inp-1]]):
                                members[list(members.keys())[inp-1]] = round(inp1, 2)
                                break
                            else:
                                print("Value must be greater than 0 and lower or equal to remaining amount")
                        except:
                            print("Wrong input. Try again")
                else:
                    print("Wrong input. Try again")
            except:
                if inp == "":
                    remaining = round(value - sum(members.values()),2)
                    if remaining == 0:
                        return members
                    else:
                        print("Remaining money to split")
                else:
                    print("Wrong input. Try again")
    def CalculateUnequallyPercentage(self, members, value):
        while True:
            print("Choose person to change percentage or type enter to confirm selection")
            remaining = round((value - sum(percentage*value for percentage in members.values()))/value,4)*100
            print("Remaining % of value: {}%".format(remaining))
            for i in range(len(members)):
                mem = list(members.keys())[i]
                print("({}) {} {}: {}%".format(i+1, mem.name, mem.surname, members[mem]*100))
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(members):
                    while True:
                        inp1 = input("Enter percentage or \"0\" to cancel: ")
                        try:
                            inp1 = round(float(inp1),2)
                            if inp1 == 0:
                                break
                            elif inp1 > 0 and inp1 <= (remaining + members[list(members.keys())[inp-1]]*100):
                                members[list(members.keys())[inp-1]] = round(inp1/100, 4)
                                break
                            else:
                                print("Value must be greater than 0 and lower or equal to remaining percentage")
                        except:
                            print("Wrong input. Try again")
                else:
                    print("Wrong input. Try again")
            except:
                if inp == "":
                    remaining = round((value - sum(percentage*value for percentage in members.values()))/value,4)*100
                    if remaining == 0:
                        for mem in members:
                            members[mem] = round(members[mem]*value,2)
                        if sum(members.values()) != value:
                            members[list(members)[random.randint(0, len(members)-1)]] += round((value - sum(members.values())), 2)
                        return members
                    else:
                        print("Remaining money to split")
                else:
                    print("Wrong input. Try again")
    def CalculateUnequallyShares(self, members, value):
        while True:
            print("Choose person to change share or type enter to confirm selection")
            for i in range(len(members)):
                mem = list(members.keys())[i]
                print("({}) {} {}: {} shares".format(i+1, mem.name, mem.surname, members[mem]))
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(members):
                    while True:
                        inp1 = input("Enter share or \"0\" to cancel: ")
                        try:
                            inp1 = int(inp1)
                            if inp1 == 0:
                                break
                            elif inp1 > 0:
                                members[list(members.keys())[inp-1]] = inp1
                                break
                            else:
                                print("Value must be greater than 0")
                        except:
                            print("Wrong input. Try again")
                else:
                    print("Wrong input. Try again")
            except:
                if inp == "":
                    if 0 in members.values():
                        print("People without share remaining")
                    else:
                        shares = sum(members.values())
                        for mem in members:
                            members[mem] = round((members[mem]/shares)*value,2)
                        if sum(members.values()) != value:
                            members[list(members)[random.randint(0, len(members)-1)]] += round((value - sum(members.values())), 2)
                        return members
                else:
                    print("Wrong input. Try again")
    def SelectCurrency(self):
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
                        self.currency = "$"
                        return
                    case 2:
                        self.currency = "€"
                        return
                    case 3:
                        self.currency = "£"
                        return
                    case 4:
                        self.currency ="¥"
                        return
                    case 5:
                        self.currency = "元"
                        return
                    case 6:
                        self.currency = "PLN"
                        return
                    case 7:
                        self.currency = "AUD"
                        return
                    case 8:
                        self.currency = "CAD"
                        return
                    case 9:
                        self.currency = "CHF"
                        return
                    case 0:
                        self.currency = input("Type currency: ")
                        return
                    case _:
                        print("Wrong input. Try again")
            except:
                print("Wrong input. Try again")
class Expense:
    def __init__(self, name, value, currency, payer, members, category, type):
        self.name = name
        self.value = value
        self.currency = currency
        self.payer = payer
        self.members = members
        self.category = category
        self.type = type
    def ShowExpense(self):
        print("Type anything to exit")
        print("\"{0}\"   -   category: {1}".format(self.name, self.category))
        print("{0}{1}".format(self.value,self.currency))
        print("{0} {1} paid {2}{3}".format(self.payer.name, self.payer.surname, self.value, self.currency))
        for member in self.members:
            print("{0} {1} owes {2}{3}".format(member.name, member.surname, self.members[member], self.currency))
        input()
        return   

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
            if inp >= 0 and inp < len(list_groups):
                list_groups[inp].ShowGroupInfo()
        except:
            if inp == "a":
                name = input("Name of group: ")
                Group(name)
            elif inp == "d":
                DeleteGroup()
            elif inp == "m":
                break
            elif inp == "e":
                exit()
            else:
                print("Wrong input. Try again")

def DeleteGroup():
    if len(list_groups) == 0:
        print("No groups to delete")
        return
    while True:
        print("Choose group to delete (if group is not settled expenses will be deleted)")
        for i in range(len(list_groups)):
            group = list_groups[i]
            if group.IsSettled():
                print("({0}) {1}".format(i, group.name))
            else:
                print("({0}) {1} (group not settled)" .format(i, group.name))
        print("(c) Cancel action")
        inp = input()
        try:
            inp = int(inp)
            if inp >= 0 and inp < len(list_groups):
                group = list_groups.pop(inp)
                for mem in group.members:
                    mem.groups.remove(group)
                print("Deleted group: \"{}\"".format(group.name))
                del group
                return
        except:
            if inp == "c":
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
            if inp >= 0 and inp < len(list_users):
                list_users[inp].ShowInfo()       
        except: 
            if inp == "a":
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
        settled_users = []
        for i in range(len(list_users)):
            user = list_users[i]
            if user.IsSettled():
                settled_users.append(user)
        if len(settled_users) == 0:
            print("No settled users")
            return
        print("Choose user to delete (showing only users settled in all groups): ")
        for i in range(len(settled_users)):
            user = settled_users[i]
            print("({0}) {1} {2}".format(i, user.name, user.surname))
        print("(c) Cancel action")
        inp = input()
        try:
            inp = int(inp)
            if inp >= 0 and inp < len(settled_users):
                user = list_users.pop(list_users.index(settled_users[inp]))
                print("Deleted user: \"{0} {1}\"".format(user.name, user.surname))
                del user
                return
        except:
            if inp == "c":
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

# Add remaining options to group info (all members' balance)
# Add another type of expenses
# Add calculating transfers in both ways (also not finished showing balance)
# Add option to settle up two users
# Add specific transfers in Show balance member
# ... 