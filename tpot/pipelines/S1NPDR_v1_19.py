import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVC
from tpot.builtins import StackingEstimator, ZeroCount
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the class is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1).values
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'].values, random_state=42)

# Score on the training set was:0.8084210897797854
exported_pipeline = make_pipeline(
    make_union(
        make_pipeline(
            make_union(
                SelectPercentile(score_func=f_classif, percentile=34),
                make_pipeline(
                    ZeroCount(),
                    ZeroCount()
                )
            ),
            PCA(iterated_power=4, svd_solver="randomized")
        ),
        FunctionTransformer(copy)
    ),
    StackingEstimator(estimator=LogisticRegression(C=0.01, dual=True, penalty="l2")),
    PCA(iterated_power=8, svd_solver="randomized"),
    LinearSVC(C=0.001, dual=False, loss="squared_hinge", penalty="l2", tol=0.01)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
