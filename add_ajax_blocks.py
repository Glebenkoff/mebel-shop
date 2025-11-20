# add_ajax_blocks.py
with open('catalog/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Находим где добавить AJAX блоки
wishlist_index = None
comparison_index = None

for i, line in enumerate(lines):
    if 'def wishlist_toggle' in line:
        # Ищем конец блока added = True
        for j in range(i, len(lines)):
            if 'added = True' in lines[j]:
                wishlist_index = j + 1
                break
    elif 'def comparison_toggle' in line:
        for j in range(i, len(lines)):
            if 'added = True' in lines[j]:
                comparison_index = j + 1
                break

# Добавляем AJAX блок для wishlist
if wishlist_index is not None:
    ajax_block = [
        '\n',
        '        # AJAX поддержка\n',
        '        if request.headers.get(\'X-Requested-With\') == \'XMLHttpRequest\':\n',
        '            return JsonResponse({\n',
        '                \'success\': True,\n',
        '                \'message\': message,\n',
        '                \'added\': added,\n',
        '                \'wishlist_count\': wishlist.products.count()\n',
        '            })\n',
        '\n'
    ]
    lines[wishlist_index:wishlist_index] = ajax_block

# Добавляем AJAX блок для comparison  
if comparison_index is not None:
    ajax_block = [
        '\n',
        '        # AJAX поддержка\n',
        '        if request.headers.get(\'X-Requested-With\') == \'XMLHttpRequest\':\n',
        '            return JsonResponse({\n',
        '                \'success\': True,\n',
        '                \'message\': message,\n',
        '                \'added\': added,\n',
        '                \'comparison_count\': comparison.products.count()\n',
        '            })\n',
        '\n'
    ]
    # Учитываем смещение от первого добавления
    comparison_index_adj = comparison_index + len(ajax_block) if wishlist_index < comparison_index else comparison_index
    lines[comparison_index_adj:comparison_index_adj] = ajax_block

with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("AJAX блоки добавлены!")