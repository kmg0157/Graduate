import json

class write_json:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def save_data_to_json(self, data):
        with open(self.file_path, "a+") as file_object:
            json.dump(data,file_object)
            file_object.write('\n')

    def initialize_json_file(self):
        with open(self.file_path, 'w') as file_object:
            file_object.write("[")

    def close_json_file(self):
        with open(self.file_path, "a+") as file_object:
            file_object.write("]\n")
