import pandas as pd
import numpy as np
from sklearn.naive_bayes import BernoulliNB
import math


from apps import db_onnections


def anomality_model(history,predict):
    '''
    model used: Bernoulli Naive Bayse
    :param history: the dataframe with which fit the model
    :param predict: the element to be used for the prediction
    :return: the probability of the user for the given array.

    '''
    user = predict["display_name"]
    history = history.drop(['timestamp'], axis=1)

    history["display_name"] = np.where(history["display_name"] == user, 1, 0)

    df_target = history[history["display_name"] == 1]
    df_core = history[history["display_name"] == 0]

    df_core = df_core.drop_duplicates() # Reduce the "No-events"

    df = df_target.append(df_core)

    model = BernoulliNB()
    label = df['display_name']
    main = df.drop(['display_name'], axis=1)

    model.fit(main, label)

    #print(user)
    predict = predict.drop(['timestamp', 'display_name'])
    #print("### predict #####")

    output = model.predict_proba(np.array(predict).reshape(1,-1))

    return output[0][1]


def checker_anomalitics():#from_data='2018-01-01', border_data= "2018-06-18", end_date= "2018-06-25"

    history, predict = db_onnections.anomalityDB() #from_data= from_data, border_data= border_data, end_date= end_date)

    dataframe = pd.DataFrame()
    for index, item in predict.iterrows():
        ser = pd.Series()
        ser["Display Name"] = item["display_name"]
        ser['Hostname'] = item['Hostname_']
        ser['Protocol'] = item['Protocol_']
        ser['Subnet'] = item['Subnet_']

        item=item.drop(['Hostname_','Protocol_','Subnet_'])

        proba = anomality_model(history=history, predict=item)

        ser["Probability"] = math.sqrt(proba)

        ser["Time"] = pd.to_datetime(item['timestamp'])
        ser["Time"] = pd.to_datetime(ser["Time"])
        ser['Time'] = ser['Time'].strftime("%Y-%m-%d %H:%M:%S")

        dataframe = dataframe.append(ser, ignore_index=True)

        dataframe = dataframe.sort_values("Probability")
        dataframe = dataframe[["Time", "Display Name", "Subnet", "Protocol", "Hostname", "Probability"]]

        dataframe['Time'] = pd.to_datetime(dataframe['Time'])

    return dataframe
