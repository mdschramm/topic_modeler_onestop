import os
import requests
import traceback
import pandas as pd


class BaseListingsDownloader:
    LISTINGS_FILE = 'LISTINGS_FILE.csv'
    # name, date posted, url, description columns of listings dataframe
    ID = 'id'
    NAME = 'title'
    URL = 'job_url'
    DESCRIPTION = 'description'
    DATE_POSTED = 'date_posted'

    def __init__(self, directory_path, credentials, host_endpoint):
        self.directory_path = directory_path
        self.credentials = credentials
        self.host_endpoint = host_endpoint
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


        self.listings_path = os.path.join(directory_path, BaseListingsDownloader.LISTINGS_FILE)
        if not os.path.exists(self.listings_path):
            pd.DataFrame({
                self.ID: [],
                self.NAME: [],
                self.URL: [],
                self.DESCRIPTION: [],
                self.DATE_POSTED: []
            }).to_csv(self.listings_path, index=False)

    def format_request_params(self, page):
        pass

    def make_headers(self, credentials):
        pass

    def wait_rate_limit(self, response):
        # Implement rate limit handling logic here
        pass

    def get_page_listings(self, payload):
        pass

    def get_id_from_listing(self, obj):
        pass

    def get_name_from_listing(self, obj):
        pass

    def get_url_from_listing(self, obj):
        pass

    def get_description_from_listing(self, obj):
        pass

    def get_date_posted_from_listing(self, obj):
        pass

    def has_next_page(self, payload):
        # Implement logic to check if there is a next page after a payload
        pass

    def next_page(self, payload=None):
        pass

    def make_df_row_from_listing(self, listing):
        id = self.get_id_from_listing(listing)
        name = self.get_name_from_listing(listing)
        url = self.get_url_from_listing(listing)
        description = self.get_description_from_listing(listing)
        date_posted = self.get_date_posted_from_listing(listing)
        return {
            self.ID: id,
            self.NAME: name,
            self.URL: url,
            self.DESCRIPTION: description,
            self.DATE_POSTED: date_posted
        }


        # Add name, date posted, url, description to listings dataframe

    def run(self):
        listings = pd.read_csv(self.listings_path)
        seen_listings = set(listings[self.ID])
        payload = None
        try:
            while True:
                next_page = self.next_page(payload)
                endpoint, params = self.format_request_params(next_page)
                headers = self.make_headers(self.credentials)
                response = requests.get(endpoint, headers=headers, params=params)
                if response.status_code != 200:
                    raise Exception({'error': response.status_code,
                                    'message': response.text})
                payload = response.json()
                next_listings = self.get_page_listings(payload)

                # Get a batch of listings to append
                new_rows = []
                for l in next_listings:
                    id = self.get_id_from_listing(l)
                    if id in seen_listings:
                        continue
                    seen_listings.add(id)
                    new_rows.append(self.make_df_row_from_listing(l))

                listings = pd.concat([listings, pd.DataFrame(new_rows)], axis=0)
                listings.to_csv(self.listings_path, index=False)

                if not self.has_next_page(payload):
                    break

                self.wait_rate_limit(response)
        except Exception as e:
            print('Error:', e)
            print(traceback.format_exc())
