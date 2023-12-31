import pandas as pd
from src.model_pipeline.preprocessing import preprocess_data
from src.model_pipeline.preprocessing import create_features
from src.model_pipeline import utils, model_training
from src.model_pipeline.model_training import data_split
import warnings

warnings.filterwarnings("ignore")


def mlpipeline():
    """
        Calls preprocessing.py function for data cleaning, data preprocessing,
        feature extraction and feature selection
        Calls model_training.py to train the data on ML Algorithms

        Returns
        -------
        True - on Successful execution of function

    """

    try:
        df = utils.read_data('../input/Pune Real Estate Data.xlsx')

        # preprocess data
        preprocessed_df = preprocess_data(df)

        # generate features
        created_feature_df = create_features(preprocessed_df)

        # Splitting the data for model training and test
        x_train, x_test, y_train, y_test = data_split(created_feature_df, "Price_In_Lakhs", 0.3, 1234)

        # Training Models on Linear Model and Regularized Models
        output_df, linear_estimator, ridge_estimator, lasso_estimator = model_training.regression_model_training(
            x_train, x_test, y_train, y_test)

        # Training Models on Voting Regressor
        model_estimators = [('lr', linear_estimator), ('rid', ridge_estimator), ('lasso', lasso_estimator)]
        df_dict, voting_ensemble = model_training.ensemble_model_training(x_train, x_test, y_train, y_test,
                                                                          model_estimators)
        output_df = pd.concat([output_df, df_dict], ignore_index=True)

        # saving model
        utils.pickle_dump(voting_ensemble, '../output/property_price_prediction_voting.sav')
        print("Voting Regressor model has been trained and saved in output folder!")
    except Exception as e:
        print('Error in model_training_engine.mlpipeline function', e)
    else:
        return True
