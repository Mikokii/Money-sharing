from collections import OrderedDict
from threading import Timer
import random
import pickle
import os

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prGray(skk): print("\033[90m {}\033[00m" .format(skk))

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
        if input() == "exit":
            QuitApp()
class Group:
    def __init__(self, name):
        self.name = name
        list_groups.append(self)
        self.members = OrderedDict()
        self.expense_matrix = []
        self.expense_simplify_matrix = []
        self.list_expenses = []
        self.calculation_type = "normal"    #normal or simplify
        self.currency = "$"
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
        if category != "Settlement":
            if not (currency in self.total.keys()):
                self.total[currency] = 0
            self.total[currency] += round(value,2)
        self.members[payer] += round(value,2)
        index = list(self.members).index(payer)
        for mem in expense.members:
            self.members[mem] -= round(expense.members[mem],2)
            if category != "Settlement":
                if not (currency in mem.total.keys()):
                    mem.total[currency] = 0
                mem.total[currency] += round(expense.members[mem],2)
            if mem != expense.payer:
                index_member = list(self.members).index(mem)
                self.expense_matrix[index_member][index] -= round(expense.members[mem],2)
                self.expense_matrix[index][index_member] += round(expense.members[mem],2)
    def ChangeCalculationType(self):
        if self.IsSettled():
            for i in range(len(self.expense_matrix)):
                for j in range(len(self.expense_matrix)):
                    self.expense_matrix[i][j] = 0
        if self.calculation_type == "normal":
            self.calculation_type = "simplify"
            print("Changed calculation type to \"simplify\"")
        else:
            self.calculation_type = "normal"
            print("Changed calculation type to \"normal\"")
        if input() == "exit":
            QuitApp()
    def IsSettled(self):
        for mem in self.members:
            if self.members[mem] != 0:
                return False
        return True
    def ShowGroupInfo(self):
         for mem in self.members:
            self.members[mem] = round(self.members[mem],2)
         while True:
            print("\n----------------------------------------------------------------")
            print("\"{}\"".format(self.name))
            print("Group expense calculation type: {}".format(self.calculation_type))
            print("Group currency: {}".format(self.currency))
            print("--------------------------------")
            print("(1) Add new expense")
            print("(2) Show balance of all members")
            print("(3) Settle up members")
            print("(4) Show all members")
            print("(5) Add new member")
            print("(6) Show expense history")
            print("(7) Show total spendings of group")
            print("(8) Change expense calculation type (to see diffrence between calculation types type \"h\")")
            print("(9) Change currency of the group")
            print("(0) Go back to group list")
            print("----------------------------------------------------------------")
            inp = input()
            match inp:
                case "1":
                    self.AddExpenseMenu()
                case "2":
                    self.ShowBalanceAll()
                case "3":
                    self.SettleUpMenu()
                case "4":
                    self.ShowMembers()
                case "5":
                    self.AddMemberMenu()
                case "6":
                    self.ShowExpensesHistory()
                case "7":
                    self.ShowTotalSpendings()
                case "8":
                    self.ChangeCalculationType()
                case "9":
                    self.ChangeCurrency()
                case "0":
                    return
                case "h":
                    print("Normal type of expense calculation type is the intuitive way of calculating who owes who what amount of money.")
                    print("Simplify type of expense calculation reduce the amount of needed transfers between users, but can be unintuitive.")
                    print("Example: A owes B 5$ and B owes C 5$. Simplify type of expense calculation reduce trasfers number from 2 to 1 - A owes C 5$.")
                    if input() == "exit":
                        QuitApp()
                case "exit":
                    QuitApp()
                case _:
                    print("Wrong input. Try again")
    def ChangeCurrency(self):
        if self.IsSettled():
            self.SelectCurrency()
            print("Currency changed to {}".format(self.currency))
            if input() == "exit":
                QuitApp()
        else:
            print("Group members are not settled!")
            print("Changing currency will convert existing debts to new currency (it won't affect currency of expenses in history)")
            print("Type \"1\" to continue or anything else to cancel this action")
            inp = input()
            if inp == "1":
                self.SelectCurrency()
                print("Currency changed to {}".format(self.currency))
                if input() == "exit":
                    QuitApp()
            elif inp == "exit":
                QuitApp()
            else:
                return
    def ShowTotalSpendings(self):
        if len(self.list_expenses) == 0:
            print("There are no expenses")
            if input() == "exit":
                QuitApp()
            return
        print("Total spendings:")
        for currency, value in sorted(self.total.items(), key = lambda item: item[1]):
            print(value, currency)
        if input() == "exit":
            QuitApp()
    def ShowExpensesHistory(self):
        if len(self.list_expenses) == 0:
            print("There are no expenses")
            if input() == "exit":
                QuitApp()
            return
        while True:
            print("\n----------------------------------------------------------------")
            print("Type number to see more information about particular expense or \"0\" to go back to group menu")
            for i in range(len(self.list_expenses)-1, -1, -1):
                expense = self.list_expenses[i]
                print("({0}) \"{1}\" - {2}{3} - {4}".format(len(self.list_expenses)-i, expense.name, expense.value, expense.currency, expense.category))
            print("----------------------------------------------------------------")
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(self.list_expenses):
                    self.list_expenses[len(self.list_expenses)-inp].ShowExpense()
                elif inp == 0:
                    return
                else:
                    print("Wrong input. Try again")
            except ValueError:
                if inp == "exit":
                    QuitApp()
                print("Wrong input. Try again")
    def ShowBalanceAll(self):
        if len(self.members) == 0:
            print("There are no members in this group")
            if input() == "exit":
                QuitApp()
            return
        print("\n----------------------------------------------------------------")
        for mem in self.members:
            self.ShowBalanceMember(mem)
        print("----------------------------------------------------------------")
        if input() == "exit":
            QuitApp()
    def ShowMembers(self):
        if len(self.members) == 0:
            print("There are no members in this group")
            if input() == "exit":
                QuitApp()
            return
        for member in self.members:
            print("{0} {1}".format(member.name, member.surname))
        if input() == "exit":
            QuitApp
    def AddMemberMenu(self):
        while True:
            print("\n----------------------------------------------------------------")
            print("Choose existing user or press enter add new user")
            list_not_in_group = []
            for user in list_users:
                if not (user in list(self.members)):
                    list_not_in_group.append(user)
            for i in range(len(list_not_in_group)):
                user = list_not_in_group[i]
                print("({0}) {1} {2}".format(i+1, user.name, user.surname))
            print("(0) Return to group menu")
            print("----------------------------------------------------------------")
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(list_not_in_group):
                    self.AddMember(list_not_in_group[inp-1])
                    print("Added {} {} to group".format(list_not_in_group[i-1].name, list_not_in_group[i-1].surname))
                    if input() == "exit":
                        QuitApp()
                    return
                elif inp == 0:
                    return
                else:
                    print("Wrong input. Try again")
            except ValueError:
                if inp == "":
                    if AddUser():
                        self.AddMember(list_users[-1])
                        print("Added new user {} {} to group".format(list_users[-1].name, list_users[-1].surname))
                        if input() == "exit":
                            QuitApp()
                        return
                elif inp == "exit":
                    QuitApp()
                else:
                    print("Wrong input. Try again")
    def SettleUpMenu(self):
        if len(self.members) == 0:
            print("There are no members in this group")
            if input() == "exit":
                QuitApp()
            return
        while True:
            print("\n----------------------------------------------------------------")
            print("Type number of member to see detailed info and settle up his/her expense(s) or \"0\" to return to group menu")
            for i in range(len(self.members)):
                member = list(self.members)[i]
                print("({}) {} {} - Balance: {}{}".format(i+1, member.name, member.surname, self.members[member], self.currency))
            print("----------------------------------------------------------------")
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(self.members):
                    member = list(self.members)[inp-1]
                    self.ShowBalanceMember(member)                 
                    print(("Type \"1\" to settle up this member, \"2\" to select another member or \"0\" to go back to group menu"))
                    inp1 = input()
                    if inp1 == "0":
                        return
                    elif inp1 == "1":
                        self.SettleUp(member)
                    elif inp1 == "2":
                        continue
                    elif inp1 == "exit":
                        QuitApp()
                    else:
                        print("Wrong input. Try again.")
                elif inp == 0:
                    return
                else:
                    print("Wrong input. Try again.")
            except ValueError:
                if inp == "exit":
                    QuitApp()
                print("Wrong input. Try again.")
    def ShowBalanceMember(self, member):
        if self.calculation_type == "simplify":
            self.CalculateSimplifyMatrix()
            value = round(self.members[member],2)
            if value == 0:
                print("{} {} is settled".format(member.name, member.surname))
            elif value < 0:
                print("{} {} owes {}{}".format(member.name, member.surname, -value, self.currency))
                self.CalculateSimplifyBalance(member)
            else:
                print("{} {} is owed {}{}".format(member.name, member.surname, value, self.currency))
                self.CalculateSimplifyBalance(member)
        else:
            balance_positive = 0
            balance_negative = 0
            for value in self.expense_matrix[list(self.members).index(member)]:
                value = round(value,2)
                if value > 0:
                    balance_positive += value
                else:
                    balance_negative -= value
            if balance_positive == 0 and balance_negative == 0:
                print("{} {} is settled".format(member.name, member.surname))
            elif balance_positive == 0:
                print("{} {} owes {}{}".format(member.name, member.surname, balance_negative, self.currency))
                self.CalculateNormalBalance(member)
            elif balance_negative == 0:
                print("{} {} is owed {}{}".format(member.name, member.surname, balance_positive, self.currency))
                self.CalculateNormalBalance(member)
            else:
                print("{} {} owes {}{} and is owed {}{}".format(member.name, member.surname, balance_negative, self.currency, balance_positive, self.currency))
                self.CalculateNormalBalance(member)
        print("")
    def CalculateNormalBalance(self, member):
        index = list(self.members).index(member)
        for i in range(len(self.expense_matrix)):
            value = self.expense_matrix[index][i]
            member2 = list(self.members)[i]
            if value > 0:
                print("{} {} owes {}{} to {} {}".format(member2.name, member2.surname, value, self.currency, member.name, member.surname))
        for i in range(len(self.expense_matrix)):
            value = self.expense_matrix[index][i]
            member2 = list(self.members)[i]
            if value < 0:
                print("{} {} owes {}{} to {} {}".format(member.name, member.surname, -value, self.currency, member2.name, member2.surname))
    def CalculateSimplifyMatrix(self):
        members_copy = self.members.copy()
        self.expense_simplify_matrix = []
        for i in range(len(self.expense_matrix)):
            self.expense_simplify_matrix.append([])
            for _ in range(len(self.expense_matrix)):
                self.expense_simplify_matrix[i].append(0)
        while not all(num == 0 for num in list(members_copy.values())):
            list_values = list(members_copy.values())
            max_value = max(list_values)
            min_value = min(list_values)
            index_max = list_values.index(max_value)
            index_min = list_values.index(min_value)
            if max_value >= abs(min_value):
                diff = abs(min_value)
            else:
                diff = abs(max_value)
            self.expense_simplify_matrix[index_max][index_min] += diff
            self.expense_simplify_matrix[index_min][index_max] -= diff
            members_copy[list(members_copy)[index_max]] -= diff
            members_copy[list(members_copy)[index_min]] += diff
    def CalculateSimplifyBalance(self, member):
        index = list(self.members).index(member)
        for i in range(len(self.expense_simplify_matrix)):
            value = round(self.expense_simplify_matrix[index][i],2)
            member2 = list(self.members)[i]
            if value > 0:
                print("{} {} owes {}{} to {} {}".format(member2.name, member2.surname, value, self.currency, member.name, member.surname))
            elif value < 0:
                print("{} {} owes {}{} to {} {}".format(member.name, member.surname, -value, self.currency, member2.name, member2.surname))
    def SettleUp(self, member):
        while True:
            if self.calculation_type == "normal":
                matrix = self.expense_matrix
                balance_positive = 0
                balance_negative = 0
                for value in self.expense_matrix[list(self.members).index(member)]:
                    if value > 0:
                        balance_positive += value
                    else:
                        balance_negative -= value
                if balance_positive == 0 and balance_negative == 0:
                    print("{} {} is settled".format(member.name, member.surname))
                    if input() == "exit":
                        QuitApp()
                    return
            else:
                matrix = self.expense_simplify_matrix
                if self.members[member] == 0:
                    print("{} {} is settled".format(member.name, member.surname))
                    if input() == "exit":
                        QuitApp()
                    return
            print("Choose member to settle up with or \"0\" to cancel action")
            index = list(self.members.keys()).index(member)
            not_settled_dict = {}
            count = 1
            for i in range(len(matrix)):
                if matrix[index][i] == 0:
                    continue
                else:
                    member2 = list(self.members.keys())[i]
                    print("({}) {} {}".format(count, member2.name, member2.surname))
                    not_settled_dict[count] = member2
                    count += 1
            inp = input()
            try:
                inp = int(inp)
                if inp == 0:
                    return
                elif inp >= 1 and inp < count:
                    member2 = not_settled_dict[inp]
                    index2 = list(self.members.keys()).index(member2)
                    value = matrix[index][index2]
                    if value > 0:
                        payer = member2
                        members = {member:value}
                    else:
                        payer = member
                        members = {member2:-value}
                    self.AddExpense("Settlement", abs(value), self.currency, payer, members, "Settlement", "")         
                else:
                    print("Wrong input. Try again")
            except ValueError:
                if inp == "exit":
                    QuitApp()
                print("Wrong input. Try again")   
    def AddExpenseMenu(self):  
        if len(self.members) == 0:
            print("There are no members in group")
            if input() == "exit":
                QuitApp()
            return
        while True:
            print("\n----------------------------------------------------------------")
            print("Follow instructions or type \"0\" at any point to cancel adding expense")
            name = input("Name of expense: ")
            if name == "0":
                return
            elif name == "exit":
                QuitApp()
            category = self.SelectCategory()
            if category == "0":
                return
            elif category == "exit":
                QuitApp()
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
            if members == "0":
                return
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
                        print("Expense added successfully")
                        if input() == "exit":
                            QuitApp()
                        return
                    case "2":
                        break
                    case "exit":
                        QuitApp()
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
            except ValueError:
                if inp == "exit":
                    QuitApp()
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
            except ValueError:
                if value == "exit":
                    QuitApp()
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
            except ValueError:
                if inp == "exit":
                    QuitApp()
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
            except ValueError:
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
                elif inp == "exit":
                    QuitApp()
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
            except ValueError:
                if inp == "exit":
                    QuitApp()
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
        value_by_person = round(value/len(members),2)
        for mem in members:
            members[mem] = value_by_person
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
                        except ValueError:
                            if inp1 == "exit":
                                QuitApp()
                            print("Wrong input. Try again")
                elif inp == 0:
                    return "0"
                else:
                    print("Wrong input. Try again")
            except ValueError:
                if inp == "":
                    remaining = round(value - sum(members.values()),2)
                    if remaining == 0:
                        return members
                    else:
                        print("Remaining money to split")
                elif inp == "exit":
                    QuitApp()
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
                        except ValueError:
                            if inp1 == "exit":
                                QuitApp()
                            print("Wrong input. Try again")
                elif inp == 0:
                    return "0"
                else:
                    print("Wrong input. Try again")
            except ValueError:
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
                elif inp == "exit":
                    QuitApp()
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
                        except ValueError:
                            if inp1 == "exit":
                                QuitApp()
                            print("Wrong input. Try again")
                elif inp == 0:
                    return "0"
                else:
                    print("Wrong input. Try again")
            except ValueError:
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
                elif inp == "exit":
                    QuitApp()
                else:
                    print("Wrong input. Try again")
    def SelectCurrency(self):
        while True:
            print("\n----------------------------------------------------------------")
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
            print("----------------------------------------------------------------")
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
                        currency_tmp = input("Type currency: ")
                        if currency_tmp == "exit":
                            QuitApp()
                        self.currency = currency_tmp
                        return
                    case _:
                        print("Wrong input. Try again")
            except ValueError:
                if inp == "exit":
                    QuitApp()
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
        print("\n----------------------------------------------------------------")
        if self.category == "Settlement":
            print("\"{}\"".format(self.name))
            print("{} {} paid {} {} {}{}".format(self.payer.name, self.payer.surname, list(self.members.keys())[0].name, list(self.members.keys())[0].surname, self.value, self.currency))
        else:
            print("\"{0}\"   -   category: {1}".format(self.name, self.category))
            print("{0}{1}".format(self.value,self.currency))
            print("{0} {1} paid {2}{3}".format(self.payer.name, self.payer.surname, self.value, self.currency))
            for member in self.members:
                print("{0} {1} owes {2}{3}".format(member.name, member.surname, self.members[member], self.currency))
        print("----------------------------------------------------------------")
        if input() == "exit":
            QuitApp()
        return   
