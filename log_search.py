import time
from typing import Dict

import requests


class LogRhythmSearchAPI:
    """
    A class to interact with the LogRhythm Search API.

    Attributes:
        base_url (str): The base URL of the API.
        bearer_token (str): The bearer token for authorization.
    """

    def __init__(self, base_url: str, bearer_token: str):
        """
        Initializes the LogRhythmSearchAPI instance.

        Args:
            base_url (str): The base URL of the API.
            bearer_token (str): The bearer token for authorization.
        """
        self.base_url = base_url
        self.bearer_token = bearer_token

    def initiate_search(self, search_data: Dict) -> Dict:
        """
        Initiates a search using the provided search data.

        Args:
            search_data (dict): The data to be used for initiating the search.

        Returns:
            dict: The response JSON containing the task ID and status.
        """
        url = f"{self.base_url}/actions/search-task"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.bearer_token}'
        }
        response = requests.post(url, json=search_data, headers=headers)
        return response.json()

    def get_search_result(self, task_id: str) -> Dict:
        """
        Retrieves the search result for a given task ID.

        Args:
            task_id (str): The ID of the task for which search result is requested.

        Returns:
            dict: The response JSON containing the search result.
        """
        url = f"{self.base_url}/actions/search-result"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.bearer_token}'
        }
        search_result_body = {"SearchResultBody": {"searchGuid": task_id}}
        response = requests.post(url, json=search_result_body, headers=headers)
        return response.json()

    def wait_and_get_result(self, task_id: str, timeout: int = 300, polling_interval: int = 5) -> Dict:
        """
        Waits for the search to complete and returns the result.

        Args:
            task_id (str): The ID of the task.
            timeout (int): Maximum time to wait for the search to complete in seconds (default: 300).
            polling_interval (int): Interval between polling for search completion in seconds (default: 5).

        Returns:
            dict: The search result.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            task_response = self.get_search_result(task_id)
            task_status = task_response.get("taskStatus")
            if task_status in ["Completed: No Results", "Completed: Max Results", "Completed: All Results",
                               "Completed: Partial Results"]:
                return task_response
            elif task_status in ["Search Failed", "Search Cancelled"]:
                raise Exception(f"Search failed with status: {task_status}")
            time.sleep(polling_interval)
        raise TimeoutError("Search did not complete within the specified timeout period.")

    @staticmethod
    def generate_query(max_msgs_to_query: int = 100, query_timeout: int = 60, search_mode: str = "MaxN",
                       date_criteria: Dict = None, query_log_sources: list = None,
                       log_source_ids: list = None, query_filter: Dict = None,
                       query_event_manager: bool = True) -> Dict:
        """
        Generates a search query with the provided parameters.

        Args:
            max_msgs_to_query (int): Maximum number of messages to query (default: 100).
            query_timeout (int): Query timeout in seconds (default: 60).
            search_mode (str): Search mode (default: "MaxN").
            date_criteria (dict): Date criteria for the search (default: None).
            query_log_sources (list): List of log sources to query (default: None).
            log_source_ids (list): List of log source IDs (default: None).
            query_filter (dict): Query filter (default: None).
            query_event_manager (bool): Whether to query event manager (default: True).

        Returns:
            dict: The generated search query.
        """
        query = {
            "maxMsgsToQuery": max_msgs_to_query,
            "queryTimeout": query_timeout,
            "searchMode": search_mode,
            "dateCriteria": date_criteria or {},
            "queryLogSources": query_log_sources or [],
            "logSourceIds": log_source_ids or [],
            "queryFilter": query_filter or {},
            "queryEventManager": query_event_manager
        }
        return query


# Example usage:
if __name__ == "__main__":
    base_url = "https://example.com/api"
    bearer_token = "your_bearer_token_here"
    api = LogRhythmSearchAPI(base_url, bearer_token)
    search_data = LogRhythmSearchAPI.generate_query(max_msgs_to_query=100,
                                                    query_timeout=60,
                                                    search_mode="MaxN",
                                                    date_criteria={"dateMin": "2024-01-01T00:00:00Z",
                                                                   "dateMax": "2024-05-01T00:00:00Z"},
                                                    query_log_sources=[1, 2, 3],
                                                    log_source_ids=[4, 5, 6],
                                                    query_filter={"msgFilterType": 1,
                                                                  "filterGroup": {"filterItemType": 1,
                                                                                  "fieldOperator": 1,
                                                                                  "filterMode": 1,
                                                                                  "filterGroupOperator": 0,
                                                                                  "filterItems": []}},
                                                    query_event_manager=True)
    task_response = api.initiate_search(search_data)
    task_id = task_response.get("taskId")
    if task_id:
        search_result = api.wait_and_get_result(task_id)
        print(search_result)
    else:
        print("Task ID not found in response.")
