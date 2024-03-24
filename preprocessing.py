#!/usr/bin/env python
# coding: utf-8

# # Preprocessing

# ## Imports

# In[1]:

def run_preproc():
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine
    from collections import Counter

    from sklearn.metrics import accuracy_score, balanced_accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn import preprocessing
    from imblearn.over_sampling import RandomOverSampler

    # import function from local cleaning.py for column renaming
    from cleaning import col_mapper

    # Initialize engine connecting to the SQLite database
    engine = create_engine('sqlite:///resources/cleaned.db')

    # SQL query
    query = 'SELECT * FROM main'

    # Execute query and read the data into a DataFrame
    df = pd.read_sql_query(query, con=engine)

    # Log the beginning of preprocessing
    print('running preprocessing...')

    # set uuid as index
    df = df.set_index('uuid')
    #df.head(2)

    # making a copy of the df imported from SQL
    df_encoded = df.copy()

    # ## Encoding
    # Converting objects into numeric for ML

    # making yes/no columns binary
    columns_for_conversion = ['instrumentalist',
                            'composer',
                            'while_working',
                            'exploratory',
                            'foreign_languages'
                            ]

    for col in columns_for_conversion:
        df_encoded[col] = df_encoded[col].map({
            'Yes': 1,
            'No' : 0
            })

    #df_encoded.head(2)

    # change frequency_<genre> values to numeric
    frequency_mapping = {
        'Never': 0,
        'Rarely': 1,
        'Sometimes': 2,
        'Very frequently': 3
    }

    # loop to change all frequency_<genre> columns
    for col in df_encoded.columns:
        if col.startswith('frequency_'):
            df_encoded[col] = df_encoded[col].map(frequency_mapping)

    #df_encoded.head(2)

    # cols_for_processing = df_encoded.columns.drop('uuid')
    df_encoded = pd.get_dummies(df_encoded)#[cols_for_processing])
    #df_encoded.head(2)



    df_encoded.rename(columns=col_mapper, inplace=True)
    print(df_encoded.columns)


    # Define testing and training data
    # Split, scale, and resample.

    # ### I. Splitting encoded data into training and test data

    # define target and feature data
    target_col = 'music_effects'

    y = df_encoded[target_col].values
    X = df_encoded.drop(columns=target_col).values


    # split into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=17)

    print(f'Training features shape: {X_train.shape}')
    print(f'Training targets shape: {y_train.shape}')
    print(f'Testing features shape: {X_test.shape}')
    print(f'Testing targets shape: {y_test.shape}')


    # ### II. Scale

    # Define and instantiate scaler
    scaler = preprocessing.StandardScaler().fit(X_train)
    #scaler

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(len(X_train_scaled))

    # ### III. Resample with imbalamced-learn

    print(df_encoded['music_effects'].value_counts())

    ros = RandomOverSampler(random_state=0)
    X_resampled, y_resampled = ros.fit_resample(X_train_scaled, y_train)
    print(sorted(Counter(y_resampled).items()))

    return X_resampled, X_test_scaled, y_resampled, y_test

    print('exported successfully from preprocessing.py')

# Run script
run_preproc()
