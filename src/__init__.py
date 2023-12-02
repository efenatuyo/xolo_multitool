import os
import importlib

from .utils import sort_string

class multi:
    modules = [entry for entry in os.listdir("modules") if os.path.isdir(os.path.join("modules", entry))]
    clear = "cls" if os.name == 'nt' else "clear"
    
    def __init__(self, config):
        self.sorted = sort_string.sort(self.modules)
        self.config = config
    
    @staticmethod
    def _import(name):
        return importlib.import_module("modules." + name)  
                
    def choose_option(self):
        while True:
            print(self.sorted)
            try:
                option = int(input(f"\033[38;2;0;0;255mOption: \033[0m"))
                os.system(self.clear)
                self._import(self.modules[option-1]).Run(self.config)
                input("\nPress enter to continue...")
            except:
                os.system(self.clear)
                input("\033[38;2;255;0;0mError: Invalid option provided \033[0m")
            finally:
                os.system(self.clear)
                
            