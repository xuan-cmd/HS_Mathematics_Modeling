
import scipy
import openpyxl


#首先计算目标样的几个色度值，在附件三中

workbook = openpyxl.load_workbook('../赛题/附件3.xlsx')

worksheet = workbook.active


'''============计算三刺激值XYZ==========='''
k = 0.1

# 计算离散点的积分


