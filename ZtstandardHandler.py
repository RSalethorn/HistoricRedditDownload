import logging
import zstandard
import json
import os
import time

class ZstandardHandler():
    def __init__(self, t_info_storage):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

        self.t_info_storage = t_info_storage
    
    # Function decompresses file_path and returns line by line (Generator)
    # Code used from: github.com/Watchful1/PushshiftDumps
    def read_file(self, inner_torrent_path, save_folder_path):
        file_save_path = save_folder_path + inner_torrent_path
        
        file_exists = False
        while file_exists == False:
            print(f"Waiting for {file_save_path} to exist")
            if os.path.exists(file_save_path) == True:
                file_exists = True
                print(f"The file ({file_save_path}) has been found")
            time.sleep(0.5)

        with open(file_save_path, 'rb') as file_handle:
            buffer = ''
            reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
            total_waits = 0
            while True:
                torrent_info = self.t_info_storage.get_torrent_info(inner_torrent_path)
                # Progress is 0 to 1 representing how much of the file is downloaded, size is total size in bytes
                downloaded_total = torrent_info['progress'] *  torrent_info['size']
                
                # Change Multiplier to 2 if breaking?
                downloaded_total_needed = file_handle.tell() + ((2**27) * 2) 

                if ( downloaded_total_needed > downloaded_total and torrent_info['progress'] != 1):
                    logging.info(f"Waiting for more of {file_save_path} to download ({downloaded_total}/{downloaded_total_needed})")
                    total_waits += 1
                    time.sleep(2)
                else:
                    #logging.info(f"Reading a chunk of {file_save_path}")
                    total_waits = 0

                    chunk = self.read_and_decode(reader, 
                                                chunk_size=2**27, 
                                                max_window_size=(2**29) * 2)
                    # If nothing returned above then stop reading
                    # (I.e. End of file)
                    if not chunk:
                        break
                    
                    # Adds last bit of previous chunk to start of this chunk
                    # Then splits by new line
                    lines = (buffer + chunk).split("\n")

                    # Returns all lines except last line
                    for line in lines[:-1]:
                        json_line = json.loads(line.strip())
                        # Returns JSON and amount of bits read through the file
                        yield json_line, file_handle.tell()

                    # Save the last line of this chunk as likely not complete so can add it to next chunk
                    buffer = lines[-1]

            reader.close()

    # Functions for uncompressing each chunk
    # Code used from: github.com/Watchful1/PushshiftDumps
    def read_and_decode(self, reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
        try:
            chunk = reader.read(chunk_size)
        except zstandard.ZstdError as e:
            print("Error happened")
        bytes_read += chunk_size
        if previous_chunk is not None:
            chunk = previous_chunk + chunk
        try:
            return chunk.decode()
        except UnicodeDecodeError:
            if bytes_read > max_window_size:
                raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
            logging.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
            return self.read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)
