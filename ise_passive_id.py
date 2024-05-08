import base64
import sys
from datetime import datetime

import requests

# Get the current datetime in UTC timezone
current_time = datetime.utcnow()

# Format the datetime as per the required format
demo_timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')

class CiscoISEPICManager:
    """
    Class to manage user identity events for Passive Identity services with Cisco ISE-PIC.
    """

    def __init__(self, ise_ip, user, pwd, verify=False):
        """
        Initializes the CiscoISEPICManager instance.

        Args:
            ise_ip (str): IP address of the Cisco ISE-PIC.
            user (str): Username for authentication.
            pwd (str): Password for authentication.
            verify (bool, optional): Whether to verify SSL certificates. Defaults to False.
        """
        self.ise_ip = ise_ip
        self.user = user
        self.pwd = pwd
        self.auth_token = self.generate_auth_token(user, pwd)
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update({"X-auth-access-token": self.auth_token})

    def generate_auth_token(self, u, p):
        """
        Generates an authentication token.

        Args:
            u (str): Username for authentication.
            p (str): Password for authentication.

        Returns:
            str: Authentication token if successful, None otherwise.
        """
        b64 = base64.b64encode((u + ':' + p).encode()).decode()
        headers = {
            'Authorization': f'Basic {b64}'
        }
        url = f"https://{self.ise_ip}:9094/api/fmi_platform/v1/identityauth/generatetoken"
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code == 204:
            return response.headers['X-auth-access-token']
        else:
            return None

    def add_identity_mapping(self, user, src_ip, agent_info, timestamp, domain, src_pat_start=None, src_pat_end=None,
                 pat_range_start=None):
        """
        Adds a user identity mapping.

        Args:
            user (str): Username.
            src_ip (str): Source IP address.
            agent_info (str): Agent information.
            timestamp (str): Timestamp in the format 'YYYY-MM-DDTHH:MM:SSZ'.
            domain (str): Domain.
            src_pat_start (int, optional): Source PAT start value. Defaults to None.
            src_pat_end (int, optional): Source PAT end value. Defaults to None.
            pat_range_start (int, optional): PAT range start value. Defaults to None.

        Returns:
            dict: Response JSON if successful, None otherwise.
        """
        url = f"https://{self.ise_ip}:9094/api/identity/v1/identity/useridentity"
        session = {
            "user": user,
            "srcIpAddress": src_ip,
            "agentInfo": agent_info,
            "timestamp": timestamp,
            "domain": domain
        }
        if src_pat_start and src_pat_end and pat_range_start:
            session["srcPatRange"] = {
                "userPatStart": src_pat_start,
                "userPatEnd": src_pat_end,
                "patRangeStart": pat_range_start
            },
        response = self.session.post(url, json=session)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def delete_identity_mapping_by_id(self, mapping_id):
        """
        Deletes a user identity mapping by ID.

        Args:
            mapping_id (str): Mapping ID.

        Returns:
            dict: Response JSON if successful, None otherwise.
        """
        url = f"https://{self.ise_ip}:9094/api/identity/v1/identity/useridentity/{mapping_id}"
        response = self.session.delete(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def delete_all_identity_mappings_by_agent_id(self, agent_id):
        """
        Deletes all user identity mappings by agent ID.

        Args:
            agent_id (str): Agent ID.

        Returns:
            dict: Response JSON if successful, None otherwise.
        """
        url = f"https://{self.ise_ip}:9094/api/identity/v1/identity/useridentity/deleteby"
        params = {"agent_id": agent_id}
        response = self.session.delete(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None


# Example usage:
if __name__ == "__main__":
    # Initialize CiscoISEPICManager
    ise_ip = sys.argv[1]
    pic_user = sys.argv[2]
    pic_pwd = sys.argv[3]
    agent_id = sys.argv[4]
    manager = CiscoISEPICManager(ise_ip, pic_user, pic_pwd)

    # Add user
    new_mapping = manager.add_identity_mapping(user="example_user",
                                src_ip="Endpoint IP",
                                agent_info=agent_id,
                                timestamp=demo_timestamp,
                                domain="example.com")
    if new_mapping:
        print("User added successfully:", new_mapping)
    else:
        print("Failed to add user")

    # Remove user (replace <id> with the actual user ID received from the Add response)
    map_id = new_mapping['id']
    removed_user = manager.delete_identity_mapping_by_id(map_id)
    if removed_user:
        print("User removed successfully:", removed_user)
    else:
        print("Failed to remove user")

    # Delete all identity mappings by agent ID
    removed = manager.delete_all_identity_mappings_by_agent_id(agent_id)
    if removed:
        print("All identity mappings deleted for agent ID:", agent_id)
    else:
        print("Failed to delete identity mappings for agent ID:", agent_id)