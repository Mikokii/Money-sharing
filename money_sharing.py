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
    def AddMember(self, member):
        self.members[member] = 0
        member.groups.append(self)
        self.matrix.append([0]*len(self.members))
        for i in range(len(self.members)-1):
            self.matrix[i].append(0)
        

        

class Expense:
    def __init__(self, value):
        self.value = value

list_groups = []



group1 = Group("test")
print(group1.matrix)
per1 = User("Mikołaj", "Kiszka", "Mikokii", "miko123@gmail.com")
group1.AddMember(per1)
print(group1.matrix)
per2 = User("Mikołaj", "Kiszka", "Mikokii", "miko123@gmail.com")
group1.AddMember(per2)
print(group1.matrix)
per3 = User("Mikołaj", "Kiszka", "Mikokii", "miko123@gmail.com")
group1.AddMember(per3)
print(group1.matrix)
    