# Person은 사람 한 명을 만들기 위한 기본 설계도입니다.
class Person:
    # 사람을 만들 때 번호와 이름을 받습니다.
    def __init__(self, id, name):
        # 받은 번호를 사람의 번호로 보관합니다.
        self.id = id

        # 받은 이름을 사람의 이름으로 보관합니다.
        self.name = name

    # 사람의 번호와 이름을 화면에 보여주는 기능입니다.
    def printInfo(self):
        print(f"ID: {self.id}, 이름: {self.name}")


# Manager는 Person을 물려받은 관리자 설계도입니다.
# 부모인 Person의 번호와 이름 기능도 사용할 수 있습니다.
class Manager(Person):
    # 관리자를 만들 때 번호, 이름, 직책을 받습니다.
    def __init__(self, id, name, title):
        # 부모 설계도에게 번호와 이름을 저장해 달라고 합니다.
        super().__init__(id, name)

        # 관리자의 직책을 보관합니다.
        self.title = title

    # 관리자의 번호, 이름, 직책을 화면에 보여줍니다.
    def printInfo(self):
        print(f"ID: {self.id}, 이름: {self.name}, 직책: {self.title}")


# Employee는 Person을 물려받은 직원 설계도입니다.
# 직원도 사람이라서 번호와 이름을 가지고 있습니다.
class Employee(Person):
    # 직원을 만들 때 번호, 이름, 잘하는 기술을 받습니다.
    def __init__(self, id, name, skill):
        # 부모 설계도에게 번호와 이름을 저장해 달라고 합니다.
        super().__init__(id, name)

        # 직원이 잘하는 기술을 보관합니다.
        self.skill = skill

    # 직원의 번호, 이름, 기술을 화면에 보여줍니다.
    def printInfo(self):
        print(f"ID: {self.id}, 이름: {self.name}, 기술: {self.skill}")


# 사람들을 한 명씩 넣어 둘 수 있는 큰 상자를 만듭니다.
people = [
    # 관리자 5명을 만듭니다.
    Manager(1, "김민수", "개발팀장"),
    Manager(2, "이서연", "기획팀장"),
    Manager(3, "박지훈", "인사팀장"),
    Manager(4, "최유진", "영업팀장"),
    Manager(5, "정현우", "디자인팀장"),

    # 직원 5명을 만듭니다.
    Employee(6, "강하늘", "Python"),
    Employee(7, "윤서준", "Java"),
    Employee(8, "한지민", "JavaScript"),
    Employee(9, "오수빈", "SQL"),
    Employee(10, "배도윤", "C++"),
]

# 상자에서 사람을 한 명씩 꺼내서 반복합니다.
for person in people:
    # 꺼낸 사람에게 자신의 정보를 말해 달라고 합니다.
    person.printInfo()