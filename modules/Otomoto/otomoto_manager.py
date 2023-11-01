from datetime import datetime
import os
from datetime import date

import pandas as pd
from pandas import DataFrame

from modules.Images.s3_link_generator import S3LinkGenerator
from modules.Otomoto.otomoto_api import OtomotoApi
from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager

ROWS_TO_SKIP = 2236
ROWS_TO_READ = 1
DATETIME = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
REPORT_FILE_PATH = f"/tmp/Reports/report {DATETIME}.txt"


class OtomotoManager:
    def __init__(self, excel_file_name, sheet_name):
        self.working_data_table = None
        self.df1 = None
        # self.first_126_values = None
        self.file_name = excel_file_name
        self.sheet_name = sheet_name
        self.excel_handler = ExcelHandler()
        self.otomoto_api = OtomotoApi()
        self.one_drive_manager = OneDriveManager()
        self.s3_link_generator = S3LinkGenerator()

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
            list_of_adverts_dict.append(advert_dict)
            advert_dict = {}
        return list_of_adverts_dict

    def _create_report(self, list_created_adverts_id, list_of_errors, is_unexpected: bool):
        try:
            reports_folder = os.path.join(os.getcwd(), "Reports")

            if not os.path.exists(reports_folder):
                os.makedirs(reports_folder)

            if not is_unexpected:
                full_path = os.path.join(reports_folder, f"report{date.today()}.txt")
            else:
                full_path = os.path.join(reports_folder, f"unexpected report{date.today()}.txt")

            with open(full_path, 'w') as file:
                file.write("List of created ads:\n")
                for product_id, advert_id in list_created_adverts_id:
                    file.write(f"Stock number: {product_id}, ID created ads: {advert_id}\n")

                file.write("\nError List:\n")
                for product_id, error_message in list_of_errors:
                    file.write(f"Stock number: {product_id}, Error message: {error_message}\n")

            print(f"Репорт збережено у файлі {full_path}")
            with open(full_path, 'r') as file:
                report_contents = file.read()
                print(report_contents)
        except Exception as e:
            print(f"Сталася помилка при створенні звіту: {e}")

    def _create_basic_report(self, message: str) -> str:
        # Шлях до папки та файлу
        folder_path = "/tmp/Reports"
        file_path = REPORT_FILE_PATH

        # Перевірка і створення папки, якщо її немає
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Відкриття файлу та запис повідомлення у новий рядок
        with open(file_path, "a") as file:
            file.write(message + "\n")
        return file_path

    def _post_adverts(self, list_ready_to_create: list[DataFrame]) -> tuple[list, list]:
        list_created_adverts_id = []
        list_of_errors = []
        adverts_dict = self._convert_adverts_to_dict(list_ready_to_create)
        for item in adverts_dict:
            if (item.get("номер на складі") == 0 and item.get("title") == 0 and item.get(
                    "description") == 0 and item.get("price") == 0 and item.get("new_used") == 0 and item.get(
                    "manufacturer")):
                return list_created_adverts_id, list_of_errors
            try:
                created_advert_id = self.otomoto_api.create_otomoto_advert(product_id=item.get("номер на складі"),
                                                                           title=item.get("title"),
                                                                           description=item.get("description"),
                                                                           price=item.get("price"),
                                                                           new_used=item.get("new_used"),
                                                                           manufacturer=item.get("manufacturer"))
                if "Error:" in created_advert_id:
                    nubmer_in_stock = item.get("номер на складі")
                    message = f"{nubmer_in_stock}, {created_advert_id}"
                    self._create_basic_report(message=message)
                    # list_of_errors.append((item.get("номер на складі"), created_advert_id))
                else:
                    nubmer_in_stock = item.get("номер на складі")
                    message = f"{nubmer_in_stock}, Advert successfully posted with ID: {created_advert_id}"
                    self._create_basic_report(message=message)
                    test_excel_file_path = "/tmp/New tested file.xlsx"
                    self.excel_handler.set_otomoto_id_by_storage_id(df=self.working_data_table,
                                                                    otomoto_id=created_advert_id,
                                                                    storage_id=item.get("номер на складі"),
                                                                    excel_file_path=test_excel_file_path)

                    main_excel_file_path = "/tmp/Main excel file.xlsx"
                    self.excel_handler.set_otomoto_id_by_storage_id(df=self.df1,
                                                                    otomoto_id=created_advert_id,
                                                                    storage_id=item.get("номер на складі"),
                                                                    excel_file_path=main_excel_file_path)


            except Exception as e:
                print(f"Помилка при створенні оголошення {item}: {e}")
                self._create_basic_report(f"Unexpected error {item} : {e}")

        try:
            main_excel_file_path = "/tmp/Main excel file.xlsx"

            self.one_drive_manager.upload_file_to_onedrive(file_path=main_excel_file_path,
                                                           rows_to_read=ROWS_TO_READ,
                                                           rows_to_skip=ROWS_TO_SKIP)
            self.s3_link_generator.upload_file_to_s3(file_path=main_excel_file_path,
                                                     rows_to_read=ROWS_TO_READ,
                                                     rows_to_skip=ROWS_TO_SKIP)
        except Exception as e:
            print(e)
        try:
            reports_file_name = REPORT_FILE_PATH
            self.one_drive_manager.upload_file_to_onedrive(file_path=reports_file_name,
                                                           rows_to_read=ROWS_TO_READ,
                                                           rows_to_skip=ROWS_TO_SKIP)
            self.s3_link_generator.upload_file_to_s3(file_path=reports_file_name,
                                                     rows_to_read=ROWS_TO_READ,
                                                     rows_to_skip=ROWS_TO_SKIP)
        except Exception as e:
            print(e)

        try:
            file_path = "/tmp/New tested file.xlsx"
            self.one_drive_manager.upload_file_to_onedrive(file_path=file_path,
                                                           rows_to_read=ROWS_TO_READ,
                                                           rows_to_skip=ROWS_TO_SKIP)
            self.s3_link_generator.upload_file_to_s3(file_path=file_path,
                                                     rows_to_read=ROWS_TO_READ,
                                                     rows_to_skip=ROWS_TO_SKIP)
        except Exception as e:
            print(e)

        return list_created_adverts_id, list_of_errors

    def create_list_need_to_create(self, in_stock: list[DataFrame]) -> tuple[list[DataFrame], list[DataFrame]]:
        list_check_need_to_edit = []  # Ліст для товарів з непорожнім полем "ID otomoto"
        list_ready_to_create = []  # Ліст для товарів з порожнім полем "ID otomoto"

        for item in in_stock:
            if not pd.isna(item['ID otomoto']):  # Перевірка, чи поле "ID otomoto" не порожнє
                list_check_need_to_edit.append(item)
            else:
                list_ready_to_create.append(item)

        return list_check_need_to_edit, list_ready_to_create

    def read_selected_rows_from_excel(self, file_path, rows_to_skip: int, rows_to_read):
        if rows_to_skip > 0:
            working_data_table = pd.read_excel(file_path, skiprows=range(1, rows_to_skip), nrows=rows_to_read)
        else:
            working_data_table = pd.read_excel(file_path, nrows=rows_to_read)
        return working_data_table

    def create_page(self):
        file_content = self.excel_handler.get_exel_file(self.file_name)
        # create file
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)
        self.excel_handler.create_file_on_data(file_content=file_content, file_name="New tested file.xlsx")

        main_excel_file_path = self.excel_handler.get_file_path(file_name=self.file_name)
        self.df1 = pd.read_excel(main_excel_file_path)

        # self.first_126_values = self.df1.head(126)
        self.working_data_table = self.read_selected_rows_from_excel(file_path=main_excel_file_path,
                                                                     rows_to_skip=ROWS_TO_SKIP,
                                                                     rows_to_read=ROWS_TO_READ)

        in_stock, out_of_stock, invalid_quantity = self.create_lists_of_produts(self.working_data_table)
        list_check_need_to_edit, list_ready_to_create = self.create_list_need_to_create(in_stock)
        print(f"adverts to create:", len(list_ready_to_create))
        self._create_basic_report(message=f"adverts to create: {len(list_ready_to_create)}")
        self._create_basic_report(message=str(list_ready_to_create))
        self._post_adverts(list_ready_to_create)

        print("Page created")
        return self

    def create_list_to_create_in_s3(self):
        file_content = self.excel_handler.get_exel_file(self.file_name)
        # create file
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)
        main_excel_file_path = self.excel_handler.get_file_path(file_name=self.file_name)
        self.working_data_table = self.read_selected_rows_from_excel(file_path=main_excel_file_path,
                                                                     rows_to_skip=0,
                                                                     rows_to_read=6400)
        in_stock, out_of_stock, invalid_quantity = self.create_lists_of_produts(self.working_data_table)
        list_check_need_to_edit, list_ready_to_create = self.create_list_need_to_create(in_stock)

        dict_ready_to_create = self._convert_adverts_to_dict(list_ready_to_create=list_ready_to_create)
        test_file_path = "/tmp/my_test_file.txt"
        count = 0
        for item in dict_ready_to_create:
            print(item.get('номер на складі'))
            with open(test_file_path, "a") as file:
                file.write(str(item.get('номер на складі')) + "\n")
            count += 1
            if count % 25 == 0:
                with open(test_file_path, "a") as file:
                    file.write("-" * 50 + "\n")
        self.s3_link_generator.upload_file_to_s3(file_path=test_file_path,
                                                 rows_to_read=None,
                                                 rows_to_skip=None)