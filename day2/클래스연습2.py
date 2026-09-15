# Developer클래스를 정의하면서
# id, name, skill 변수가 있고,
# printInfo() 메서드를가 있다.

class Developer:
    def __init__(self, id, name, skill):
        self.id = id
        self.name = name
        self.skill = skill

    def printInfo(self):
        print('ID: {0}, Name: {1}, Skill: {2}'.format(self.id, self.name, self.skill))

#인스턴스 생성
dev = Developer(1, "홍길동", "Python")
dev.printInfo()
