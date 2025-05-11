import socketio

class SocketClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.sio = socketio.Client()

        self.sio.on("connect", self._on_connect)
        self.sio.on("disconnect", self._on_disconnect)

    def connect(self):
        try:
            print(f"[*] Conectando a {self.server_url}...")
            self.sio.connect(self.server_url)
        except Exception as e:
            print(f"[!] Error de conexión: {e}")

    def _on_connect(self):
        print("[✔] Conectado al microservicio")

    def _on_disconnect(self):
        print("[!] Desconectado del microservicio")

    def send(self, event_name, data):
        self.sio.emit(event_name, data)
