import time

class Ping:
    def execute(self, ip: str):
        if not ip.startswith("192."):
            print(t"[Proxy Error] La dirección IP debe comenzar con '192.'")
            return
        self.executefree(ip)

    def executefree(self, ip: str):
        print(f"Iniciando 10 intentos de ping a: {ip}")
        for i in range(1, 11):
            print(f"  Intento {i}: Respuesta desde {ip}: bytes=32 tiempo=10ms")
            time.sleep(0.05) 

class PingProxy:
    def __init__(self):
        self._real_ping = Ping()

    def execute(self, ip: str):
        if ip == "192.168.0.254":
            print(f"\n[Proxy] Desvío detectado para {ip}. Redirigiendo a Google...")
            self._real_ping.executefree("www.google.com")
        else:
            print(f"\n[Proxy] IP estándar detectada. Delegando a Ping tradicional.")
            self._real_ping.execute(ip)

if __name__ == "__main__":
    proxy = PingProxy()
    
    proxy.execute("192.168.0.1")
    
    proxy.execute("192.168.0.254")