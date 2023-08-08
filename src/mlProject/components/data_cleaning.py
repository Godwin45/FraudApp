import os
import os
from mlProject import logger
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from mlProject.entity.config_entity import DataCleaningConfig


class DataCleaning:
    def __init__(self, config: DataCleaningConfig):
        self.config = config


    def cleaned_data(self) -> pd.DataFrame:
      
        df = pd.read_csv(self.config.unzip_data_dir)

        rob_scaler = RobustScaler()

        df['scaled_amount'] = rob_scaler.fit_transform(df['Amount'].values.reshape(-1,1))
        df['scaled_time'] = rob_scaler.fit_transform(df['Time'].values.reshape(-1,1))

        df.drop(['Time','Amount'], axis=1, inplace=True)

        scaled_amount = df['scaled_amount']
        scaled_time = df['scaled_time']

        df.drop(['scaled_amount', 'scaled_time'], axis=1, inplace=True)
        df.insert(0, 'scaled_amount', scaled_amount)
        df.insert(1, 'scaled_time', scaled_time)

        df = df.sample(frac=1)

        fraud_df = df.loc[df['Class'] == 1]
        non_fraud_df = df.loc[df['Class'] == 0][:492]

        normal_distributed_df = pd.concat([fraud_df, non_fraud_df])

        new_df = normal_distributed_df.sample(frac=1, random_state=42)


        v14_fraud = new_df['V14'].loc[new_df['Class'] == 1].values
        q25, q75 = np.percentile(v14_fraud, 25), np.percentile(v14_fraud, 75)
        print('Quartile 25: {} | Quartile 75: {}'.format(q25, q75))
        v14_iqr = q75 - q25
        print('iqr: {}'.format(v14_iqr))

        v14_cut_off = v14_iqr * 1.5
        v14_lower, v14_upper = q25 - v14_cut_off, q75 + v14_cut_off
        outliers = [x for x in v14_fraud if x < v14_lower or x > v14_upper]
        print('Feature V14 Outliers for Fraud Cases: {}'.format(len(outliers)))
        print('V10 outliers:{}'.format(outliers))

        new_df = new_df.drop(new_df[(new_df['V14'] > v14_upper) | (new_df['V14'] < v14_lower)].index)
        print('----' * 44)

        # -----> V12 removing outliers from fraud transactions
        v12_fraud = new_df['V12'].loc[new_df['Class'] == 1].values
        q25, q75 = np.percentile(v12_fraud, 25), np.percentile(v12_fraud, 75)
        v12_iqr = q75 - q25

        v12_cut_off = v12_iqr * 1.5
        v12_lower, v12_upper = q25 - v12_cut_off, q75 + v12_cut_off
        outliers = [x for x in v12_fraud if x < v12_lower or x > v12_upper]
        new_df = new_df.drop(new_df[(new_df['V12'] > v12_upper) | (new_df['V12'] < v12_lower)].index)

        # Removing outliers V10 Feature
        v10_fraud = new_df['V10'].loc[new_df['Class'] == 1].values
        q25, q75 = np.percentile(v10_fraud, 25), np.percentile(v10_fraud, 75)
        v10_iqr = q75 - q25

        v10_cut_off = v10_iqr * 1.5
        v10_lower, v10_upper = q25 - v10_cut_off, q75 + v10_cut_off
        outliers = [x for x in v10_fraud if x < v10_lower or x > v10_upper]
        new_df = new_df.drop(new_df[(new_df['V10'] > v10_upper) | (new_df['V10'] < v10_lower)].index)


        save_path = os.path.join(self.config.root_dir, "new_df.csv")
        new_df.to_csv(save_path, index=False)

        return new_df