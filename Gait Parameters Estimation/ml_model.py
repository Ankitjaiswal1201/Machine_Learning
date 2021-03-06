
#matplotlib inline
#config InlineBackend.figure_format = 'retina'
from __future__ import print_function
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 200)


from datetime import datetime
from matplotlib.colors import ListedColormap
#from sklearn.datasets import make_classification, make_moons, make_circles
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

nan = float('nan')


dataset = pd.read_excel('JOE_Test4.xlsx')

dataset.loc[dataset['Normal1_T1']== 'Normal.1','Normal1_T1']= 1
dataset.loc[dataset['Normal2_T1']== 'Normal.2','Normal2_T1']= 2
dataset.loc[dataset['RW7_T1']== 'RW7','RW7_T1']= 3
dataset.loc[dataset['Woerter_T1']== 'Woerter','Woerter_T1']= 4
dataset.loc[dataset['Normal1_T2']== 'Normal.1','Normal1_T2']= 5
dataset.loc[dataset['Normal2_T2']== 'Normal.2','Normal2_T2']= 6
dataset.loc[dataset['RW7_T2']== 'RW7','RW7_T2']= 7
dataset.loc[dataset['Woerter_T2']== 'Woerter','Woerter_T2']= 8

dataset2 = dataset.loc[:, ['Normal1_T1','mean_steplength_RW7_T1',
                            'mean_steptime_RW7_T1','mean_frequency_RW7_T1','mean_speed_RW7_T1',
                            'mean_stepwidth_RW7_T1','MOCA_CERAD_korr_T1']]

dataset2[['mean_steplength_RG1-RW7_T1','mean_steptime_RG1-RW7_T1',
          'mean_frequency_RG1-RW7_T1','mean_speed_RG1-RW7_T1', 
          'mean_stepwidth_RG1-RW7_T1']] = \
          dataset[['mean_steplength_normal1_T1','mean_steptime_normal1_T1',
                            'mean_frequency_normal1_T1','mean_speed_normal1_T1',
                            'mean_stepwidth_normal1_T1']] - \
          dataset[['mean_steplength_RW7_T1','mean_steptime_RW7_T1','mean_frequency_RW7_T1',
                   'mean_speed_RW7_T1','mean_stepwidth_RW7_T1']].values

dataset2['Exp_RW7-RG1'] = 2

dataset2[['mean_steplength_RG1-RG2_T1','mean_steptime_RG1-RG2_T1',
          'mean_frequency_RG1-RG2_T1','mean_speed_RG1-RG2_T1', 
          'mean_stepwidth_RG1-RG2_T1']] = \
          dataset[['mean_steplength_normal1_T1','mean_steptime_normal1_T1',
                            'mean_frequency_normal1_T1','mean_speed_normal1_T1',
                            'mean_stepwidth_normal1_T1']] - \
                   dataset[['mean_steplength_normal2_T1','mean_steptime_normal2_T1',
                            'mean_frequency_normal2_T1','mean_speed_normal2_T1',
                            'mean_stepwidth_normal2_T1']].values
dataset2['Exp_RG1-RG2'] = 3                           
dataset2[['mean_steplength_RG1-WSPL_T1','mean_steptime_RG1-WSPL_T1',
          'mean_frequency_RG1-WSPL_T1','mean_speed_RG1-WSPL_T1', 
          'mean_stepwidth_RG1-WSPL_T1']] = \
          dataset[['mean_steplength_normal1_T1','mean_steptime_normal1_T1',
                            'mean_frequency_normal1_T1','mean_speed_normal1_T1',
                            'mean_stepwidth_normal1_T1']] - \
                   dataset[['mean_steplength_Woerter_T1','mean_steptime_Woerter_T1',
                            'mean_frequency_Woerter_T1','mean_speed_Woerter_T1',
                            'mean_stepwidth_Woerter_T1']].values
dataset2['Exp_RG1-WSPL'] = 4

dataset4 = dataset.loc[:, ['Normal1_T2','mean_steplength_RW7_T2',
                            'mean_steptime_RW7_T2','mean_frequency_RW7_T2','mean_speed_RW7_T2',
                            'mean_stepwidth_RW7_T2','MOCA_CERAD_korr_T2']]

