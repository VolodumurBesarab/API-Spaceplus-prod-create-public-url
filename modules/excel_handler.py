import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

class ExcelHandler:
    def read_excel(self, file_content, sheet_name):
        df = pd.read_excel(file_content, sheet_name=sheet_name)
        return df

    def fill_missing_values(self, df, column_name, default_value):
        df[column_name] = df[column_name].fillna(default_value)
        return df

    def save_excel(self, df1, df2, output_excel_filename):
        # Створення нового Excel файлу
        wb = Workbook()

        # Вибір або створення першої сторінки
        sheet1 = wb.active
        sheet1.title = 'Sheet1'

        # Додавання даних з DataFrame df на першу сторінку
        for row in dataframe_to_rows(df1, index=False, header=True):
            sheet1.append(row)

        # Створення другої сторінки
        sheet2 = wb.create_sheet(title='Sheet2')

        # Додавання даних з DataFrame df2 на другу сторінку
        for row in dataframe_to_rows(df2, index=False, header=True):
            sheet2.append(row)

        # Збереження Excel файлу з назвою 'new table.xlsx'
        wb.save(output_excel_filename)

        print("Excel файл успішно збережено!")

    def get_exel_file(self, root_folder_onedrive, name: str):
        exel_file = None
        file_content = None
        for file in root_folder_onedrive['value']:
            if file['name'] == name:
                exel_file = file
                break

        if exel_file:
            # Отримайте URL для звернення до вмісту файлу
            file_url = exel_file['@microsoft.graph.downloadUrl']

            # Зробіть GET-запит до Microsoft Graph API для отримання вмісту файлу
            response = requests.get(url=file_url)

            # Перевірте, чи успішно отримано вміст файлу
            if response.status_code == 200:
                file_content = response.content
        return file_content
