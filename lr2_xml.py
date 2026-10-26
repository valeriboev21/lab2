import xml.dom.minidom as minidom  

xml_file = open('currency.xml', 'r', encoding='windows-1251')  
xml_data = xml_file.read()  

dom = minidom.parseString(xml_data)  # разбираем строку и получаем объект документа
dom.normalize()  

elements = dom.getElementsByTagName('Valute')  # получаем список всех тегов Valute (валют)
values = []  # список для значений Value

for node in elements:  # перебираем каждую валюту
    for child in node.childNodes:  # перебираем дочерние узлы валюты
        if child.nodeType == 1:  # проверяем, что узел - это тег (элемент)
            if child.tagName == 'Value':  # нас интересует только тег Value
                if child.firstChild.nodeType == 3:  # проверяем, что внутри тега находится текст
                    values.append(float(child.firstChild.data.replace(',', '.')))  

average = sum(values) / len(values)  

print(f'Количество валют: {len(values)}')  # выводим количество обработанных валют
print(f'Средний показатель Value: {average:.1f}')  

xml_file.close()  