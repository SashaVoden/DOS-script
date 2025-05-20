import os
import time
import socket
import random
from datetime import datetime
import threading
import sys
import requests

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
WHITE = '\033[97m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_slow(text, color="", delay=0.03):
 
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def loading_animation():

    stages = [
        "[====================] 100%"
    ]
    for stage in stages:
        print_slow(stage, YELLOW, 1.5)
        time.sleep(1)

def start_script_animation(name):

    print_slow(f"\n[..] Launching {name}...", BLUE, 0.07)
    time.sleep(1)

def install_file(url, file_name):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    print_slow("[..] Downloading file...", YELLOW)
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print_slow("[✓] File downloaded successfully!", GREEN)
        else:
            print_slow("[!] Failed to download file. GitHub may block direct access.", RED)
    except Exception as e:
        print_slow(f"[!] Download error: {str(e)}", RED)

def resolve_domain():
    domain = input("Enter domain (example.com): ")
    try:
        ip = socket.gethostbyname(domain)
        port = input("Port: ")
        print_slow(f"Domain {domain} resolved to IP: {ip}, Port: {port}", GREEN)
    except Exception as e:
        print_slow(f"Error resolving domain: {e}", RED)

def main_menu():

    while True:
        clear_screen()
        loading_animation()
        print_slow("""
 ____   ___   ____     _____           _ 
|  _ \ / _ \ / ___|   |_   _|__   ___ | |
| | | | | | | \___ \    | |/ _ \ / _ \| |
| |_| | |_| |  ___) |   | | (_) | (_) | |
|____/ \___/ |_____/    |_|\___/ \___/|_|
                PyDos Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""", CYAN)

        print_slow("[1] Resolve domain to IP", GREEN)
        print_slow("[2] Start PyDos", RED)
        print_slow("[3] Download PyDos manually", BLUE)
        print_slow("[0] Exit", YELLOW)

        choice = input("\nSelect an option: ")
        if choice == "1":
            clear_screen()
            resolve_domain()
        elif choice == "2":
            start_script_animation("PyDos")
        elif choice == "3":
            install_file("https://raw.githubusercontent.com/SashaVoden/PyDos/main/PyDos.py", "PyDos.py")
        elif choice == "0":
            print_slow("Goodbye!", YELLOW)
            break
        else:
            print_slow("Invalid choice!", RED)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
