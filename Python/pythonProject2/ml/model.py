import scipy.io
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

train_data = scipy.io.loadmat('extra_32x32.mat')

x = train_data['X']
y = train_data['Y']

X = X.reshape()