import os
import json
import os.path


class Config:
    def __init__(self):
        self.config_data = {}
        self.conf_path = os.path.join("config.json")
        try:
            with open(self.conf_path) as json_data_file:
                self.config_data = json.load(json_data_file)
        except OSError as err:
            print("OS error: {0}".format(err))
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
