import threading
import csv
import os
import logging
from queue import Empty

class CSVWriteThread(threading.Thread):
    # file_path is the path of the file that this thread will write the data from
    # write_job_queue is a queue containing content ready for this thread to write to file.
    # progress_info is thread safe data structure to store progress of threads
    # write_folder_path is the folder that should be written to
    # file_prefix is an optional prefix to be put on file_names
    def __init__(self, file_path, write_job_queue, progress_info, write_folder_path, write_file_prefix):
        fp_without_extension = file_path.split(".")[0]
        file_name = fp_without_extension.split("/")[-1]
        type_folder = fp_without_extension.split("/")[-2]

        if write_file_prefix != None:
            write_file_prefix = f"{write_file_prefix}_"

        LINE_BUFFER_AMOUNT = 25

        file_path = f"{write_folder_path}/{type_folder}/{write_file_prefix}{file_name}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        progress_info.init_write_file(file_path)

        csv_file = open(file_path, 'w+', newline='', encoding='utf-8')
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        line_buffer = []
        #logging.info(f"CSV Write Thread Started on {file_path}")
        while not write_job_queue.empty() or progress_info.get_filter_threads_status() == True:
            try:
                content_line = write_job_queue.get(timeout=5)
            except Empty:
                continue
            json_content_line = self.json_to_csv(content_line)
            line_buffer.append(json_content_line)
            if (len(line_buffer) >= LINE_BUFFER_AMOUNT):
                #print(f"WRITING TO {file_path}")
                writer.writerows(line_buffer)
                csv_file.flush()
                line_buffer.clear()
                progress_info.add_write_content_written(file_path, LINE_BUFFER_AMOUNT)
        #Write the buffer before closing the thread
        writer.writerows(line_buffer)
        csv_file.flush()
        progress_info.add_write_content_written(file_path, len(line_buffer))


    
    def json_to_csv(self, json_content):
        csv_content = []
        for key in json_content:
            content_attribute = json_content[key]

            if isinstance(content_attribute, str):
                # Remove new lines
                content_attribute = content_attribute.replace("\n", "")
                content_attribute = content_attribute.replace("\r", "")

                # Change double quotes to single quotes
                content_attribute = content_attribute.replace("\"", "\'")

            csv_content.append(content_attribute)
        return csv_content