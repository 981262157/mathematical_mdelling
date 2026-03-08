import numpy as np

#nunpy库都以元组为标准

#一维数组
a=np.array([1,2,3])    #要求是同一数据类型
print(a)

#二维数组
b=np.array([[1,2],[3,4]])

#快速创建数组
np.zeros((2,3))    #全零矩阵，2行3列,注意要传入的变量是元组
np.ones((3,3))     #全1矩阵
np.eye(3)          #单位矩阵
np.arange(0,10,2)  #np.array 0,2,4,6,8
np.linspace(0,1,5) #0到1之间均匀的五个数

#数组属性
a.shape    #几行几列
a.ndim     #维度
a.dtype    #数据类型
a.size     #总元素个数

#矩阵乘法
c=np.array([[1],[2],[3]])
print(c)
d=a@c
e=a.dot(c)
print(d)
