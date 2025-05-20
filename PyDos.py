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

# Language dictionaries
LANGUAGES = {
    "en": {
        "banner": r"""
 ____   ___   ____     _____           _ 
|  _ \ / _ \ / ___|   |_   _|__   ___ | |
| | | | | | | \___ \    | |/ _ \ / _ \| |
| |_| | |_| |  ___) |   | | (_) | (_) | |
|____/ \___/ |_____/    |_|\___/ \___/|_|
                PyDos Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""",
        "menu_1": "1. Resolve domain to IP",
        "menu_2": "2. Start PyDos script",
        "menu_3": "3. Change language",
        "menu_4": "4. Play Dino Game",
        "menu_0": "0. Exit",
        "select_option": "Select an option: ",
        "invalid_choice": "Invalid choice!",
        "goodbye": "Goodbye!",
        "enter_domain": "Enter domain (e.g. example.com): ",
        "domain_resolved": "Domain {domain} resolved to IP: {ip}, Port: {port}",
        "error_resolve": "Error resolving domain: {e}",
        "press_enter": "Press Enter to return to menu...",
        "script_started": "Script started: {time}",
        "ip_target": "IP Target or exit: ",
        "exiting": "Exiting script...",
        "invalid_port": "Invalid port!",
        "port": "Port: ",
        "target": "Target:",
        "thread": "Thread",
        "packets_sent": "Packets sent:",
        "menu_lang": "Select language (en/ru): ",
        "lang_changed": "Language changed to {lang}."
    },
    "ru": {
        "banner": r"""
 ____   ___   ____     _____           _ 
|  _ \ / _ \ / ___|   |_   _|__   ___ | |
| | | | | | | \___ \    | |/ _ \ / _ \| |
| |_| | |_| |  ___) |   | | (_) | (_) | |
|____/ \___/ |_____/    |_|\___/ \___/|_|
                PyDos Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""",
        "menu_1": "1. Определить IP по домену",
        "menu_2": "2. Запустить PyDos скрипт",
        "menu_3": "3. Сменить язык",
        "menu_4": "4. Играть в Dino Game",
        "menu_0": "0. Выход",
        "select_option": "Выберите опцию: ",
        "invalid_choice": "Неверный выбор!",
        "goodbye": "До свидания!",
        "enter_domain": "Введите домен (например, example.com): ",
        "domain_resolved": "Домен {domain} определён как IP: {ip}, Порт: {port}",
        "error_resolve": "Ошибка при определении домена: {e}",
        "press_enter": "Нажмите Enter для возврата в меню...",
        "script_started": "Скрипт запущен: {time}",
        "ip_target": "Целевой IP или exit: ",
        "exiting": "Выход из скрипта...",
        "invalid_port": "Неверный порт!",
        "port": "Порт: ",
        "target": "Цель:",
        "thread": "Поток",
        "packets_sent": "Пакетов отправлено:",
        "menu_lang": "Выберите язык (en/ru): ",
        "lang_changed": "Язык изменён на {lang}."
    }
}

current_lang = "en"

def tr(key, **kwargs):
    return LANGUAGES[current_lang][key].format(**kwargs)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_slow(text, color="", delay=0.03):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")

def loading_animation():
    stages = [
        "[                    ] 0%",
        "[=====               ] 25%",
        "[==========          ] 50%",
        "[===============     ] 75%",
        "[====================] 100%"
    ]
    for stage in stages:
        print_slow(stage, YELLOW, 0.2)
        time.sleep(0.3)

def animated_menu():
    options = [
        (tr("menu_1"), GREEN),
        (tr("menu_2"), RED),
        (tr("menu_3"), BLUE),
        (tr("menu_4"), CYAN),
        (tr("menu_0"), YELLOW)
    ]
    for text, color in options:
        print_slow(text, color)
        time.sleep(0.2)

def start_script_animation(name):
    print_slow(f"\n[..] Launching {name}...", BLUE, 0.07)
    time.sleep(1)

def resolve_domain():
    domain = input(tr("enter_domain"))
    try:
        ip = socket.gethostbyname(domain)
        port = input(tr("port"))
        print(tr("domain_resolved", domain=domain, ip=ip, port=port))
    except Exception as e:
        print(tr("error_resolve", e=e))
    input(tr("press_enter"))

def change_language():
    global current_lang
    lang = input(tr("menu_lang")).strip().lower()
    if lang in LANGUAGES:
        current_lang = lang
        print_slow(tr("lang_changed", lang=lang), GREEN)
    else:
        print_slow("Language not supported!", RED)
    time.sleep(1)

def main_menu():
    while True:
        clear_screen()
        print_slow(tr("banner"), CYAN)
        loading_animation()
        animated_menu()
        choice = input("\n" + tr("select_option"))
        if choice == "1":
            clear_screen()
            resolve_domain()
        elif choice == "3":
            clear_screen()
            change_language()
        elif choice == "0":
            print_slow(tr("goodbye"), YELLOW)
            break
        else:
            print_slow(tr("invalid_choice"), RED)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
