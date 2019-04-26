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
import csv
import scipy.io.wavfile as wav
import soundfile as sf
import numpy as np
from scipy.stats import skew
from scipy.stats import kurtosis
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split,ShuffleSplit

loaded_model=pickle.load(open("/home/pi/Documents/finalized_model.sav",'rb'))
def classify(csvname):
    filename="/home/pi/Documents/"+csvname #write the full address of the test file containing the mfcc matrix
    mfcc_feat = np.genfromtxt (filename,delimiter=",")
    print(mfcc_feat.shape)
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
    print(feature_vector.shape)
    result1=loaded_model.predict_proba([feature_vector])
    result =loaded_model.predict([feature_vector])
    #x=result[0][0]
    #if (result1[0][x]>=0.35):
     #   result=result
    #else:
     #   result=np.array([5])
    return (result)
