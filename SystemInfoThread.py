class SystemInfoThread(threading.Thread):
    # file_path is the path to the zst file to be unzipped
    # t_info_storage is storage class for torrent file info
    def __init__(self, zstd_job_queue, filter_job_queue, save_folder_path, t_info_storage):