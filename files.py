"""存放文件相关的常用函数"""
import zipfile
import requests


class PrintFileByLine:
    """同时向文件和STD中输出内容"""

    def __init__(self, file_path, *args):
        with open(file_path, "w") as _f:
            pass
        if len(args) > 0:
            self.__call__(*args)
        self.file_path = file_path

    def __call__(self, *args):
        """直接使用instance_name()的方式调用"""
        parsed_args = " ".join([str(arg) for arg in args])
        with open(self.file_path, "a") as _f:
            print(*args)
            _f.write(parsed_args + "\n")


def read_data(data_path: str, seperator: str = '\t', dtype=str):
    """从文件中读取多行数据，每个数据之间以seperator分隔"""
    _data = []
    with open(data_path, 'r', encoding='utf-8') as _f:
        raw_data = _f.readlines()
        for _item in raw_data:
            if _item.startswith('#'):
                continue
            _item_list = str(_item).strip().split(seperator)
            _item_list = map(dtype, _item_list)
            _data.append(list(_item_list))
    return _data


def read_multiple_data(path_list, seperator: str = '\t', dtype=str):
    """从多个文件读取多行数据，每个数据之间以seperator分隔"""
    _data = []
    for data_path in path_list:
        _new_data = read_data(data_path, seperator, dtype)
        _data.extend(_new_data)
    return _data


def read_dict_data(data_path: str, item_seperator: str = ",",
                   key_value_seperator: str = ":"):
    """从文件中读取多行数据，每行数据都是一个dict
        例如某行数据为  key1: value1, key2: values2, key3: values3
        其中item_seperator是逗号“,”
        key_value_seperator是冒号“:”
    """
    _data = []
    with open(data_path, 'r', encoding='utf-8') as _f:
        raw_data = _f.readlines()
        for _raw_line in raw_data:
            if _raw_line.startswith('#'):
                continue
            _line = str(_raw_line).strip().split(item_seperator)
            _line_dict = {}
            for _pair in _line:
                _pair = _pair.strip().split(key_value_seperator)
                _key = _pair[0].strip()
                _value = _pair[1].strip()
                _line_dict[_key] = _value
            _data.append(_line_dict)
    return _data

        


class LazyReader:
    """不会一次性全部读取整个文件，调用readline才会读入一行"""

    def __init__(self, data_path: str, seperator: str = '\t', dtype=str) -> None:
        self._data_file = open(data_path, "r", encoding='utf-8')
        self.seperator = seperator
        self.dtype = dtype

    def reset(self):
        """从头开始读取"""
        self._data_file.seek(0)

    def readline(self):
        """读取一行数据，如果是空，则表示读到末尾"""
        _item = self._data_file.readline()
        while _item.startswith("#"):
            _item = self._data_file.readline()
        if _item == "":
            return None
        _item_list = str(_item).strip().split(self.seperator)
        _item_list = list(map(self.dtype, _item_list))
        return _item_list
        

class LazyReaders:
    """给一个文件path列表，读入多个文件，只有调用readline才读入一行"""

    def __init__(self, path_list, seperator: str = '\t', dtype=str) -> None:
        self._cur_file_index = 0
        self._path_list = path_list
        self.seperator = seperator
        self.dtype = dtype
        self.reader = LazyReader(
            self._path_list[0], self.seperator, self.dtype)

    def reset(self):
        """从头开始读取"""
        self._cur_file_index = 0
        self.reader = LazyReader(
            self._path_list[0], self.seperator, self.dtype)

    def readline(self):
        if self._cur_file_index >= len(self._path_list):
            return None
        _item = self.reader.readline()
        while _item is None:
            self._cur_file_index += 1
            if self._cur_file_index >= len(self._path_list):
                return None
            self.reader = LazyReader(self._path_list[self._cur_file_index],
                                     self.seperator, self.dtype)
            _item = self.reader.readline()
        return _item


class Reader:
    """不会一次性全部读取整个文件，调用readline才会读入一行"""

    def __init__(self, data_path: str, seperator: str = '\t', dtype=str) -> None:
        self._data_file = open(data_path, "r", encoding='utf-8')
        self.seperator = seperator
        self.dtype = dtype

    def reset(self):
        """从头开始读取"""
        self._data_file.seek(0)

    def readline(self):
        """读取一行数据，如果是空，则表示读到末尾"""
        _item = self._data_file.readline()
        while _item.startswith("#"):
            _item = self._data_file.readline()
        if _item == "":
            return None
        _item_list = str(_item).strip().split(self.seperator)
        _item_list = list(map(self.dtype, _item_list))
        return _item_list
        

class Readers:
    """给一个文件path列表，读入多个文件，只有调用readline才读入一行"""

    def __init__(self, path_list, seperator: str = '\t', dtype=str) -> None:
        self._cur_file_index = 0
        self._path_list = path_list
        self.seperator = seperator
        self.dtype = dtype
        self.reader = LazyReader(
            self._path_list[0], self.seperator, self.dtype)

    def reset(self):
        """从头开始读取"""
        self._cur_file_index = 0
        self.reader = LazyReader(
            self._path_list[0], self.seperator, self.dtype)

    def readline(self):
        if self._cur_file_index >= len(self._path_list):
            return None
        _item = self.reader.readline()
        while _item is None:
            self._cur_file_index += 1
            if self._cur_file_index >= len(self._path_list):
                return None
            self.reader = LazyReader(self._path_list[self._cur_file_index],
                                     self.seperator, self.dtype)
            _item = self.reader.readline()
        return _item
    

def download_file_from_proxy(url, proxy, destination_path):
    """
    使用代理下载文件

    参数:
    - url: 要下载的文件的URL
    - proxy: 代理的格式为 "http://ip:port" 或 "https://ip:port"
    - destination_path: 下载文件的保存路径

    返回:
    - 下载成功返回True，否则返回False
    """
    try:
        proxies = {
            'http': proxy,
            'https': proxy
        }

        # 使用代理发送GET请求
        response = requests.get(url, proxies=proxies, stream=True)

        # 检查请求是否成功
        if response.status_code == 200:
            # 以二进制写入文件
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return True
        else:
            print(f"下载失败，HTTP状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"下载过程中发生错误: {str(e)}")
        return False


def unzip(zip_file_path, extract_to):
    """
    解压ZIP文件到指定目录

    参数:
    - zip_file_path: 要解压的ZIP文件的路径
    - extract_to: 解压后文件的保存路径

    返回:
    - 解压成功返回True，否则返回False
    """
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"解压过程中发生错误: {str(e)}")
        return False
