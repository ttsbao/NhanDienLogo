import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, KFold

nc = 14

names = ['abbott', 'acecook', 'vinamilk', 'viettel', 'bosch', 'cgv', 'thegioididong',
         'vnpt', 'tiki', 'mobifone', 'lg', 'fpt', 'grab', 'highland_coffee']

path = "D:/Project/MachineLearning/NhanDienLogo/datasets/Logo/"
dir = path + "data_class/"

k = 5

class Logo:
    def __init__(self, name):
        file = np.array(os.listdir(dir+name+"/"), dtype=object)
        for i in range(file.shape[0]):
            file[i] = "./images/"+file[i]
        train = np.reshape(file, (file.shape[0], 1))
        test = np.ones(file.shape[0])
        kf = KFold(n_splits=k, random_state=None, shuffle=False)
        self.train, self.val, self.test, i = [None]*k, [None]*k, [None]*k, 0
        for train_index, test_index in kf.split(train):
            X_train, self.test[i] = train[train_index], train[test_index]
            y_train, _ = test[train_index], test[test_index]
            self.train[i], self.val[i], _, _ = train_test_split(
                X_train, y_train, test_size=0.1, random_state=None, shuffle=False)
            #print(self.train[i].shape, self.val[i].shape, self.test[i].shape)
            i += 1

    def get_data(self):
        return self.train, self.val, self.test

class Preprocessing_Data:
    def __init__(self):
        abbott = Logo(names[0])
        self.TRAIN, self.VAL, self.TEST = abbott.get_data()
        for i in range(1, len(names)):
            logo = Logo(names[i])
            train, val, test = logo.get_data()
            for j in range(k):
                self.TRAIN[j] = np.vstack((self.TRAIN[j], train[j]))
                self.VAL[j] = np.vstack((self.VAL[j], val[j]))
                self.TEST[j] = np.vstack((self.TEST[j], test[j]))


    def export_text(self):
        for i in range(k):
            np.savetxt(path + "train_"+str(i) + ".txt", self.TRAIN[i], fmt="%s")
            np.savetxt(path + "val_" + str(i) + ".txt", self.VAL[i], fmt="%s")
            np.savetxt(path + "test_" + str(i) + ".txt", self.TEST[i], fmt="%s")




pdd = Preprocessing_Data()
pdd.export_text()

