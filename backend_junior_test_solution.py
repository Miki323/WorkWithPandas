import pandas as pd

# Загружаем данные из JSON-файла в DataFrame
data = pd.read_json("trial_task.json")

# Устанавливаем опции для отображения максимального числа строк и столбцов в выводе
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


# Задача 1: Найти тариф стоимости доставки для каждого склада
# Группируем данные по складам и вычисляем сумму стоимости доставки и количество товаров
warehouse_tariffs = data.groupby("warehouse_name").agg({"highway_cost": "sum", "products": "size"})

# Вычисляем тариф стоимости доставки для каждого склада
warehouse_tariffs["tariff_per_item"] = warehouse_tariffs["highway_cost"] / warehouse_tariffs["products"]

# Выводим результат
print(warehouse_tariffs)
print("\n\n\n")
# Задача 2: Составить табличку со столбцами 'product', 'quantity', 'income', 'expenses', 'profit'
# Создаем пустой список, в который будем добавлять данные о продуктах
product_data = []

# Проходим по каждой строке в данных
for index, row in data.iterrows():
    order_id = row["order_id"]
    warehouse_name = row["warehouse_name"]
    highway_cost = row["highway_cost"]

    # Проходим по каждому продукту в заказе
    for product in row["products"]:
        product_name = product["product"]
        price = product.get("price", 0)  # Use a default value of 0 if "price" is missing
        quantity = product["quantity"]
        income = price * quantity
        expenses = highway_cost * quantity
        profit = income - expenses

        # Добавляем данные о продукте в список
        product_data.append({
            "product": product_name,
            "quantity": quantity,
            "income": income,
            "expenses": expenses,
            "profit": profit
        })

# Создаем DataFrame из списка данных о продуктах
product_summary = pd.DataFrame(product_data)

# Выводим результат
print(product_summary)
print("\n\n\n")

# Задача 3: Составить табличку с 'order_id' (id заказа) и 'order_profit' (прибыль полученная с заказа).
# А также вывести среднюю прибыль заказов
# Вычисляем прибыль (profit) для каждого заказа
data["profit"] = data["products"].apply(
    lambda products: sum(product.get("price", 0) * product["quantity"] for product in products))

# Группируем данные по 'order_id' и вычисляем суммарную прибыль для каждого заказа
order_profit_summary = data.groupby("order_id")["profit"].sum().reset_index()

# Переименовываем столбец для лучшей читаемости
order_profit_summary.rename(columns={"profit": "order_profit"}, inplace=True)

# Выводим табличку с id заказа и прибылью
print(order_profit_summary)

# Вычисляем среднюю прибыль всех заказов
average_profit = order_profit_summary["order_profit"].mean()

# Выводим среднюю прибыль
print("Средняя прибыль заказов:", average_profit)
print("\n\n\n")

# Задача 4: Составить таблицу типа 'warehouse_name', 'product', 'quantity', 'profit',
# 'percent_profit_product_of_warehouse'
# Создадим пустой список, в который будем добавлять данные о прибыли продуктов с каждого склада
warehouse_product_profit_data = []

# Проходим по каждой строке в данных
for index, row in data.iterrows():
    warehouse_name = row["warehouse_name"]
    highway_cost = row["highway_cost"]

    # Проходим по каждому продукту в заказе
    for product in row["products"]:
        product_name = product["product"]
        price = product.get("price", 0)  # Если "price" отсутствует, то по умолчанию используется значение 0
        quantity = product["quantity"]
        income = price * quantity
        expenses = highway_cost * quantity
        profit = income - expenses
        percent_profit_product_of_warehouse = (profit / row["profit"]) * 100

        # Добавляем данные о прибыли продукта с каждого склада в список
        warehouse_product_profit_data.append({
            "warehouse_name": warehouse_name,
            "product": product_name,
            "quantity": quantity,
            "profit": profit,
            "percent_profit_product_of_warehouse": percent_profit_product_of_warehouse
        })

# Создаем DataFrame из списка данных о прибыли продуктов с каждого склада
warehouse_product_profit_table = pd.DataFrame(warehouse_product_profit_data)

# Выводим результат
print(warehouse_product_profit_table)
print("\n\n\n")

# Задача 5: Отсортировать 'percent_profit_product_of_warehouse' по убыванию и посчитать накопленный процент.
# Сортируем таблицу по убыванию столбца 'percent_profit_product_of_warehouse'
sorted_table = warehouse_product_profit_table.sort_values(by="percent_profit_product_of_warehouse", ascending=False)

# Вычисляем накопленный процент
sorted_table["accumulated_percent_profit_product_of_warehouse"] = sorted_table["percent_profit_product_of_warehouse"].cumsum()

# Выводим результат
print(sorted_table)
print("\n\n\n")

# Задача 6: Присвоить категории A, B, C на основании значения накопленного процента.
# Присваиваем категории A, B, C на основании значения накопленного процента
sorted_table["category"] = pd.cut(
    sorted_table["accumulated_percent_profit_product_of_warehouse"],
    bins=[-float("inf"), 70, 90, float("inf")],
    labels=["A", "B", "C"],
    right=False
)

# Выводим результат с категориями
print(sorted_table)
print("\n\n\n")
