"""
Poly Phone Manager - A web-based tool for managing Poly (Polycom) phones
Copyright (C) 2025 Jaron Davis

Licensed under the Elastic License 2.0
See LICENSE file for details.
Contact davisjaron@pm.me for commercial licensing.
"""

#########################################################################################
# Author: Jaron Davis
# Last Updated: 2024-07-25
# Purpose: This script provides a Flask web application to interact with Poly CCX phones.
# Notes: 
#########################################################################################
from flask import Flask, render_template, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import logging
import urllib3
import threading
import time
import os
import json
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Global variable to store command execution status
command_status = {}

def format_response(response_data):
    if isinstance(response_data, dict):
        table = "<table><tr><th>Key</th><th>Value</th></tr>"
        for key, value in response_data.items():
            if isinstance(value, dict):
                value = format_response(value)
            elif isinstance(value, list):
                value = "<ul>" + "".join(f"<li>{item}</li>" for item in value) + "</ul>"
            table += f"<tr><td>{key}</td><td>{value}</td></tr>"
        table += "</table>"
        return table
    return str(response_data)

def check_phone_status(ip, username, password, max_retries=3, retry_delay=2):
    """
    Check the status of the Poly phone.
    
    Args:
        ip (str): The IP address of the phone.
        username (str): The username for authentication.
        password (str): The password for authentication.
        max_retries (int): The maximum number of retry attempts.
        retry_delay (int): The delay between retry attempts in seconds.
    
    Returns:
        tuple: A tuple containing a boolean indicating success and a message.
    """
    url = f"https://{ip}/api/v1/mgmt/device/info"
    for attempt in range(max_retries):
        try:
            response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False, timeout=5)
            if response.status_code == 200:
                device_info = response.json()
                logging.debug(f"Device info: {device_info}")
                
                data = device_info.get('data', device_info)
                model_number = data.get('ModelNumber', '')
                firmware_release = data.get('FirmwareRelease', '')

                # Check for supported models and their minimum software versions
                if ('CCX' in model_number and firmware_release >= '8.0') or \
                   ('VVX' in model_number and firmware_release >= '5.9') or \
                   ('Trio 8500' in model_number and firmware_release >= '7.2') or \
                   ('Trio 8800' in model_number and firmware_release >= '7.2') or \
                   ('Trio C60' in model_number and firmware_release >= '8.0') or \
                   ('Trio 8300' in model_number and firmware_release >= '8.0') or \
                   ('Edge E' in model_number and firmware_release >= '8.0'):
                    return True, f"Poly phone detected and online. Model: {model_number}, Firmware: {firmware_release}"
                else:
                    return False, f"Device is online but not recognized as a supported Poly phone. Model: {model_number}, Firmware: {firmware_release}"
            elif response.status_code == 401:
                return False, "Authentication failed. Please check your username and password."
            else:
                logging.warning(f"Attempt {attempt + 1}: Failed to get device info. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1}: Error connecting to the phone: {str(e)}")
        
        if attempt < max_retries - 1:
            logging.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    return False, f"Failed to connect to the phone after {max_retries} attempts. The phone may be in sleep state or offline."

