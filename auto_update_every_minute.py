# auto_update_every_minute.py
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path

def auto_update():
    """ункция автоматического обновления"""
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"🕐 [{current_time}] Auto-updating progress...")
            
            # апускаем команду обновления
            result = subprocess.run(
                ['python', 'manage.py', 'auto_update_progress'], 
                capture_output=True, 
                text=True,
                cwd=Path(__file__).parent
            )
            
            if result.returncode == 0:
                print(f"✅ [{current_time}] Update successful")
                # ыводим только важные сообщения
                for line in result.stdout.split('\n'):
                    if 'progress:' in line.lower() or 'report' in line.lower():
                        print(f"   📊 {line.strip()}")
            else:
                print(f"❌ [{current_time}] Update failed: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
        
        # дем 60 секунд (1 минута)
        time.sleep(60)

def start_auto_updater():
    """апускаем авто-обновление в отдельном потоке"""
    print("🚀 Starting MINUTE auto-update system...")
    print("⏰ Updates every 60 seconds")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    # апускаем в отдельном потоке
    updater_thread = threading.Thread(target=auto_update, daemon=True)
    updater_thread.start()
    return updater_thread

if __name__ == "__main__":
    start_auto_updater()
    
    # ержим основной поток активным
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Auto-update stopped by user")
