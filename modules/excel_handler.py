import os

import pandas as pd
import requests
from pandas import DataFrame

from modules.auth_manager import AuthManager
from modules.onedrive_manager import OneDriveManager


class ExcelHandler:
    def __init__(self):
        self.onedrive_manager = OneDriveManager()
        self.auth_manager = AuthManager()

        self.endpoint = self.auth_manager.get_endpoint()
        self.access_token = self.auth_manager.get_access_token_default_scopes()
        self.one_drive_url = self.auth_manager.get_endpoint() + "drive/root/children"
        self.headers = self.auth_manager.get_default_header(access_token=self.access_token)

    def read_excel(self, file_content, sheet_name):
        df = pd.read_excel(file_content, sheet_name=sheet_name)
        return df

    def fill_missing_values(self, df, column_name, default_value):
        df[column_name] = df[column_name].fillna(default_value)
        return df

    # def save_excel(self, df1, df2, output_excel_filename):
    #     # Створення нового Excel файлу
    #     wb = Workbook()
    #
    #     # Вибір або створення першої сторінки
    #     sheet1 = wb.active
    #     sheet1.title = 'Sheet1'
    #
    #     # Додавання даних з DataFrame df на першу сторінку
    #     for row in dataframe_to_rows(df1, index=False, header=True):
    #         sheet1.append(row)
    #
    #     # Створення другої сторінки
    #     sheet2 = wb.create_sheet(title='Sheet2')
    #
    #     # Додавання даних з DataFrame df2 на другу сторінку
    #     for row in dataframe_to_rows(df2, index=False, header=True):
    #         sheet2.append(row)
    #
    #     # Збереження Excel файлу з назвою 'new table.xlsx'
    #     wb.save(output_excel_filename)
    #
    #     print("Excel файл успішно збережено!")

    def get_exel_file(self, name: str):
        root_folder_onedrive = self.onedrive_manager.get_root_folder_json(one_drive_url=self.one_drive_url,
                                                                          headers=self.headers)
        exel_file = None
        file_content = None
        for file in root_folder_onedrive['value']:
            if file['name'] == name:
                exel_file = file
                break
            # rework this
            # else:
            #     print("Name of exel file not found")
            #     print(file['name'])

        if exel_file:
            # Отримайте URL для звернення до вмісту файлу
            file_url = exel_file['@microsoft.graph.downloadUrl']

            # Зробіть GET-запит до Microsoft Graph API для отримання вмісту файлу
            response = requests.get(url=file_url)

            # Перевірте, чи успішно отримано вміст файлу
            if response.status_code == 200:
                file_content = response.content
                print("excel file download successful")
        return file_content

    def get_file_path(self, file_name) -> str:
        current_directory = os.getcwd()
        save_path = os.path.join(current_directory, 'Data', file_name)
        return save_path

    def create_file_on_data(self, file_content, file_name):
        save_path = self.get_file_path(file_name=file_name)
        with open(save_path, 'wb') as file:
            file.write(file_content)

    def create_lines_list(self):
        pass

    def set_otomoto_id_by_storage_id(self, df:  DataFrame, otomoto_id, storage_id):
        row = df[df['номер на складі'] == storage_id]

        # Перевіряємо, чи такий рядок був знайдений
        if not row.empty:
            # Отримуємо значення otomoto_id для цього рядка
            current_otomoto_id = row.iloc[0]['ID otomoto']

            # Перевіряємо, чи otomoto_id є NaN (пустим)
            if pd.isna(current_otomoto_id):
                # Вставляємо нове otomoto_id у відповідне поле
                df.loc[df['номер на складі'] == storage_id, 'ID otomoto'] = str(otomoto_id)
        # Зберігаємо оновлений DataFrame у файл
        df.to_excel('New tested file.xlsx', index=False)
        # Повертаємо оновлений DataFrame
        return df

