import click
import os
import json
#from HRH import fetch_content

@click.group()
def main():
    pass

@main.command()
@click.option('--qbt-host', help='This is the IP address associated with your QBitTorrent API')
@click.option('--qbt-port', help='This is the port associated with your QBitTorrent API')
@click.option('--qbt-user', help='This is your username associated with your QBitTorrent API') 
@click.option('--qbt-password', help='This is your password associated with your QBitTorrent API')
@click.option('--magnetlink', help='This is the magnet link to the torrent containing content')
def setup(qbt_host, qbt_port, qbt_user, qbt_password, magnetlink):
    '''For making changes to config file'''
    # Find the place this Python module is installed to.
    install_location = os.path.dirname(os.path.abspath(__file__))
    config_file_name = '\config.json'
    config_path = install_location + config_file_name
    print(config_path)
    current_config_data = None

    required_config_options = ['qbthost', 'qbtport', 'qbtuser', 'qbtpassword', 'magnetlink']

    all_data_given = qbt_host != None and qbt_port != None and qbt_user != None and qbt_password != None and magnetlink != None

    #If config file already exists read data
    if os.path.isfile(config_path):
        with open(config_path, 'r') as json_config:
            current_config_data = json.load(json_config)
            # Check if current config file has all required data
            for key in required_config_options:
                if key not in current_config_data and all_data_given != True:
                    raise click.ClickException("Current config file doesn't contain all needed data")
    # Config file doesn't exist and not all data needed for it has been given
    elif all_data_given == False:
        raise click.ClickException("No previous config file found, please give all arguments with setup command")
        current_config_data = dict()

    # Adjust previous config to new values
    if qbt_host != None:
        current_config_data["qbthost"] = qbt_host

    if qbt_port != None:
        current_config_data["qbtport"] = qbt_port

    if qbt_user != None:
        current_config_data["qbtuser"] = qbt_user
    
    if qbt_password != None:
        current_config_data["qbtpassword"] = qbt_password

    if magnetlink != None:
        current_config_data["magnetlink"] = magnetlink

    print(current_config_data)

    # Write new config to JSON
    with open(config_path, 'w') as json_config:
        json.dump(current_config_data, json_config)

@main.command()
@click.option('--startmonth', type=click.DateTime(formats=['%m-%y']),  help="This is the first month & year for the content to be fetched (Inclusive) (Format is mm-yy)")
@click.option('--endmonth', type=click.DateTime(formats=['%m-%y']), help="This is the last month & year for the content to be fetched (Inclusive) (Format is mm-yy)")
def fetch(startmonth, endmonth):
    '''For downloading content'''
    click.echo(f"Start: {startmonth}, End: {endmonth}")



        
    
    


    

    