# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

from deeptables.models.deeptable import DeepTable
from deeptables.models.hyper_dt import HyperDT
from deeptables.models.hyper_dt import mini_dt_space
from hypernets.core.callbacks import SummaryCallback, FileLoggingCallback
from hypernets.core.searcher import OptimizeDirection
from hypernets.searchers.random_searcher import RandomSearcher
from .. import homedir


class Test_HyperDT_Regression():

    def test_boston(self):

        print("Loading datasets...")
        boston_dataset = load_boston()

        df_train = pd.DataFrame(boston_dataset.data)
        df_train.columns = boston_dataset.feature_names
        self.y = pd.Series(boston_dataset.target)
        self.X = df_train

        self.X_train, \
        self.X_test, \
        self.y_train, \
        self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        rs = RandomSearcher(mini_dt_space, optimize_direction=OptimizeDirection.Maximize, )
        hdt = HyperDT(rs,
                      callbacks=[SummaryCallback(), FileLoggingCallback(rs, output_dir=f'{homedir}/hyn_logs')],
                      reward_metric='RootMeanSquaredError',
                      dnn_params={
                          'hidden_units': ((256, 0, False), (256, 0, False)),
                          'dnn_activation': 'relu',
                      },
                      )
        hdt.search(self.X_train, self.y_train, self.X_test, self.y_test, max_trails=3)

        best_trial = hdt.get_best_trail()

        estimator = hdt.final_train(best_trial.space_sample, self.X, self.y)
        score = estimator.predict(self.X_test)
        result = estimator.evaluate(self.X_test, self.y_test)
        assert result
        assert isinstance(estimator.model, DeepTable)
