import os
import pandas as pd
import matplotlib.pyplot as plt

root_dir = './1_sim_for_iterations'

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
                df.plot(x=0, y=1)

#plt.show()
# 保存图片
plt.savefig('all_curves.png')
