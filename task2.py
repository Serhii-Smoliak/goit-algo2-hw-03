import csv
import timeit
from BTrees.OOBTree import OOBTree

def add_item_to_tree(tree, item):
    tree[item['ID']] = item

def add_item_to_dict(dict_obj, item):
    dict_obj[item['ID']] = item

def range_query_tree(tree, min_price, max_price):
    result = []
    for _, value in tree.items(min_price, max_price):
        if min_price <= value['Price'] <= max_price:
            result.append(value)
    return result

def range_query_dict(dict_obj, min_price, max_price):
    result = []
    for _, value in dict_obj.items():
        if min_price <= value['Price'] <= max_price:
            result.append(value)
    return result

def load_data(filename):
    items = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                'ID': int(row['ID']),
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            }
            items.append(item)
    return items

def measure_time(func, *args):
    start_time = timeit.default_timer()
    func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time

def compare_performance(filename, num_queries=100):
    items = load_data(filename)
    
    tree = OOBTree()
    dict_obj = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dict_obj, item)

    min_price = 10.0
    max_price = 100.0

    tree_time = 0
    for _ in range(num_queries):
        tree_time += measure_time(range_query_tree, tree, min_price, max_price)

    dict_time = 0
    for _ in range(num_queries):
        dict_time += measure_time(range_query_dict, dict_obj, min_price, max_price)

    print(f"Загальний час виконання діапазонного запиту для {tree_time:.6f} секунд")
    print(f"Загальний час виконання діапазонного запиту для {dict_time:.6f} секунд")

compare_performance('data/generated_items_data.csv')
