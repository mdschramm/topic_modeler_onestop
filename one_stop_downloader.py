from base_listings_downloader import BaseListingsDownloader
import time
from urllib.parse import quote
import requests
import random

WAIT_TIME = 3

CUTOFF = 10000

class OneStopDownloader(BaseListingsDownloader):
    def __init__(self, dir_path, credentials, host_api_url):
        super().__init__(dir_path, credentials, host_api_url)
        # Cursor for first listing on given page
        
        self.keyword = 'data science'
        self.location = 'united states'
        self.radius = '25'
        self.sortColumns = 'acquisitiondate'
        self.sortOrder = 'asc'
        self.cursor = 0
        self.pageSize = 500
        self.days = '0'

        # Number of consecutive times rate-limited
        self.num_limits = 0


    def format_request_params(self, page=0):

        return '{}/{}/{}/{}/{}/{}/{}/{}/{}/{}'.format(
            self.host_endpoint,
            self.credentials['user_id'],
            quote(self.keyword),
            quote(self.location),
            self.radius,
            self.sortColumns,
            self.sortOrder,
            self.cursor,
            self.pageSize,
            self.days
        ), {}
    

    def make_headers(self, credentials):
        return  {
            'Authorization': 'Bearer %s' % credentials['token'],
        }
    
    def wait_rate_limit(self, response):

        if response.status_code == 429:
            print('Rate limited %s times' % self.num_limits + 1)
            self.num_limits += 1
        else:
            self.num_limits = 0

        time.sleep(WAIT_TIME * 2**(self.num_limits) + random.uniform(0,2))

    def _get_job_description(self, id):
        user_id = self.credentials['user_id']
        headers = self.make_headers(self.credentials)

        query = '/{}/{}'.format(user_id, id)
        url = self.host_endpoint + query
        res =  requests.get(url, headers=headers)
        if res.status_code != 200:
            print('err', res.status_code, res.text)
        else:
            body = res.json()
            # Also subject to rate limit
            # self.wait_rate_limit(res)
            return body

    def get_page_listings(self, payload):
        jobs = payload['Jobs']
        numJobs = len(jobs)
        for i in range(numJobs):
            job = jobs[i]
            body = self._get_job_description(job['JvId'])
            body[self.ID] = job['JvId']
            yield body

    def get_id_from_listing(self, listing):
        return listing[self.ID]
    
    def get_name_from_listing(self, listing):
        return listing['JobTitle']
    
    def get_description_from_listing(self, listing):
        return listing['Description']
    
    def get_date_posted_from_listing(self, listing):
        return listing['DatePosted']
    

    def has_next_page(self, payload):
        # stop for test run
        if self.cursor + self.pageSize > CUTOFF:
            return False
        num_on_page = len(payload['Jobs'])
        print('Record {} to {} of {}'.format(payload['JobsKeywordLocations']['StartRow'], 
                                             payload['JobsKeywordLocations']['EndRow'], 
                                             payload['Jobcount']))
        return num_on_page == self.pageSize

    def next_page(self, payload=None):
        self.cursor += self.pageSize
        return self.cursor