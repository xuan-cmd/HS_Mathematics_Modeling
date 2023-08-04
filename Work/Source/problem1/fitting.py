import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
path = '附件2.xlsx'
data = pd.DataFrame(pd.read_excel(path))#读取数据,设置None可以生成一个字典，字典中的key值即为sheet名字，此时不用使用DataFram，会报错
#print(data.index)#获取行的索引名称
#print(data.columns)#获取列的索引名称
#print(data['400nm'])#获取列名为姓名这一列的内容
##print(data.loc[0])#获取行名为0这一行的内容

wavelength = [400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700]


##参数
red_factor = []
yellow_factor = []
blue_factor = []
##拟合优度
red_rr = []
yellow_rr = []
blue_rr = []


# #################################拟合优度R^2的计算######################################
def __sst(y_no_fitting):
    """
    计算SST(total sum of squares) 总平方和
    :param y_no_predicted: List[int] or array[int] 待拟合的y
    :return: 总平方和SST
    """
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_no_fitting]
    sst = sum(s_list)
    return sst


def __ssr(y_fitting, y_no_fitting):
    """
    计算SSR(regression sum of squares) 回归平方和
    :param y_fitting: List[int] or array[int]  拟合好的y值
    :param y_no_fitting: List[int] or array[int] 待拟合y值
    :return: 回归平方和SSR
    """
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_fitting]
    ssr = sum(s_list)
    return ssr


def __sse(y_fitting, y_no_fitting):
    """
    计算SSE(error sum of squares) 残差平方和
    :param y_fitting: List[int] or array[int] 拟合好的y值
    :param y_no_fitting: List[int] or array[int] 待拟合y值
    :return: 残差平方和SSE
    """
    s_list = [(y_fitting[i] - y_no_fitting[i])**2 for i in range(len(y_fitting))]
    sse = sum(s_list)
    return sse


def goodness_of_fit(y_fitting, y_no_fitting):
    """
    计算拟合优度R^2
    :param y_fitting: List[int] or array[int] 拟合好的y值
    :param y_no_fitting: List[int] or array[int] 待拟合y值
    :return: 拟合优度R^2
    """
    SSR = __ssr(y_fitting, y_no_fitting)
    SST = __sst(y_no_fitting)
    rr = SSR /SST
    return rr

def fitting(m,n):
    fig = plt.figure()
    for i in range(16):

        ##提取出浓度和KS值
        consistency = np.array(data['浓度（%）'][m:n])
        consistency = consistency.tolist()
        KS = np.array(data[(str(wavelength[i])+"nm")][m:n])
        KS = KS.tolist()

        ##使用t次多项式拟合
        z1 = np.polyfit(consistency, KS, 1)
        print("参数系数",z1)
        f1 = np.poly1d(z1)
        y_pre = f1(consistency)

        plt.subplot(4, 4, i+1)
        fig.tight_layout(h_pad=0.3)
        plt.plot(consistency,KS,'.')
        plt.plot(consistency, y_pre)
        plt.xlabel('浓度',fontsize=7)
        plt.ylabel('K/S',fontsize=7)
        plt.tick_params(pad=0.03)
        plt.title(str(wavelength[i])+"nm",fontsize=7)
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        rr = goodness_of_fit(y_pre, KS)
        print("拟合优度为:", rr)

        print("KS:",KS)

        if(m==1):
            red_factor.append(z1)
            red_rr.append(rr)
        elif(m==9):
            yellow_factor.append(z1)
            yellow_rr.append(rr)
        else :
            blue_factor.append(z1)
            blue_rr.append(rr)

    if (m == 1):
        fig.suptitle('红着色剂在不同波长下K/S与浓度的关系')
    elif (m == 9):
        fig.suptitle('黄着色剂在不同波长下K/S与浓度的关系')
    else:
        fig.suptitle('蓝着色剂在不同波长下K/S与浓度的关系')
    plt.subplots_adjust(top=0.85)
    plt.show()
    plt.close()

def main():
    fitting(1,9) ##红着色剂
    fitting(9, 17)  ##黄着色剂
    fitting(17, 25)  ##蓝着色剂

main()
print("red_factor:",red_factor)
print("red_rr:",red_rr)
print("yellow_factor:",yellow_factor)
print("yellow_rr:",yellow_rr)
print("blue_factor:",blue_factor)
print("blue_rr:",blue_rr)


