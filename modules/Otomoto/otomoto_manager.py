from typing import Any

from pandas import DataFrame

from modules.excel_handler import ExcelHandler


class OtomotoManager:
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.excel_handler = ExcelHandler()


    def _create_page(self):
        file_name = "storage 09_23_site"
        sheet_name = "OtoMoto"
        file_content = self.excel_handler.get_exel_file(file_name)
        qwe = self.excel_handler.read_excel(file_content=file_content, sheet_name=sheet_name)
        print(qwe)
        return self

    def read_page_line(self):

        status = "Error"
        # read article count in storage
            # read article id
                # create product
                # read other atribbutes
                    #edit atributes

        status = "Complete"
        return status

    def read_all_items(self):
        self._create_page()

        pass
