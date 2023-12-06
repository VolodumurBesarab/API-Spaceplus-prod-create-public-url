import json
from datetime import datetime
import os
from datetime import date

import boto3
import pandas as pd
from pandas import DataFrame

from modules.Images.s3_link_generator import S3LinkGenerator
from modules.Otomoto.otomoto_api import OtomotoApi
from modules.auth_manager import AuthManager
from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager

ROWS_TO_SKIP = None
ROWS_TO_READ = None
DATETIME = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
REPORT_FILE_PATH = f"/tmp/Reports/basic_report {DATETIME}.txt"
# EXCEL_FILE_PATH = f"/tmp/New tested file {ROWS_TO_SKIP+1}-{ROWS_TO_READ+ROWS_TO_SKIP}.xlsx"
EXCEL_FILE_PATH = f"/tmp/Excel working data table.xlsx"


class OtomotoManager:
    def __init__(self, excel_file_name, sheet_name):
        self.df2 = None
        self.working_data_table = None
        self.df1 = None
        # self.first_126_values = None
        self.file_name = excel_file_name
        self.sheet_name = sheet_name
        self.excel_handler = ExcelHandler()
        self.otomoto_api = OtomotoApi()
        self.one_drive_manager = OneDriveManager()
        self.s3_link_generator = S3LinkGenerator()
        self.auth_manager = AuthManager()

    def create_lists_of_produts(self, df1) -> tuple[list[DataFrame], list[DataFrame], list[DataFrame]]:
        in_stock = []
        out_of_stock = []
        invalid_quantity = []
        for index, row in df1.iterrows():
            if row['наявність на складі'] == 0:
                out_of_stock.append(row)
            elif row['наявність на складі'] == 1:
                in_stock.append(row)
            else:
                invalid_quantity.append(row)
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

    def set_char_by_number_in_stock(self, number_in_stock: str, char):
        file_path = "/tmp/ready_to_create.txt"
        if not os.path.isfile(file_path):
            self.one_drive_manager.download_file_to_tmp(
                path=f"/Holland/Reports/{self.one_drive_manager.current_day}/Lists/ready_to_create.txt",
                file_name="ready_to_create.txt")

        with open(file_path, "r") as file:
            lines = file.readlines()

        with open(file_path, "w") as file:
            for line in lines:
                if number_in_stock in line:
                    line = line.rstrip('\n ') + char + '\n'
                file.write(line)

    def _create_report(self, list_created_adverts_id, list_of_errors, is_unexpected: bool):
        try:
            reports_folder = os.path.join(os.getcwd(), "Reports")

            if not os.path.exists(reports_folder):
                os.makedirs(reports_folder)

            if not is_unexpected:
                full_path = os.path.join(reports_folder, f"basic_report{date.today()}.txt")
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

    def _post_adverts(self, list_ready_to_create: DataFrame):
        for index, row in list_ready_to_create.iterrows():
            nubmer_in_stock = row.get("номер на складі")
            try:
                # call lambda here
                advert_dict = {
                    "product_id": row.get("номер на складі"),
                    "title": row.get("title"),
                    "description": row.get("description"),
                    "price": row.get("price"),
                    "new_used": row.get("new_used"),
                    "manufacturer": row.get("manufacturer"),
                }
                advert_json = json.dumps(advert_dict)

                client = boto3.client('lambda')
                response = client.invoke(
                    FunctionName='prod-spaceplus-create-advert',
                    InvocationType='Event',
                    Payload=advert_json,
                )
                print(response)

                # created_advert_id = self.otomoto_api.create_otomoto_advert(product_id=row.get("номер на складі"),
                #                                                            title=row.get("title"),
                #                                                            description=row.get("description"),
                #                                                            price=row.get("price"),
                #                                                            new_used=row.get("new_used"),
                #                                                            manufacturer=row.get("manufacturer"))
                # if "Error:" in created_advert_id:
                #     message = f"{nubmer_in_stock}, {created_advert_id}"
                #     self._create_basic_report(message=message)
                #     self.set_char_by_number_in_stock(number_in_stock=str(nubmer_in_stock), char="-")
                #     # list_of_errors.append((item.get("номер на складі"), created_advert_id))
                # else:
                #     message = f"{nubmer_in_stock}, Advert successfully posted with ID: {created_advert_id}"
                #     self._create_basic_report(message=message)
                #     self.set_char_by_number_in_stock(number_in_stock=str(nubmer_in_stock), char="+")

            except Exception as e:
                print(f"Error with create advert {nubmer_in_stock}: {e}")
                self._create_basic_report(f"Unexpected error {nubmer_in_stock} : {e}")

        try:
            reports_file_name = REPORT_FILE_PATH
            self.one_drive_manager.upload_file_to_onedrive(file_path="/tmp/ready_to_create.txt",
                                                           path_after_current_day="Lists")

            self.one_drive_manager.upload_file_to_onedrive(file_path=reports_file_name,
                                                           rows_to_read=ROWS_TO_READ,
                                                           rows_to_skip=ROWS_TO_SKIP)

            self.s3_link_generator.upload_file_to_s3(file_path=reports_file_name,
                                                     rows_to_read=ROWS_TO_READ,
                                                     rows_to_skip=ROWS_TO_SKIP)
        except Exception as e:
            print(e)

        try:
            file_path = EXCEL_FILE_PATH
            self.one_drive_manager.upload_file_to_onedrive(file_path=file_path,
                                                           rows_to_read=ROWS_TO_READ,
                                                           rows_to_skip=ROWS_TO_SKIP)
            self.s3_link_generator.upload_file_to_s3(file_path=file_path,
                                                     rows_to_read=ROWS_TO_READ,
                                                     rows_to_skip=ROWS_TO_SKIP)
        except Exception as e:
            print(e)

    def create_list_need_to_create(self, in_stock: list[DataFrame]) -> tuple[list[DataFrame], list[DataFrame]]:
        list_check_need_to_edit = []
        list_ready_to_create = []
        with open('/tmp/adverts_dict.json', 'r') as json_file:
            adverts_dict: dict = json.load(json_file)

        for item in in_stock:
            in_stock_id = str(item["номер на складі"])
            if in_stock_id in adverts_dict.keys():
                list_check_need_to_edit.append(item)
            else:
                list_ready_to_create.append(item)
        return list_check_need_to_edit, list_ready_to_create

    def create_list_need_to_delete(self, out_of_stock: list[DataFrame], whole_table: DataFrame) -> list[DataFrame]:
        list_need_to_delete = []
        with open('/tmp/adverts_dict.json', 'r') as json_file:
            adverts_dict: dict = json.load(json_file)

        for item in out_of_stock:
            in_stock_id = str(item['номер на складі'])
            if in_stock_id in adverts_dict.keys():
                if any((whole_table['номер на складі'].astype(str) == in_stock_id) & (whole_table['наявність на складі'] == 1)):
                    continue
                list_need_to_delete.append(item)
        return list_need_to_delete

    def read_selected_rows_from_excel(self, file_path, rows_to_skip: int, rows_to_read: int):
        if rows_to_skip > 0:
            working_data_table = pd.read_excel(file_path, skiprows=range(1, rows_to_skip), nrows=rows_to_read)
        else:
            working_data_table = pd.read_excel(file_path, nrows=rows_to_read)
        return working_data_table

    def upload_list_to_onedrive(self, uploaded_list: list[DataFrame], uploaded_list_path: str):
        column_name = "номер на складі"
        uploaded_list_values = []

        if uploaded_list:
            for df_check in uploaded_list:
                uploaded_list_values.append(df_check[column_name])

        df_uploaded_list_values = pd.DataFrame({column_name: uploaded_list_values})
        df_uploaded_list_values.to_csv(uploaded_list_path, index=False)
        self.one_drive_manager.upload_file_to_onedrive(file_path=uploaded_list_path,
                                                       path_after_current_day="Lists")

    def find_current_line_in_json(self, json_file_path, current_line: str):
        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            for key, value in data.items():
                if str(current_line) == str(key):
                    return value

        except Exception as e:
            print(f'Cant find in json: {e}')

    def delete_adverts(self) -> bool:
        is_deleted = False
        if not os.path.exists("/tmp/list_need_to_delete.txt"):
            self.one_drive_manager.download_file_to_tmp(path=f"/Holland/Reports/{self.one_drive_manager.current_day}/Lists/list_need_to_delete.txt",
                                                        file_name="list_need_to_delete.txt")
        if not os.path.exists("/tmp/list_need_to_delete.txt"):
            self.one_drive_manager.download_file_to_tmp(path=f"/Holland/Reports/{self.one_drive_manager.current_day}/Lists/list_need_to_delete.txt",
                                                        file_name="list_need_to_delete.txt")

        if not os.path.exists("/tmp/adverts_dict.json"):
            self.one_drive_manager.download_file_to_tmp(path="/Holland/API-Spaceplus/adverts_dict.json",
                                                        file_name="adverts_dict.json")

        with open("/tmp/list_need_to_delete.txt", "r") as otomoto_id_del:
            lines = otomoto_id_del.readlines()

        updated_lines = []

        for line in lines:
            current_line = line.strip()
            otomoto_id = self.find_current_line_in_json(json_file_path="/tmp/adverts_dict.json",
                                                        current_line=current_line)
            response = self.otomoto_api.delete_advert(in_stock_id=current_line, otomoto_id=otomoto_id)
            print(f"{response.status_code} : {current_line}")
            if response.status_code == 204:
                is_deleted = True
                updated_lines.append(f"{current_line} +\n")
            else:
                updated_lines.append(f"{current_line} -\n")

        with open("/tmp/list_need_to_delete.txt", "w") as otomoto_id_del:
            otomoto_id_del.writelines(updated_lines)
        self.one_drive_manager.upload_file_to_onedrive(file_path="/tmp/adverts_dict.json",
                                                       onedrive_path="Holland/API-Spaceplus")
        self.one_drive_manager.upload_file_to_onedrive(file_path="/tmp/list_need_to_delete.txt",
                                                       path_after_current_day="Lists")

        return is_deleted
    def create_lists(self):
        file_content = self.excel_handler.get_exel_file(self.file_name)
        # create file
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)
        self.excel_handler.create_file_on_data(file_content=file_content, file_name="Excel working data table.xlsx")

        main_excel_file_path = self.excel_handler.get_file_path(file_name=self.file_name)
        self.df1 = pd.read_excel(main_excel_file_path)  # file to read

        if not self.one_drive_manager.is_current_day_folder_created():
            self.one_drive_manager.create_current_day_folder()

        if not self.one_drive_manager.is_list_folder_created():
            self.one_drive_manager.create_lists_folder()
            in_stock, out_of_stock, invalid_quantity = self.create_lists_of_produts(self.df1)
            list_need_to_delete = self.create_list_need_to_delete(out_of_stock=out_of_stock, whole_table=self.df1)
            list_check_need_to_edit, list_ready_to_create = self.create_list_need_to_create(in_stock)

            ready_to_create_path = "/tmp/ready_to_create.txt"
            invalid_quantity_path = "/tmp/invalid_quantity.txt"
            list_need_to_delete_path = "/tmp/list_need_to_delete.txt"

            self.upload_list_to_onedrive(uploaded_list=list_ready_to_create, uploaded_list_path=ready_to_create_path)
            self.upload_list_to_onedrive(uploaded_list=invalid_quantity, uploaded_list_path=invalid_quantity_path)
            self.upload_list_to_onedrive(uploaded_list=list_need_to_delete, uploaded_list_path=list_need_to_delete_path)
        else:
            self.one_drive_manager.download_file_to_tmp(path=f"/Holland/Reports/{self.one_drive_manager.current_day}/Lists/ready_to_create.txt",
                                                        file_name="ready_to_create.txt")
            self.one_drive_manager.download_file_to_tmp(path=f"/Holland/Reports/{self.one_drive_manager.current_day}/Lists/list_need_to_delete.txt",
                                                        file_name="list_need_to_delete.txt")

    def create_df_from_ready_to_create(self, df: DataFrame, adverts_create_in_one_time=20) -> DataFrame:
        with open('/tmp/ready_to_create.txt', 'r') as file:
            lines = file.readlines()

        counter = 0
        in_stock_numbers = []
        for line in lines:
            if counter >= adverts_create_in_one_time + 1:
                break

            if '+' in line or '-' in line:
                continue
            else:
                counter += 1
            in_stock_numbers.append(line.strip())

        df1 = df[(df['номер на складі'].astype(str).isin(in_stock_numbers)) & (df['наявність на складі'] == 1)].reset_index(drop=True)
        # df1.to_excel('/tmp/df_from_ready_to_create.xlsx', index=False)  # Збереження у файл
        return df1

    def create_next_twenty_adverts(self):
        is_any_deleted = False
        file_content = self.excel_handler.get_exel_file(self.file_name)
        # create file
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)
        self.excel_handler.create_file_on_data(file_content=file_content, file_name="Excel working data table.xlsx")

        main_excel_file_path = self.excel_handler.get_file_path(file_name=self.file_name)
        self.one_drive_manager.download_file_to_tmp(path="/Holland/Final_exel_file.xlsx",
                                                    file_name="Final_exel_file")
        self.one_drive_manager.download_file_to_tmp(path="/Holland/API-Spaceplus/adverts_dict.json",
                                                    file_name="adverts_dict.json")
        df1 = pd.read_excel(main_excel_file_path)  # file to read
        self.create_lists()
        twenty_adverts_from_ready_to_create = self.create_drom_ready_to_create(df1)
        # add variable for twenty_adverts_from_ready_to_create.empty
        if not twenty_adverts_from_ready_to_create.empty:
            print(f"adverts to create:", len(twenty_adverts_from_ready_to_create))
            self._create_basic_report(message=f"adverts to create: {len(twenty_adverts_from_ready_to_create)}")
            self._create_basic_report(message=str(twenty_adverts_from_ready_to_create))
            self._post_adverts(list_ready_to_create=twenty_adverts_from_ready_to_create)
        else:
            is_any_deleted = self.delete_adverts()
        if twenty_adverts_from_ready_to_create.empty and not is_any_deleted:
            self.create_reports_from_base()
            # self.excel_handler.update_excel_from_success_report(self.one_drive_manager.current_day)
        print("Working is done")
        return self

    def create_list_to_create_in_s3(self):
        file_content = self.excel_handler.get_exel_file(self.file_name)
        # create file
        self.excel_handler.create_file_on_data(file_content=file_content, file_name=self.file_name)
        main_excel_file_path = self.excel_handler.get_file_path(file_name=self.file_name)
        # need rework without lines as df = pd.read_excel
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

    def convert_text_to_dict(self, successfully_file_path: str) -> dict:
        with open(successfully_file_path, "r") as success_file:
            lines = success_file.readlines()

        otomoto_ids = {}

        for line in lines:
            if "del" in line:
                continue
            elif not line.strip():
                break
            parts = line.split(", ")
            storage_id = parts[0].strip()

            parts = line.split("ID: ")
            otomoto_id = parts[1].strip()

            if storage_id not in otomoto_ids:
                otomoto_ids[str(storage_id)] = str(otomoto_id)
            else:
                print(F"Cant add {storage_id} : {otomoto_id} to dict")
        return otomoto_ids

    def merge_and_save_one_drive_dict(self, successfully_file_path, json_file_path):
        successfully_file_dict = self.convert_text_to_dict(successfully_file_path=successfully_file_path)
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
        merged_dict = {**successfully_file_dict, **data}
        with open(json_file_path, "w") as output_file:
            json.dump(merged_dict, output_file)

    def create_reports_from_base(self):
        # folder_path = "D:\API-Spaceplus\\tmp\\text_reports4"
        self.one_drive_manager.download_reports_to_tmp()

        folder_path = "/tmp/text_reports"

        successfully_lines = []
        error_lines = []

        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        if "successfully" in line:
                            successfully_lines.append(line)
                        elif "Error:" in line:
                            error_lines.append(line)
                        elif "Unexpected" in line:
                            error_lines.append(line)

        # Відредагувати дікшинарі

        successfully_file_path = "/tmp/successfully.txt"
        with open(successfully_file_path, 'w') as success_file:
            success_file.writelines(successfully_lines)

        errors_file_path = "/tmp/errors.txt"
        with open(errors_file_path, 'w') as error_file:
            error_file.writelines(error_lines)

        json_file_path = "/tmp/adverts_dict.json"
        self.merge_and_save_one_drive_dict(successfully_file_path=successfully_file_path, json_file_path=json_file_path)

        self.one_drive_manager.upload_file_to_onedrive(file_path=json_file_path, onedrive_path="/Holland/API-Spaceplus")
        self.one_drive_manager.upload_file_to_onedrive(file_path=successfully_file_path)
        self.one_drive_manager.upload_file_to_onedrive(file_path=errors_file_path)

# otomotomanager = OtomotoManager(excel_file_name=r"Final_exel_file.xlsx", sheet_name="OtoMoto")
# otomotomanager.create_reports_from_base()
# otomotomanager.create_next_twenty_adverts()
