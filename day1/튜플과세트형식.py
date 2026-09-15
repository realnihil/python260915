# tp = (100,200,300)
# print(len(tp))
# print(tp.count(300))
# print(tp.index(200))

# h = ('kim', '김유신')

# print('id: %s, name: %s' % h)

# # 여러개를  리턴
# def times(a, b):
#     c = a+b
#     d = a*b
#     return c, d

# # 호출
# result = times(3,4)
# print(result)

# # 형식변환
# a = list((1,2,3))
# a.append(4)
# print(a)
# b = set(a)
# print(b)

# # Set형식
# s1 = {1,2,3,3}
# s2 = {3,4,4,5}
# print(s1.union(s2))
# print(s1.intersection(s2))
# print(s1.difference(s2))

# Dict 형식

fruits = {'apple':10, 'kiwi':20}
fruits['banana'] = 50
print(fruits)

del fruits['kiwi']
print(fruits)
for item in fruits.items():
    print(item)

for i in fruits.values():
    print(i)