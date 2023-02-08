#
import pandas as pd

def get_value(csv_file,item_name,item_length):
    data = pd.read_csv(csv_file)
    for i in data.values:
        #print(i)
        if i[0] == item_name:
            return i[1:item_length+1]