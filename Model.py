import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn_extra.cluster import KMedoids
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.spatial.distance import cdist
import lightgbm as lgb
from catboost import CatBoostRegressor
from ngboost import NGBRegressor
from ngboost.distns import Normal
from ngboost.scores import MLE

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn_extra.cluster import KMedoids
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.metrics import mean_squared_error, r2_score
from scipy.spatial.distance import cdist
import lightgbm as lgb
from catboost import CatBoostRegressor
from ngboost import NGBRegressor
from ngboost.distns import Normal
from ngboost.scores import MLE

# Function for selecting mutants in the first round
def first_round(labels, embeddings, explicit_variants=None, num_mutants_per_round=16, first_round_strategy='random', embedding_type=None, random_seed=None):
    print("Starting labels length:", len(labels))
    variants_without_WT = labels.variant[labels.variant != 'WT']
    print("Starting non-wt length:", len(variants_without_WT))

    if first_round_strategy == 'random':
        if random_seed is not None:
            np.random.seed(random_seed)
        iteration_zero_ids = np.random.choice(variants_without_WT, size=num_mutants_per_round, replace=False)

    elif first_round_strategy == 'diverse_medoids':
        if random_seed is not None:
            np.random.seed(random_seed)
        num_clusters = num_mutants_per_round
        embeddings_without_WT = embeddings.drop('WT') if 'WT' in embeddings.index else embeddings.copy()
        print("embeddings without wildtype:", len(embeddings_without_WT))
        pca_embeddings_reduced = PCA(n_components=10).fit_transform(embeddings_without_WT) if embedding_type != 'embeddings_pca' else embeddings_without_WT
        cluster_medoids = KMedoids(n_clusters=num_clusters, metric='euclidean', random_state=random_seed).fit(pca_embeddings_reduced).medoid_indices_
        iteration_zero_ids = embeddings_without_WT.index[cluster_medoids].tolist()

    elif first_round_strategy == 'activity_topk':
        sorted_variants = labels[labels.variant != 'WT'].sort_values(by='activity', ascending=False)
        iteration_zero_ids = sorted_variants.head(num_mutants_per_round).variant.tolist()

    elif first_round_strategy == 'mixed_diverse_random':
        if random_seed is not None:
            np.random.seed(random_seed)
        half = num_mutants_per_round // 2
        # Half diverse_medoids
        embeddings_without_WT = embeddings.drop('WT') if 'WT' in embeddings.index else embeddings.copy()
        pca_embeddings_reduced = PCA(n_components=10).fit_transform(embeddings_without_WT) if embedding_type != 'embeddings_pca' else embeddings_without_WT
        medoids = KMedoids(n_clusters=half, metric='euclidean', random_state=random_seed).fit(pca_embeddings_reduced).medoid_indices_
        medoid_variants = embeddings_without_WT.index[medoids].tolist()
        # Half random
        remaining = list(set(variants_without_WT) - set(medoid_variants))
        random_variants = np.random.choice(remaining, size=num_mutants_per_round - half, replace=False).tolist()
        iteration_zero_ids = medoid_variants + random_variants

    elif first_round_strategy == 'explicit_variants':
        iteration_zero_ids = explicit_variants

    else:
        raise ValueError("Invalid first round search strategy.")

    iteration_zero = pd.DataFrame({'variant': iteration_zero_ids, 'iteration': 0})
    WT = pd.DataFrame({'variant': 'WT', 'iteration': 0}, index=[0])
    iteration_zero = pd.concat([iteration_zero, WT], ignore_index=True)
    this_round_variants = iteration_zero.variant
    labels_zero = pd.merge(labels, iteration_zero, on='variant', how='left')
    return labels_zero, iteration_zero, this_round_variants


