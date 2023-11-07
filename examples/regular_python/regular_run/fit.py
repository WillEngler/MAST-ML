from mastml.data_splitters import SklearnDataSplitter, NoSplit
from mastml.preprocessing import SklearnPreprocessor
from mastml.datasets import LocalDatasets
from mastml.models import SklearnModel
from mastml.domain import Domain

from pathlib import Path

import subprocess
import shutil
import glob
import os

target = 'E_regression_shift'  # The target variable
extra_columns = ['mat', 'group']  # Columns not used as features

# Load the data in a standard manner
d = LocalDatasets(
                  file_path='./diffusion.csv',
                  target=target,
                  extra_columns=extra_columns,
                  as_frame=True
                  )
data_dict = d.load_data()  # The actual loading

# Data in a useful form
X = data_dict['X']  # The features
y = data_dict['y']  # The target

'''
# Regression metrics to include
metrics = [
           'r2_score',
           'mean_absolute_error',
           'root_mean_squared_error',
           'rmse_over_stdev',
           ]

# Data scaling that comes standard with many models
preprocessor = SklearnPreprocessor(
                                   preprocessor='StandardScaler',
                                   as_frame=True,
                                   )

# The type of regression model to use
model = SklearnModel(model='RandomForestRegressor')

# The type of cross validation to conduct
splitter = SklearnDataSplitter(
                               splitter='RepeatedKFold',
                               n_repeats=1,
                               n_splits=5
                               )

# Perform unceratinty quantification
splitter.evaluate(
                  X=X,
                  y=y,
                  models=[model],
                  preprocessor=preprocessor,
                  metrics=metrics,
                  plots=['Scatter', 'Histogram', 'Error'],
                  error_method='stdev_weak_learners',
                  recalibrate_errors=True,
                  )

# Rename the output directory
file_to_move = glob.glob('Ran*')[0]
cal_name = 'calibration_run'
subprocess.run(['mv', file_to_move, cal_name])

# Domain with MADML
params = {'n_repeats': 2}
domain = ('madml', params)

# MADML has a default set of splitters (can add other set with params)
splitter = NoSplit()
splitter.evaluate(
                  X=X,
                  y=y,
                  models=[model],
                  preprocessor=preprocessor,
                  metrics=metrics,
                  plots=['Scatter', 'Histogram'],
                  domain=[domain],
                  )

# Rename the output directory
file_to_move = glob.glob('Ran*')[0]
dom_name = 'domain_run'
subprocess.run(['mv', file_to_move, dom_name])
'''

# Gather the standard objects to create a single model
cal_params = os.path.join(cal_name, 'recalibration_parameters_train.csv')
model_path = os.path.join(dom_name, 'RandomForestRegressor.pkl')
preprocessor_path = os.path.join(dom_name, 'StandardScaler.pkl')
domain_path = list(map(str, Path(dom_name).rglob('domain_*.pkl')))

files = [cal_params, model_path, preprocessor_path, *domain_path]

# Copy the files
X.to_csv('X_train.csv', index=False)  # The training features
output = 'container_files'
for f in files:
    shutil.copy(f, os.path.join(output, os.path.basename(f)))

# The training features
X.to_csv(
         os.path.join(output, 'X_train.csv'), 
         index=False
         )
