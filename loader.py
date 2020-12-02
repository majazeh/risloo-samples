import json

class loader:
    __type = None
    __data = None
    def __init__(self, data, type = 'object'):
        self.__type = type
        self.__data = data
    
    def load(self):
        try:
            get_data = getattr(self, 'load_'+ self.__type)
        except:
            raise Exception('type ' + self.__type + ' not defined')
        return get_data(self.__data)
    
    def load_raw(self, _data):
        return json.loads(_data)

    def load_file(self, _data):
        with open(_data, 'r') as file:
            return self.load_raw(file.read())
    def load_object(self, _data):
        return _data
    