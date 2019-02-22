"""
This file
"""
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.model_selection import StratifiedShuffleSplit

# Load data
targetNames = [0, 1]
dataFrame = pandas.read_csv("../data_files/data.csv", sep='|')

# Assign data and target to X, y variables to be used later on
npArray = dataFrame.values

# Obtain X excluding the 2 first column
idx_OUT_columns = [0]
idx_IN_columns = [i for i in range(np.shape(npArray)[1]) if i not in idx_OUT_columns]
X = npArray[:,idx_IN_columns]

# Obtain y
Y = dataFrame['diagnosis'].values

validation_size = 0.20
seed = 7
scoring = 'accuracy'
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)

# Compare Algorithms
#fig = plt.figure()
#fig.suptitle('Algorithm Comparison')
#ax = fig.add_subplot(111)
#plt.boxplot(results)
#ax.set_xticklabels(names)
#plt.show()

LDA = LinearDiscriminantAnalysis()
LDA.fit(X_train, Y_train)
predictions = LDA.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
## The model is saved in a .pkl file
joblib.dump(LDA, '../models/lda_model.pkl')

LR = LogisticRegression()
LR.fit(X_train, Y_train)
predictions = LR.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
## The model is saved in a .pkl file
joblib.dump(LR, '../models/lr_model.pkl')

KNN = KNeighborsClassifier()
KNN.fit(X_train, Y_train)
predictions = KNN.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
## The model is saved in a .pkl file
joblib.dump(KNN, '../models/knn_model.pkl')

CART = DecisionTreeClassifier()
CART.fit(X_train, Y_train)
predictions = CART.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
## The model is saved in a .pkl file
joblib.dump(CART, '../models/cart_model.pkl')

NB = GaussianNB()
NB.fit(X_train, Y_train)
predictions = NB.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
## The model is saved in a .pkl file
joblib.dump(NB, '../models/nb_model.pkl')

SVC = SVC()
SVC.fit(X_train, Y_train)
predictions = SVC.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
## The model is saved in a .pkl file
joblib.dump(SVC, '../models/svc_model.pkl')

myStratifiedShuffleSplit = StratifiedShuffleSplit(1, 0.3, random_state = 42)

for train_index, test_index in myStratifiedShuffleSplit.split(X, Y):
    XTrain = X[train_index,:]
    XTest = X[test_index,:]
    yTrain = Y[train_index]
    yTest = Y[test_index]

# Sizes of each data split
print("Number of samples and dimensions for XTrain: " +str(XTrain.shape))
print("Number of labels for yTrain: " +str(yTrain.shape))
print("Number of samples and dimensions for XTest: " +str(XTest.shape))
print("Number of labels for yTest: " +str(yTest.shape))


##We use DecisionTree method for training
clf = DecisionTreeClassifier(criterion='gini', max_depth=3, min_samples_leaf=1)
clf.fit(XTrain, yTrain)
clf.score(XTest,yTest)

## The model is saved in a .pkl file
joblib.dump(clf, '../models/dtc_model.pkl')