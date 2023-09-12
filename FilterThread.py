import threading
from queue import Queue, Empty
from FieldTypes import SubFields, ComFields

class FilterThread(threading.Thread):
    def __init__(self, filter_job_queue, write_job_queue, progress_info, subreddits=[], authors=[], submission_fields=[], comment_fields=[]):
        print(f"SUB FILTER: {subreddits}")
        subreddits_filter = False
        if len(subreddits) > 0:
            subreddits_filter = True

        authors_filter = False
        if len(authors) > 0:
            authors_filter = True

        if len(submission_fields) == 0:
            #TODO: FIND A WAY TO MAKE STATIC METHOD OR CHANGE CLASS COMPLETELY
            sub_field_types = SubFields()
            submission_fields = sub_field_types.all_fields()

        if len(comment_fields) == 0:
            #TODO: FIND A WAY TO MAKE STATIC METHOD OR CHANGE CLASS COMPLETELY
            com_field_types = ComFields()
            comment_fields = com_field_types.all_fields()

        sub_attributes_found = []
        com_attributes_found = []

        while filter_job_queue.empty() == False or progress_info.get_decompress_threads_status() == True:
            try:
                content = filter_job_queue.get(timeout=5)
            except Empty:
                continue

            progress_info.add_filter_content_checked(1)
            if subreddits_filter and content["subreddit"] not in subreddits:
                continue
            
            if authors_filter and content["author"] not in authors:
                continue

            write_content = {}

            if "title" in content:
                #self.check_for_new_attributes(content, sub_attributes_found, "comment")

                content["type"] = "submissions"
                # Go through each field user has given to write to file
                for field in submission_fields:
                    write_content[field] = content.get(field)
            else:
                #self.check_for_new_attributes(content, com_attributes_found, "submission")

                content["type"] = "comments"
                for field in comment_fields:
                    write_content[field] = content.get(field)
            

            original_file_name = content["file"]
            write_job_queue[original_file_name].put(write_content)

            progress_info.add_filter_valid_content(1)
        progress_info.set_filter_threads_status(False)
        print("Filter thread complete")



    def check_for_new_attributes(self, content, attribute_list, type):
        for key in content:
            if key not in attribute_list:
                attribute_list.append(key)
                print(f"**** NEW {type} KEY FOUND - {key}\n\
                        {attribute_list}")

            
            
            