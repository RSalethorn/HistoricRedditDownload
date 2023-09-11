import threading
import logging
import time

class ProgressReporterThread():
    def __init__(self, progress_info):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info("ProgressReporterThread started")
        while True:
            progress = progress_info.get_all_info()
            logging.info(f'''
                         (DECOMPRESS) {progress.decompress.bytes_complete} / {progress.decompress.total_bytes} bytes complete, {progress.decompress.content_found} content found.\n
                         (FILTER) {progress.filter.content_checked} / {progress.decompress.content_found} content checked, {progress.filter.valid_content} valid content found.
                         (WRITE) {progress.write.content_written} / {progress.filter.valid_content} content written to disk.
                        ''')
            time.sleep(20)
            

class ProgressInfo:
    def __init__(self):#, torrent_info):
        # Holds all progress info
        self.progress_info = dict()
        # Holds a dictionary for each decompress thread that stores the progress for each file
        self.progress_info["decompress"] = dict()#total_bytes = 0, bytes_complete = 0, content_found = 0

        self.progress_info["filter"] = dict(content_checked = 0, valid_content = 0)

        self.progress_info["write"] = dict()

        # Holds all locks for progress info
        self.progress_info_locks = dict()

        # Holds a dictionary for each decompress thread that holds a lock for type of progress tracked in a decompress thread
        self.progress_info_locks["decompress"] = dict()#total_bytes = threading.Lock(), bytes_complete = threading.Lock(), content_found = threading.Lock()

        self.progress_info_locks["filter"] = dict(content_checked = threading.Lock(), valid_content = threading.Lock())
        self.progress_info_locks["write"] = dict()

        self.thread_status = dict()
        self.thread_status_locks = dict()

        self.thread_status["decompress"] = dict()
        self.thread_status_locks["decompress"] = dict()

        self.thread_status["filter"] = True
        self.thread_status_locks["filter"] = threading.Lock()

        self.thread_status["write"] = dict()
        self.thread_status_locks["write"] = dict()

    # DECOMPRESSION FUNCTIONS
    
    # Sets decompress progress dictionaries and locks up for 'file_name'
    def init_decompress_file(self, file_name):
        self.progress_info["decompress"][file_name] = dict(total_bytes = 0, bytes_decompressed = 0, content_found = 0)
        self.progress_info_locks["decompress"][file_name] = dict(total_bytes = threading.Lock(), bytes_decompressed = threading.Lock(), content_found = threading.Lock())

        self.thread_status["decompress"][file_name] = True
        self.thread_status_locks["decompress"][file_name] = threading.Lock()

    # Set the amount of total bytes contained within a uncompressed file.
    def set_decompress_total_bytes(self, file_name, total):
        with self.progress_info_locks["decompress"][file_name]["total_bytes"]:
            self.progress_info["decompress"][file_name]["total_bytes"] = total

    # Set the total amount of bytes that have been uncompressed within a file.
    def set_decompress_bytes_complete(self, file_name, bytes_decompressed):
        with self.progress_info_locks["decompress"][file_name]["bytes_decompressed"]:
            self.progress_info["decompress"][file_name]["bytes_decompressed"] = bytes_decompressed

    # Adds to the total amount of lines of content that have been decompressed
    def add_decompress_content_found(self, file_name, content_found):
        with self.progress_info_locks["decompress"][file_name]["content_found"]:
            self.progress_info["decompress"][file_name]["content_found"] += content_found

    def set_decompress_thread_status(self, file_name, bool_value):
        with self.thread_status_locks["decompress"][file_name]:
            self.thread_status_locks["decompress"][file_name] = bool_value

    def get_decompress_threads_status(self):
        for file_name in self.thread_status_locks["decompress"]:
            with self.thread_status_locks["decompress"][file_name]:
                if not self.thread_status_locks["decompress"][file_name]:
                    return False
        return True


    # FILTER FUNCTIONS

    # Adds to the total amount of lines of content that have been checked by filter threads
    def add_filter_content_checked(self, content_checked):
        with self.progress_info_locks["filter"]["content_checked"]:
            self.progress_info["filter"]["content_checked"] += content_checked

    # Adds to the total amount of lines have content that have been found to pass filters
    def add_filter_valid_content(self, valid_content):
        with self.progress_info_locks["filter"]["valid_content"]:
            self.progress_info["filter"]["valid_content"] += valid_content
    
    # WRITE FUNCTIONS

    # Sets write progress dictionaries and locks up for 'file_name'
    def init_write_file(self, file_name):
        self.progress_info["write"][file_name] = dict(content_written = 0)
        self.progress_info_locks["write"][file_name] = dict(content_written = threading.Lock(),)

    # Adds to total amount of lines of content that have been written to a file
    def add_write_content_written(self, file_name, content_written):
        with self.progress_info_locks["write"][file_name]["content_written"]:
            self.progress_info["write"][file_name]["content_written"] += content_written

    def get_all_info(self):
        return self.progress_info
    
    def get_progress_overview(self):
        progress_overview = dict()
        progress_overview["decompress"] = dict(total_bytes = 0, bytes_decompressed = 0, content_found = 0)

        # Sum together progress stats of each file being decompressed
        for file in self.progress_info["decompress"]:
            with self.progress_info_locks["decompress"][file]["total_bytes"]:
                progress_overview["decompress"]["total_bytes"] += self.progress_info["decompress"][file]["total_bytes"]

            with self.progress_info_locks["decompress"][file]["bytes_decompressed"]:
                progress_overview["decompress"]["bytes_decompressed"] += self.progress_info["decompress"][file]["bytes_decompressed"]

            with self.progress_info_locks["decompress"][file]["content_found"]:
                progress_overview["decompress"]["content_found"] += self.progress_info["decompress"][file]["content_found"]

        progress_overview["filter"] = dict()
        progress_overview["filter"]["content_checked"] = self.progress_info["filter"]["content_checked"]
        progress_overview["filter"]["valid_content"] = self.progress_info["filter"]["valid_content"]


        # Sum together progress stats of each file being written
        progress_overview["write"] = dict(content_written = 0,)
        for file in self.progress_info["write"]:
            with self.progress_info_locks["write"][file]["content_written"]:
                progress_overview["write"]["content_written"] += self.progress_info["write"][file]["content_written"]
        
        return progress_overview
    

if __name__ == "__main__":
    pi = ProgressInfo(1)
    pi.init_decompress_file("1")
    for n in range(5):
        pi.add_decompress_content_found("1", 1)
    pi.set_decompress_bytes_complete("1", 2000000)
    pi.set_decompress_total_bytes("1", 1234567890)
    pi.init_decompress_file("2")
    for n in range(11):
        pi.add_decompress_content_found("2", 1)
    pi.set_decompress_bytes_complete("2", 4000000)
    pi.set_decompress_total_bytes("2", 9876543210)
    pi.init_decompress_file("3")
    for n in range(27):
        pi.add_decompress_content_found("3", 1)
    pi.set_decompress_bytes_complete("3", 6000000)
    pi.set_decompress_total_bytes("3", 2424242424)

    for n in range(327):
        pi.add_filter_content_checked(1)

    for n in range(168):
        pi.add_filter_valid_content(1)

    pi.init_write_file("1")
    for n in range(59):
        pi.add_write_content_written("1", 1)

    pi.init_write_file("2")
    for n in range(72):
        pi.add_write_content_written("2", 1)

    overview = pi.get_progress_overview()
    print(overview)