dataset4[['mean_steplength_RW7-RG1_T2','mean_steptime_RW7-RG1_T2',
          'mean_frequency_RW7-RG1_T2','mean_speed_RW7-RG1_T2', 
          'mean_stepwidth_RW7-RG1_T2']] = \
          dataset[['mean_steplength_RW7_T2','mean_steptime_RW7_T2','mean_frequency_RW7_T2',
                   'mean_speed_RW7_T2','mean_stepwidth_RW7_T2']]- \
                   dataset[['mean_steplength_Normal1_T2','mean_steptime_Normal1_T2',
                            'mean_frequency_Normal1_T2','mean_speed_Normal1_T2',
                            'mean_stepwidth_Normal1_T2']].values
dataset4['Exp_RW7-RG1'] = 2

dataset4[['mean_steplength_RW7-RG2_T2','mean_steptime_RW7-RG2_T2',
          'mean_frequency_RW7-RG2_T2','mean_speed_RW7-RG2_T2', 
          'mean_stepwidth_RW7-RG2_T2']] = \
          dataset[['mean_steplength_RW7_T2','mean_steptime_RW7_T2','mean_frequency_RW7_T2',
                   'mean_speed_RW7_T2','mean_stepwidth_RW7_T2']]- \
                   dataset[['mean_steplength_Normal2_T2','mean_steptime_Normal2_T2',
                            'mean_frequency_Normal2_T2','mean_speed_Normal2_T2',
                            'mean_stepwidth_Normal2_T2']].values
dataset4['Exp_RW7-RG2'] = 3                           
dataset4[['mean_steplength_RW7-WSPL_T2','mean_steptime_RW7-WSPL_T2',
          'mean_frequency_RW7-WSPL_T2','mean_speed_RW7-WSPL_T2', 
          'mean_stepwidth_RW7-WSPL_T2']] = \
          dataset[['mean_steplength_RW7_T2','mean_steptime_RW7_T2','mean_frequency_RW7_T2',
                   'mean_speed_RW7_T2','mean_stepwidth_RW7_T2']]- \
                   dataset[['mean_steplength_Woerter_T2','mean_steptime_Woerter_T2',
                            'mean_frequency_Woerter_T2','mean_speed_Woerter_T2',
                            'mean_stepwidth_Woerter_T2']].values

dataset4['Exp_RW7-WSPL'] = 4

writer = pd.ExcelWriter('D:/Ankit_Jaiswal/Codes/Python/df_T1a.xlsx', engine='openpyxl') 
wb = writer.book
dataset2.to_excel(writer, index=False)
wb.save('D:/Ankit_Jaiswal/Codes/Python/df_T1a.xlsx')

dataset3 = dataset2.iloc[:,6:]
dataset_RG1_T1 = dataset2.iloc[:, 7:13]
dataset_RG1_T1[['MOCA_CERAD_korr_T1']] = dataset.loc[:,['MOCA_CERAD_korr_T1']]
dataset_RG2_T1 = dataset2.iloc[:, 13:19]
dataset_RG2_T1[['MOCA_CERAD_korr_T1']] = dataset.loc[:,['MOCA_CERAD_korr_T1']]
dataset_RW7_T1 = dataset2.iloc[:, 19:25]
dataset_RW7_T1[['MOCA_CERAD_korr_T1']] = dataset.loc[:,['MOCA_CERAD_korr_T1']]

dataset5 = dataset4.iloc[:,6:]
dataset_RG1_T2 = dataset2.iloc[:, 7:13]
dataset_RG1_T2[['MOCA_CERAD_korr_T2']] = dataset.loc[:,['MOCA_CERAD_korr_T2']]
dataset_RG2_T2 = dataset2.iloc[:, 13:19]
dataset_RG2_T2[['MOCA_CERAD_korr_T2']] = dataset.loc[:,['MOCA_CERAD_korr_T2']]
dataset_RW7_T2 = dataset2.iloc[:, 19:25]
dataset_RW7_T2[['MOCA_CERAD_korr_T2']] = dataset.loc[:,['MOCA_CERAD_korr_T2']]

# number of columns
n_columns = len(dataset_RG1_T1.columns)

# save final columns names
columns = dataset_RG1_T1.columns
columns2 = dataset_RG1_T2.columns
# rename both columns to numbers
dataset_RG1_T1.columns = range(n_columns)
dataset_RG2_T1.columns = range(n_columns)
dataset_RW7_T1.columns = range(n_columns)

