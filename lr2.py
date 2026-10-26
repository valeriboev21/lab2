from csv import reader  
from datetime import datetime 
from random import sample  


MIN_PRICE = 150  # цена от 150 рублей


def open_table():  # функция открывает books.csv и возвращает таблицу без заголовка
    try: 
        with open('books.csv', 'r', encoding='windows-1251', newline='') as csvfile:  
            table = list(reader(csvfile, delimiter=';'))  
            table = table[1:]  # отбрасываем первую строку с названиями столбцов
            return table  # возвращаем таблицу данных
    except FileNotFoundError:  
        print('Файл не найден!')  # сообщаем пользователю об ошибке
        return 0  


def count_long_titles(table):  # функция считает книги с названием длиннее 30 символов
    flag = 0  # счётчик подходящих записей
    for row in table:  
        if len(row[1]) > 30:  # проверяем что название длиннее 30 символов
            flag += 1  
    print(f'Записей с названием длиннее 30 символов: {flag}') 
    input('Нажмите Enter') 


def find_string(searchline, string):  # функция ищет подстроку без учёта регистра
    string = string.lower()  # приводим строку из таблицы к нижнему регистру
    index = string.find(searchline.lower())  # ищем шаблон (тоже в нижнем регистре), -1 если не найден
    return index  # возвращаем позицию найденной подстроки или -1


def search(table):  # функция поиска книги по автору с ограничением по цене
    searchline = input('Введите автора для поиска: ')  
    if searchline in ['0', '']:  
        return 0  
    output = open('result.txt', 'w', encoding='utf-8')  # открываем файл результата на запись
    output.write(f'Поиск от: {datetime.today()}\n\n')  # пишем в файл дату и время поиска
    flag = 0  
    for row in table:  
        if find_string(searchline, row[3]) != -1 and float(row[7]) >= MIN_PRICE:  # row[3] - автор, row[7] - цена 
            print(f'{row[3]} - {row[1]}, цена {row[7]} руб.')  # выводим автора, название и цену на экран
            output.write(f'ID {row[0]}. {row[3]} - {row[1]}. Цена {row[7]} руб.\n')  # записываем ту же запись в файл
            flag += 1  

    if flag == 0:  # если ничего не нашли
        print('Ничего не найдено!')  
    else:  # если что-то нашли
        print(f'Найдено позиций: {flag}')  
    input('Нажмите Enter')  
    output.close()  


def make_links(table):  # функция генерирует библиографические ссылки для 20 записей
    filtered = []  # список записей, у которых указан автор
    for row in table:  
        if row[3] != '':  # пропускаем записи с пустым полем "Автор"
            filtered.append(row)  
    chosen = sample(filtered, 20)  
    output = open('links.txt', 'w', encoding='utf-8')  
    number = 1  # номер текущей строки в файле
    for row in chosen:  
        year = row[6].split(' ')[0].split('.')[2]  # из даты  берём год (третья часть даты)
        link = f'{row[3]}. {row[1]} - {year}'  # собираем ссылку вида <автор>. <название> - <год>
        print(f'{number}. {link}')  
        output.write(f'{number}. {link}\n')  
        number += 1  
    output.close()  
    print('Список сохранён в файл links.txt')  
    input('Нажмите Enter')  


while True:  # бесконечный цикл главного меню
    table = open_table()  # загружаем таблицу из файла
    if table == 0:  
        break  
    print('Меню:\n1 - Количество книг с названием длиннее 30 символов\n2 - Поиск по автору (от 150 руб.)\n3 - Сгенерировать 20 библиографических ссылок\n0 - Выход')  
    menu = input('Выберите пункт меню: ')  
    match menu:  
        case '1': 
            count_long_titles(table)  
        case '2': 
            search(table)  
        case '3': 
            make_links(table)  
        case '0': 
            break  
        case _:  # любой другой ввод
            print('Нет пункта меню, нажмите Enter')  
            input() 

