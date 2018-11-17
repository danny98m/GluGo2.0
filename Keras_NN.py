import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
#from keras.utils import plot_model

# load dataset
dataframe = pandas.read_csv("C:\\Users\\Ethan\\Desktop\\Startup_2018\\Experiment_#3_POWELL\\glucose_dataset_-_lags,_hour_of_day.csv")
dataset = dataframe.values
# split into input (X) and output (Y) variables
X = dataset[:,2:16]
Y = dataset[:,1]

print(X[0])
print(Y)

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(14, input_dim=14, kernel_initializer='normal', activation='relu'))
	model.add(Dense(7, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=baseline_model, epochs=45, batch_size=20, verbose=0)

print("okay so far")

kfold = KFold(n_splits=3, random_state=seed)
print("still going")

#model = baseline_model()
#model_fitted = model.fit(X, Y, epochs = 45, batch_size = 10, verbose = 0)
#plot_model(model, to_file = 'model.png')
#Y_predicted = model.predict(X)


results = cross_val_score(estimator, X, Y, cv=kfold)

print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

print(results.mean())


#numpy.random.seed(seed)
#estimators = []
#estimators.append(('standardize', StandardScaler()))
#estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=45, batch_size=10, verbose=0)))
#pipeline = Pipeline(estimators)
#kfold = KFold(n_splits=3, random_state=seed)
#results = cross_val_score(pipeline, X, Y, cv=kfold)
#print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))