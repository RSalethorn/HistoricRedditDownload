import os
import click
import json

class ConfigHandler:
    def __init__(self):
        install_location = os.path.dirname(os.path.abspath(__file__))
        config_file_name = '\config.json'
        config_path = install_location + config_file_name
        
        required_config_options = ['qbthost', 'qbtport', 'qbtuser', 'qbtpassword', 'magnetlink']
        
        # If config file already exists read data
        if os.path.isfile(config_path):
            with open(config_path, 'r') as json_config:
                current_config_data = json.load(json_config)
                # Check if current config file has all required data
                for key in required_config_options:
                    if key not in current_config_data:
                        raise click.ClickException("Current config file doesn't contain all needed data")
        # Config file doesn't exist and not all data needed for it has been given
        else:
            raise click.ClickException("No previous config file found, please give all arguments with setup command")

        self.conn_info = dict(
            host=current_config_data['qbthost'],
            port=current_config_data['qbtport'],
            username=current_config_data['qbtuser'],
            password=current_config_data['qbtpassword'],
        )
        
        self.magnetlink = current_config_data['magnetlink']

if __name__ == '__main__':
    ch = ConfigHandler()

    print(ch.conn_info)
    print(ch.magnetlink)