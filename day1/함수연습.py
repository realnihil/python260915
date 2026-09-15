# # 함수 연습
# # 1) 함수 정의

# def times(a, b):
#     return a*b

# # 2) 함수 호출

# result = times(3,4)
# print(result)

# # 전역변수
# x = 5
# def func(a):
#     # 지역변수
#     global x
#     if not x:
#         x = 10
#     return x+a

# # 전역 호출
# print(func(1))


# 전역변수
x = 5
def func(a=3, x=10):
    # 지역변수
    # x = 10
    return x+a

# 전역 호출
print(func(1, x))
print(func(2))
print(func([],2))