# Импортируем нужное
from datetime import datetime, date, timedelta
from decimal import Decimal

#Объявляем словарь
goods = {}

# Добавляем константу
DATE_FORMAT = '%Y-%m-%d'

def add(items, title, amount, expiration_date=None):
    product_information = []
    # Проверяем наличие даты
    if expiration_date is None: # Если даты нет
        product = {'amount': amount, 'expiration_date': expiration_date}
        product_information.append(product)  
    else:
        # Убедимся, что expiration_date это datetime
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, DATE_FORMAT).date()
        product = {'amount': amount, 'expiration_date': expiration_date}
        product_information.append(product)
    
    if title not in items:
        items[title] = product_information
    else:
        items[title] += product_information

# Вызов функции add
add(goods, 'Пельмени Универсальные', Decimal('0.5'), '2025-03-20')

def add_by_note(items, note):

    # Убираем запятые
    note = note.replace(',', '')

    # Делим строки на части
    for line in str.split(note, '\n'):
        parts = str.split(line, ' ')

        # Последняя часть
        last_part = parts[-1]
        # Предпоследняя часть
        second_last_part = parts[-2]

        #print(second_last_part)
        #print(last_part)

        # Последняя часть - дата или количество
        if len(str.split(parts[-1], '-')) == 3:  #  Если последняя часть - дата
            expiration_date = last_part # Присваиваем последний элемент дате
            good_amount = Decimal(second_last_part) # Присваиваем предпоследний элемент числу, и преобразуем в Decimal
            title = str.join(' ', parts[0:-2]).strip() # Объединяем все кроме даты и числа
            add(items, title, good_amount, expiration_date)
        else: # Если не дата
            expiration_date = None # Даты нет, присваиваем None
            good_amount = Decimal(last_part) # Присваиваем последний элемент числу, и преобразуем в Decimal
            title = str.join(' ', parts[0:-1]).strip() # Объединяем все кроме числа
            add(items, title, good_amount, expiration_date) 
    
add_by_note(goods, 'Яблоки, 2')
add_by_note(goods, 'Молоко, 1.5, 2023-10-10')

def find(items, needle):
    results = [] # Место хранения заголовков
    needle_lower = needle.lower() #Не учитываем регистр
    #Добавляем заголовки с помощью append
    for key in items.keys():
        if needle_lower in key.lower():  
            results.append(key)
    return results

def amount(items, needle):
    # применяем find()
    find_items = find(items, needle)
    total_amount = Decimal('0') # Начало для суммирования в виде Decimal
    # Суммируем
    for item in find_items:
        for batch in items[item]:
            total_amount += batch['amount']
    return total_amount

def expire(items, in_advance_days=0):
    today = date.today() # Сегодня
    future_day = today + timedelta(days = in_advance_days) # Добавляем дни

    perishable_products = [] # Создаем список для портящихся

    # Итерируемся по всем товарам в items
    for title, product_info in items.items():
        for product in product_info:
            expiration_date = product['expiration_date']
            if expiration_date and expiration_date <= future_day:
                perishable_products.append((title, product['amount']))

    products_name = [parts[0] for parts in perishable_products] # Список названий продуктов
    products_quantities = [parts[1] for parts in perishable_products] # Список количества продуктов

    # Проверяем, равны ли длины списков
    if len(product_names) != len(products_quantities):
        raise ValueError("Списки должны быть равны по длине.")

    # Создаем список уникальных продуктов и удаляем дубликаты
    unique_product_names = list(set(products_names)) 

    # Создаем список количества уникальных продуктов и используем Decimal
    unique_product_quantities = [Decimal('0') for _ in unique_product_names]

    # Проверяем, равны ли длины списков
    if len(products_names) != len(unique_product_quantities):
        raise ValueError("Списки должны быть равны по длине.")
    
    # Получаем два списка: уникальные наименования и их количества
    final_product_names = list(unique_product_quantities.keys())
    final_product_quantities = list(unique_product_quantities.values())

    # Объединяем их в список кортежей
    result = list(zip(final_product_names, final_product_quantities))

    return result
    