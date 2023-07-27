import qbittorrentapi
import threading
import config
import logging
from datetime import datetime
import time
import os

class TorrentThread(threading.Thread):
    def __init__(self, file_paths, info_storage):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

        # Declare magnet_link for Torrent of PushshiftDump
        magnet_link = "magnet:?xt=urn:btih:7c0645c94321311bb05bd879ddee4d0eba08aaee&tr=https%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"

        # Extract hash from magnet link
        torrent_hash = magnet_link.split("&")[0].split(":")[-1]

        
        # Define directorys to place downloading and downloaded torrents
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        download_location = current_directory + "\\Saved\\"
        saved_location = current_directory + "\\Saved\\"

        qb = self.connect()

        # Add torrent to QBT
        qb.torrents_add(urls=magnet_link, 
                             use_download_path=True, 
                             save_path=saved_location, 
                             download_path=download_location,
                             is_sequential_download=True)
        
        self.select_relevant_files(qb, torrent_hash, file_paths)

        while True:
            t_file_info = qb.torrents_info(torrent_hashes=torrent_hash)[0].files
            info_storage.set_torrent_info(t_file_info)
            time.sleep(2)

    def connect(self):
        # Get QBitTorrent Connection Details
        # TODO: May have move all QBT connection code into own class in future
        conn_info = config.conn_info
        qb = qbittorrentapi.Client(**conn_info)
        # Setup Authorisation for client
        try:
            qb.auth_log_in()
            logging.info("Succesfully connected to QBitTorrent.")
        except qbittorrentapi.LoginFailed as e:
            logging.info(f"An error occured connecting to QBitTorrent API. \n{e}")
        return qb

    def wait_for_torrent_added(self, qb, torrent_hash):
        # Wait loop incase API running slow and torrent hasn't been added yet
        torrent_added = False
        while torrent_added == False:
            try:
                torrent = qb.torrents_info(torrent_hashes=torrent_hash)[0]
                # torrent_added only changed if previous line doesn't cause error. (Needs verifying)
                torrent_added = True
            except IndexError:
                logging.info("Waiting for torrent to be added to QBitTorrent")
                time.sleep(1.5)
        logging.info("Torrent identified in QBitTorrent")

    def wait_for_metadata(self, qb, torrent_hash):
        # Loop gets program to wait for metadata of torrent to be downloaded
        metadata_downloaded = False
        while metadata_downloaded == False:
            torrent = qb.torrents_info(torrent_hashes=torrent_hash)[0]
            # If torrent.files has items in it then metadata has been downloaded
            if len(torrent.files) > 0:
                metadata_downloaded = True
                logging.info("Torrent metadata downloaded")
                break
            logging.info("Waiting for Metadata")
            time.sleep(1)
    
    def select_relevant_files(self, qb, torrent_hash, file_paths):
        # Wait for Torrent to be loaded into QBT so adjustments can be made
        self.wait_for_torrent_added(qb, torrent_hash)
        self.wait_for_metadata(qb, torrent_hash)

        torrent = qb.torrents_info(torrent_hashes=torrent_hash)[0]

        file_names = []
        for file in torrent.files:
            for selected_file in file_paths:
                if file.name == selected_file:
                    qb.torrents_file_priority(torrent_hash, file.id, 1)
                    file_names.append(file.name)
                    break
                else:
                    qb.torrents_file_priority(torrent_hash, file.id, 0)

        logging.info(f"The following files have been chosen as needed for your required search: \n{file_names}")