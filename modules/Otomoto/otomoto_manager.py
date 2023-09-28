import os

import pandas as pd
from pandas import DataFrame

from modules.Otomoto.otomoto_api import OtomotoApi
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
        self.otomoto_api = OtomotoApi()

    def create_lists_of_produts(self, df1) -> tuple[list[DataFrame], list[DataFrame], list[DataFrame]]:
        in_stock = []
        out_of_stock = []
        invalid_quantity = []
        for index, row in df1.iterrows():
            if row['наявність на складі'] < 0:
                invalid_quantity.append(row)
            elif row['наявність на складі'] == 0:
                out_of_stock.append(row)
            elif row['наявність на складі'] > 0:
                in_stock.append(row)
        return in_stock, out_of_stock, invalid_quantity

    def _convert_adverts_to_dict(self, list_ready_to_create: list[DataFrame]) -> list[dict]:
        advert_dict = {}
        list_of_adverts_dict = []
        for row in list_ready_to_create:
            for column_name, value in row.items():
                advert_dict.update({column_name: value})
            # print(advert_dict)
            list_of_adverts_dict.append(advert_dict)
            advert_dict = {}
        return list_of_adverts_dict

    def post_adverts(self, list_ready_to_create: list[DataFrame]):
        testttt = self._convert_adverts_to_dict(list_ready_to_create)
        print(testttt)
        # advert_dict = {}
        # for row in list_ready_to_create:
        #     for column_name, value in row.items():
        #         advert_dict.update({column_name: value})
        #     print(advert_dict)
        #     advert_dict = {}
                # print(f"{column_name}: {value}")
        # self.otomoto_api.create_otomoto_advert()

    def create_list_need_to_create(self, in_stock: list[DataFrame]) -> tuple[list[DataFrame], list[DataFrame]]:
        list_check_need_to_edit = []  # Ліст для товарів з непорожнім полем "ID otomoto"
        list_ready_to_create = []  # Ліст для товарів з порожнім полем "ID otomoto"

        for item in in_stock:
            if not pd.isna(item['ID otomoto']):  # Перевірка, чи поле "ID otomoto" не порожнє
                list_check_need_to_edit.append(item)
            else:
                list_ready_to_create.append(item)

        return list_check_need_to_edit, list_ready_to_create

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

        # self.otomoto_api.

        columns_to_display = ["номер на складі", "наявність на складі", "title", "description", "price", "new_used"]

        # num_rows, num_columns = first_100_values.shape
        # print(num_rows, num_columns)

        list_check_need_to_edit, list_ready_to_create = self.create_list_need_to_create(in_stock)
        print("edit", len(list_check_need_to_edit))
        print("create", len(list_ready_to_create))

        self.post_adverts(list_ready_to_create)



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
