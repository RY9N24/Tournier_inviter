import pyautogui
import time
import json
from config import *

time.sleep(3)
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


def click(pos, delay=0.5):
    pyautogui.moveTo(*pos)
    pyautogui.click()
    time.sleep(delay)

def type_text(text):
    pyautogui.write(text, interval=0.05)

def stable_right_click(pos):
    pyautogui.moveTo(*pos, duration=0.3)
    time.sleep(1.2)
    pyautogui.mouseDown(button='right')
    time.sleep(1.1)
    pyautogui.mouseUp(button='right')
    time.sleep(1)

def invite_player(dota_id):
    click(ADD_FRIEND_BUTTON)
    click(STEAMID_INPUT_FIELD)
    pyautogui.hotkey('ctrl', 'a')
    type_text(dota_id)
    click(SEARCH_BUTTON)
    time.sleep(2)
    click(TROPHIES_BUTTON)
    click(TROPHIES_BUTTON)

    # ПКМ по нику — как ты делал вручную
    pyautogui.moveTo(*PLAYER_NICK, duration=0.3)
    time.sleep(1.2)
    pyautogui.mouseDown(button='right')
    time.sleep(1.1)
    pyautogui.mouseUp(button='right')

    # Подождать появления меню
    time.sleep(1)

    # Теперь ЛКМ по пункту "Пригласить в лобби"
    click(INVITE_TO_LOBBY)

    # Вернуться в главное меню
    click(DOTA_ICON)

def send_lobby_message(text):
    click(LOBBY_BACK_BUTTON)
    click(LOBBY_CHAT_SELECT)
    click(CHAT_INPUT)
    type_text(text)
    pyautogui.press('enter')

def countdown(minutes=5):
    total_seconds = minutes * 60
    step = 30  # сообщение каждые 30 сек

    while total_seconds >= 0:
        mins = total_seconds // 60
        secs = total_seconds % 60
        time_str = f"{mins}:{secs:02d}"

        if total_seconds > 0:
            send_lobby_message(f"Осталось {time_str} на подключение")
        else:
            send_lobby_message("Время вышло. Запускаем матч...")

        time.sleep(step)
        total_seconds -= step

def main():
    with open('dota_ids.json', 'r') as f:
        data = json.load(f)
    
    print("Создаём лобби...")
    click(PLAY_BUTTON)
    click(CREATE_LOBBY_BUTTON)
    time.sleep(2)

    print("Приглашаем игроков...")
    for team in ['team1', 'team2']:
        for pid in data[team]:
            invite_player(pid)

    print("Обратный отсчёт до старта...")
    countdown(5)

    print("Выбираем сторону...")
    click(SIDE_SELECTION)
    time.sleep(1)

    print("Запускаем матч...")
    click(START_MATCH_BUTTON)

if __name__ == '__main__':
    main()
