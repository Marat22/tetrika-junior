# Установка
- Linux
```bash
git clone https://github.com/Marat22/tetrika-junior.git
cd tetrika-junior
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
- Windows
```cmd
git clone https://github.com/Marat22/tetrika-junior.git
cd tetrika-junior
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```
# Запустить все тесты
После активации среды можно запустить все тесты (т.к. нужны библиотеки из requirements.txt):
```
python -m unittest discover
```

# Тестовое задание  
Общие требования:
- Для решения использовать python версии 3.9 или выше
- Для задания 2 можно использовать библиотеки, задачи 1 и 3 реализовать, используя встроенные средства языка
- Ссылку на репозиторий с готовым тестовым заданием вместе с ссылкой резюме отправлять на: https://t.me/arheugene
- Решение каждой задачи должно быть в папке с ее условием, в файле `solution.py` или в модуле solution 
- К каждой задаче необходимо написать тесты  
# Удачи!

[Задача 1](task1/task1.md)   
[Задача 2](task2/task2.md)  
[Задача 3](task3/task3.md)
