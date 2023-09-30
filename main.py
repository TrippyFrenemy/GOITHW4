import http.server
import socketserver
import socket
import json
from datetime import datetime
import threading


# Клас для обробки запитів HTTP сервера
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            # Обробка статичних ресурсів
            if self.path.endswith('.html') or self.path.endswith('.css') or self.path.endswith('.png'):
                super().do_GET()
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            # Обробка помилки 404 Not Found
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", 'utf-8'))

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            # Розбираємо дані форми з рядка post_data
            form_data = {}
            for item in post_data.split('&'):
                key, value = item.split('=')
                form_data[key] = value
            try:
                # Перетворити дані форми в JSON
                json_data = json.dumps(form_data).encode('utf-8')
                # Відправити дані на Socket сервер
                send_to_socket_server(json_data)
                # Перенаправити користувача на головну сторінку
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            except Exception as e:
                # Обробка помилок
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(f"Internal Server Error: {str(e)}", 'utf-8'))


# Функція для обробки даних форми і відправки їх на Socket сервер
def send_to_socket_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        server_address = ('localhost', 5000)
        sock.sendto(data, server_address)


# Функція для обробки даних Socket сервера і збереження їх у data.json
def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        server_address = ('localhost', 5000)
        sock.bind(server_address)
        while True:
            data, _ = sock.recvfrom(1024)
            try:
                message = json.loads(data.decode('utf-8'))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                # Спочатку завантажте існуючі дані з JSON-файлу (якщо вони є)
                try:
                    with open('storage/data.json', 'r') as file:
                        existing_data = json.load(file)
                except FileNotFoundError:
                    existing_data = {}

                # Оновіть дані
                existing_data[timestamp] = message

                # Збережіть оновлені дані назад у JSON-файл
                with open('storage/data.json', 'w') as file:
                    json.dump(existing_data, file)

            except json.JSONDecodeError:
                print("Invalid JSON data received")


if __name__ == '__main__':
    # Запустити Socket сервер в окремому потоці
    socket_thread = threading.Thread(target=socket_server)
    socket_thread.start()

    # Запустити HTTP сервер на порту 3000
    PORT = 3000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT} http://localhost:3000/")
        httpd.serve_forever()
