import threading
class TorrentInfoStorage:
    def __init__(self):
        self.resource_lock = threading.Lock()
        self.torrent_info = {}
        self.has_init = False
    
    def set_torrent_info(self, t_file_list):
        with self.resource_lock:
            self.has_init = True
            for file in t_file_list:
                #print(file.name)
                self.torrent_info[file.name] = file
    
    def get_torrent_info(self, file_name):
        with self.resource_lock:
            try:
                #print(f"TIS: {self.torrent_info[file_name]}")
                return self.torrent_info[file_name]
            except KeyError as e:
                #print(f"TIS: EMPTY \n {e}")
                return {}
            
    def get_has_init(self):
        with self.resource_lock:
            return self.has_init