import os
import numpy as np
from EElogging.EELogger import EELogger
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV, KFold, RandomizedSearchCV
from sklearn.metrics import r2_score


class EEModelFinder:
    """
    :Class Name: EEModelFinder
    :Description: This class will be used to train different models and select the best one
                  amongst them.

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """

    def __init__(self):

        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")

        self.log_path = "EElogging/training/EEModelFinder.txt"
        self.logger = EELogger()

        self.rfr = RandomForestRegressor(n_jobs=-1, verbose=0)
        self.xgb = XGBRegressor()
        self.ridge = Ridge()
        self.lasso = Lasso()
        self.svr = SVR()
        self.kfold = KFold(shuffle=True, random_state=42)

    def ee_adj_r2(self, estimator, x, y_true):
        """
        :Method Name: ee_adj_r2
        :Description: This method will be used by GridSearchCV to score the different models generated by adjusted r2
                      value.

        :param estimator: The sklearn model which will be fitted using GridSearchCV
        :param x: Input training data
        :param y_true: Output training labels
        :return: adjusted R2 score
        """
        n, p = x.shape
        pred = estimator.predict(x)
        return 1 - ((1 - r2_score(y_true, pred)) * (n - 1)) / (n - p - 1)

    def ee_best_ridge_regressor(self, train_x, train_y):
        """
        :Method Name: ee_get_best_ridge_regressor
        :Description: This method trains and returns the best model amongst many trained ridge regressor.

        :param train_x: Input training Data
        :param train_y: Input training labels
        :return: The best ridge regressor model
        :On failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            param_grid = {
                'alpha': np.random.uniform(0, 10, 50),
                'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
            }
            message = f"Using GridSearchCV to obtain the optimum parameters({param_grid.keys()})  of Ridge Regressor"
            self.logger.log(log_file, message)

            # GridSearchCV is used as there are only a few combination of parameters.
            grid = GridSearchCV(estimator=self.ridge, param_grid=param_grid,
                                cv=self.kfold, n_jobs=-1,
                                scoring={'n-mse': 'neg_mean_squared_error',
                                         'adjusted-R2': self.ee_adj_r2},
                                refit='adjusted-R2', verbose=0)

            grid.fit(train_x, train_y)

            alpha = grid.best_params_['alpha']
            solver = grid.best_params_['solver']
            score = grid.best_score_

            message = f" The optimum parameters of Ridge Regressor are alpha={alpha}, solver={solver} with the " \
                      f"adjusted R2 score of {score}"
            self.logger.log(log_file, message)

            self.ridge = Ridge(alpha=alpha, solver=solver)
            self.ridge.fit(train_x, train_y)

            message = "Best Ridge Regressor trained"
            self.logger.log(log_file, message)

            log_file.close()
            return self.ridge

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while fitting Ridge Regressor: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_best_lasso_regressor(self, train_x, train_y):
        """
        :Method Name: ee_get_best_lasso_regressor
        :Description: This method trains and returns the best model amongst many trained lasso regressor.

        :param train_x: Input training Data
        :param train_y: Input training labels
        :return: The best lasso regressor model
        :On failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            param_grid = {
                'alpha': np.random.uniform(0, 10, 50),
                'selection': ['cyclic', 'random']
            }
            message = f"Using GridSearchCV to obtain the optimum parameters({param_grid.keys()})  of Lasso Regressor"
            self.logger.log(log_file, message)

            # GridSearchCV is used as there are only a few combination of parameters.
            grid = GridSearchCV(estimator=self.lasso, param_grid=param_grid,
                                cv=self.kfold, n_jobs=-1,
                                scoring={'n-mse': 'neg_mean_squared_error',
                                         'adjusted-R2': self.ee_adj_r2},
                                refit='adjusted-R2', verbose=0)

            grid.fit(train_x, train_y)

            alpha = grid.best_params_['alpha']
            selection = grid.best_params_['selection']
            score = grid.best_score_

            message = f" The optimum parameters of Lasso Regressor are alpha={alpha}, selection={selection}" \
                      f" with the adjusted R2 score of {score}"
            self.logger.log(log_file, message)

            self.lasso = Lasso(alpha=alpha, selection=selection)
            self.lasso.fit(train_x, train_y)

            message = "Best Lasso Regressor trained"
            self.logger.log(log_file, message)

            log_file.close()
            return self.lasso

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while fitting Lasso Regressor: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_best_svr(self, train_x, train_y):
        """
        :Method Name: ee_get_best_svr
        :Description: This method trains and returns the best model amongst many trained SVR.

        :param train_x: Input training Data
        :param train_y: Input training labels
        :return: The best SVR model
        :On failure: Exception
        """

        try:
            log_file = open(self.log_path, 'a+')

            param_grid = {
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'gamma': ['scale', 'auto'],
                'C': [0.01, 0.03, 0.1, 0.3, 1, 3, ],
                'degree': [2, 3, 4],
                'epsilon': [0.01, 0.03, 0.1, 0.3, 1]
            }

            message = f"Using GridSearchCV to obtain the optimum parameters({param_grid.keys()}) of SVR"
            self.logger.log(log_file, message)

            # GridSearchCV is used as there are only a few combination of parameters.
            grid = GridSearchCV(estimator=self.svr, param_grid=param_grid,
                                cv=self.kfold, n_jobs=-1,
                                scoring={'n-mse': 'neg_mean_squared_error',
                                         'adjusted-R2': self.ee_adj_r2},
                                refit='adjusted-R2', verbose=0)

            grid.fit(train_x, train_y)

            kernel = grid.best_params_['kernel']
            gamma = grid.best_params_['gamma']
            c = grid.best_params_['C']
            degree = grid.best_params_['degree']
            epsilon = grid.best_params_['epsilon']
            score = grid.best_score_

            message = f" The optimum parameters of SVR are kernel={kernel}, gamma={gamma}, C={c}, degree ={degree}, " \
                      f"epsilon={epsilon} with the adjusted R2 score of {score}"
            self.logger.log(log_file, message)

            self.svr = SVR(kernel=kernel, gamma=gamma, C=c, degree=degree, epsilon=epsilon)
            self.svr.fit(train_x, train_y)

            message = "Best SVR trained"
            self.logger.log(log_file, message)

            log_file.close()
            return self.svr

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while fitting SVR: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_best_random_forest(self, train_x, train_y):
        """
        :Method Name: ee_best_random_forest
        :Description: This method trains and returns the best model amongst many trained random forest regressor.

        :param train_x: Input training Data
        :param train_y: Input training labels
        :return: The best random forest regressor model
        :On failure: Exception"""

        try:
            log_file = open(self.log_path, 'a+')

            param_grid = {
                "n_estimators": [50, 100, 130, 150],
                'criterion': ['mse', 'mae'],
                'min_samples_split': [2, 3, 4, 5],
                'max_features': ['auto', 'sqrt', 'log2'],
                'ccp_alpha': np.arange(0, 0.012, 0.001),

            }

            message = f"Using GridSearchCV to obtain the optimum parameters({param_grid.keys()}) of random forest " \
                      f"regressor "
            self.logger.log(log_file, message)

            # RandomSearchCV is used as there are a large number combination of parameters.
            grid = RandomizedSearchCV(estimator=self.rfr, param_distributions=param_grid, n_iter=500,
                                      cv=self.kfold, n_jobs=-1,
                                      scoring={'n-mse': 'neg_mean_squared_error',
                                               'adjusted-R2': self.ee_adj_r2},
                                      refit='adjusted-R2', verbose=0)

            grid.fit(train_x, train_y)

            n_estimators = grid.best_params_['n_estimators']
            criterion = grid.best_params_['criterion']
            min_samples_split = grid.best_params_['min_samples_split']
            max_features = grid.best_params_['max_features']
            ccp_alpha = grid.best_params_['ccp_alpha']
            score = grid.best_score_

            message = f" The optimum parameters of random forrest regressor are n_estimators={n_estimators}," \
                      f" criterion={criterion}, min_samples_split={min_samples_split}, max_features ={max_features}" \
                      f",ccp_alpha={ccp_alpha} with the adjusted R2 score of {score}"
            self.logger.log(log_file, message)

            self.rfr = RandomForestRegressor(n_jobs=-1, verbose=0,
                                             n_estimators=n_estimators, criterion=criterion,
                                             min_samples_split=min_samples_split,
                                             max_features=max_features, ccp_alpha=ccp_alpha
                                             )
            self.rfr.fit(train_x, train_y)

            message = "Best random forest regressor trained"
            self.logger.log(log_file, message)

            log_file.close()
            return self.rfr

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while fitting Random Forest Regressor: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_best_xgb_regressor(self, train_x, train_y):
        """
        :Method Name: ee_best_xgb_regressor
        :Description: This method trains and returns the best model amongst many trained xgb regressors.

        :param train_x: Input training Data
        :param train_y: Input training labels
        :return: The best xgb regressor model
        :On failure: Exception
        """

        try:
            log_file = open(self.log_path, 'a+')

            param_grid = {
                'learning_rate': [0.01, 0.03, 0.1, 0.3],
                'colsample_bytree': [.1, .2, .3, .4, .5, .6, .7, .8],
                'max_depth': [3, 5, 10],
                'n_estimators': [30, 100, 300, 1000],
                "verbosity": [0]
            }

            message = f"Using GridSearchCV to obtain the optimum parameters({param_grid.keys()}) of xgb regressor"
            self.logger.log(log_file, message)

            # RandomSearchCV is used as there are a large number combination of parameters.
            grid = RandomizedSearchCV(estimator=self.xgb, param_distributions=param_grid, n_iter=250,
                                      cv=self.kfold, n_jobs=-1,
                                      scoring={'n-mse': 'neg_mean_squared_error',
                                               'adjusted-R2': self.ee_adj_r2},
                                      refit='adjusted-R2', verbose=0)
            grid.fit(train_x, train_y)

            learning_rate = grid.best_params_['learning_rate']
            colsample_bytree = grid.best_params_['colsample_bytree']
            max_depth = grid.best_params_['max_depth']
            n_estimators = grid.best_params_['n_estimators']
            score = grid.best_score_

            message = f" The optimum parameters of xgb-regressor are learning_rate={learning_rate}, " \
                      f"max_depth={max_depth}, colsample_bytree={colsample_bytree}, n_estimators ={n_estimators} " \
                      f"with the adjusted R2 score of {score}"
            self.logger.log(log_file, message)

            self.xgb = XGBRegressor(n_jobs=-1, verbose=0, learning_rate=learning_rate,
                                    colsample_bytree=colsample_bytree,
                                    max_depth=max_depth, n_estimators=n_estimators)

            self.xgb.fit(train_x, train_y)
            message = "Best xgb regressor trained"
            self.logger.log(log_file, message)

            log_file.close()
            return self.xgb

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while fitting Random Forest Regressor: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_best_model_from_adj_r2(self, r2_adj):
        """
        :Method Name: ee_best_model_from_adj_r2
        :Description: This method takes in a dictionary with model name as keys and adjusted r2 score as values,
                      it then returns the best model based on highest adjusted r2 score.

        :param r2_adj: The dictionary of all adjusted r2 scores
        :return: The best sklearn model for the given dataset
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            keys = list(r2_adj.keys())
            values = list(r2_adj.values())
            ind = values.index(max(values))
            if keys[ind] == "ridge":
                message = "The best model is ridge regressor"
                self.logger.log(log_file, message)
                log_file.close()
                return keys[ind], self.ridge
            elif keys[ind] == "lasso":
                message = "The best model is lasso regressor"
                self.logger.log(log_file, message)
                log_file.close()
                return keys[ind], self.lasso
            elif keys[ind] == "svr":
                message = "The best model is svr"
                self.logger.log(log_file, message)
                log_file.close()
                return keys[ind], self.svr
            elif keys[ind] == "rfr":
                message = "The best model is random forest regressor"
                self.logger.log(log_file, message)
                log_file.close()
                return keys[ind], self.rfr
            else:
                message = "The best model is xgb regressor"
                self.logger.log(log_file, message)
                log_file.close()
                return keys[ind], self.xgb

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while obtaining best model from adjusted r2 dictionary: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_best_model(self, train_x, train_y, test_x, test_y):
        """
        :Method Name: ee_best_model
        :Description: This method is used to select the best model from all the best model from all categories.

        :param train_x: the training features
        :param train_y: the training labels
        :param test_x: the test features
        :param test_y: the test labels
        :return: The best sklearn model for the given dataset
        :On Failure: Exception
        """

        try:
            log_file = open(self.log_path, 'a+')
            message = "Search for best model started"
            self.logger.log(log_file, message)

            r2_adj = {}

            message = "Search for best ridge model started"
            self.logger.log(log_file, message)

            self.ridge = self.ee_best_ridge_regressor(train_x, train_y)
            r2_adj["ridge"] = self.ee_adj_r2(self.ridge, test_x, test_y)

            message = "Search for best ridge model ended"
            self.logger.log(log_file, message)

            message = "Search for best lasso model started"
            self.logger.log(log_file, message)

            self.lasso = self.ee_best_lasso_regressor(train_x, train_y)
            r2_adj["lasso"] = self.ee_adj_r2(self.lasso, test_x, test_y)

            message = "Search for best lasso model ended"
            self.logger.log(log_file, message)

            message = "Search for best svr model started"
            self.logger.log(log_file, message)

            self.svr = self.ee_best_svr(train_x, train_y)
            r2_adj["svr"] = self.ee_adj_r2(self.svr, test_x, test_y)

            message = "Search for best svr model ended"
            self.logger.log(log_file, message)

            message = "Search for best random forest regressor model started"
            self.logger.log(log_file, message)

            self.rfr = self.ee_best_random_forest(train_x, train_y)
            r2_adj["rfr"] = self.ee_adj_r2(self.rfr, test_x, test_y)

            message = "Search for best random forest regressor model ended"
            self.logger.log(log_file, message)

            message = "Search for best xgb regressor model started"
            self.logger.log(log_file, message)

            self.xgb = self.ee_best_xgb_regressor(train_x, train_y)
            r2_adj["xgb"] = self.ee_adj_r2(self.xgb, test_x, test_y)

            message = "Search for best xgb regressor model ended"
            self.logger.log(log_file, message)

            return self.ee_best_model_from_adj_r2(r2_adj)

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was a problem while obtaining best model : {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
