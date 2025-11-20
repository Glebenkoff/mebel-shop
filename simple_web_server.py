#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ПРОСТОЙ ВЕБ-СЕРВЕР НА ВСТРОЕННОМ HTTP.SERVER
"""

import http.server
import socketserver
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Настройка Django для данных
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from catalog.models import Category, Product

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            categories = Category.objects.count()
            products = Product.objects.count()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>🏪 Мебельный магазин</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>🏪 Мебельный магазин</h1>
                <p><strong>Категории:</strong> {categories}</p>
                <p><strong>Товары:</strong> {products}</p>
                
                <h2>📦 Товары в наличии:</h2>
            """
            
            for product in Product.objects.all():
                html += f"""
                <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
                    <h3>{product.name}</h3>
                    <p><strong>Цена:</strong> {product.price} руб.</p>
                    <p>{product.description}</p>
                    <p><strong>В наличии:</strong> {product.stock} шт.</p>
                </div>
                """
            
            html += """
                <footer>
                    <p>🚀 Сервер работает на Python http.server</p>
                </footer>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode('utf-8'))
            
        elif parsed_path.path == '/api/categories':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            categories = list(Category.objects.values('id', 'name', 'description'))
            self.wfile.write(json.dumps(categories, ensure_ascii=False).encode('utf-8'))
            
        elif parsed_path.path == '/api/products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            products = list(Product.objects.values('id', 'name', 'price', 'description', 'stock'))
            self.wfile.write(json.dumps(products, ensure_ascii=False).encode('utf-8'))
            
        else:
            super().do_GET()

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{PORT}")
        print(f"📊 Данные: {Category.objects.count()} категорий, {Product.objects.count()} товаров")
        print("⏹️  Для остановки нажмите Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == "__main__":
    run_server()