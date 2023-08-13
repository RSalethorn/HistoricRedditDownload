import threading
from ZtstandardHandler import ZstandardHandler
import logging
import time
from MemoryHandler import MemoryHandler

class ZstandardThread(threading.Thread):
    # file_path is the path to the zst file to be unzipped
    # t_info_storage is storage class for torrent file info
    def __init__(self, zstd_job_queue, filter_job_queue, save_folder_path, t_info_storage):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info("Script started")

        progress_info_percentage = 5

        while zstd_job_queue.empty() != True:
            self.wait_for_torrent_info(t_info_storage)

            file_path = zstd_job_queue.get()

            zstd_handler = ZstandardHandler(t_info_storage)
            mem_handler = MemoryHandler()

            current_file_info = t_info_storage.get_torrent_info(file_path)
            current_file_size = current_file_info.size
            progress_info_byte_interval = current_file_size / progress_info_percentage

            for content, file_bytes_processed in zstd_handler.read_file(file_path, save_folder_path):
                    self.wait_for_free_memory(mem_handler)
                    content["file"] = file_path
                    filter_job_queue.put(content)
                    if file_bytes_processed >= progress_info_byte_interval: 
                        percentage = (file_bytes_processed / current_file_size) * 100
                        logging.info(f"{percentage}% of {file_path} processed")
                                    #\nExample of Content: {content}")
                        progress_info_byte_interval += current_file_size / progress_info_percentage

        logging.info("ZstandardThread finished.")

    def wait_for_torrent_info(self, t_info_storage):
        while t_info_storage.get_has_init() == False:
            logging.info("Zstd Thread - Waiting for torrent info")
            time.sleep(1)

    def wait_for_free_memory(self, mem_handler):
         while mem_handler.is_memory_allocated_full():
            time.sleep(0.05)
        


    