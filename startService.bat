:: Poly Phone Manager - A web-based tool for managing Poly (Polycom) phones
:: Copyright (C) 2025 Jaron Davis
::
:: Licensed under the Elastic License 2.0
:: See LICENSE file for details.
:: Contact davisjaron@pm.me for commercial licensing.

@echo off
REM Start the Flask application
start python polyFactoryResetGUI.py
REM Wait for 5 seconds to allow the server to start
timeout /t 5 /nobreak > NUL
REM Open the index.html page in the default web browser
start "" "http://127.0.0.1:5000"
REM Wait for 2 seconds before closing the command prompt
timeout /t 2 /nobreak > NUL
exit