class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    def stop(self):
        self._timer.cancel()
        self.is_running = False

def ShowGroupsOptions():
    while True:
        print("\n----------------------------------------------------------------")
        print("(1) Show Existing Groups")
        print("(2) Add new group")
        print("(3) Delete existing group")
        print("(0) Return to main manu")
        print("----------------------------------------------------------------")
        inp = input()
        if inp == "1":
            ShowGroups()
        elif inp == "2":
            name = input("Name of group: ")
            if name == "exit":
                QuitApp()
            Group(name)
            print("Group \"{}\" created".format(name))
            if input() == "exit":
                QuitApp()
        elif inp == "3":
            DeleteGroup()
        elif inp == "0":
            return
        elif inp == "exit":
            QuitApp()
        else:
            print("Wrong input. Try again")

def ShowGroups():
    if len(list_groups) == 0:
        print("There are no existing groups.")
        if input() == "exit":
            QuitApp()
        return
    else:
        while True:
            print("\n----------------------------------------------------------------")
            for i in range(len(list_groups)):
                print("({}) {}".format(i+1, list_groups[i].name))
            print("(0) Return to groups menu")
            print("----------------------------------------------------------------")
            inp = input()
            try:
                inp = int(inp)
                if inp >= 1 and inp <= len(list_groups):
                    list_groups[inp-1].ShowGroupInfo()
                elif inp == 0:
                    return
                else:
                    print("Wrong input. Try again")
            except ValueError:
                if inp == "exit":
                    QuitApp()
                print("Wrong input. Try again.")