# Active learning function for one iteration
def top_layer(iter_train, iter_test, embeddings_pd, labels_pd, measured_var, regression_type='randomforest', top_n=None, final_round=10, experimental=False):
    
    # if experimental, check alignment between embeddings and labels. This is done in the data loading for dms data
    if experimental:
        label_variants = labels_pd['variant'].tolist()
        embedding_variants = embeddings_pd.index.tolist()

        # Check if embedding row names and label variants are identical
        if label_variants == embedding_variants:
            print('Embeddings and labels are aligned')
        else:
            print('Embeddings and labels are not aligned')
            print('Exiting.')
            return None
    
    # reset the indices of embeddings_pd and labels_pd
    embeddings_pd = embeddings_pd.reset_index(drop=True)
    labels_pd = labels_pd.reset_index(drop=True)    

    # save column 'iteration' in the labels dataframe
    iteration = labels_pd['iteration']

    # save labels
    labels = labels_pd

    # save mean embeddings as numpy array
    a = embeddings_pd

    # subset a, y to only include the rows where iteration = iter_train and iter_test
    idx_train = iteration[iteration.isin(iter_train)].index.to_numpy()
    if iter_test is not None:
        idx_test = iteration[iteration == iter_test].index.to_numpy()
    else:
        idx_test = iteration[iteration.isna()].index.to_numpy()

    # subset a to only include the rows where iteration = iter_train and iter_test
    X_train = a.loc[idx_train, :]
    X_test = a.loc[idx_test, :]
    
    y_train = labels[iteration.isin(iter_train)][measured_var]
    y_train_activity_scaled = labels[iteration.isin(iter_train)]['activity_scaled']
    y_train_activity_binary = labels[iteration.isin(iter_train)]['activity_binary']

    if iter_test is not None:
        y_test = labels[iteration.isin([iter_test])][measured_var]
        print(y_test.shape)
        y_test_activity_scaled = labels[iteration.isin([iter_test])]['activity_scaled']
        y_test_activity_binary = labels[iteration.isin([iter_test])]['activity_binary']
    else:
        y_test = labels[iteration.isna()][measured_var]
        print(y_test.shape)
        y_test_activity_scaled = labels[iteration.isna()]['activity_scaled']
        y_test_activity_binary = labels[iteration.isna()]['activity_binary']        


    # fit
    if regression_type == 'ridge':
        model = linear_model.RidgeCV()
    elif regression_type == 'lasso':
        model = linear_model.LassoCV(max_iter=100000, tol=1e-3)
    elif regression_type == 'elasticnet':
        model = linear_model.ElasticNetCV(max_iter=100000, tol=1e-3)
    elif regression_type == 'linear':
        model = linear_model.LinearRegression()
    elif regression_type == 'neuralnet':
        model = MLPRegressor(hidden_layer_sizes=(5), max_iter=1000, activation='relu', solver='adam', alpha=0.001)
    elif regression_type == 'randomforest':
        model = RandomForestRegressor(n_estimators=100, random_state=1)
    elif regression_type == 'gradientboosting':
        model = xgboost.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                                     max_depth=5, alpha=10, n_estimators=10, verbosity=0)
    elif regression_type == 'lightgbm':
        model = lgb.LGBMRegressor(objective='regression', n_estimators=500,learning_rate=0.05, subsample=0.8, colsample_bytree=0.7, num_leaves=31,
                                     max_depth=6, reg_alpha=1.0, reg_lambda=1.0, random_state=42,  n_jobs=-1)
    elif regression_type == 'catboost':

        from sklearn.ensemble import VotingRegressor
        model = VotingRegressor([
            ('catboost_config4', CatBoostRegressor(
                verbose=0, iterations=800, learning_rate=0.08,
                depth=4, l2_leaf_reg=1, random_seed=1
            )),
            ('catboost_config3', CatBoostRegressor(
                verbose=0, iterations=500, learning_rate=0.05,
                depth=4, l2_leaf_reg=1, random_seed=1
            )),
            ('catboost_config5', CatBoostRegressor(
                verbose=0, iterations=800, learning_rate=0.08,
                depth=4, l2_leaf_reg=3, random_seed=1
            ))
        ])

    elif regression_type == 'xgboost':

        model = xgboost.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.05, max_depth=4,
                                     subsample=0.8, colsample_bytree=0.8, reg_alpha=0.05, reg_lambda=1, random_state=1,
                                     verbosity=0, n_jobs=-1)
    elif regression_type == 'ngboost':
        model = NGBRegressor(Dist=Normal, Score=MLE, n_estimators=500, learning_rate=0.05, natural_gradient=True,
                             verbose=False, random_state=42,minibatch_frac=0.5)
    elif regression_type == 'knn':
        model = KNeighborsRegressor(n_neighbors=5)
    elif regression_type == 'gp':
        model = GaussianProcessRegressor()
    else:
        raise ValueError(f"Unknown regression_type: {regression_type}")

    model.fit(X_train, y_train)

    # make predictions on train data
    y_pred_train = model.predict(X_train)
    y_std_train = np.zeros(len(y_pred_train))
    # make predictions on test data
    # NOTE: can work on alternate 2-n round strategies here
    y_pred_test = model.predict(X_test)
    y_std_test = np.zeros(len(y_pred_test))

    # calculate metrics
    train_error = mean_squared_error(y_train, y_pred_train)
    test_error = None if experimental else mean_squared_error(y_test, y_pred_test)
    # compute train and test r^2
    train_r_squared = r2_score(y_train, y_pred_train)
    test_r_squared = None if experimental else r2_score(y_test, y_pred_test)
    if regression_type in ['linear', 'neuralnet', 'randomforest', 'gradientboosting', 'lightgbm', 'catboost', 'xgboost','ngboost',
                           'knn', 'gp']:
        alpha = 0
    else:
        alpha = model.alpha_

    dist_metric_train = cdist(X_train, X_test, metric='euclidean').min(axis=1)
    dist_metric_test = None if experimental else cdist(X_test, X_train, metric='euclidean').min(axis=1)

    # combine predicted and actual thermostability values with sequence IDs into a new dataframe
    df_train = pd.DataFrame({'variant': labels.variant[idx_train], 'y_pred': y_pred_train, 'y_actual': y_train, 
                             'y_actual_scaled': y_train_activity_scaled, 'y_actual_binary': y_train_activity_binary,
                             'dist_metric': dist_metric_train, 'std_predictions': y_std_train})
    df_test = pd.DataFrame({'variant': labels.variant[idx_test], 'y_pred': y_pred_test, 'y_actual': y_test, 
                            'y_actual_scaled': y_test_activity_scaled, 'y_actual_binary': y_test_activity_binary,
                            'dist_metric': dist_metric_test, 'std_predictions': y_std_test})
    df_all = pd.concat([df_train, df_test])

    df_sorted_all = df_all.sort_values('y_pred', ascending=False).reset_index(drop=True)

    # Get this round variants
    this_round_variants = df_train.variant

    # Calculate additional metrics
    median_activity_scaled = df_sorted_all.loc[:final_round, 'y_actual_scaled'].median()
    top_activity_scaled = df_sorted_all.loc[:final_round, 'y_actual_scaled'].max()
    top_variant = df_sorted_all.loc[df_sorted_all['y_actual_scaled'] == top_activity_scaled, 'variant'].values[0]
    top_final_round_variants = ",".join(df_sorted_all.loc[:final_round, 'variant'].tolist())
    spearman_corr = df_sorted_all[['y_pred', 'y_actual']].corr(method='spearman').iloc[0, 1]
    activity_binary_percentage = df_sorted_all.loc[:final_round, 'y_actual_binary'].mean()

    if experimental:
        return this_round_variants, df_test, df_sorted_all
    else:
        return train_error, test_error, train_r_squared, test_r_squared, alpha, median_activity_scaled, top_activity_scaled, top_variant, top_final_round_variants, activity_binary_percentage, spearman_corr, df_test, this_round_variants

