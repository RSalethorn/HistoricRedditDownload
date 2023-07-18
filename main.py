from datetime import datetime
from TorrentDownloader import TorrentHandler
from ZtstandardHandler import ZstandardHandler
import time
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info("Script started")

start_date = datetime(2013, 10, 1)
end_date = datetime(2013, 10, 1)

t_handler = TorrentHandler(start_date, end_date).start()
zstd_handler = ZstandardHandler()

# Every X% through unzipping a file the program will inform you of progress
progress_info_percentage = 10
total_file_size = 3.3501e+9

progress_info_byte_interval = total_file_size / 10

script_start = datetime.now()

current_file_date = start_date 
while current_file_date <= end_date:
    current_file_path = f"./Saved/reddit/comments/RC_{current_file_date.strftime('%Y-%m')}.zst"         
    for content, file_bytes_processed in zstd_handler.read_file(current_file_path):
            if file_bytes_processed >= progress_info_byte_interval:
                  percentage = (file_bytes_processed / total_file_size) * 100
                  logging.info(f"{percentage}% of RC_{current_file_date.strftime('%Y-%m')}.zst processed")
                  progress_info_byte_interval += total_file_size / 10
            #print(f"RC r/{content['subreddit']} - {content['author']} - {content['body']}")
            #time.sleep(0.8)
          
    new_month = current_file_date.month + 1
    new_year = current_file_date.year
    if new_month > 12:
          new_month = 1
          new_year = new_year + 1
    current_file_date = datetime(new_year, new_month, 1)
script_end = datetime.now()
total_time = script_end - script_start

average_rspeed = total_file_size / total_time.total_seconds()
logging.info(f"Script finished in {total_time}, average speed was {average_rspeed} b/sec")
    