def execute_command(ip, username, password, command, custom_command=None, custom_method=None):
    """
    Execute a command on the Poly CCX phone.
    
    Args:
        ip (str): The IP address of the phone.
        username (str): The username for authentication.
        password (str): The password for authentication.
        command (str): The command to execute (getInfo, reboot, factoryReset).
        custom_command (str): The custom command to execute.
        custom_method (str): The HTTP method for the custom command.
    """
    global command_status
    command_status[ip] = {"status": "pending", "message": f"Executing {command} command..."}
    
    # Check phone status before executing the command
    success, message = check_phone_status(ip, username, password)
    if not success:
        command_status[ip] = {"status": "error", "message": message}
        return

    # Prepare the command execution
    base_url = f"https://{ip}/api/v1/"
    command_endpoints = {
        "getInfo": {"url": base_url + "mgmt/device/info", "method": "GET"},
        "reboot": {"url": base_url + "mgmt/safeRestart", "method": "POST"},
        "factoryReset": {"url": base_url + "mgmt/factoryReset", "method": "POST"},
        "custom": {"url": base_url + (custom_command.lstrip('/') if custom_command else ''), "method": custom_method or "GET"},
    }

    # Ensure the command is valid
    if command not in command_endpoints:
        command_status[ip] = {"status": "error", "message": f"Unknown command: {command}"}
        return

    endpoint = command_endpoints[command]
    headers = {'Content-Type': 'application/json'}

    try:
        if endpoint["method"] == "GET":
            response = requests.get(endpoint["url"], headers=headers, auth=HTTPBasicAuth(username, password), verify=False, timeout=10)
        else:
            response = requests.post(endpoint["url"], headers=headers, auth=HTTPBasicAuth(username, password), verify=False, timeout=10)

        if response.status_code == 200:
            if command == "getInfo":
                info = response.json().get('data', {})
                formatted_info = "<table><tr><th>Property</th><th>Value</th></tr>"
                for key, value in info.items():
                    formatted_info += f"<tr><td>{key}</td><td>{value}</td></tr>"
                formatted_info += "</table>"
                command_status[ip] = {"status": "complete", "message": f"<h3>Phone Information for {ip}:</h3>{formatted_info}"}
            elif command == "custom":
                try:
                    response_json = response.json()
                    formatted_response = format_response(response_json)
                    command_status[ip] = {
                        "status": "complete", 
                        "message": f"<h3>Custom command executed successfully on {ip}:</h3>{formatted_response}"
                    }
                except json.JSONDecodeError:
                    command_status[ip] = {
                        "status": "complete", 
                        "message": f"<h3>Custom command executed successfully on {ip}:</h3><pre>{response.text}</pre>"
                    }
            else:
                command_status[ip] = {"status": "complete", "message": f"Command {command} executed successfully on {ip}."}
        else:
            command_status[ip] = {"status": "error", "message": f"Failed to execute {command} on {ip}: Status code {response.status_code}, Response: {response.text}"}
    except requests.exceptions.RequestException as e:
        command_status[ip] = {"status": "error", "message": f"Error connecting to {ip}: {str(e)}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the main page and command execution.
    
    Returns:
        Rendered HTML template for the main page or JSON response for command execution.
    """
    global command_status
    if request.method == 'POST':
        ip = request.form.get('ip', '').strip()
        username = request.form['username']
        password = request.form['password']
        command = request.form['command']
        custom_command = request.form.get('customCommand', '')
        custom_method = request.form.get('customMethod', 'GET')
        bulk_file = request.files.get('bulkUpload')

        # Clear previous command_status
        command_status.clear()

        if bulk_file:
            # Process the uploaded file
            ip_addresses = []
            try:
                content = bulk_file.read().decode('utf-8')
                ip_addresses = [line.strip() for line in content.splitlines() if line.strip()]
            except Exception as e:
                return jsonify({"status": "error", "message": f"Failed to read file: {str(e)}"})

            # Initialize all IPs with pending status
            for ip in ip_addresses:
                command_status[ip] = {"status": "pending", "message": f"Queued {command} command..."}

            # Start concurrent execution
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda ip: execute_command(ip, username, password, command, custom_command, custom_method), ip_addresses)

            return jsonify({"status": "pending", "results": [{"ip": ip, "status": "pending", "message": f"Queued {command} command..."} for ip in ip_addresses]})
        else:
            # Single IP processing
            command_status[ip] = {"status": "pending", "message": f"Executing {command} command..."}
            threading.Thread(target=execute_command, args=(ip, username, password, command, custom_command, custom_method)).start()
            return jsonify({"status": "pending", "message": f"Executing {command} command...", "ip": ip})

    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    """
    Execute a command and return the status.
    
    Returns:
        JSON response with the command execution status.
    """
    ip = request.form.get('ip')
    bulk_file = request.files.get('bulkUpload')
    
    if bulk_file or len(command_status) > 1:
        # Handle bulk execution status
        results = [{"ip": ip, "status": status["status"], "message": status["message"]} for ip, status in command_status.items()]
        all_complete = all(status["status"] != "pending" for status in command_status.values())
        
        logging.debug(f"Bulk execution results: {json.dumps(results, indent=2)}")
        
        return jsonify({"status": "complete" if all_complete else "pending", "results": results})
    else:
        # Handle single IP execution status
        status = command_status.get(ip, {"status": "pending", "message": "Executing command..."})
        
        logging.debug(f"Single IP execution status: {json.dumps(status, indent=2)}")
        
        return jsonify(status)

@app.route('/retry_failures', methods=['POST'])
def retry_failures():
    global command_status
    username = request.form['username']
    password = request.form['password']
    command = request.form['command']

    failed_ips = [ip for ip, status in command_status.items() if status['status'] == 'error']
    
    for ip in failed_ips:
        command_status[ip] = {"status": "pending", "message": f"Retrying {command} command..."}
        threading.Thread(target=execute_command, args=(ip, username, password, command)).start()

    return jsonify({"status": "pending", "message": f"Retrying {len(failed_ips)} failed IP(s)"})

@app.route('/retry_device', methods=['POST'])
def retry_device():
    ip = request.form['ip']
    username = request.form['username']
    password = request.form['password']
    command = request.form['command']

    logging.debug(f"Retrying command for IP: {ip}")
    
    # Set the status to pending before attempting to retry
    command_status[ip] = {"status": "pending", "message": f"Retrying {command} command..."}
    
    success, message = check_phone_status(ip, username, password)
    logging.debug(f"Phone status check result: Success={success}, Message={message}")
    
    if success:
        threading.Thread(target=execute_command, args=(ip, username, password, command)).start()
        return jsonify({"status": "pending", "message": f"Retrying {command} command for {ip}...", "ip": ip})
    else:
        command_status[ip] = {"status": "error", "message": message}
        return jsonify({"status": "error", "message": message, "ip": ip})

if __name__ == '__main__':
    app.run(debug=True)
