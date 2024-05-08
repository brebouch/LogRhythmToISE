# Cisco ISE Passive ID Manager with LogRhythm Search Integration

This script integrates Cisco ISE Passive ID management with LogRhythm Search API. It allows users to perform searches using LogRhythm and use the search results to update user identity mappings in Cisco ISE.

## Prerequisites

- Python 3.x installed on your system
- Required Python packages can be installed via pip using `requirements.txt`

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/cisco-ise-passive-id-manager.git
   ```

2. Navigate to the project directory:

   ```bash
   cd cisco-ise-passive-id-manager
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Operation

1. Obtain necessary credentials and access tokens:
   - Cisco ISE IP address
   - Cisco ISE username and password
   - LogRhythm base URL
   - LogRhythm API bearer token

2. Update the \`config.json\` file with your credentials and settings.

3. Run the script using Python:

   ```bash
   python main.py
   ```

## Usage

The script integrates Cisco ISE Passive ID management with LogRhythm Search API. It performs the following steps:

1. Initializes CiscoISEPICManager with provided credentials for Cisco ISE.
2. Initializes LogRhythmSearchAPI with provided credentials for LogRhythm.
3. Initiates a search using LogRhythm Search API.
4. Waits for the search to complete.
5. Uses the search results to update user identity mappings in Cisco ISE.

Example usage:

```bash
python logs2ise.py <ise_ip> <ise_username> <ise_password> <agent_id> <log_rhythm_api_url> <log_rhythm_token>
```

Replace `<ise_ip>`, `<ise_username>`, `<ise_password>`, and `<agent_id>` with your Cisco ISE IP address, username, password, and agent ID respectively.

## Running Tests
To run the tests, execute the following command:

```bash
python tests.py
```

This will run the unit tests for the script and ensure its functionality.

## Contributors

- [Brennan Bouchard](https://github.com/brebouch)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
