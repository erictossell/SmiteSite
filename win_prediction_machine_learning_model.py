import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
smite = pd.read_excel("NewTrainingSet.xlsx", sheet_name="Sheet1")

print(smite.shape)
print(smite.count())

X = smite[["Team 1 Hours", "Team 1 Wins", "Team 1 KDA", "Team 2 Hours", "Team 2 Wins", "Team 2 KDA"]]
y = smite["Result"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=0)



classifier = LogisticRegression(solver='lbfgs')
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)
score = classifier.score(X,y)
print(score)
print(len(y_pred))
for x in y_pred:
    print(x)
