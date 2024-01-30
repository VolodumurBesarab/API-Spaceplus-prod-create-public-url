import os
from modules.onedrive_manager import OneDriveManager

REPORT_FILE_PATH = f"/tmp/reports/general_report.txt"


class ReportsGenerator:
    def __init__(self):
        self.one_drive_manager = OneDriveManager()

    def create_general_report(self, message: str) -> str:
        folder_path = "/tmp/reports"
        file_path = REPORT_FILE_PATH

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, "a") as file:
            file.write(message + "\n")

        self.one_drive_manager.upload_file_to_onedrive(file_path=REPORT_FILE_PATH)
        return file_path
