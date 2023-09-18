from datetime import datetime
from TorrentThread import TorrentThread
from ZstandardThread import ZstandardThread
from TorrentInfoStorage import TorrentInfoStorage
from FilterThread import FilterThread
from CSVWriteThread import CSVWriteThread
from ProgressReporting import ProgressInfo
from queue import Queue
import time
import logging
import threading
import click
import os
from FieldTypes import SubFields, ComFields

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

#TODO: MOVE TO TorrentInfoStorage
def wait_for_torrent_info(t_info_storage):
      no_of_waits = 0
      while t_info_storage.get_has_init() == False:
            no_of_waits += 1
            print(f"\r(QBitTorrent) Waiting for torrent info ({no_of_waits})", end="")
            time.sleep(1)

def report_progress(progress_info, t_info_storage, torrent_file_paths):
      while True:
            print("===-----[ NEW UPDATE ]-----===")
            current_progress = progress_info.get_progress_overview()
            if current_progress['write']['content_written'] == current_progress['filter']['valid_content'] and not progress_info.get_filter_threads_status():
                  break
            

            decomp_total_mb = round(current_progress["decompress"]["total_bytes"] / 1024 / 1024, 0)
            
            downloaded_total = 0
            for file in torrent_file_paths:
                  file_info = t_info_storage.get_torrent_info(file)
                  downloaded_total += file_info["size"] * file_info["progress"]
            downloaded_total = round(downloaded_total / 1024 / 1024, 2)
            downloaded_percentage = round(downloaded_total/decomp_total_mb*100, 2)

            print(f"(DOWNLOAD) {downloaded_total}/{decomp_total_mb} mb downloaded ({downloaded_percentage}%)")
            decomp_progress_mb = round(current_progress["decompress"]["bytes_decompressed"] / 1024 / 1024, 0)
            try:
                  decomp_percentage = current_progress["decompress"]["bytes_decompressed"] / current_progress["decompress"]["total_bytes"] * 100
            except ZeroDivisionError:
                  decomp_percentage = 0
            
            print(f"(DECOMPRESS) {decomp_progress_mb}/{decomp_total_mb} mb decompressed ({round(decomp_percentage, 2)}%)")
            try:
                  filter_percentage = current_progress['filter']['content_checked'] / current_progress['decompress']['content_found'] * 100
            except ZeroDivisionError:
                  filter_percentage = 0
            print(f"(FILTER) {current_progress['filter']['content_checked']}/{current_progress['decompress']['content_found']} content found been filtered ({round(filter_percentage, 2)}%)")
            try:
                  write_percentage = current_progress['write']['content_written'] / current_progress['filter']['valid_content'] * 100
            except ZeroDivisionError:
                  write_percentage = 0
            print(f"(WRITE) {current_progress['write']['content_written']}/{current_progress['filter']['valid_content']} succesfully filtered content been written to file ({round(write_percentage, 2)}%)")
            time.sleep(5)

# start_date & end_date should be DateTime objects            
def fetch_content(start_date, end_date, subreddit, write_folder_path, write_file_prefix, submission_fields, comment_fields):
      script_start = datetime.now()

      print(submission_fields)

      # Define folder to download data into
      save_folder_path = './Saved/'
      os.makedirs(os.path.dirname(save_folder_path), exist_ok=True)

      filter_kwargs = {"subreddits": subreddit,
                       "submission_fields": submission_fields,
                       "comment_fields": comment_fields}

      torrent_file_paths = generate_file_paths_by_date(start_date, end_date)

      # Data structures used by threads to communicate
      t_info_storage = TorrentInfoStorage()
      progress_info = ProgressInfo()

      # Start Torrent Handler Thread
      t_handler = threading.Thread(target=TorrentThread, args=(torrent_file_paths, t_info_storage, progress_info))
      t_handler.start()

      # Wait for Torrents to be properly loaded
      wait_for_torrent_info(t_info_storage)

      # Define job queues for each thread
      zstd_job_queue = Queue(0)
      filter_job_queue = Queue(0)
      write_job_queues = {}

      for file in torrent_file_paths:
            # Populate ZStd job queue
            zstd_job_queue.put(file)

            # Initialise write job queues for each file to be written
            write_job_queues[file] = Queue(0)

            progress_info.init_decompress_file(file)

            # Initialise total size of each file being decompressed
            file_info = t_info_storage.get_torrent_info(file)
            progress_info.set_decompress_total_bytes(file, file_info["size"])

      # Start ZStd Threads      
      zstd_thread_amount = 5
      zstd_threads = []
      for n in range(zstd_thread_amount):
            zstd_threads.append(threading.Thread(target=ZstandardThread, args=(zstd_job_queue, filter_job_queue, save_folder_path, t_info_storage, progress_info,)))
            zstd_threads[n].start()

      # Start Filter Thread
      filter_thread = threading.Thread(target=FilterThread, args=(filter_job_queue, write_job_queues, progress_info,), kwargs=filter_kwargs)
      filter_thread.start()

      # Start Write Threads
      write_threads = {}

      for file in torrent_file_paths:
            write_threads[file] = threading.Thread(target=CSVWriteThread, args=(file, write_job_queues[file], progress_info, write_folder_path, write_file_prefix))
            write_threads[file].start()
      
      report_progress(progress_info, t_info_storage, torrent_file_paths)

      script_end = datetime.now()
      total_time = script_end - script_start
      logging.info(f"Script finished in {total_time}")

if __name__ == "__main__":
      fetch_content()