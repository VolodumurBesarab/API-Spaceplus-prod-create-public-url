

class FileCreator:
    def get_file_in_tmp(self, file_name: str):
        file_path = f"/tmp/{file_name}"

        with open(file_path, "a") as file:
            file.write("\n")

        return file

        pass
