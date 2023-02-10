import os
import pandas as pd
import matplotlib.pyplot as plt

root_dir = './1_sim_for_iterations'

# 遍历根目录下的所有文件夹
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        # 找到后缀是.txt的文件
        if file.endswith('.txt'):
            file_path = os.path.join(subdir, file)
            # 读取txt文件中的两列数字
            df = pd.read_csv(file_path, delimiter='\t', header=None, usecols=[0, 1])
            # 绘制曲线
            df.plot(x=0, y=1)

#plt.show()
# 保存图片
plt.savefig('all_curves.png')
