import multiprocessing
import time
import qbittorrentapi
import config

class TorrentInfoPoller:
    # file_paths should be a list of strings containing all inner torrent paths for files being accessed by this search
    def __init__(self, file_paths, start_date, end_date):
        self.file_paths = file_paths
        self.torrent_info_lock = multiprocessing.Lock()

        # Get QBitTorrent Connection Details
        # TODO: May have move all QBT connection code into own class in future
        self.conn_info = config.conn_info

        # Months and Years (Including) to be downloaded from torrent
        self.start_date = start_date #datetime(2007, 8, 1)
        self.end_date = end_date #datetime(2007, 9, 1)
        
        self.torrent_info = []

    def set_torrent_info(self):
        with self.torrent_info_lock:
            torrent_info = []
            for file_path in self.file_paths:
                # TODO: CHANGE get_file_info TO BE ABLE TO ACCEPT A LIST OF FILE PATHS SO DON'T NEED TO DO A CALL PER FILE_PATH
                torrent_info.append(self.torrent_handler.get_file_info(file_path))
            self.torrent_info = torrent_info
    
    def get_torrent_info(self, file_path):
        with self.torrent_info_lock:
            selected_torrent_info = filter(lambda torrent_file: torrent_file.get("name") == file_path, self.torrent_info)
            print(selected_torrent_info[0])
            return selected_torrent_info[0]
    
    def run(self):
        while True:
            self.set_torrent_info()
            time.sleep(1)
        