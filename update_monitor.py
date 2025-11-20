# update_monitor.py
import json
from datetime import datetime
from pathlib import Path

def log_update():
    """огирует каждое обновление"""
    log_file = Path(__file__).parent / 'update_log.json'
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'time_display': datetime.now().strftime("%H:%M:%S"),
        'type': 'auto_update'
    }
    
    # итаем существующий лог
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            try:
                log_data = json.load(f)
            except:
                log_data = []
    else:
        log_data = []
    
    # обавляем новую запись
    log_data.append(log_entry)
    
    # Сохраняем только последние 100 записей
    log_data = log_data[-100:]
    
    # Сохраняем лог
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"📝 Update logged at {log_entry['time_display']}")

if __name__ == "__main__":
    log_update()
