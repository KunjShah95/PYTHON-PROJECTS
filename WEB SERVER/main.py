import socket
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the specified address and port number
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Listening on port {SERVER_PORT}.... ")

def serve_file(file_path, content_type):
    """Serve a file from the server."""
    try:
        with open(file_path, 'r') as fin:
            content = fin.read()
        response = f'HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n' + content
    except FileNotFoundError:
        response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
    return response

def send_error_response(client_socket, error_message):
    """Send an error response to the client."""
    response = f'HTTP/1.1 {error_message}\n\n'
    client_socket.sendall(response.encode())

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1500).decode()
    print(request)
    
    headers = request.split('\n')
    
    try:
        first_header_components = headers[0].split()
        
        # Check if the request line is empty
        if not first_header_components:
            raise ValueError("Empty request line received.")

        http_method = first_header_components[0]
        path = first_header_components[1]

        if http_method == 'GET':
            if path == '/':
                response = serve_file('D:/PYTHON PROJECTS/WEB SERVER/index.html', 'text/html')
            elif path == '/book':
                response = serve_file('D:/PYTHON PROJECTS/WEB SERVER/book.json', 'application/json')
            else:
                response = 'HTTP/1.1 404 NOT FOUND\n\nPage Not Found'
        else:
            response = 'HTTP/1.1 405 METHOD NOT ALLOWED\n\nAllowed: GET'
    
    except ValueError as e:
        print(f"Error processing request: {e}")
        send_error_response(client_socket, "400 Bad Request")
        response = ''
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        send_error_response(client_socket, "500 Internal Server Error")
        response = ''

    if response:
        client_socket.sendall(response.encode())
    
    client_socket.close()