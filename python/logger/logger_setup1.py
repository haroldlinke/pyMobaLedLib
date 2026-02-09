# logger_setup.py
import logging.config
import json

def setup_logging(config_path='logger/logging_config.json'):
    with open(config_path, 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)
