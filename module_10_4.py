import queue
from queue import Queue
import time
import threading
import random
from time import sleep

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        sleep_ = random.randint(3,10)
        sleep(sleep_)
class Cafe:

    def __init__(self, queue, *tables):
        self.queue = Queue()
        self.tables = tables
    #прибытие
    def guest_arrival(self, *guests):  #принимает неограниченное количество объектов(гостей)
        for guest in guests:
            table = None
            stol = [x for x in self.tables if x.guest is None] #проверка
            if len(stol) > 0: # если номер стола больше 0
                table = stol[0] #занимаем первый из номеров
            if table is not None:
                table.guest = guest
                guest.start() #запускаем поток гостя
                print(f'{guest.name} сел(-а) за стол номер {table.number}')
            else:
                self.queue.put(guest) #ставим в очередь
                print(f'{guest.name} в очереди')


    def discuss_guests(self):
        while not self.queue.empty() or any(x.guest is not None for x in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None #стол освободился
                if table.guest is None and not self.queue.empty():
                    guest = self.queue.get() #взяли из очереди
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')




# Создание столов
tables = [Table(number) for number in range(1,6)]
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman','Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()