import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import Binarizer, StandardScaler
from sklearn.svm import LinearSVC
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=42)

# Score on the training set was:0.8291955789781877
exported_pipeline = make_pipeline(
    make_union(
        make_pipeline(
            make_union(
                FunctionTransformer(copy),
                FunctionTransformer(copy)
            ),
            StackingEstimator(estimator=LogisticRegression(C=0.1, dual=True, penalty="l2")),
            SelectPercentile(score_func=f_classif, percentile=78)
        ),
        make_pipeline(
            make_union(
                FunctionTransformer(copy),
                FunctionTransformer(copy)
            ),
            SelectPercentile(score_func=f_classif, percentile=46),
            Binarizer(threshold=0.1)
        )
    ),
    StandardScaler(),
    LinearSVC(C=0.001, dual=True, loss="hinge", penalty="l2", tol=0.01)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
