import graphviz
import pandas
import pickle
from sklearn import tree
import os
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
import csv
import scipy.io.wavfile as wav
import soundfile as sf
import numpy as np
from scipy.stats import skew
from scipy.stats import kurtosis
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split,ShuffleSplit
directory = os.fsencode("/home/nilabjo/COP315/Bird_sound_cloud_new")
mfcc_training_set=[]
mfcc_test_set=[]
rate=1600
Y=[]

Y_test=[]
for file in os.listdir(directory):
     #print("jbjvb")
     filename = os.fsdecode(file)
     type(filename)
     #print(filename)
     if filename.endswith(".csv"):
        #print("jbjvb")
        print(filename)
        Y.append(int(filename[0]))
         # print(os.path.join(directory, filename))
        #(sig,rate)=sf.read("/home/nilabjo/COP315/mlsp-2013-birds/mlsp_contest_dataset/mlsp_contest_dataset/essential_data/src_wavs"+"/"+filename)
        sig = np.genfromtxt ("/home/nilabjo/COP315/Bird_sound_cloud_new/"+filename,delimiter=",")
        #signal=csve[;,0]
        mfcc_feat=sig
        #mfcc_feat = mfcc(sig,rate,nfft=512)
        mfcc_red_features=[]
        feature_vector=[]
        for i in range(0,13):
            #print("ok")
            metric_min=np.min(mfcc_feat[:,i])
            metric_max=np.max(mfcc_feat[:,i])
            metric_median= np.median(mfcc_feat[:,i])
            metric_mean=np.mean(mfcc_feat[:,i])
            metric_variance= np.var(mfcc_feat[:,i])
            metric_skewness= skew(mfcc_feat[:,i])
            metric_kurtosis= kurtosis(mfcc_feat[:,i])
            c=np.gradient(mfcc_feat[:,i])
            metric_mean_dev1=np.mean(c)
            metric_var_dev1=np.var(c)
            v=np.gradient(c)
            metric_mean_dev2=np.mean(v)
            metric_var_dev2=np.var(v)
            feature_vector=np.hstack((feature_vector,metric_min,metric_max,metric_median,metric_mean,metric_variance,metric_skewness,metric_kurtosis,metric_mean_dev1,metric_var_dev1,metric_mean_dev2,metric_var_dev2))
        mfcc_training_set.append(feature_vector)
     else:
         continue
Y=np.asarray(Y)
print(Y.size)
cv=ShuffleSplit(n_splits=3, test_size=0.1, random_state=0)
base_model = RandomForestClassifier(n_estimators =5)

best_grid=RandomForestClassifier(bootstrap=False,max_depth=9, min_samples_leaf=2,min_samples_split=12,n_estimators=20)
best_grid.fit(mfcc_training_set,Y)
scores=cross_val_score(best_grid,mfcc_training_set,Y,cv=cv)
scores1=cross_val_score(base_model,mfcc_training_set,Y,cv=cv)
print("Accuracy of tuned model: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print("Accuracy of base model: %0.2f (+/- %0.2f)" % (scores1.mean(), scores.std() * 2))
# #print(clf.feature_importances_)
filename='finalized_model_cloud.sav'
pickle.dump(best_grid, open(filename, 'wb'))

