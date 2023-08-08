from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_cleaning import DataCleaning
from mlProject import logger



STAGE_NAME = "Data Cleaning stage"

class DataCleaningPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_cleaning_config = config.get_cleaned_data_config()
        data_cleaned = DataCleaning(config=data_cleaning_config)
        data_cleaned.cleaned_data()


    
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataCleaningPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

