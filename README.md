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

## Usage

1. Run `startService.bat` to launch the application
2. Access web interface through your browser (automatically opens)
3. Enter device credentials:
   - Default username: Polycom
   - Password: Your phone's admin password
4. Choose operation mode (single IP or bulk upload)
5. Select desired command
6. Monitor operation status in real-time

## Target Users
This tool is specifically designed for IT administrators who need to:
- Manage multiple Poly phones efficiently
- Perform routine maintenance operations
- Gather device information
- Execute custom API commands
- Handle bulk operations through a user-friendly interface

## Requirements
- Python 3.7 or higher
- Flask
- Modern web browser
- Network access to target Poly phones
- Administrative credentials for the phones

## Installation and Setup

### Method 1: Direct Installation
1. Install Python 3.7+ from [python.org](https://www.python.org/downloads/)
2. Install required Python packages:
   ```bash
   pip install flask requests urllib3
   ```
3. Download or clone this repository to your local machine

### Method 2: Virtual Environment (Recommended)
1. Install Python 3.7+ from [python.org](https://www.python.org/downloads/)
2. Open a terminal/command prompt in the project directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
5. Install required packages:
   ```bash
   pip install flask requests urllib3
   ```

## Running the Application

### Windows Users
1. Double-click `startService.bat`
   - This will start the Flask server
   - Open your default web browser to the application
   - The interface will be available at `http://127.0.0.1:5000`

### Manual Start (All Platforms)
1. Open terminal/command prompt in the project directory
2. Activate virtual environment (if using):
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Run the Flask application:
   ```bash
   python polyFactoryResetGUI.py
   ```
4. Open your web browser and navigate to `http://127.0.0.1:5000`

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
