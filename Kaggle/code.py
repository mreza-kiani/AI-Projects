import pandas as pd

train = pd.read_json('train.json')
print("train length:", len(train))
print(train.head())

test = pd.read_json('test.json')
print("test length:", len(test))
print(test.head())

import numpy as np
import pandas as pd

train.loc[train['bathrooms'] > 3, ['bathrooms']] = 3

train.loc[train['bedrooms'] < 6, ['bedrooms']] = 6

up_price = train.quantile(0.99).price
train.loc[train['price'] > up_price, ['price']] = up_price

train['ppr'] = train['price'] / (train['bathrooms'] + train['bedrooms'] + 1)

up_latitude = train.quantile(0.99).latitude
low_latitude = train.quantile(0.01).latitude
train.loc[train['latitude'] > up_latitude, ['latitude']] = up_latitude
train.loc[train['latitude'] < low_latitude, ['latitude']] = low_latitude

up_longitude = train.quantile(0.99).longitude
low_longitude = train.quantile(0.01).longitude
train.loc[train['longitude'] > up_longitude, ['longitude']] = up_longitude
train.loc[train['longitude'] < low_longitude, ['longitude']] = low_longitude

train['created'] = pd.to_datetime(train['created'])
train['date_created'] = train['created'].dt.date
date_feature_count = train['date_created'].value_counts()

train['hour_created'] = train['created'].dt.hour
hour_feature_count = train['hour_created'].value_counts()

train['photos_cnt'] = train['photos'].apply(len)
train.loc[train['photos_cnt'] > 14, ['photos_cnt']] = 14

train['features_cnt'] = train['features'].apply(len)
features_cnt = train['features_cnt'].value_counts()
train.loc[train['features_cnt'] > 16, ['features_cnt']] = 16

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss

def prepare_data(df):
  fearures = ['bathrooms', 'bedrooms', 'latitude', 'longitude', 'price',
         'photos_cnt', 'features_cnt', 'description_words_cnt']
        # unuseful features: ['created_year', 'created_month', 'created_day'] 
  df['photos_cnt'] = df['photos'].apply(len)
  df['features_cnt'] = df['features'].apply(len)
  df['description_words_cnt'] = df['description'].apply(lambda x: len(x.split(' ')))
  df['created'] = pd.to_datetime(df['created'])
  df['created_year'] = df['created'].dt.year
  df['created_month'] = df['created'].dt.month
  df['created_day'] = df['created'].dt.day
  return df[fearures]

X = prepare_data(train)
Y = train['interest_level']

x_train, x_val, y_train, y_val = train_test_split(X, Y, test_size=0.20)


print("start training random forest")
rf = RandomForestClassifier(n_estimators=1000)
rf.fit(x_train, y_train)
y_val_pred = rf.predict_proba(x_val)
print("loss on validation:", log_loss(y_val, y_val_pred))

x_test = prepare_data(test)
y_test_pred = rf.predict_proba(x_test)

labels = {label: i for i, label in enumerate(rf.classes_)}
print("labels:", labels)

sub = pd.DataFrame()
sub['listing_id'] = test['listing_id']
for label, index in labels.items():
    sub[label] = y_test_pred[:, index]
sub.to_csv("submission_rf.csv", index=False)
print("submission_rf.csv exported")
