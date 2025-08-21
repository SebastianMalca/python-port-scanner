# Python Port Scanner 🔍

This project contains **two versions of a Python port scanner** that allow you to detect open ports, identify services, and capture banners.  
Results can be exported in **TXT** and **JSON** formats.

---

## 📌 Features
- TCP port scanning.
- Service identification using `socket.getservbyport`.
- Basic banner grabbing to gather service information.
- Export results to:
  - `resultados.txt`
  - `resultados.json`
- Supports:
  - Interactive console input.
  - Command-line arguments execution.

---

## 📂 Project Structure

python-port-scanner/  
│  
├── EscannerPuertos.py → Interactive version (input)  
├── EscannerCLI.py → Command-line arguments version (argparse)  
├── README.md  

---

## 🚀 Usage

### 🔹 1. Interactive Version (`EscannerPuertos.py`)
**Run the script:**
```
python EscannerPuertos.py
```

**Example flow:**
```
Ingrese la IP que desee escanear: 193.167.12.1
¿Desea mostrar los puertos cerrados? (s/n): s
```
Results will appear in the console and be saved in:

- resultados.txt  
- resultados.json  

---

### 🔹 2. Command-Line Version (`EscannerCLI.py`)

**Basic usage:**
```
python EscannerCLI.py -t <IP> -p <RANGE> -o <OUTPUT_FILE>
```
**Available parameters:**
- `-t` → Target IP or domain.  
- `-p` → Port range (e.g., 1-1024).  
- `-o` → Output file name (optional).  

**Example:**
```
python EscannerCLI.py -t 193.167.12.1 -p 1-65535 -o results.txt
```
---
## ⚙️ Requirements

- Python 3.x  
- No external libraries required (only standard modules: `socket`, `argparse`, `json`)  

Optional:  
- `colorama` → For colored console output.  

Install with:
```
pip install colorama
```

---
## 📑 Notes
- This scanner is intended for **educational purposes and learning**.  
- Do not use it on third-party systems without explicit authorization.  
- It is a lightweight script and does not replace professional tools like **Nmap**.  

---

## 📜 License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it for personal or educational purposes.
