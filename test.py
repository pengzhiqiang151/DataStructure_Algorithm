import pandas as pd
import sklearn.datasets as sd
import sklearn.model_selection as sm
import sklearn.linear_model as lm

iris = sd.load_iris()
print(iris.keys())

df = pd.DataFrame(iris['data'], columns=iris['feature_names'])
df['target'] = iris['target']

# 1类别和2类别分类
sub_data = df[df['target'] != 0]

x = df.iloc[:, :-1]
y = df.iloc[:, -1]

train_x, test_x, train_y, test_y = sm.train_test_split(x, y, test_size=0.1, random_state=7)

model = lm.LogisticRegression(solver='liblinear')
model.fit(train_x, train_y)

y_pred = model.predict(test_x)
print(y_pred)
print(test_y.values)