def DeleteGroup():
    if len(list_groups) == 0:
        print("No groups to delete")
        if input() == "exit":
            QuitApp()
        return
    while True:
        print("\n----------------------------------------------------------------")
        print("Choose group to delete (if group is not settled expenses will be deleted)")
        for i in range(len(list_groups)):
            group = list_groups[i]
            if group.IsSettled():
                print("({0}) {1}".format(i+1, group.name))
            else:
                print("({0}) {1} (group not settled)" .format(i+1, group.name))
        print("(0) Cancel action")
        print("----------------------------------------------------------------")
        inp = input()
        try:
            inp = int(inp)
            if inp >= 1 and inp <= len(list_groups):
                group = list_groups.pop(inp-1)
                for mem in group.members:
                    mem.groups.remove(group)
                print("Deleted group: \"{}\"".format(group.name))
                del group
                if input() == "exit":
                    QuitApp()
                return
            elif inp == 0:
                return
        except ValueError:
            if inp == "exit":
                QuitApp()
            print("Wrong input. Try again")

def ShowUsersOptions():
    while True:
        print("\n----------------------------------------------------------------")
        print("(1) See specific information about existing users")
        print("(2) Add new user")
        print("(3) Delete existing settled user")
        print("(0) Exit to main manu")
        print("----------------------------------------------------------------")
        inp = input()
        match inp:
            case "1":
                ShowUsers()
            case "2":
                AddUser()
                print("Added new user: {} {}".format(list_users[-1].name, list_users[-1].surname))
                if input() == "exit()":
                    QuitApp()
            case "3":
                DeleteUser()
            case "0":
                return
            case "exit":
                QuitApp()
            case _:
                print("Wrong input. Try again.")

