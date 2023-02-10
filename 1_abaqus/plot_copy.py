import os
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_excel('../2_exp_data/Exp_data/HR3C BM/拉伸曲线/HR3C BM工程应力-应变曲线.xlsx', skiprows=1)
x = data['Column_1']
y = data['Column_2']

x = x * 0.01




root_dir = './1_sim_for_iterations'

# 创建图形
fig = plt.figure()

# 遍历根目录下的第一级文件夹
for dir in os.listdir(root_dir):
    subdir = os.path.join(root_dir, dir)
    if os.path.isdir(subdir):
        for file in os.listdir(subdir):
            # 找到后缀是.txt的文件
            if file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                # 读取txt文件中的两列数字，排除以#开始的行
                skiprows = [i for i, line in enumerate(open(file_path, 'r')) if line.startswith('#')]
                df = pd.read_csv(file_path, delimiter=' ', header=None, usecols=[0, 1], skiprows=skiprows)
                # 绘制曲线
                df.plot(x=0, y=1, ax=fig.gca())

plt.plot(x,y)
#plt.show()
# 保存图片
plt.savefig('all_curves.png')
