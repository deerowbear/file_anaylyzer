import os

class FileModel:

    def __init__(self, source_path: str, export_path: str, file_name: str, json_path: str):
        self.source_path = source_path
        self.export_path = export_path
        self.file_name = file_name
        self.source_file = source_path + os.sep + file_name
        self.file_exits = False
        self.is_exact_copy = False
        self.is_written = False
        self.json_file =  self.export_path + json_path
        self.create_date = 'NULL'
        self.destination_path = 'NULL'
        self.file_size = 'NULL'
        self.x_resolution = 'NULL'
        self.y_resolution = 'NULL'

    def toString(self):
        return self.file_name, self.dateToString(), self.file_size,self.x_resolution, self.y_resolution,self.source_path, self.destination_path,str(self.file_exits),str(self.is_exact_copy),str(self.is_written)
    
    def dateToString(self):
        try:
            return self.create_date.strftime('%m-%d-%Y')
        except:
            return 'NULL'