def ShowUsers():
    print("\n----------------------------------------------------------------")
    for i in range(len(list_users)):
        user = list_users[i]
        print("({}) {} {}".format(i+1, user.name, user.surname))
    print("(0) Return to Users Menu")
    print("----------------------------------------------------------------")
    inp = input()
    try:
        inp = int(inp)
        if inp >= 1 and inp <= len(list_users):
            list_users[inp-1].ShowInfo()
        elif inp == 0:
            return
        else:
            print("Wrong input. Try again.")
    except ValueError:
        if inp == "exit":
            QuitApp()
        print("Wrong input. Try again.")

def AddUser():
    while True:
        print("To cancel whole action type \"0\" at any stage")
        name = input("Name: ")
        if name == "0":
            return False
        elif name == "exit":
            QuitApp()
        surname = input("Surname: ")
        if surname == "0":
            return False
        elif surname == "exit":
            QuitApp()
        username = input("Username: ")
        if username == "0":
            return False
        elif username == "exit":
            QuitApp()
        email = input("Email: ")
        if email == "0":
            return False
        elif email == "exit":
            QuitApp()
        print("Confirm data: {0} {1}, {2}, {3}".format(name, surname, username, email))
        while True:
            inp = input("Type \"1\" if you want to confirm data, \"2\" if you want to enter it again or \"0\" if you want to cancel whole action: ")
            if inp == "1":
                User(name, surname, username, email)
                return True
            elif inp == "2":
                break
            elif inp == "0":
                return False
            elif inp == "exit":
                QuitApp()
            else:
                print("Wrong input. Try again")
    
