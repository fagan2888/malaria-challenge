import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectPercentile, VarianceThreshold, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=42)

# Score on the training set was:0.8158815640880859
exported_pipeline = make_pipeline(
    make_union(
        StackingEstimator(estimator=make_pipeline(
            make_union(
                StackingEstimator(estimator=make_pipeline(
                    SelectPercentile(score_func=f_classif, percentile=88),
                    VarianceThreshold(threshold=0.2),
                    LogisticRegression(C=10.0, dual=False, penalty="l1")
                )),
                SelectPercentile(score_func=f_classif, percentile=74)
            ),
            StandardScaler(),
            LogisticRegression(C=10.0, dual=False, penalty="l1")
        )),
        SelectPercentile(score_func=f_classif, percentile=74)
    ),
    StandardScaler(),
    LogisticRegression(C=0.001, dual=False, penalty="l2")
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
