import threading
class FilterThread(threading.Thread):
    def __init__(self, filter_job_queue, write_job_queue, subreddits=[], authors=[]):
        print(f"SUB FILTER: {subreddits}")
        subreddits_filter = False
        if len(subreddits) > 0:
            subreddits_filter = True

        authors_filter = False
        if len(authors) > 0:
            authors_filter = True

        while True:
            content = filter_job_queue.get()
            if subreddits_filter and content["subreddit"] not in subreddits:
                continue
            
            if authors_filter and content["author"] not in authors:
                continue

            if "title" in content:
                content["type"] = "submissions"
            else:
                content["type"] = "comments"
            
            self.add_content_to_queue(content, write_job_queue)

    def add_content_to_queue(self, content, write_queues):
        file_path = write_queues.pop("file")
        write_queues[file_path].put(content)

            
            
            