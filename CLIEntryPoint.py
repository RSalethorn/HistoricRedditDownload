import click
import os
import json
#from HRH import fetch_content

@click.group()
def main():
    pass

@main.command()
@click.option('--qbthost', help='This is the IP address associated with your QBitTorrent API')
@click.option('--qbtport', help='This is the port associated with your QBitTorrent API')
@click.option('--qbtuser', help='This is your username associated with your QBitTorrent API') 
@click.option('--qbtpassword', help='This is your password associated with your QBitTorrent API')
@click.option('--magnetlink', help='This is the magnet link to the torrent containing content')
def setup(qbthost, qbtport, qbtuser, qbtpassword, magnetlink):
    # Find the place this Python module is installed to.
    install_location = os.path.dirname(os.path.abspath(__file__))
    config_file_name = '\config.json'
    config_path = install_location + config_file_name
    print(config_path)
    current_config_data = None

    required_config_options = ['qbthost', 'qbtport', 'qbtuser', 'qbtpassword', 'magnetlink']

    all_data_given = qbthost != None and qbtport != None and qbtuser != None and qbtpassword != None and magnetlink != None

    #If config file already exists read data
    if os.path.isfile(config_path):
        with open(config_path, 'r') as json_config:
            current_config_data = json.load(json_config)
            # Check if current config file has all required data
            for key in required_config_options:
                if key not in current_config_data:
                    if all_data_given != True:
                        raise click.ClickException("Current config file doesn't contain all needed data")
    else:
        if all_data_given == False:
            raise click.ClickException("No previous config file found, please give all arguments with setup command")
        current_config_data = dict()

    if qbthost != None:
        current_config_data["qbthost"] = qbthost

    if qbtport != None:
        current_config_data["qbtport"] = qbtport

    if qbtuser != None:
        current_config_data["qbtuser"] = qbtuser
    
    if qbtpassword != None:
        current_config_data["qbtpassword"] = qbtpassword

    if magnetlink != None:
        current_config_data["magnetlink"] = magnetlink

    print(current_config_data)

    with open(config_path, 'w') as json_config:
        json.dump(current_config_data, json_config)




        
    
    


    

    