value = 5
while value > 0:
    print(value)
    value -= 1


# range() 함수
for i in range(5):
    print(i)

print(list(range(10)))
print(list(range(1, 32)))
print(list(range(2000, 2027)))

#리스트함축(압축)
lst = list(range(1, 11))
print([i**2 for i in lst if i>5])
tp = ('apple', 'kiwi')
print([len(i) for i in tp])

#람다함수 활용
lst1 = [10, 25, 30]
itemL = filter(None, lst1)
for k in itemL:
    print(k)

def getBigger(x):
    return x > 20

print('필터링 함수 사용')
itemL2 = filter(getBigger, lst1)
for ii in itemL2:
    print(ii)

lst1 = [10, 25, 30]
print('람다 함수 사용')
for ii in filter(lambda x:x>20, lst1):
    print(ii)