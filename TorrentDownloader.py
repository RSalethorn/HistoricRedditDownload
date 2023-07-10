import qbittorrentapi
from datetime import datetime
import time
#Secret Config File
import config

# Declare magnet_link for Torrent of PushshiftDump
magnet_link = "magnet:?xt=urn:btih:7c0645c94321311bb05bd879ddee4d0eba08aaee&tr=https%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce"
# Extract hash from magnet link
torrent_hash = magnet_link.split("&")[0].split(":")[-1]

# Get QBitTorrent Connection Details
conn_info = config.conn_info

# Months and Years (Including) to be downloaded from torrent
startMonth = datetime(2006, 12, 1)
endMonth = datetime(2007, 1, 1)

qb = qbittorrentapi.Client(**conn_info)

# Setup Authorisation for client
try:
    qb.auth_log_in()
    print("Login Success")
except qbittorrentapi.LoginFailed as e:
    print(e)

# Add torrent to QBT
qb.torrents_add(urls=magnet_link)

# Sync torrents? (May not be needed unsure)
qb.torrents_info()

# Check through all torrents in client for torrent that shares the hash of magnet link
matching_torrents = [torrent for torrent in qb.torrents_info() if torrent.hash == torrent_hash]
torrent = matching_torrents[0]

# Loop gets program to wait for metadata of torrent to be downloaded
metadata_downloaded = False
while metadata_downloaded == False:
    print("Waiting for Metadata")
    # If torrent.files has items in it then metadata has been downloaded
    if len(torrent.files) > 0:
        print(True)
        metadata_downloaded = True
    time.sleep(1)

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
        # If not don't download
        qb.torrents_file_priority(torrent_hash, file['id'], 0)
        
        

        
    


    