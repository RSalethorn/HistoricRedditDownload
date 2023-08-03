import threading
import csv
import os

class CSVWriteThread(threading.Thread):
    def __init__(self, file_path, write_job_queue):
        fp_without_extension = file_path.split(".")[0]
        file_name = fp_without_extension.split("/")[-1]
        type_folder = fp_without_extension.split("/")[-2]
        write_folder_path = './Processed'
        custom_folder_name = "NewlyProcessed"
        custom_file_prefix = "NP"

        LINE_BUFFER_AMOUNT = 25

        file_path = f"{write_folder_path}/{custom_folder_name}/{type_folder}/{custom_file_prefix}_{file_name}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        csv_file = open(file_path, 'w+', newline='', encoding='utf-8')
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        line_buffer = []
        while True:
            content_line = write_job_queue.get()
            json_content_line = self.json_to_csv(content_line)
            line_buffer.append(json_content_line)
            if (len(line_buffer) >= LINE_BUFFER_AMOUNT):
                print(f"WRITING TO {file_path}, WRITE EXAMPLE: {line_buffer[-1]}")
                writer.writerows(line_buffer)
                csv_file.flush()
                line_buffer.clear()
    
    def json_to_csv(self, json_content):
        csv_content = []
        for key in json_content:
            csv_content.append(json_content[key])
        return csv_content