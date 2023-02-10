import os
import shutil

# 源路径
src_path = "./1_sim_for_iterations/"
# 目标路径
dst_path = "./target/"

# 遍历源路径下的所有文件和文件夹
for item in os.listdir(src_path):
    s = os.path.join(src_path, item)
    d = os.path.join(dst_path, item)
    # 如果是文件夹，则复制到目标路径下
    if os.path.isdir(s):
        shutil.copytree(s, d, False, None)
    # 如果是以.txt结尾的文件，则复制到目标路径下
    elif s.endswith(".txt"):
        shutil.copy2(s, d)
