# Poly Phone Manager

A web-based tool designed to manage and control Poly (Polycom) phones, providing a user-friendly interface for IT administrators to perform bulk operations and maintenance tasks.

## Features

### Core Functionality
- Get device information
- Reboot phones
- Perform factory resets
- Execute custom API commands

### Key Features
- Bulk operations support for managing multiple phones simultaneously
- Authentication handling with secure password management
- Error handling and automatic retry functionality
- Real-time status updates
- Concurrent execution for efficient bulk operations
- Clean, table-based results display

### Interface Options
- Single IP address operations
- Bulk upload via text file
- Custom API command execution
- Real-time operation status monitoring

## Supported Phone Models and Minimum Firmware
- CCX (Firmware 8.0+)
- VVX (Firmware 5.9+)
- Trio 8500/8800 (Firmware 7.2+)
- Trio C60 (Firmware 8.0+)
- Trio 8300 (Firmware 8.0+)
- Edge E (Firmware 8.0+)

## Components

### polyFactoryResetGUI.py
- Flask web server providing API interface
- Handles authentication and device communication
- Manages concurrent operations and error handling

### startService.bat
- One-click startup solution
- Initializes Flask server
- Opens web interface in default browser
- Manages server startup sequence

### index.html
- User-friendly web interface
- Authentication input fields
- Command selection options
- Real-time status display
- Retry functionality for failed operations

## Target Users
This tool is specifically designed for IT administrators who need to:
- Manage multiple Poly phones efficiently
- Perform routine maintenance operations
- Gather device information
- Execute custom API commands
- Handle bulk operations through a user-friendly interface

## Requirements
- Python 3.7 or higher
- Flask, requests, urllib3 packages
- Modern web browser
- Network access to target Poly phones
- Administrative credentials for the phones

## Windows Installation & Usage

### Installation
1. Install Python 3.7+ from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
2. Download or clone this repository
3. Open Command Prompt (cmd) or PowerShell as administrator and run:
   ```cmd
   pip install flask requests urllib3
   ```

### Usage
1. Double-click `startService.bat` to launch the application
2. The web interface will automatically open in your default browser
3. Enter device credentials:
   - Default username: Polycom
   - Password: Your phone's admin password
4. Choose operation mode:
   - Single IP: Enter individual phone IP
   - Bulk Upload: Create a text file (.txt) with one IP address per line, like:
     ```text
     192.168.1.100
     192.168.1.101
     192.168.1.102
     ```
5. Select desired command
6. Monitor operation status in real-time

## Linux Installation & Usage

### Installation
1. Install Python 3.7+ using your package manager:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3
   # Mac (using homebrew)
   brew install python3
   ```
2. Download or clone this repository
3. Install required packages:
   ```bash
   pip3 install flask requests urllib3
   ```

### Running on Linux
1. Open terminal in project directory
2. Run:
   ```bash
   python3 polyFactoryResetGUI.py
   ```
3. Open browser to `http://127.0.0.1:5000`
4. Enter device credentials:
   - Default username: Polycom
   - Password: Your phone's admin password
5. Choose operation mode:
   - Single IP: Enter individual phone IP
   - Bulk Upload: Create a text file (.txt) with one IP address per line, like:
     ```text
     192.168.1.100
     192.168.1.101
     192.168.1.102
     ```
6. Select desired command
7. Monitor operation status in real-time

## Troubleshooting

### Common Issues
1. **Port 5000 already in use**
   - Close other applications using port 5000
   - Or modify the port in `polyFactoryResetGUI.py`

2. **Connection Refused**
   - Ensure target phones are on the same network
   - Verify network firewall settings
   - Check phone IP addresses are correct

3. **Authentication Failed**
   - Verify phone admin credentials
   - Default username is "Polycom"
   - Ensure phone admin password is correct

4. **Python/Flask Not Found**
   - Verify Python is installed: `python --version`
   - Verify Flask is installed: `pip list | grep Flask`
   - Reinstall requirements if needed

### Getting Help
If you encounter issues not covered here:
1. Check your Python version and package installations
2. Verify network connectivity to target phones
3. Ensure you have administrative access to the phones
4. Check phone firmware versions match minimum requirements

## Security Note
Ensure proper security measures when using this tool, as it requires administrative access to phone systems.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). This means:

- You can use, modify, and distribute this software
- If you modify and use this software in a network service, you must:
  - Make your modified source code available to users of that service
  - Include the original copyright notice
  - State significant changes made to the software
  - Provide a way to obtain the source code

See the [LICENSE](LICENSE) file for the full license text. 
