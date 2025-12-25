"""
Telegram Broadcast Script
English: Script for collecting active chats and sending broadcast messages
Русский: Скрипт для сбора активных чатов и массовой рассылки
Polski: Skrypt do zbierania aktywnych czatów i wysyłania wiadomości
Українська: Скрипт для збору активних чатів та масової розсилки
Deutsch: Skript zum Sammeln aktiver Chats und Versenden von Nachrichten
中文: 用于收集活跃聊天并发送群发消息的脚本

Author | Автор | Autor | Автор | Autor | 作者: Ernesto Miyake
"""

import json
import asyncio
from telethon import TelegramClient
from datetime import datetime, timedelta
import os

def load_config():
    """
    EN: Load configuration from config.json file
    RU: Загрузка конфигурации из файла config.json
    PL: Wczytywanie konfiguracji z pliku config.json
    UA: Завантаження конфігурації з файлу config.json
    DE: Konfiguration aus config.json-Datei laden
    CN: 从 config.json 文件加载配置
    """
    if not os.path.exists('config.json'):
        default_config = {
            "api_id": "YOUR_API_ID",
            "api_hash": "YOUR_API_HASH",
            "phone": "+380000000000",
            "days_limit": 30,
            "broadcast_message": "Привет! Это тестовое сообщение."
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=4)
        print("Создан config.json. Заполни его своими данными!")
        print("Created config.json. Fill it with your data!")
        return None
    
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chats(chats):
    """
    EN: Save collected chats to users.txt file
    RU: Сохранение собранных чатов в файл users.txt
    PL: Zapisywanie zebranych czatów do pliku users.txt
    UA: Збереження зібраних чатів у файл users.txt
    DE: Speichern gesammelter Chats in users.txt-Datei
    CN: 将收集的聊天保存到 users.txt 文件
    """
    with open('users.txt', 'w', encoding='utf-8') as f:
        for chat_id, chat_name, date in chats:
            f.write(f"{chat_id}|{chat_name}|{date}\n")

