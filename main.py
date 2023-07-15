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


current_file_date = start_date 
while current_file_date <= end_date:
    current_file_path = f"./Saved/reddit/comments/RC_{current_file_date.strftime('%Y-%m')}.zst"         
    for content, file_bytes_processed in zstd_handler.read_file(current_file_path):
            pass
            #print(f"RC r/{content['subreddit']} - {content['author']} - {content['body']}")
            #time.sleep(0.8)
          
    new_month = current_file_date.month + 1
    new_year = current_file_date.year
    if new_month > 12:
          new_month = 1
          new_year = new_year + 1
    current_file_date = datetime(new_year, new_month, 1)
logging.info("Script finished")
    