dataset_RG1_T2.columns = range(n_columns)
dataset_RG2_T2.columns = range(n_columns)
dataset_RW7_T2.columns = range(n_columns)

# concat columns
df_T1 = pd.concat([dataset_RG1_T1, dataset_RG2_T1,dataset_RW7_T1], axis=0, ignore_index=True)
df_T2 = pd.concat([dataset_RG1_T2, dataset_RG2_T2,dataset_RW7_T2], axis=0, ignore_index=True)
# rename columns in new dataframe
df_T1.columns = columns
df_T2.columns = columns2


#Dataset = df_T1

# 3. Prepare Data
# a) Data Cleaning


#Dropping the outlier rows with standard deviation
#factor = 3
#upper_lim = Dataset.iloc[:,:].mean() + Dataset.iloc[:,:].std()*factor
#lower_lim = Dataset.iloc[:,:].mean() - Dataset.iloc[:,:].std()*factor
#
#data = Dataset[(Dataset.iloc[:,:] < upper_lim) & (Dataset.iloc[:,:] > lower_lim)]
#
#print("No. of columns containing null values")
#print(len(data.columns[data.isna().any()]))
df_T2 = df_T2.dropna(how = 'any')

writer = pd.ExcelWriter('D:/Ankit_Jaiswal/Codes/Python/df_T1.xlsx', engine='openpyxl') 
wb = writer.book
df_T1.to_excel(writer, index=False)
wb.save('D:/Ankit_Jaiswal/Codes/Python/df_T1.xlsx')
data = df_T1
data2 = df_T2
X = data.iloc[:,0:7].values
y = data.iloc[:,6:7].values.ravel()

X2 = data2.iloc[:,0:7].values
y2 = data2.iloc[:,6:7].values.ravel()

sc = StandardScaler()
X[:,0:5] = sc.fit_transform(X[:,0:5])
X2[:,0:5] = sc.fit_transform(X2[:,0:5])

X1 = X
# Encoding categorical data
from sklearn.compose import ColumnTransformer
ct = ColumnTransformer([('encoder',OneHotEncoder(),[5])], remainder = 'passthrough')
X = np.array(ct.fit_transform(X),dtype =np.float)
X2 = np.array(ct.fit_transform(X2),dtype =np.float)


from pandas.plotting import scatter_matrix
# box and whisker plots
data.plot(kind='box', subplots=True, layout=(5,5), sharex=False, sharey=False)
plt.show()
# histograms
data.hist()
plt.show()
# scatter plot matrix
scatter_matrix(data)
plt.show()


sns.set_style("whitegrid");
sns.pairplot(data, hue="MOCA_CERAD_korr_T1", size=3);
plt.show()

validation_size = 0.3
seed = 7
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y,
                    test_size=validation_size, random_state=seed)


#
# c) Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
    
## Compare Algorithms
#fig = plt.figure()
#fig.suptitle('Algorithm Comparison')
#ax = fig.add_subplot(111)
#plt.boxplot(results)
#ax.set_xticklabels(names)
#plt.show()

SVM = SVC(gamma='auto')
SVM.fit(X_train, Y_train)
predictions = SVM.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

KNN = KNeighborsClassifier()
KNN.fit(X_train, Y_train)
predictions = KNN.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(SVM, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X2, y2)
print(result)


sns.set_style("whitegrid")
sns.FacetGrid(data, hue='MOCA_CERAD_korr_T1', size=3) \
   .map(plt.scatter, 'mean_steplength_RG1-RW7_T1','mean_steptime_RG1-RW7_T1') \
   .add_legend()
plt.show()

## agglomerative clustering
#from numpy import unique
#from numpy import where
#from sklearn.datasets import make_classification
#from sklearn.cluster import AgglomerativeClustering
#from matplotlib import pyplot
## define dataset
##X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
## define the model
#model = AgglomerativeClustering(n_clusters=3)
## fit model and predict clusters
#yhat = model.fit_predict(X1)
## retrieve unique clusters
#clusters = unique(yhat)
## create scatter plot for samples from each cluster
#for cluster in clusters:
#	# get row indexes for samples with this cluster
#	row_ix = where(yhat == cluster)
#	# create scatter of these samples
#	pyplot.scatter( X1[row_ix, 0],X1[row_ix, 1], X1[row_ix, 2], X1[row_ix, 3],X1[row_ix, 4])
## show the plot
#pyplot.show()
#print(accuracy_score(y, yhat))