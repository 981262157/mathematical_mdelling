#print()输出自带换行符，如果修改，加end
print(2,end="")

score=int(input("输入分数："))
if score>=90:
    print("优秀")
elif score>=80:
    print("良好")
elif score>=60:
    print("及格")
else:
    print("不及格")

username=input("请输入账号")
password=input("请输入密码")

correct_user = "python123"
correct_pwd = "123456"

if username==correct_user and password==correct_pwd:
    print("登录成功")
else:
    print("登录失败")


#循环
#for 变量 in 可迭代对象:
    #循环体代码（注意缩进）
for i in range(5):
    print(i)

count=1
while count<=5:
    print(count)
    count+=1


#range函数，生成一个不可变的证书序列（不是列表，是可迭代对象），
#核心原则是左闭右开
#参数传单值时，默认从 0 开始，到「结束值 - 1」结束，步长为 1。
for i in range(5):
    print(i)

#双参数时，从「起始值」开始，到「结束值 - 1」结束，步长为 1。
for i in range(1,6):
    print(i)

#三参数时，从「起始值」开始，每次增加 / 减少「步长」，直到接近
#但不超过「结束值」（也不能是结束值）。
print("步长为2：")
for i in range(1, 10, 2):
    print(i, end=" ")