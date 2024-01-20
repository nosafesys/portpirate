
# PortPirate

## Introduction
PortPirate is a versatile port scanning tool written in Python. It is designed to scan a target host for open ports quickly and efficiently. Utilizing multithreading, PortPirate can perform scans on multiple ports concurrently, making it a powerful tool for network administrators and cybersecurity enthusiasts.

## Requirements
- Python 3.x
- Additional Python packages: `socket`, `sys`, `threading`, `datetime`, `argparse`, `subprocess`, `time`, `colorama`, `concurrent.futures`, `queue`

## Installation
Clone the repository or download the script directly. Ensure that you have Python 3.x installed on your system.

```bash
git clone https://github.com/your-repository/PortPirate.git
cd PortPirate
```

## Usage
To use PortPirate, run the script with the target IP address or hostname and specify the port range. For example:

```bash
python portpirate.py 192.168.1.1 -p 1-1000
```

### Command-Line Arguments
- `target`: Specify the target IP address or hostname.
- `-p`, `--ports`: Specify port(s) to scan. Scan a single port, a comma separated list of ports, a range of ports or use the keyword \"all\" to scan all 65,535 ports.
- `-t`, `--threads`: Specify the number of threads to use (default=50).
- `-o`, `--timeout`: Specify timeout for port connection attempts.   

- Additional options and flags can be viewed with `-h` or `--help`.
