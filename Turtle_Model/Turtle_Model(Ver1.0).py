import vectors as vectors
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import  accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns



#데이터 불러오기
data = pd.read_csv("turtledata.csv")
col = list(map(str,data.columns))
x = data[col[:-1]]
y = data[col[-1]]

#Standard Scaler
scaler = StandardScaler()
scaler.fit(x)
X_scaled = scaler.transform(x)


# data split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=121)

# grid search을 통한 svm 파라미터 결정시 필요한 요소 설정
parameters = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000],
          'gamma': [0.0001, 0.001, 0.01, 1, 10, 100, 1000]}
model = SVC(kernel='rbf')
# grid search Part
grid = GridSearchCV(estimator=model, param_grid=parameters)
grid.fit(X_train, y_train)
print(grid)
# grid search 결과 출력
print(grid.best_score_)
print(grid.best_estimator_)
