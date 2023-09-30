# Simple Python Web Application with Socket Communication

This is a simple Python web application that serves two HTML pages, handles form submissions, and communicates with a socket server to save the form data in a JSON file.


## Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.x
- A modern web browser


## Setup and Usage

1. Clone or download this repository to your local machine.

2. Open a terminal and navigate to the project directory:

    ```bash
    cd path/to/project
    ```
3. Build the Docker container using the provided Dockerfile:
   ```
   docker build -t my-python-app .
   ```
4. Run the Docker container, mounting a local directory for data storage:
   ```
   docker run -v /path/to/host/directory/storage:/app/storage -p 3000:3000 my-python-app
   ```
   * Replace `/path/to/host/directory` with the path to a local directory on your host machine where you want to store the `data.json` file.
   * The `-p 3000:3000` option maps port 3000 from the container to port 3000 on your host machine.
5. Access the web application in your browser by visiting http://localhost:3000.


## Features
* The application serves two HTML pages: index.html and message.html.

* Users can submit messages using a form on the message.html page.

* Submitted messages are sent to a Socket server and saved in a JSON file (data.json) with a timestamp.

* Static resources like style.css and logo.png are served from the server.

* Error handling is implemented for 404 Not Found and 500 Internal Server Error.


