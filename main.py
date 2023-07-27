from datetime import datetime
from TorrentThread import TorrentThread
from ZtstandardHandler import ZstandardHandler
from TorrentInfoStorage import TorrentInfoStorage
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

def wait_for_torrent_info(t_info_storage):
      while t_info_storage.get_has_init() == False:
            print("Waiting for torrent info")
            time.sleep(1)
            


if __name__ == '__main__':
      save_folder_path = './Saved/'

      start_date = datetime(2012, 9, 1)
      end_date = datetime(2012, 9, 1)

      torrent_file_paths = generate_file_paths_by_date(start_date, end_date)

      t_info_storage = TorrentInfoStorage()

      t_handler = threading.Thread(target=TorrentThread, args=(torrent_file_paths, t_info_storage,))
      t_handler.start()

      wait_for_torrent_info(t_info_storage)

      zstd_handler = ZstandardHandler(t_info_storage)
      # Every X% through unzipping a file the program will inform you of progress
      progress_info_percentage = 5

      script_start = datetime.now()

      total_file_size = 0

      for torrent_file_path in torrent_file_paths:

            current_file_path = save_folder_path + torrent_file_path

            current_file_size = t_info_storage.get_torrent_info(torrent_file_path).size
            total_file_size += current_file_size

            progress_info_byte_interval = current_file_size / progress_info_percentage

            for content, file_bytes_processed in zstd_handler.read_file(current_file_path, torrent_file_path):
                  if file_bytes_processed >= progress_info_byte_interval:
                        percentage = (file_bytes_processed / total_file_size) * 100
                        logging.info(f"{percentage}% of {torrent_file_path} processed\n\
                                    Example of Content: {content}")
                        progress_info_byte_interval += total_file_size / progress_info_percentage
                        #print(f"RC r/{content['subreddit']} - {content['author']} - {content['body']}")


      script_end = datetime.now()
      total_time = script_end - script_start

      average_rspeed = total_file_size / total_time.total_seconds()
      logging.info(f"Script finished in {total_time}, average speed was {average_rspeed} b/sec")



      