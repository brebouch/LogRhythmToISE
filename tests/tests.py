import unittest
from unittest.mock import patch

from logs2ise import CiscoISEPICManager, LogRhythmSearchAPI


class TestCiscoISEPICManager(unittest.TestCase):
    def test_generate_auth_token(self):
        # Test if the authentication token is generated correctly
        manager = CiscoISEPICManager("example_ip", "example_user", "example_pwd")
        expected_token = "example_token"
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 204
            mock_post.return_value.headers = {"X-auth-access-token": expected_token}
            token = manager.generate_auth_token("user", "pwd")
        self.assertEqual(token, expected_token)


class TestLogRhythmSearchAPI(unittest.TestCase):
    def test_initiate_search(self):
        # Test if search initiation returns a task ID
        lr_api = LogRhythmSearchAPI("https://logrhythm.example.com/api", "example_bearer_token")
        expected_task_id = "example_task_id"
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"taskId": expected_task_id}
            task_id = lr_api.initiate_search({})
        self.assertEqual(task_id, expected_task_id)


if __name__ == "__main__":
    unittest.main()
