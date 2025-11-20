from PIL import Image, ImageDraw, ImageFont
import os
import zipfile

# Создаём папку static/images
os.makedirs("static/images", exist_ok=True)

# Параметры
banner_size = (1200, 600)
category_size = (400, 400)

# Цвета фона для разных типов
banner_bg = "#4A90E2"
category_bg = ["#8A2BE2", "#FF4500", "#32CD32", "#FFD700"]

# Тексты
banner_texts = ["Баннер 1", "Баннер 2", "Баннер 3"]
category_texts = ["Гостиная", "Спальня", "Кухня", "Офис"]

# Создаём баннеры
for i, text in enumerate(banner_texts, 1):
    img = Image.new("RGB", banner_size, banner_bg)
    draw = ImageDraw.Draw(img)
    try:
        # Пытаемся использовать системный шрифт (Windows)
        font = ImageFont.truetype("arial.ttf", 72)
    except:
        # Используем дефолтный шрифт
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((banner_size[0] - w) // 2, (banner_size[1] - h) // 2), text, fill="white", font=font)
    img.save(f"static/images/banner{i}.jpg")

# Создаём категории
for i, (text, color) in enumerate(zip(category_texts, category_bg), 1):
    img = Image.new("RGB", category_size, color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((category_size[0] - w) // 2, (category_size[1] - h) // 2), text, fill="white", font=font)
    img.save(f"static/images/category{i}.jpg")

# Создаём ZIP
with zipfile.ZipFile("mebel_placeholders.zip", "w") as zipf:
    for root, dirs, files in os.walk("static"):
        for file in files:
            zipf.write(os.path.join(root, file))

print("✅ Успешно создано!")
print("📁 Файлы изображений: static/images/")
print("📦 ZIP-архив: mebel_placeholders.zip")