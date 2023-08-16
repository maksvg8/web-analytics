import datetime
import numpy as np
import pandas as pd
from credentials import DATA_DIRECTORY

class CustomReport:
    def __init__(self,
                report_name: str,
                project_name: str = "ED",
                report_type: str = "default"):
        self.at_report_name: str = report_name
        self.at_project_name: str = project_name
        self.at_report_type: str = report_type
        self.at_file_name: str = None
        dt_today = datetime.date.today()
        dt_yesterday = str(dt_today - datetime.timedelta(days=1))
        self.at_start_date: str = dt_yesterday
        self.at_end_date: str = dt_yesterday
        self.at_report_df = pd.DataFrame()


    def create_file_name(self):
        self.at_file_name: str = f"{self.at_project_name}_{self.at_report_type}_{self.at_report_name}"

    
    def overwriting_old_csv_report(self, df=pd.DataFrame(), file_name=None):
        '''if the method was called without arguments, then the values from the attributes are used

        '''
        # TODO Добавить возможность удаления дубликатов
        if df.empty == True:
            df = self.at_report_df
        if file_name is None:
            self.create_file_name()
            file_name = self.at_file_name
        file_path = f"{DATA_DIRECTORY}{file_name}.csv"
        try:
            old_df = pd.read_csv(file_path)
        except:
            df.to_csv(file_path, index=False)
        else:
            df = pd.concat([old_df, df])
            df.to_csv(file_path, index=False)
        print("Report exported to csv")
        return df
