# LatencyQuality

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Main Program: `netpulse.py`](#main-program-netpulsepy)
  - [Multithreading Version: `netpulse_multy.py`](#multithreading-version-netpulse_multypy)
  - [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Overview

LatencyQuality is a project aimed at measuring Quality of Service (QoS) in the client-side network environment. It provides a set of tools and scripts to evaluate latency and network performance metrics. The project includes the main program, `netpulse.py`, as well as a multithreading version, `netpulse_multy.py`. Additionally, there is a configuration file called `configuration.py`.

## Features

- Measure latency and network performance metrics in the client-side network environment.
- Perform tests using the main program, `netpulse.py`, or the multithreading version, `netpulse_multy.py`.
- Easily configure the project using the `configuration.py` file.

## Getting Started

To get started with LatencyQuality, follow these instructions:

1. Clone the repository: `git clone https://github.com/your-username/LatencyQuality.git`
2. Navigate to the project directory: `cd LatencyQuality`

## Usage

### Main Program: `netpulse.py`

To run the main program and measure latency and QoS metrics, execute the following command:

```bash
python sourceCode/netpulse.py
```

The program will start running and display the results on the console.

### Multithreading Version: `netpulse_multy.py`

To run the multithreading version of the program, which allows for concurrent measurements, use the following command:


```bash
python sourceCode/netpulse_multi.py
```

The multithreading version provides improved performance when measuring latency and network performance metrics.

### Configuration

The `configuration.py` file contains various settings that can be customized for your specific environment. Open the file using a text editor and modify the configuration options as needed.

## Dependencies

The LatencyQuality project has the following dependencies:

- Python 3.x
- Additional dependencies specified in the `requirements.txt` file

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions to LatencyQuality are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details on how to contribute to this project.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

We would like to acknowledge the following resources and projects that have inspired and helped in the development of LatencyQuality:

- [Awesome Network Analysis Tools](https://github.com/caesar0301/awesome-network-analysis)
- [Scapy](https://scapy.net/)
- [Python Threading](https://docs.python.org/3/library/threading.html)

## Contact

For any questions or suggestions, please feel free to reach out to the project maintainer at [your-email@example.com](mailto:your-email@example.com).
