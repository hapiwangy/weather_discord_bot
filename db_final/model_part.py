from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
# from sklearn.externals import joblib
import joblib

import pandas as pd

# 記得手動把X改掉(目前是補零)

df = pd.read_excel(r"training_data_set.xlsx")
datas = df[["時間","海平面氣壓","氣溫","風速"]]
labels = df["降水量"]
new_data = []
for x in range(1, len(datas)):
    new_data.append([datas["時間"][x],datas["海平面氣壓"][x],datas["氣溫"][x],datas["風速"][x]])
labels = labels[:-1]
new_label = []
for r in labels:
    if r == 'T':new_label.append(0.09)
    else:new_label.append(r)
labels, datas = new_label, new_data
X_train, X_test, Y_train, Y_test = train_test_split(datas ,labels, test_size=0.4)
print("引入並修改資料完成")
print("KNN模型進行中")
# knn的部分
knn = KNeighborsClassifier()
# knn.fit(X_train, Y_train)
knn.fit(datas, labels)
pred = knn.predict(X_test)
# 模型存檔
joblib.dump(knn, r'orig_knn.pkl')
# 若要使用的話
# model = joblib.load('knn.pkl')
# model.predict(data)
print(pred[:5])
print("KNN prediction point is:",accuracy_score(pred, Y_test))

# kmeans的部分

print("Decisiontree進行中")
# decisiontdctree
dct = DecisionTreeClassifier(criterion="entropy", max_depth=6, random_state=42)
dct.fit(X_train, Y_train)
pred = dct.predict(X_test)
# 模型存檔
joblib.dump(dct, r'orig_dct.pkl')
# 若要使用的話
# model = joblib.load('dct.pkl')
# model.predict(data)
print(pred[:5])
print("Decision_tree_prediction point is:",accuracy_score(pred, Y_test))
