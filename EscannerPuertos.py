import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import json
import re

# Inicializar colorama
init(autoreset=True)

# Firmas simples para detección de servicios
FIRMAS = {
    r"Apache/([\d\.]+)": "Apache HTTP Server v{}",
    r"nginx/([\d\.]+)": "Nginx v{}",
    r"Microsoft-IIS/([\d\.]+)": "Microsoft IIS v{}",
    r"OpenSSH_([\d\.]+)": "OpenSSH v{}",
    r"MySQL\s+([\d\.]+)": "MySQL v{}",
    r"PostgreSQL\s+([\d\.]+)": "PostgreSQL v{}"
}

def banner_grabbing(ip, puerto):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, puerto))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No disponible"
    except:
        return "No disponible"

def detectar_servicio(banner, servicio):
    for patron, descripcion in FIRMAS.items():
        match = re.search(patron, banner, re.IGNORECASE)
        if match:
            return descripcion.format(match.group(1))
    return servicio

def escanear_puerto(ip, puerto, mostrar_cerrados, resultados):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    result = sock.connect_ex((ip, puerto))
    sock.close()

    try:
        servicio = socket.getservbyport(puerto, "tcp")
    except OSError:
        servicio = "Desconocido"

    if result == 0:
        banner = banner_grabbing(ip, puerto)
        servicio = detectar_servicio(banner, servicio)
        resultados.append((puerto, "Abierto", servicio, banner))
    elif mostrar_cerrados:
        resultados.append((puerto, "Cerrado", servicio, ""))

def imprimir_resultados(ip, resultados):
    print(f"\nEscaneo de {ip}")
    print("-" * 80)
    print(f"{'Puerto':<10}{'Estado':<12}{'Servicio':<30}{'Banner'}")
    print("-" * 80)
    for puerto, estado, servicio, banner in sorted(resultados):
        if estado == "Abierto":
            print(Fore.GREEN + f"{puerto:<10}{estado:<12}{servicio:<30}{banner}")
        else:
            print(Fore.RED + f"{puerto:<10}{estado:<12}{servicio:<30}{banner}")

def guardar_resultados(ip, resultados, archivo_base):
    data = {
        "objetivo": ip,
        "resultados": [
            {"puerto": puerto, "estado": estado, "servicio": servicio, "banner": banner}
            for puerto, estado, servicio, banner in resultados
        ]
    }
    with open(f"{archivo_base}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    with open(f"{archivo_base}.txt", "w", encoding="utf-8") as f:
        f.write(f"Escaneo de {ip}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Puerto':<10}{'Estado':<12}{'Servicio':<30}{'Banner'}\n")
        f.write("-" * 80 + "\n")
        for puerto, estado, servicio, banner in sorted(resultados):
            f.write(f"{puerto:<10}{estado:<12}{servicio:<30}{banner}\n")

def main():
    ip = input("Ingrese la IP o dominio objetivo: ")
    rango = input("Ingrese el rango de puertos (ej: 1-1024): ")
    archivo = input("Nombre base para guardar resultados: ")
    mostrar_cerrados = input("¿Mostrar puertos cerrados? (s/n): ").lower() == "s"

    if "-" in rango:
        inicio, fin = map(int, rango.split("-"))
    else:
        inicio = fin = int(rango)

    resultados = []
    with ThreadPoolExecutor(max_workers=200) as executor:
        for puerto in range(inicio, fin + 1):
            executor.submit(escanear_puerto, ip, puerto, mostrar_cerrados, resultados)

    imprimir_resultados(ip, resultados)
    guardar_resultados(ip, resultados, archivo)

if __name__ == "__main__":
    main()
