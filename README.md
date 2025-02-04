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
- Python with Flask
- Modern web browser
- Network access to target Poly phones
- Administrative credentials for the phones

## Security Note
Ensure proper security measures when using this tool, as it requires administrative access to phone systems. 
