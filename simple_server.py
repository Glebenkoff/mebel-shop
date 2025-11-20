#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ПРОСТОЙ ВЕБ-СЕРВЕР НА FLASK
"""

from flask import Flask, jsonify
import os
import sys
from pathlib import Path

# Настройка Django для данных
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from catalog.models import Category, Product

app = Flask(__name__)

@app.route('/')
def home():
    categories = Category.objects.count()
    products = Product.objects.count()
    return f"""
    <h1>🏪 Мебельный магазин</h1>
    <p>Категории: {categories}</p>
    <p>Товары: {products}</p>
    <p>🚀 Сервер работает на Flask!</p>
    """

@app.route('/api/categories')
def api_categories():
    categories = list(Category.objects.values('id', 'name', 'description'))
    return jsonify(categories)

@app.route('/api/products')
def api_products():
    products = list(Product.objects.values('id', 'name', 'price', 'description', 'stock'))
    return jsonify(products)

if __name__ == '__main__':
    print("🚀 Запуск простого сервера на http://127.0.0.1:5000")
    app.run(debug=True)