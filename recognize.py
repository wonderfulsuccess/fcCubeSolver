import sklearn

# from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.gaussian_process import GaussianProcess
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

import numpy as np
import pandas as pd
import pickle

class Cubereg:
    def __init__(self):

        train_amount = 10000

        df = pd.read_csv('data.csv')
        
        x_data = []
        for i in range(0,train_amount):
            x_data.append([df.iat[i,0],df.iat[i,1],df.iat[i,2]])
        
        x=np.array(x_data)
        
        y_data = []
        for i in range(0,train_amount):
            y_data.append(df.iat[i,3])
        
        y=np.array(y_data)
        
        #最邻近分类器
        self.clf = KNeighborsClassifier()
        #训练分类器
        print("开始训练模型 训练数据量为:", format(train_amount))
        self.clf.fit(x,y)
        print("训练结束")
        
        #整理测试数据
        p_x_data = []
        for i in range(train_amount, 12000):
            p_x_data.append([df.iat[i,0],df.iat[i,1],df.iat[i,2]])
        self.p_x=np.array(p_x_data)
        
        p_y_data = []
        for i in range(train_amount, 12000):
            p_y_data.append(df.iat[i,3])
        self.p_y=np.array(p_y_data)
        # 是否需要保存模型
        # self.save_model()

    def predict(self, data):
        return(self.clf.predict(np.array(data)))

    def test_score(self):
        print(self.clf.score(self.p_x,self.p_y))


    def save_model(self):
        with open('color_detect.pickle', 'wb') as handle:
            pickle.dump(self.clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
