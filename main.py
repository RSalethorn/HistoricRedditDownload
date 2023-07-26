from datetime import datetime
from TorrentDownloader import TorrentHandler
from ZtstandardHandler import ZstandardHandler
import time
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info("Script started")

save_folder_path = './Saved/'

start_date = datetime(2012, 9, 1)
end_date = datetime(2012, 9, 1)

t_handler = TorrentHandler(start_date, end_date)
t_handler.start()

zstd_handler = ZstandardHandler(t_handler)

# Every X% through unzipping a file the program will inform you of progress
progress_info_percentage = 10

script_start = datetime.now()

def generate_file_paths_by_date(start_date, end_date):
      content_types = ["comments", "submissions"]

      torrent_file_paths = []

      current_file_date = start_date 

      while current_file_date <= end_date:
            for content_type in content_types:
                  file_type_prefix = content_type[0].upper()
                  inner_torrent_path = f"reddit/{content_type}/R{file_type_prefix}_{current_file_date.strftime('%Y-%m')}.zst" 
                  torrent_file_paths.append(inner_torrent_path)

            new_month = current_file_date.month + 1
            new_year = current_file_date.year
            if new_month > 12:
                  new_month = 1
                  new_year = new_year + 1
            current_file_date = datetime(new_year, new_month, 1)
      
      return torrent_file_paths


torrent_file_paths = generate_file_paths_by_date(start_date, end_date)

for torrent_file_path in torrent_file_paths:
      current_file_path = save_folder_path + torrent_file_path

      total_file_size = t_handler.get_file_info(torrent_file_path).size

      progress_info_byte_interval = total_file_size / progress_info_percentage

      for content, file_bytes_processed in zstd_handler.read_file(current_file_path, torrent_file_path):
            if file_bytes_processed >= progress_info_byte_interval:
                  percentage = (file_bytes_processed / total_file_size) * 100
                  logging.info(f"{percentage}% of {torrent_file_path} processed\n\
                                 Example of Content: {content}")
                  progress_info_byte_interval += total_file_size / 10
                  #print(f"RC r/{content['subreddit']} - {content['author']} - {content['body']}")


script_end = datetime.now()
total_time = script_end - script_start

average_rspeed = total_file_size / total_time.total_seconds()
logging.info(f"Script finished in {total_time}, average speed was {average_rspeed} b/sec")



    