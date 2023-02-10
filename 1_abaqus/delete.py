import os

target_dir = "./target/"

# 遍历所有文件和文件夹
for root, dirs, files in os.walk(target_dir):
    for filename in files:
        if not filename.endswith(".txt"):
            file_path = os.path.join(root, filename)
            os.remove(file_path)
