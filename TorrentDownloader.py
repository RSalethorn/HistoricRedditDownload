import qbittorrentapi
from datetime import datetime
import time
import os
import math
import logging
import json

#Secret Config File
import config


class TorrentHandler():
    def __init__(self, start_date, end_date):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        
        # Declare magnet_link for Torrent of PushshiftDump
        self.magnet_link = "magnet:?xt=urn:btih:7c0645c94321311bb05bd879ddee4d0eba08aaee&tr=https%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"

        # Extract hash from magnet link
        self.torrent_hash = self.magnet_link.split("&")[0].split(":")[-1]

        # Define directorys to place downloading and downloaded torrents
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        
        self.download_location = self.current_directory + "\\Download\\"
        self.saved_location = self.current_directory + "\\Saved\\"

        # Get QBitTorrent Connection Details
        # TODO: May have move all QBT connection code into own class in future
        self.conn_info = config.conn_info

        # Months and Years (Including) to be downloaded from torrent
        self.start_date = start_date #datetime(2007, 8, 1)
        self.end_date = end_date #datetime(2007, 9, 1)
    
    def start(self):
        # Connect to QBT
        self.connect()

        # Add torrent to QBT
        self.qb.torrents_add(urls=self.magnet_link, 
                             use_download_path=True, 
                             save_path=self.saved_location, 
                             download_path=self.download_location)
        
        # Only download files including Reddit posts between given dates
        self.select_relevant_files()

        # Wait for downloads to finish so rest of program can continue (For now)
        self.wait_for_download()
    
    def connect(self):
        self.qb = qbittorrentapi.Client(**self.conn_info)

        # Setup Authorisation for client
        try:
            self.qb.auth_log_in()
            logging.info("Succesfully connected to QBitTorrent.")
        except qbittorrentapi.LoginFailed as e:
            logging.info(f"An error occured connecting to QBitTorrent API. \n{e}")
    
    def update_torrent_info(self):
        self.torrent = self.qb.torrents_info(torrent_hashes=self.torrent_hash)[0]

    def get_file_info(self, file_path):
        self.update_torrent_info()
        for file in self.torrent.files:
            if file.name == file_path:
                #print(f"FILE: {file}")
                return file
    

    def wait_for_torrent_added(self):
        # Wait loop incase API running slow and torrent hasn't been added yet
        torrent_added = False
        while torrent_added == False:
            try:
                self.update_torrent_info()
                # torrent_added only changed if previous line doesn't cause error. (Needs verifying)
                torrent_added = True
            except IndexError:
                logging.info("Waiting for torrent to be added to QBitTorrent")
                time.sleep(1.5)
        logging.info("Torrent identified in QBitTorrent")
    
    def wait_for_metadata(self):
        # Loop gets program to wait for metadata of torrent to be downloaded
        metadata_downloaded = False
        while metadata_downloaded == False:
            self.update_torrent_info()
            # If torrent.files has items in it then metadata has been downloaded
            if len(self.torrent.files) > 0:
                metadata_downloaded = True
                logging.info("Torrent metadata downloaded")
                break
            logging.info("Waiting for Metadata")
            time.sleep(1)
    
    def select_relevant_files(self):
        # Wait for Torrent to be loaded into QBT so adjustments can be made
        self.wait_for_torrent_added()
        self.wait_for_metadata()

        # Loop through all files in Pushshift torrent
        for file in self.torrent.files:
            # Convert file name into date
            date_str = file.name.split("_")[-1].split(".")[0] + "-01"
            date = datetime.strptime(date_str, "%Y-%m-%d")
            self.file_names = []
            # If date on this file is included in the timeframe given set priority to one
            if date >= self.start_date and date <= self.end_date:
                self.qb.torrents_file_priority(self.torrent_hash, file['id'], 1)
                self.file_names.append(file.name)
            else:
                # If not don't download (Priority = 0)
                self.qb.torrents_file_priority(self.torrent_hash, file['id'], 0)
        logging.info(f"The following files have been chosen as needed for your required search: \n{self.file_names}")

    def wait_for_download(self):
        # Loop waits till torrent is finished downloading
        torrent_download_finished = False
        while torrent_download_finished == False:
            self.update_torrent_info()
            if self.torrent.amount_left == 0:
                torrent_download_finished = True
                logging.info("Torrent download is finished")
            else:
                for file in self.file_names:
                    self.get_download_progress(file)
                total_parts = self.torrent.amount_left + self.torrent.completed
                percentage_complete = math.floor(100 - ((self.torrent.amount_left / total_parts) * 100))
                logging.info(f"Torrent {percentage_complete}% downloaded")
            time.sleep(1.5)



