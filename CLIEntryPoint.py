import click
import os
import json
from datetime import datetime
from HRH import fetch_content

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
    '''Setup is for making changes to config file'''
    # Find the place this Python module is installed to.
    install_location = os.path.dirname(os.path.abspath(__file__))
    config_file_name = '\\config.json'
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
@click.option('--startmonth', required=True, type=click.DateTime(formats=['%m-%y']),  help="This is the first month & year for the content to be fetched (Inclusive) (Format is mm-yy)")
@click.option('--endmonth', required=True, type=click.DateTime(formats=['%m-%y']), help="This is the last month & year for the content to be fetched (Inclusive) (Format is mm-yy)")
@click.option('--subreddit', multiple=True, help="Subreddit that content should be fetched from (Option can be given multiple times)")
@click.option('--write-folder', type=click.Path(exists=True, file_okay=False, writable=True), help='This is the folder path you want content written to (Default current working directory)')
@click.option('--write-file-prefix', help='Optional prefix to add to each file name to be written')
@click.option('--sub-field', multiple=True, required=True, help='Fields from submissions that are to be written to file (Option can be given multiple times)')
@click.option('--com-field', multiple=True, required=True, help='Fields from comments that are to be written to file (Option can be given multiple times)')
def fetch(startmonth, endmonth, subreddit, write_folder, write_file_prefix, sub_field, com_field):
    '''For downloading content'''
    print(subreddit)
    if write_folder == None:
        current_time = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        write_folder = f'{os.getcwd()}\\HRH-{current_time}\\'
    click.echo(f"Start: {startmonth}, End: {endmonth}")
    fetch_content(start_date=startmonth, 
                  end_date=endmonth, 
                  subreddit=subreddit, 
                  write_folder_path=write_folder, 
                  write_file_prefix=write_file_prefix,
                  submission_fields=sub_field,
                  comment_fields=com_field)


if __name__ == '__main__':
    fetch([
        '--startmonth', '01-08',
        '--endmonth', '01-08',
        '--subreddit', 'london',
        '--write-folder', 'C:\\Users\\Rob\\Documents\\Test Content',
        '--write-file-prefix', 'TC',
        '--sub-field', 'created_utc',
        '--sub-field', 'author',
        '--sub-field', 'title',
        '--sub-field', 'selftext',
        '--sub-field', 'body',
        '--com-field', 'created_utc',
        '--com-field', 'author',
        '--com-field', 'body'])
        
    
    


    

    