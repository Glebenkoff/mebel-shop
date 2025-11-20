#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ПРОСТОЙ ВЕБ-СЕРВЕР
"""

import http.server
import socketserver
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

try:
    import django
    django.setup()
    
    from catalog.models import Category, Product
    
    print("✅ Django настроен успешно!")
    print(f"📊 Данные: {Category.objects.count()} категорий, {Product.objects.count()} товаров")
    
except Exception as e:
    print(f"❌ Ошибка Django: {e}")
    # Создаем тестовые данные напрямую через SQLite
    import sqlite3
    print("🔄 Используем прямой доступ к базе данных...")

class WebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Получаем данные напрямую из базы
            try:
                import django
                django.setup()
                from catalog.models import Category, Product
                categories_count = Category.objects.count()
                products_count = Product.objects.count()
                products = list(Product.objects.all())
            except:
                # Если Django не работает, используем прямой доступ
                import sqlite3
                conn = sqlite3.connect('db.sqlite3')
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM catalog_category")
                categories_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM catalog_product")
                products_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT name, price, description FROM catalog_product")
                products_data = cursor.fetchall()
                conn.close()
                
                products = [{'name': name, 'price': price, 'description': description} 
                           for name, price, description in products_data]
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>🏪 Мебельный магазин</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .product {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    .price {{ color: #2c5aa0; font-weight: bold; }}
                    .stats {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>🏪 Мебельный магазин</h1>
                
                <div class="stats">
                    <h2>📊 Статистика</h2>
                    <p><strong>Категории:</strong> {categories_count}</p>
                    <p><strong>Товары:</strong> {products_count}</p>
                </div>
                
                <h2>📦 Товары в наличии</h2>
            """
            
            if products:
                for product in products:
                    if hasattr(product, 'name'):
                        # Объект Django
                        html += f"""
                        <div class="product">
                            <h3>{product.name}</h3>
                            <p class="price">💰 {product.price} руб.</p>
                            <p>{product.description}</p>
                            <p><strong>В наличии:</strong> {getattr(product, 'stock', 'N/A')} шт.</p>
                        </div>
                        """
                    else:
                        # Данные из SQLite
                        html += f"""
                        <div class="product">
                            <h3>{product['name']}</h3>
                            <p class="price">💰 {product['price']} руб.</p>
                            <p>{product['description']}</p>
                        </div>
                        """
            else:
                html += "<p>😔 Товаров пока нет</p>"
            
            html += """
                <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
                    <p>🚀 Сервер работает на Python http.server</p>
                    <p>✅ Автономные скрипты: data_manager.py, working_manager.py</p>
                </footer>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode('utf-8'))
            
        elif parsed_path.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Простые данные для API
            data = {
                'status': 'success',
                'message': 'Сервер работает',
                'scripts': [
                    'data_manager.py - автономный менеджер',
                    'working_manager.py - создание данных', 
                    'direct_data_access.py - доступ к базе'
                ]
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("❌ Страница не найдена".encode('utf-8'))

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), WebHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{PORT}")
        print("📋 Доступные страницы:")
        print("   • http://localhost:8000/ - главная страница")
        print("   • http://localhost:8000/api/data - API данные")
        print("⏹️  Для остановки нажмите Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == "__main__":
    run_server()