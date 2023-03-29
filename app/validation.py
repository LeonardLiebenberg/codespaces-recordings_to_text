import time,requests

class ValidateMetaFiles:
    def __init__(self,list1: list,list2: list):
        self.list_one= list1
        self.list_two = list2

    def list_missmatch(self):
        if len(self.list_one) == len(self.list_two):
            pass
        else:
            return [x for x in self.list_one + self.list_two if x not in self.list_one or x not in self.list_two]

class ValidateUpload:
    def __init__(self,api_url):
        self.api_url = api_url

    def check_import_status(self):
        # send initial request to get import status
        response = requests.get(self.api_url)
        import_entry_status_counts = response.json()['importEntryStatusCounts']
        
        # check if the import is already completed
        completed_count = sum(status['count'] for status in import_entry_status_counts if status['status'] == 'Completed')
        if completed_count == import_entry_status_counts[0]['count']:
            return import_entry_status_counts
        
        # keep checking until import is completed
        while True:
            response = requests.get(self.api_url)
            import_entry_status_counts = response.json()['importEntryStatusCounts']
            
            completed_count = sum(status['count'] for status in import_entry_status_counts if status['status'] == 'Completed')
            if completed_count == import_entry_status_counts[0]['count']:
                return import_entry_status_counts
            
            # wait for a few seconds before checking again
            time.sleep(5)