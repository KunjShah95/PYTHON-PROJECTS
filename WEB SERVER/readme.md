# Simple Python Web Server


## Overview

This project implements a simple web server using Python's built-in `socket` library. It is designed to serve static HTML and JSON files over HTTP. The server supports basic error handling for common HTTP errors and provides a foundational understanding of how web servers operate at a low level.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Features

- **HTTP GET Requests**: Handles GET requests for specific paths.
- **Static File Serving**: Serves an HTML file and a JSON file.
- **Error Handling**: Provides meaningful error messages for 404, 405, and malformed requests.
- **Cross-Platform**: Compatible with any system that supports Python.

## Technologies Used

- Python 3.x
- Socket Programming

## File Structure
d:
└── PYTHON PROJECTS
└── WEB SERVER
├── main.py # The main server script ├── index.html # HTML file served at the root path └── book.json # JSON file served at the /book path

Insert Code
Edit
Copy code

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/simple-python-web-server.git
Navigate to the project directory:

bash
Insert Code
Edit
Copy code
cd simple-python-web-server
Ensure you have Python 3.x installed. You can download it from python.org.

Usage
Start the server by running the following command:

bash
Insert Code
Edit
Copy code
python main.py
Open a web browser and visit http://localhost:8080 to view the HTML page.

To access the JSON data, navigate to http://localhost:8080/book.

API Endpoints
GET /: Returns the index.html file.
GET /book: Returns the book.json file.
404 Not Found: Returned for any path not defined in the server.
405 Method Not Allowed: Returned for any request method other than GET.
Error Handling
The server includes basic error handling for common HTTP errors:

400 Bad Request: Returned when the request is malformed.
404 Not Found: Returned when the requested resource does not exist.
405 Method Not Allowed: Returned when a request method other than GET is used.
500 Internal Server Error: Returned for unexpected errors during processing.
Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License. See the LICENSE file for details.