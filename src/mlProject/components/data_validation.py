import os
from mlProject import logger
from mlProject.entity.config_entity import DataValidationConfig
import pandas as pd


import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True  # Assume validation passes initially

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)
            all_schema = self.config.all_schema.keys()

            print("Columns in dataset:", all_cols)
            print("Columns in schema:", all_schema)

            for col in all_schema:
                if col not in all_cols:
                    validation_status = False
                    print(f"Column '{col}' not found in dataset.")
                    break

            # Write the final validation status after the loop
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            print("An exception occurred:", e)
            raise e


