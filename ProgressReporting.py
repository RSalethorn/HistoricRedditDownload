import threading
import logging
import time

class ProgressReporterThread(threading.Thread):
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
    def __init__(self, torrent_info):
        self.progress_info = dict()
        self.progress_info.decompress = dict(total_bytes = 0, bytes_complete = 0, content_found = 0)
        self.progress_info.filter = dict(content_checked = 0, valid_content = 0)
        self.progress_info.write = dict(content_written = 0)

        self.progress_info_locks = dict()
        self.progress_info_locks.decompress = dict(total_bytes = threading.Lock(), bytes_complete = threading.Lock(), content_found = threading.Lock())
        self.progress_info_locks.filter = dict(content_checked = threading.Lock(), valid_content = threading.Lock())
        self.progress_info_locks.write = dict(content_written = threading.Lock())
    
    def set_decompress_total_bytes(self, total):
        self.progress_info.decompress.total_bytes = total

    def add_decompress_bytes_complete(self, bytes_decompressed):
        with self.progress_info_locks.decompress.bytes_complete:
            self.progress_info.decompress.bytes_complete += bytes_decompressed

    def add_decompress_content_found(self, content_found):
        with self.progress_info_locks.decompress.content_found:
            self.progress_info.decompress.content_found += content_found

    def add_filter_content_checked(self, content_checked):
        with self.progress_info_locks.decompress.content_checked:
            self.progress_info.decompress.content_checked += content_checked

    def add_filter_valid_content(self, valid_content):
        with self.progress_info_locks.decompress.valid_content:
            self.progress_info.decompress.valid_content += valid_content

    def add_write_content_written(self, content_written):
        with self.progress_info_locks.write.content_written:
            self.progress_info.write.content_written += content_written

    def get_all_info(self):
        return self.progress_info