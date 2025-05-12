import socketio

class SocketClient:
    def __init__(self, server_url, namespace):
        self.server_url = server_url
        self.client = socketio.AsyncClient()
        self.connected = False
        self.namespace = namespace

        self.client.on("connect", self._on_connect, namespace=self.namespace)
        self.client.on("disconnect", self._on_disconnect, namespace=self.namespace)

    async def connect(self):
        try:
            print(f"[*] Conectando a {self.server_url}...")
            await self.client.connect(
                self.server_url,
                namespaces=["/bot"],
                socketio_path="web/socket.io",
                wait=True
            )
        except Exception as e:
            print(f"[!] Error de conexión: {e}")

    async def _on_connect(self):
        self.connected = True
        print("[✔] Conectado al microservicio")

    async def _on_disconnect(self):
        self.connected = False
        print("[!] Desconectado del microservicio")

    async def send(self, event_name, data):
        if self.connected:
            await self.client.emit(event_name, data, namespace=self.namespace)
        else:
            print("[!] No se puede enviar datos, no estás conectado.")
