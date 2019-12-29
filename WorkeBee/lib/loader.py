import hashlib
import importlib
from importlib.abc import Loader


def get_md5(value):
    if isinstance(value, str):
        value = value.encode(encoding='UTF-8')
    return hashlib.md5(value).hexdigest()


def load_string_to_module(code_string, fullname=None):
    try:
        module_name = 'Bees_{0}'.format(get_md5(code_string)) 
        file_path = 'Bumble://{0}'.format(module_name)       
        poc_loader = ScriptLoader(module_name, file_path)
        poc_loader.set_data(code_string)
        spec = importlib.util.spec_from_file_location(module_name, file_path, loader=poc_loader)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        msg = "\n获取任务脚本，正在加载脚本...\n"
        print(msg)
        return mod

    except ImportError:
        error_msg = "load module '{0}' failed!".format(fullname)
        print(error_msg)
        raise


class ScriptLoader(Loader):
    """poc loader 类"""
    def __init__(self, fullname, path):
        self.fullname = fullname 
        self.path = path   
        self.data = None   

    def set_data(self, data):
        self.data = data   

    def get_filename(self, fullname):
        return self.path   

    def get_data(self, filename):
        if filename.startswith('Bumble://') and self.data:
            data = self.data  
        else:
            with open(filename, encoding='utf-8') as f:
                data = f.read()
        return data  

    def exec_module(self, module):
        filename = self.get_filename(self.fullname) 
        poc_code = self.get_data(filename)
        obj = compile(poc_code, filename, 'exec', dont_inherit=True, optimize=-1)
        exec(obj, module.__dict__)



# ss = '''
# import time

# def verify(arg):
#     time.sleep(1)
#     return {"url":arg,"name":"thinkphp"}
# '''

# model = load_string_to_module(ss)
# print(model.verify(1))