def load_chats():
    """
    EN: Load saved chats from users.txt file
    RU: Загрузка сохраненных чатов из файла users.txt
    PL: Wczytywanie zapisanych czatów z pliku users.txt
    UA: Завантаження збережених чатів з файлу users.txt
    DE: Gespeicherte Chats aus users.txt-Datei laden
    CN: 从 users.txt 文件加载已保存的聊天
    """
    if not os.path.exists('users.txt'):
        return []
    
    chats = []
    with open('users.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 3:
                chats.append((int(parts[0]), parts[1], parts[2]))
    return chats

async def collect_active_chats(client, days_limit):
    """
    EN: Collect chats with activity in the last N days
    RU: Сбор чатов с активностью за последние N дней
    PL: Zbieranie czatów z aktywnością z ostatnich N dni
    UA: Збір чатів з активністю за останні N днів
    DE: Sammeln von Chats mit Aktivität der letzten N Tage
    CN: 收集最近 N 天有活动的聊天
    """
    print(f"\nНачинаем сбор чатов с активностью за последние {days_limit} дней...")
    print(f"Collecting chats with activity from last {days_limit} days...")
    
    chats_data = []
    cutoff_date = datetime.now() - timedelta(days=days_limit)
    
    # EN: Iterate through all dialogs
    # RU: Перебор всех диалогов
    # PL: Iteracja przez wszystkie dialogi
    # UA: Перебір усіх діалогів
    # DE: Durchlaufen aller Dialoge
    # CN: 遍历所有对话
    async for dialog in client.iter_dialogs():
        if dialog.date and dialog.date >= cutoff_date:
            chat_id = dialog.id
            chat_name = dialog.name
            date_str = dialog.date.strftime('%Y-%m-%d %H:%M:%S')
            chats_data.append((chat_id, chat_name, date_str))
            print(f"  + {chat_name} (ID: {chat_id})")
    
    save_chats(chats_data)
    print(f"\n✓ Собрано {len(chats_data)} чатов | Collected {len(chats_data)} chats")
    print(f"Сохранено в users.txt | Saved to users.txt")
    
    return len(chats_data)

async def send_broadcast(client, chats, message):
    """
    EN: Send broadcast message to all collected chats
    RU: Отправка рассылки во все собранные чаты
    PL: Wysyłanie wiadomości do wszystkich zebranych czatów
    UA: Відправка розсилки у всі зібрані чати
    DE: Broadcast-Nachricht an alle gesammelten Chats senden
    CN: 向所有收集的聊天发送群发消息
    """
    print(f"\nНачинаем рассылку в {len(chats)} чатов...")
    print(f"Starting broadcast to {len(chats)} chats...")
    print(f"Сообщение | Message: {message}\n")
    
    confirm = input("Продолжить? | Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Рассылка отменена | Broadcast cancelled")
        return 0, 0
    
    success = 0
    failed = 0
    
    # EN: Send message to each chat with 2 second delay
    # RU: Отправка сообщения в каждый чат с задержкой 2 секунды
    # PL: Wysyłanie wiadomości do każdego czatu z 2-sekundowym opóźnieniem
    # UA: Відправка повідомлення в кожен чат із затримкою 2 секунди
    # DE: Nachricht an jeden Chat mit 2 Sekunden Verzögerung senden
    # CN: 向每个聊天发送消息，延迟 2 秒
    for chat_id, chat_name, _ in chats:
        try:
            await client.send_message(chat_id, message)
            success += 1
            print(f"✓ Отправлено | Sent: {chat_name}")
            await asyncio.sleep(2)
        except Exception as e:
            failed += 1
            print(f"✗ Ошибка | Error for {chat_name}: {str(e)}")
    
    print(f"\nРассылка завершена! | Broadcast completed!")
    print(f"Успешно | Success: {success}, Ошибок | Errors: {failed}")
    
    return success, failed

def show_statistics(chats, days_limit):
    """
    EN: Display statistics about collected chats
    RU: Отображение статистики по собранным чатам
    PL: Wyświetlanie statystyk zebranych czatów
    UA: Відображення статистики по зібраним чатам
    DE: Statistiken über gesammelte Chats anzeigen
    CN: 显示收集的聊天统计信息
    """
    if chats:
        print(f"\nВсего чатов | Total chats: {len(chats)}")
        print(f"Лимит дней | Days limit: {days_limit}")
        print(f"\nПоследние 15 чатов | Last 15 chats:")
        for chat_id, chat_name, date in chats[:15]:
            print(f"  - {chat_name} (ID: {chat_id}) - {date}")
    else:
        print("Список чатов пустой | Chat list is empty")

async def main():
    """
    EN: Main function - entry point of the script
    RU: Главная функция - точка входа скрипта
    PL: Funkcja główna - punkt wejścia skryptu
    UA: Головна функція - точка входу скрипту
    DE: Hauptfunktion - Einstiegspunkt des Skripts
    CN: 主函数 - 脚本的入口点
    """
    # EN: Load configuration
    # RU: Загрузка конфигурации
    # PL: Wczytywanie konfiguracji
    # UA: Завантаження конфігурації
    # DE: Konfiguration laden
    # CN: 加载配置
    config = load_config()
    if not config:
        return
    
    # EN: Initialize Telegram client with .session file
    # RU: Инициализация клиента Telegram с файлом .session
    # PL: Inicjalizacja klienta Telegram z plikiem .session
    # UA: Ініціалізація клієнта Telegram з файлом .session
    # DE: Telegram-Client mit .session-Datei initialisieren
    # CN: 使用 .session 文件初始化 Telegram 客户端
    client = TelegramClient('session', config['api_id'], config['api_hash'])
    await client.start(phone=config['phone'])
    
    print("=" * 60)
    print("Скрипт запущен! | Script started!")
    print("=" * 60)
    print("\nДоступные команды | Available commands:")
    print("1 - Собрать чаты | Collect chats")
    print("2 - Сделать рассылку | Send broadcast")
    print("3 - Показать статистику | Show statistics")
    print("0 - Выйти | Exit\n")
    
    while True:
        choice = input("Введи команду | Enter command: ").strip()
        
        if choice == '1':
            # EN: Collect active chats
            # RU: Сбор активных чатов
            # PL: Zbieranie aktywnych czatów
            # UA: Збір активних чатів
            # DE: Aktive Chats sammeln
            # CN: 收集活跃聊天
            await collect_active_chats(client, config['days_limit'])
        
        elif choice == '2':
            # EN: Send broadcast to collected chats
            # RU: Отправка рассылки в собранные чаты
            # PL: Wysyłanie wiadomości do zebranych czatów
            # UA: Відправка розсилки у зібрані чати
            # DE: Broadcast an gesammelte Chats senden
            # CN: 向收集的聊天发送群发
            chats = load_chats()
            if not chats:
                print("Нет чатов для рассылки | No chats for broadcast")
                print("Сначала собери их (команда 1) | Collect them first (command 1)")
                continue
            
            await send_broadcast(client, chats, config['broadcast_message'])
        
        elif choice == '3':
            # EN: Show statistics
            # RU: Показать статистику
            # PL: Pokaż statystyki
            # UA: Показати статистику
            # DE: Statistiken anzeigen
            # CN: 显示统计
            chats = load_chats()
            show_statistics(chats, config['days_limit'])
        
        elif choice == '0':
            # EN: Exit program
            # RU: Выход из программы
            # PL: Wyjście z programu
            # UA: Вихід з програми
            # DE: Programm beenden
            # CN: 退出程序
            print("\nДо встречи! | See you! | Do widzenia! | До зустрічі! | Auf Wiedersehen! | 再见!")
            break
        
        else:
            print("Неверная команда! | Invalid command!")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())