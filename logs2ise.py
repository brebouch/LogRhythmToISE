import sys

from ise_passive_id import CiscoISEPICManager
from log_search import LogRhythmSearchAPI

# Example usage:
if __name__ == "__main__":
    # Initialize CiscoISEPICManager
    ise_ip = sys.argv[1]
    pic_user = sys.argv[2]
    pic_pwd = sys.argv[3]
    agent_id = sys.argv[4]
    manager = CiscoISEPICManager(ise_ip, pic_user, pic_pwd)

    # Initialize LogRhythmSearchAPI
    lr_base_url = sys.argv[5]
    lr_bearer_token = sys.argv[6]
    lr_api = LogRhythmSearchAPI(lr_base_url, lr_bearer_token)

    # Example search data
    search_data = {
        "maxMsgsToQuery": 100,
        "queryTimeout": 60,
        "searchMode": "MaxN",
        "dateCriteria": {"dateMin": "2024-01-01T00:00:00Z", "dateMax": "2024-05-01T00:00:00Z"},
        "queryLogSources": [1, 2, 3],
        "logSourceIds": [4, 5, 6],
        "queryFilter": {"msgFilterType": 1, "filterGroup": {"filterItemType": 1, "fieldOperator": 1, "filterMode": 1,
                                                            "filterGroupOperator": 0, "filterItems": []}},
        "queryEventManager": True
    }

    # Initiate search
    task_response = lr_api.initiate_search(search_data)
    task_id = task_response.get("taskId")

    # Wait for search to complete
    if task_id:
        search_result = lr_api.wait_and_get_result(task_id)
        # Use search results to update ISE Passive ID
        for result in search_result["results"]:
            # Assuming the structure of search result and required data for updating ISE Passive ID
            user = result["user"]
            src_ip = result["src_ip"]
            domain = result["domain"]
            new_mapping = manager.add_identity_mapping(user=user,
                                                       src_ip=src_ip,
                                                       agent_info=agent_id,
                                                       timestamp=demo_timestamp,
                                                       domain=domain)
            if new_mapping:
                print("User added successfully:", new_mapping)
            else:
                print("Failed to add user")
    else:
        print("Task ID not found in response.")
