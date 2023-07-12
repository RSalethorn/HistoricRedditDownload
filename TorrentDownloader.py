import qbittorrentapi
from datetime import datetime
import time
#Secret Config File
import config
import os
import math
import json
import logging.handlers
import zstandard

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

# Returns the new torrent by passing in old torrent object from torrents_info
def updateTorrent(torrent):
    return qb.torrents_info(torrent_hashes=torrent.hash)[0]

# Declare magnet_link for Torrent of PushshiftDump
magnet_link = "magnet:?xt=urn:btih:7c0645c94321311bb05bd879ddee4d0eba08aaee&tr=https%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
# Extract hash from magnet link
torrent_hash = magnet_link.split("&")[0].split(":")[-1]

current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
download_location = current_directory + "\\Download\\"
saved_location = current_directory + "\\Saved\\"
print(download_location)
print(saved_location)

# Get QBitTorrent Connection Details
conn_info = config.conn_info

# Months and Years (Including) to be downloaded from torrent
startMonth = datetime(2007, 8, 1)
endMonth = datetime(2007, 9, 1)

qb = qbittorrentapi.Client(**conn_info)

# Setup Authorisation for client
try:
    qb.auth_log_in()
    print("Login Success")
except qbittorrentapi.LoginFailed as e:
    print(e)

# Add torrent to QBT
qb.torrents_add(urls=magnet_link, use_download_path=True, save_path=saved_location, download_path=download_location)

# Sync torrents? (May not be needed unsure)
qb.torrents_info()

# Wait loop incase API running slow and torrent hasn't been added yet
torrent_added = False
while torrent_added == False:
    # Check through all torrents in client for torrent that shares the hash of magnet link
    matching_torrents = [torrent for torrent in qb.torrents_info() if torrent.hash == torrent_hash]
    try:
        torrent = matching_torrents[0]
        # torrent_added only changed if previous line doesn't cause error. (Needs verifying)
        torrent_added = True
    except IndexError:
        print("Waiting for torrent being added")
        time.sleep(1)

# Loop gets program to wait for metadata of torrent to be downloaded
metadata_downloaded = False
while metadata_downloaded == False:
    print("Waiting for Metadata")
    # If torrent.files has items in it then metadata has been downloaded
    if len(torrent.files) > 0:
        print(True)
        metadata_downloaded = True
    time.sleep(1)

# Loop through all files in Pushshift torrent
for file in torrent.files:
    # Convert file name into date
    date_str = file.name.split("_")[-1].split(".")[0] + "-01"
    date = datetime.strptime(date_str, "%Y-%m-%d")
    # If date on this file is included in the timeframe given set priority to one
    if date >= startMonth and date <= endMonth:
        qb.torrents_file_priority(torrent_hash, file['id'], 1)
        print(file.name)
        metadata_downloaded = True
    else:
        # If not don't download (Priority = 0)
        qb.torrents_file_priority(torrent_hash, file['id'], 0)

print(torrent)

# Loop waits till torrent is finished downloading
torrent_download_finished = False
while torrent_download_finished == False:
    torrent = updateTorrent(torrent)
    if torrent.amount_left == 0:
        torrent_download_finished = True
        print("Torrent download is finshed")
    else:
        total_parts = torrent.amount_left + torrent.completed
        percentage_complete = math.floor(100 - ((torrent.amount_left / total_parts) * 100))
        print(f"Torrent {percentage_complete}% complete")
    time.sleep(1.5)

# Functions for uncompressing and reading zstandard files from Pushshift dumps github page
def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)

def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)

			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line.strip(), file_handle.tell()

			buffer = lines[-1]

		reader.close()
                
current_file_date = startMonth  
while current_file_date <= endMonth:
    current_file_path = f"./Saved/reddit/comments/RC_{current_file_date.strftime('%Y-%m')}.zst"
    print(f"CFP: {current_file_path}")          
    for line, file_bytes_processed in read_lines_zst(current_file_path):
          comment = json.loads(line)
          print(f"RC r/{comment['subreddit']} - {comment['author']} - {comment['body']}")
          time.sleep(0.8)
    new_month = current_file_date.month + 1
    new_year = current_file_date.year
    if new_month > 12:
          new_month = 1
          new_year = new_year + 1
    current_file_date = datetime(new_year, new_month, 1)
    
        



        
        

        
    


    