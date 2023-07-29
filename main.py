from datetime import datetime
from TorrentThread import TorrentThread
from ZstandardThread import ZstandardThread
from ZtstandardHandler import ZstandardHandler
from TorrentInfoStorage import TorrentInfoStorage
from AnalysisThread import FilterThread
from queue import Queue
import time
import logging
import threading

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info("Script started")

def increase_date_by_month(date):
      new_month = date.month + 1
      new_year = date.year
      if new_month > 12:
            new_month = 1
            new_year = new_year + 1
      return datetime(new_year, new_month, 1)

def generate_file_paths_by_date(start_date, end_date):
      content_types = ["comments", "submissions"]

      torrent_file_paths = []

      current_file_date = start_date 

      while current_file_date <= end_date:
            for content_type in content_types:
                  file_type_prefix = content_type[0].upper()
                  inner_torrent_path = f"reddit/{content_type}/R{file_type_prefix}_{current_file_date.strftime('%Y-%m')}.zst" 
                  torrent_file_paths.append(inner_torrent_path)

            current_file_date = increase_date_by_month(current_file_date)
      
      return torrent_file_paths

#TODO: MOVE TO TorrentInfoStorage?
def wait_for_torrent_info(t_info_storage):
      while t_info_storage.get_has_init() == False:
            print("Waiting for torrent info")
            time.sleep(1)
            


if __name__ == '__main__':
      save_folder_path = './Saved/'

      start_date = datetime(2009, 9, 1)
      end_date = datetime(2010, 9, 1)

      torrent_file_paths = generate_file_paths_by_date(start_date, end_date)

      t_info_storage = TorrentInfoStorage()

      t_handler = threading.Thread(target=TorrentThread, args=(torrent_file_paths, t_info_storage,))
      t_handler.start()

      wait_for_torrent_info(t_info_storage)

      #zstd_handler = ZstandardHandler(t_info_storage)

      script_start = datetime.now()

      #TODO: IMPLEMENT "QUEUE" WHICH PRIORITISES FILES WHICH ARE MORE DOWNLOADED
      zstd_job_queue = Queue(0)
      filter_job_queue = Queue(0)
      write_job_queues = {}

      for file in torrent_file_paths:
            zstd_job_queue.put(file)
            write_job_queues[file] = Queue(0)
            
      zstd_thread_amount = 5
      zstd_threads = []
      for n in range(zstd_thread_amount):
            zstd_threads.append(threading.Thread(target=ZstandardThread, args=(zstd_job_queue, filter_job_queue, save_folder_path, t_info_storage,)))
            zstd_threads[n].start()

      filter_kwargs = {"subreddits":["funny", "worldpolitics"]}
      filter_thread = threading.Thread(target=FilterThread, args=(filter_job_queue, write_job_queues,), kwargs=filter_kwargs)
      filter_thread.start()

      script_end = datetime.now()
      total_time = script_end - script_start

      #average_rspeed = total_file_size / total_time.total_seconds()
      logging.info(f"Script finished in {total_time}")#, average speed was {average_rspeed} b/sec")