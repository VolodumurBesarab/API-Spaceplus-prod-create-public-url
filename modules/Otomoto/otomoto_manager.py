import os

import pandas as pd
from pandas import DataFrame

from modules.excel_handler import ExcelHandler

def read_page_line():

    status = "Error"
    # read article count in storage
        # read article id
            # create product
            # read other atribbutes
                #edit atributes
    #

    status = "Complete"
    return status


class OtomotoManager:
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.excel_handler = ExcelHandler()

    def create_lists_of_produts(self, df1) -> tuple[list[DataFrame], list[DataFrame], list[DataFrame]]:
        in_stock = []
        out_of_stock = []
        invalid_quantity = []
        for index, row in df1.head(100).iterrows():
            if row['наявність на складі'] < 0:
                invalid_quantity.append(row)
            elif row['наявність на складі'] == 0:
                out_of_stock.append(row)
            elif row['наявність на складі'] > 0:
                in_stock.append(row)
        return in_stock, out_of_stock, invalid_quantity

    def read_page_line(self):
        status = "Error"

        # read article count in storage
            # read article id
                # create product
                # read other atribbutes
            # edit atributes
        #

        status = "Complete"
        return status

    def _create_page(self):
        file_content = self.excel_handler.get_exel_file(self.file_name)
        # create file
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)

        file_path = self.excel_handler.get_file_path(file_name=self.file_name)
        df1 = pd.read_excel(file_path)

        first_100_values = df1.head(100)

        in_stock, out_of_stock, invalid_quantity = self.create_lists_of_produts(first_100_values)
        print(len(in_stock), len(out_of_stock), len(invalid_quantity))

        columns_to_display = ["номер на складі", "наявність на складі", "title", "description", "price", "new_used"]

        num_rows, num_columns = first_100_values.shape
        print(num_rows, num_columns)



        # first_row_values = df1.iloc[32]
        # for line_count
        #
        # for column_name, value in first_row_values.items():
        #     print(f"{column_name}: {value}")






        # for column in df1.columns:
        #     print(f"Column: {column}")
        #     for value in df1[column]:
        #         print(value)
        print("Page created")
        return self

    def read_all_items(self):
        self._create_page()

        pass
