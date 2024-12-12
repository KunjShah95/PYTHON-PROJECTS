import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
import os

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = "http://" + s.getsockname()[0] + ":" + str(PORT)
    s.close()
    return ip_address

def generate_qr_code(ip_address):
    url = pyqrcode.create(ip_address)
    url.svg("myqr.svg", scale=8)

def serve_folder(port, folder):
    os.chdir(folder)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("Serving at port", port)
        print("Type this in your Browser:", get_ip_address())
        print("or use the QR code")
        httpd.serve_forever()

def main():
    global PORT
    PORT = 8010
    folder_to_share = '/path/to/folder/to/share'  # Replace with the actual path to the folder you want to share
    ip_address = get_ip_address()
    generate_qr_code(ip_address)
    webbrowser.open('myqr.svg')
    serve_folder(PORT, folder_to_share)

if __name__ == "__main__":
    main()