# import os
# import shutil

# # 源路径
# src_path = "./1_sim_for_iterations/"
# # 目标路径
# dst_path = "./target/"

# # 遍历源路径下的所有文件和文件夹
# for item in os.listdir(src_path):
#     s = os.path.join(src_path, item)
#     d = os.path.join(dst_path, item)
#     # 如果是文件夹，则复制到目标路径下
#     if os.path.isdir(s):
#         shutil.copytree(s, d, False, None)
#     # 如果是以.txt结尾的文件，则复制到目标路径下
#     elif s.endswith(".txt"):
#         shutil.copy2(s, d)


# import os
# import shutil

# def copy_folders_and_files(src_folder, dst_folder):
#     # 复制文件夹
#     folders = [f for f in os.listdir(src_folder) if os.path.isdir(os.path.join(src_folder, f))]
#     for folder in folders:
#         shutil.copytree(os.path.join(src_folder, folder), os.path.join(dst_folder, folder))

#     # 复制文件
#     for root, dirs, files in os.walk(src_folder):
#         for file in files:
#             if file.endswith('.txt'):
#                 src_file = os.path.join(root, file)
#                 dst_file = os.path.join(dst_folder, root[len(src_folder)+1:], file)
#                 shutil.copy2(src_file, dst_file)

# # 示例：将src_folder下的文件夹和文件复制到dst_folder
# src_folder = "./1_sim_for_iterations/"
# dst_folder = "./target/"
# copy_folders_and_files(src_folder, dst_folder)

import os
import shutil

src_dir = "./1_sim_for_iterations"
dst_dir = "./target/"

# 列出所有文件和文件夹
for item in os.listdir(src_dir):
    s = os.path.join(src_dir, item)
    d = os.path.join(dst_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
        # 搜索文件夹内的文件
        for filename in os.listdir(s):
            if filename.endswith(".txt"):
                src_file = os.path.join(s, filename)
                dst_file = os.path.join(d, filename)
                shutil.copy2(src_file, dst_file)
