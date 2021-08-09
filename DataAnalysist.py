import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

path = "D:/Project/MachineLearning/NhanDienLogo/datasets/Logo/data_class/"

names = ['abbott', 'acecook', 'vinamilk', 'viettel', 'bosch', 'cgv', 'thegioididong',
         'vnpt', 'tiki', 'mobifone', 'lg', 'fpt', 'grab', 'highland_coffee']

dataf = []


for i in range(14):
    file = os.listdir(path + names[i] + "/")
    dataf.append(len(file))

#nf = np.reshape(np.array(dataf), (1, len(names)))



df = pd.DataFrame({
      'Dữ liệu': dataf,
      'Trung bình': [np.mean(np.array(dataf)) for i in range(len(dataf))],
      'Độ lệch chuẩn': [np.std(np.array(dataf)) for i in range(len(dataf))]})

df.plot()
plt.show()


print(np.mean(np.array(dataf)), np.std(np.array(dataf)), np.var(np.array(dataf)))

# print(sum(dataf))
#
# plt.bar(names, dataf, width=0.8)
# plt.xticks(rotation=45)
# plt.xlabel('Số lớp', fontsize=12)
# plt.ylabel('Số phần tử', fontsize=12)
# plt.title('Số phần tử mỗi lớp')
#
# for index, data in enumerate(dataf):
#     plt.text(x=index-0.4, y=data+8, s=f"{data}", fontdict=dict(fontsize=10))
#
# plt.tight_layout()
#
# plt.show()

