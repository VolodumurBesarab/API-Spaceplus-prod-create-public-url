from typing import Tuple, List

import pandas as pd
from pandas import DataFrame, Series

from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager
from modules.otomoto.otomoto_manager import OtomotoManager

EXCEL_FILE_NAME = r"otomoto.xlsx"
SHEET_NAME = "Spaceplus"


class ListCreator:
    def __init__(self):
        # otomoto_manager = OtomotoManager(excel_file_name="otomoto.xlsx", sheet_name=None)
        self.one_drive_manager = OneDriveManager()
        self.excel_handler = ExcelHandler()

    def create_lists_of_produts(self, df1: DataFrame) -> tuple[list[Series], list[Series], list[Series]]:
        in_stock = []
        out_of_stock = []
        invalid_quantity = []
        for index, row in df1.iterrows():
            if row['stock availability'] == 0 or row['stock availability'] == 2:
                out_of_stock.append(row)
            elif row['stock availability'] == 1:
                in_stock.append(row)
            else:
                invalid_quantity.append(row)
        return in_stock, out_of_stock, invalid_quantity

    def get_excel(self) -> DataFrame:
        df1 = None
        # if not self.one_drive_manager.is_current_day_folder_created():
        #     self.one_drive_manager.create_current_day_folder()
        #
        # if not self.one_drive_manager.is_list_folder_created():
        #     self.one_drive_manager.create_lists_folder()
        if True:

            file_content = self.excel_handler.get_exel_file(EXCEL_FILE_NAME)

            self.excel_handler.create_file_on_data(file_content=file_content, file_name=EXCEL_FILE_NAME)

            main_excel_file_path = self.excel_handler.get_file_path(file_name=EXCEL_FILE_NAME)
            # df1 = pd.read_excel(main_excel_file_path)  # file to read
            df1 = pd.read_excel(io=main_excel_file_path, sheet_name=SHEET_NAME)
        return df1

    def create_lists(self):
        df1 = self.get_excel()
        in_stock, out_of_stock, invalid_quantity = self.create_lists_of_produts(df1=df1)
        print(len(in_stock))
        # print(in_stock["stock number"])

list_creator = ListCreator()
list_creator.create_lists()
