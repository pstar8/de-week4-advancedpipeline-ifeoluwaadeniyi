import configparser
import os

class ConfigManager:
    def __init__(self, config_file='../pipeline.cfg'):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found")
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
    def get_base_url(self):
        return self.config.get('API', 'base_url')
    
    def get_url_limit(self):
        return self.config.getint('API', 'url_limit')
        