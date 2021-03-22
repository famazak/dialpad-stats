from urllib.parse import urljoin
import requests
import json
import time
import pandas as pd
import csv


class DialpadStats():
    """docstring for DialpadStats."""
    
    c_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    # TODO move request logic into its own private method, raw request (_)

    def _url(self):
        url = urljoin(self.base_url, 'stats')
        return url

    # def _request(self, payload=None, method='POST', request_id=None):
    #     querystring = {"apikey": self.api_key}


    #     if method == 'POST':
    #         url = self._url()
    #         response = requests.request(method, url, json=payload, headers=headers, params=querystring)

    #     if method == 'GET':
    #         url = urljoin(self._url(), request_id)
    #         response = requests.request(method, url, headers=headers, params=querystring)

    #     try:
    #         response.raise_for_status()
    #     except requests.exceptions.HTTPError as eh:
    #         return "An HTTP error has occurred: " + repr(eh)
    #     except requests.exceptions.ConnectionError as ec:
    #         return "An error connecting to the API has occurred: " + repr(ec)
    #     except requests.exceptions.Timeout as et:
    #         return "A timeout error has occurred: " + repr(et)
    #     except requests.exceptions.RequestException as e:
    #         return "An unknown error has occurred: " + repr(e)
    #     else:
    #         response_json = json.loads(response.text)

    #     return response_json

    def get_stats_export_id(self, timezone, days_ago_start=1, days_ago_end=1, export_type='record', stat_type='calls', **kwargs):
        # refactoring this function to make POST request directly, instead of relying on requests.request abstraction
        url = self._url()
        payload = {
            "timezone": timezone,
            "days_ago_end": str(days_ago_end),
            "days_ago_start": str(days_ago_start),
            "export_type": export_type,
            "stat_type": stat_type
        }
        payload.update(kwargs)

        # response_json = self._request(payload=payload, method='POST')
        response = requests.post(url=url, data=payload, params={"apikey": self.api_key}, headers=self.c_headers)
        response_json = response.json()

        return response_json['request_id']
        # return response_json

    def get_stats_download_url(self, request_id):
        url = urljoin(self._url(), request_id)
        complete = False
        sleep_timer = 5
        while not complete:
            # response_json = self._request(payload=None, method='GET', request_id=request_id)
            response = requests.get(url, params={"apikey": self.api_key}, headers=self.c_headers)
            response_json = response.json()

            if response_json['status'] != 'complete':
                print(f"Request not yet complete -- sleeping for {sleep_timer} more seconds before checking status again")
                time.sleep(sleep_timer)
            else:
                complete = True
                return response_json['download_url']

    def load_stats(self, download_url):
        try:
            df = pd.read_csv(download_url)
        except pd.errors.EmptyDataError as e:
            return "An empty data error has occurred: " + repr(e)
        else:
            return df

    def download_stats(self, download_url):
        # TODO implement functionality to save to different directory instead of current working dir
        # TODO implement functionality to save to S3 on AWS

        # request = requests.get(download_url)
        # download_url_content = request.content
        # csv_file = open('dialpad_downloaded.csv', 'wb')

        # csv_file.write(download_url_content)
        # csv_file.close()

        response = requests.get(download_url)

        with open('outfile.csv', 'w') as f:  # TODO update file naming logic
            writer = csv.writer(f)
            for line in response.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))