def DeleteUser():
    if len(list_users) == 0:
        print("No users to delete")
        if input() == "exit":
            QuitApp()
        return
    while True:
        settled_users = []
        for i in range(len(list_users)):
            user = list_users[i]
            if user.IsSettled():
                settled_users.append(user)
        if len(settled_users) == 0:
            print("No settled users")
            if input() == "exit":
                QuitApp()
            return
        print("\n----------------------------------------------------------------")
        print("Choose user to delete (showing only users settled in all groups): ")
        for i in range(len(settled_users)):
            user = settled_users[i]
            print("({0}) {1} {2}".format(i+1, user.name, user.surname))
        print("(0) Cancel action")
        print("----------------------------------------------------------------")
        inp = input()
        try:
            inp = int(inp)
            if inp >= 1 and inp <= len(settled_users):
                user = list_users.pop(list_users.index(settled_users[inp-1]))
                print("Deleted user: \"{0} {1}\"".format(user.name, user.surname))
                del user
                if input() == "exit":
                    QuitApp()
                return
            elif inp == 0:
                return
            else:
                print("Wrong input. Try again")
        except ValueError:
            if inp == "exit":
                QuitApp()
            print("Wrong input. Try again")

def SaveToFile():
    with open("data.pkl", "wb") as file:
        pickle.dump([list_users, list_groups], file)

def LoadFromFile():
    global list_users, list_groups
    with open("data.pkl", "rb") as file:
        data = pickle.load(file)
        list_users = data[0]
        list_groups = data[1]

def QuitApp():
    saving_cycle.stop()
    SaveToFile()
    exit()

list_groups = []
list_users = []

if os.path.isfile("data.pkl"):
    LoadFromFile()
saving_cycle = RepeatedTimer(5, SaveToFile)
print("----------------------------------------------------------------")
print("Type according numbers to select options.")
print("At any point type exit to quit app.")
print("Type anything to skip messages like this one.")
print("----------------------------------------------------------------")
if input() == "exit":
    QuitApp()
while True:
    print("\n----------------------------------------------------------------")
    print("(1) Show groups menu")
    print("(2) Show all users")
    print("(0) Quit app")
    print("----------------------------------------------------------------")
    inp = input()
    if inp == "1":
        ShowGroupsOptions()
    elif inp == "2":
        ShowUsersOptions()
    elif inp == "0":
        QuitApp()
    elif inp == "exit":
        QuitApp()
    else:
        print("Wrong input. Try again")