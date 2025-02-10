:: Poly Phone Manager - A web-based tool for managing Poly (Polycom) phones
:: Copyright (C) 2025 Jaron Davis
::
:: This program is free software: you can redistribute it and/or modify
:: it under the terms of the GNU Affero General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: This program is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU Affero General Public License for more details.
::
:: You should have received a copy of the GNU Affero General Public License
:: along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
