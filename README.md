# OpenSky Data Streaming

This project provides tools to retrieve and process real-time data from the [OpenSky Network](https://opensky-network.org/), a platform that offers open access to air traffic surveillance data.

## Features

- Stream real-time flight data from the OpenSky API.
- Parse and process data for custom use cases.
- Save data locally for further analysis.

## Prerequisites

- Python 3.8 or higher
- An active OpenSky Network account (for API access)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/OpenSkyDataStreaming.git
    cd OpenSkyDataStreaming
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Configure your OpenSky credentials in the `.env` file:
    ```
    OPENSKY_USERNAME=your_username
    OPENSKY_PASSWORD=your_password
    ```

2. Run the data streaming script:
    ```bash
    python stream_data.py
    ```

3. Processed data will be saved in the `output/` directory.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is not affiliated with or endorsed by the OpenSky Network.