import logging
import zstandard
import json

class ZstandardHandler():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    
    # Function decompresses file_path and returns line by line (Generator)
    # Code used from: github.com/Watchful1/PushshiftDumps
    def read_file(self, file_path):
        with open(file_path, 'rb') as file_handle:
            buffer = ''
            reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
            while True:
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
        chunk = reader.read(chunk_size)
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
