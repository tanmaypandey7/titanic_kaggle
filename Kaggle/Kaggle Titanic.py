import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

train=pd.read_csv(r'~\Downloads\train.csv')
test=pd.read_csv(r'~\Downloads\test.csv')
sample=pd.read_csv(r'~\Downloads\gender_submission.csv')

# worked on train set here
train['Sex']=train['Sex'].map({'male':0,'female':1}).astype(int)
train_tar=train.drop(['PassengerId','Survived',"Name","Cabin","Ticket",'Fare'], axis=1)
train_tar['Embarked'] = train_tar['Embarked'].fillna('S')
train_tar['Embarked']=train_tar['Embarked'].map({'S':0,'Q':1,'C':2}).astype(int)

train_tar['Age']=train_tar['Age'].fillna('30')
train_pred=train['Survived']
train_tar['Age']=train_tar['Age'].astype(int)

train_tar.loc[train_tar['Age'] < 16, 'Age'] = 0
train_tar.loc[(train_tar['Age'] >= 16) & (train_tar['Age'] <= 32), 'Age'] = 1
train_tar.loc[(train_tar['Age'] > 32) & (train_tar['Age'] <= 48), 'Age'] = 2
train_tar.loc[(train_tar['Age'] > 48) & (train_tar['Age'] <= 64), 'Age'] = 3
train_tar.loc[(train_tar['Age'] > 64), 'Age'] = 3


'''train_tar.loc[train_tar['Fare'] < 8, 'Fare'] = 0
train_tar.loc[(train_tar['Fare'] >= 8) & (train_tar['Fare'] < 16), 'Fare'] = 1
train_tar.loc[(train_tar['Fare'] >= 16) & (train_tar['Fare'] <= 32), 'Fare'] = 2
train_tar.loc[(train_tar['Fare'] > 32)]  = 3'''

train_tar['Alone']=train_tar['Parch']+train_tar['SibSp']
train_tar.loc[train_tar['Alone']>0,'Alone']=1
train_tar.loc[train_tar['Alone']==0,'Alone']=0
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
'''train_tar['agexclass']=train_tar['Age']*train_tar['Pclass']'''
clf=SVC()
clf.fit(train_tar,train_pred)

# worked on test set here
test['Fare']=test['Fare'].fillna(test['Fare'].mean())
test['Sex']=test['Sex'].map({'male':0,'female':1}).astype(int)
test['Age']=test['Age'].fillna('30')
test_gg=test.drop(['PassengerId',"Name","Cabin","Ticket",'Fare'], axis=1)
test_gg['Embarked'] = test_gg['Embarked'].fillna('S')
test_gg['Embarked']=test_gg['Embarked'].map({'S':0,'Q':1,'C':2}).astype(int)
test_gg['Age']=test_gg['Age'].astype(int)

test_gg.loc[test_gg['Age'] < 16, 'Age'] = 0
test_gg.loc[(test_gg['Age'] >= 16) & (test_gg['Age'] <= 32), 'Age'] = 1
test_gg.loc[(test_gg['Age'] > 32) & (test_gg['Age'] <= 48), 'Age'] = 2
test_gg.loc[(test_gg['Age'] > 48) & (test_gg['Age'] <= 64), 'Age'] = 3
test_gg.loc[(test_gg['Age'] > 64), 'Age'] = 3

'''test_gg.loc[test_gg['Fare'] < 8, 'Fare'] = 0
test_gg.loc[(test_gg['Fare'] >= 8) & (test_gg['Fare'] < 16), 'Fare'] = 1
test_gg.loc[(test_gg['Fare'] >= 16) & (test_gg['Fare'] <= 32), 'Fare'] = 2
test_gg.loc[(test_gg['Fare'] > 32)]  = 3'''


test_gg['Alone']=test_gg['Parch']+test_gg['SibSp']
test_gg.loc[test_gg['Alone']>0,'Alone']=1
test_gg.loc[test_gg['Alone']==0,'Alone']=0

'''test_gg['agexclass']=test_gg['Age']*test_gg['Pclass']'''

pred=clf.predict(test_gg)
score=accuracy_score(pred,sample.iloc[:,1])
print(score)
col_names=['Survived']
#PREPARING FOR EXPORT TO EXCEL

pred_df=pd.DataFrame(pred,columns=col_names)
pred_df['PassengerId']=test['PassengerId']
columnsTitles=["PassengerId","Survived"]
pred_df=pred_df.reindex(columns=columnsTitles)


from pandas import ExcelWriter
writer= ExcelWriter('titanic_preds.xlsx',engine='xlsxwriter')
pred_df.to_excel(writer,sheet_name='sheet 1',index=False)
writer.save()

pred_df.to_csv('titan csv1.csv',index=False)
