import numpy as np

def readCurve(input, c1, c2):
    assert (c1 != 0 and c2 != 0), "c1 and c2 cannot be 0"
    listLine = []
    with open(input, 'r') as f1:  # 意为file文件夹就相当于f1
        for line in f1:
            if line[0] != '#':
                listLine.append(line)
    col1 = []
    col2 = []
    for line in listLine:
        x = list(map(float, line.split()))
        # print(x)
        col1.append(x[c1 - 1])
        col2.append(x[c2 - 1])

    col1 = np.array(col1)
    col2 = np.array(col2)

    return col1, col2
