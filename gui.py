# -*- coding: windows-1251 -*-
import tkinter as tk
from tkinter import ttk, IntVar
from tkinter import *

import utils
from utils import parseTasksAsMatrix

data = parseTasksAsMatrix("data/data.xlsx")
root = tk.Tk()
root.title("Таблица данных с кнопками и выпадающими списками")
button_frame = tk.Frame(root)
button_frame.pack(side="left", fill="y")


def filling_table(data):
  print(data[0])
  column_names = [
      "Номер", "Приоритет", "Заказчик", "Приёмщик", "Проект", "Команда",
      "Тип задачи", "Статус", "Состояние", "Аналитик", "Разработчик",
      "Тестировщик", "Релиз менеджер"
  ]
  for i in data:
    tree_view.insert("", 'end', values=i)

  for col in column_names:
    tree_view.heading(col, text=col, anchor=W)

  for i in column_names:
    tree_view.column(i, width=150, minwidth=50)


dropdown_frame = tk.Listbox(root)
dropdown_frame.pack(side="left", fill="y")


def clear_treeview():
  for _ in tree_view.get_children():
    tree_view.delete(_)


def raise_menubutton(*args):
  taskID.menu.post(taskID.winfo_rootx(),
                   taskID.winfo_rooty() + taskID.winfo_height())


taskID = tk.Menubutton(dropdown_frame, text="Номер", relief="raised")
taskID.menu = tk.Menu(taskID, tearoff=0)
taskID["menu"] = taskID.menu
taskID.pack()


def on_checkbutton_clicked(variable, label):
  if variable.get() == False:
    print(f"Кнопка '{label}' активна, добавляем в массив a")
    nums_of_tasks.append(label)
    print(nums_of_tasks)
  else:
    print(f"Кнопка '{label}' неактивна, удаляем из массива a")
    nums_of_tasks.remove(label)
    print(nums_of_tasks)
    new_list = []
    for i in nums_of_tasks:
      new_list.append(int(i))
    some_list[0] = ['Номер', new_list]

    clear_treeview()
    print(some_list[0])
    data = utils.getFilteredTasks([['Номер', new_list]], "data/data.xlsx")
    filling_table(data)


nums_of_tasks = [str(i) for i in range(1300)]
# cascade
for i in range(13):
  submenu = tk.Menu(taskID.menu, tearoff=0)
  taskID.menu.add_cascade(label=f"{i * 100}", menu=submenu)
  for z in range(10):
    submenu1 = tk.Menu(submenu, tearoff=0)
    submenu.add_cascade(label=f"{i * 100 + z * 10}", menu=submenu1)
    for j in range(10):
      on, off = 1, 0
      item = tk.IntVar(value=1)
      label = f"{i * 100 + z * 10 + j}"
      submenu1.add_checkbutton(
          label=label,
          variable=item,
          onvalue=0,
          offvalue=1,
          command=lambda l=label: on_checkbutton_clicked(item, l))

verticalScrollbar = ttk.Scrollbar(root, orient="vertical")
horizontalScrollbar = ttk.Scrollbar(root, orient="horizontal")
verticalScrollbar.pack(side="right", fill="y")
horizontalScrollbar.pack(side="bottom", fill="x")

column_names = [
    "Номер", "Приоритет", "Заказчик", "Приёмщик", "Проект", "Команда",
    "Тип задачи", "Статус", "Состояние", "Аналитик", "Разработчик",
    "Тестировщик", "Релиз менеджер"
]
tree_view = ttk.Treeview(root,
                         columns=column_names,
                         show="headings",
                         yscrollcommand=verticalScrollbar.set,
                         xscrollcommand=horizontalScrollbar.set)

some_list = []
for i in column_names:
  some_list.append((i, []))
some_list[0] = ["Номер", nums_of_tasks]
filling_table(data)

verticalScrollbar.config(command=tree_view.yview)
horizontalScrollbar.config(command=tree_view.xview)
tree_view.pack(fill='both', expand=1)

priority = tk.Menubutton(dropdown_frame, text="Приоритет", relief="raised")
priority.menu = tk.Menu(priority, tearoff=0)
priority["menu"] = priority.menu
priority.pack()
some_list[1] = ["Приоритет", ["Высокий", "Средний", "Низкий"]]

submenu = tk.Menu(priority.menu, tearoff=0)
priority.menu.add_checkbutton(label="Высокий")
priority.menu.add_checkbutton(label="Средний")
priority.menu.add_checkbutton(label="Низкий")

asker = tk.Menubutton(dropdown_frame, text="Заказчик", relief="raised")
asker.menu = tk.Menu(asker, tearoff=0)
asker["menu"] = asker.menu
asker.pack()
some_list[2] = [
    "Заказчик",
    ["Анна Попова", "Кирилл Шапошников", "Михаил Авдеев", "София Ершова"]
]
submenu = tk.Menu(asker.menu, tearoff=0)
asker.menu.add_checkbutton(label="Анна Попова")
asker.menu.add_checkbutton(label="Кирилл Шапошников")
asker.menu.add_checkbutton(label="Михаил Авдеев")
asker.menu.add_checkbutton(label="София Ершова")

getter = tk.Menubutton(dropdown_frame, text="Приёмщик", relief="raised")
getter.menu = tk.Menu(getter, tearoff=0)
getter["menu"] = getter.menu
getter.pack()

some_list[3] = ["Приёмщик", ["Дарья Захарова", "Егор Михеев", "Иван Тимофеев"]]

submenu = tk.Menu(getter.menu, tearoff=0)
getter.menu.add_checkbutton(label="Дарья Захарова")
getter.menu.add_checkbutton(label="Егор Михеев")
getter.menu.add_checkbutton(label="Иван Тимофеев")

project = tk.Menubutton(dropdown_frame, text="Проект", relief="raised")
project.menu = tk.Menu(project, tearoff=0)
project["menu"] = project.menu
project.pack()

some_list[4] = [
    "Проект", ["Проект 1", "Проект 2", "Проект 3", "Проект 4", "Проект 5"]
]

submenu = tk.Menu(project.menu, tearoff=0)
project.menu.add_checkbutton(label="Проект 1")
project.menu.add_checkbutton(label="Проект 2")
project.menu.add_checkbutton(label="Проект 3")
project.menu.add_checkbutton(label="Проект 4")
project.menu.add_checkbutton(label="Проект 5")

team = tk.Menubutton(dropdown_frame, text="Команда", relief="raised")
team.menu = tk.Menu(team, tearoff=0)
team["menu"] = team.menu
team.pack()

some_list[5] = ["Команда", ["Команда 1", "Команда 2", "Команда 3"]]

submenu = tk.Menu(team.menu, tearoff=0)
team.menu.add_checkbutton(label="Команда 1")
team.menu.add_checkbutton(label="Команда 2")
team.menu.add_checkbutton(label="Команда 3")

taskType = tk.Menubutton(dropdown_frame, text="Тип задачи", relief="raised")
taskType.menu = tk.Menu(taskType, tearoff=0)
taskType["menu"] = taskType.menu
taskType.pack()

some_list[6] = [
    "Тип задачи", ["Доработка", "Новая функциональность", "Ошибка"]
]

submenu = tk.Menu(taskType.menu, tearoff=0)
taskType.menu.add_checkbutton(label="Доработка")
taskType.menu.add_checkbutton(label="Новая функциональность")
taskType.menu.add_checkbutton(label="Ошибка")

status = tk.Menubutton(dropdown_frame, text="Статус", relief="raised")
status.menu = tk.Menu(status, tearoff=0)
status["menu"] = status.menu
status.pack()

some_list[7] = [
    "Статус",
    ["Анализ", "Новая", "Оценка", "Разработка", "Релиз", "Тестирование"]
]

submenu = tk.Menu(status.menu, tearoff=0)
status.menu.add_checkbutton(label="Анализ")
status.menu.add_checkbutton(label="Новая")
status.menu.add_checkbutton(label="Оценка")
status.menu.add_checkbutton(label="Разработка")
status.menu.add_checkbutton(label="Релиз")
status.menu.add_checkbutton(label="Тестирование")

state = tk.Menubutton(dropdown_frame, text="Состояние", relief="raised")
state.menu = tk.Menu(state, tearoff=0)
state["menu"] = state.menu
state.pack()

some_list[8] = ["Состояние", ["В очереди", "В работе", "Завершена"]]

submenu = tk.Menu(state.menu, tearoff=0)
state.menu.add_checkbutton(label="В очереди")
state.menu.add_checkbutton(label="В работе")
state.menu.add_checkbutton(label="Завершена")

analyst = tk.Menubutton(dropdown_frame, text="Аналитик", relief="raised")
analyst.menu = tk.Menu(analyst, tearoff=0)
analyst["menu"] = analyst.menu
analyst.pack()

some_list[9] = [
    "Аналитик",
    [
        "Вероника Киселева", "Даниил Фомин", "Евгения Белова",
        "Елизавета Маркелова", "Мария Овсянникова", "Никита Белов"
    ]
]

submenu = tk.Menu(analyst.menu, tearoff=0)
analyst.menu.add_checkbutton(label="Вероника Киселева")
analyst.menu.add_checkbutton(label="Даниил Фомин")
analyst.menu.add_checkbutton(label="Евгения Белова")
analyst.menu.add_checkbutton(label="Елизавета Маркелова")
analyst.menu.add_checkbutton(label="Мария Овсянникова")
analyst.menu.add_checkbutton(label="Никита Белов")

developer = tk.Menubutton(dropdown_frame, text="Разработчик", relief="raised")
developer.menu = tk.Menu(developer, tearoff=0)
developer["menu"] = developer.menu
developer.pack()

some_list[10] = [
    "Разработчик",
    [
        "Александр Кондратьев", "Вероника Потапова", "Гордей Захаров",
        "Дарья Цветкова", "Дмитрий Нестеров", "Елена Гладкова",
        "Светлана Попова"
    ]
]

submenu = tk.Menu(developer.menu, tearoff=0)
developer.menu.add_checkbutton(label="Александр Кондратьев")
developer.menu.add_checkbutton(label="Вероника Потапова")
developer.menu.add_checkbutton(label="Гордей Захаров")
developer.menu.add_checkbutton(label="Дарья Цветкова")
developer.menu.add_checkbutton(label="Дмитрий Нестеров")
developer.menu.add_checkbutton(label="Елена Гладкова")
developer.menu.add_checkbutton(label="Светлана Попова")

tester = tk.Menubutton(dropdown_frame, text="Тестировщик", relief="raised")
tester.menu = tk.Menu(tester, tearoff=0)
tester["menu"] = tester.menu
tester.pack()

labels = [
    "Даниил Емельянов", "Дмитрий Морозов", "Эмилия Игнатьева",
    "Дмитрий Нестеров"
]

some_list[11] = ["Тестировщик", labels]
submenu = tk.Menu(tester.menu, tearoff=0)
for label in labels:
  tester.menu.add_checkbutton(label="Даниил Емельянов")
  tester.menu.add_checkbutton(label="Дмитрий Морозов")
  tester.menu.add_checkbutton(label="Иван Кузнецов")
  tester.menu.add_checkbutton(label="Эмилия Игнатьева")
  tester.menu.add_checkbutton(label="Дмитрий Нестеров")

manager = tk.Menubutton(dropdown_frame,
                        text="Проект менеджер",
                        relief="raised")
manager.menu = tk.Menu(manager, tearoff=0)
manager["menu"] = manager.menu
manager.pack()


def hendle_(lable, ab):
  if lable not in some_list[-3][1]:
    print(lable)
    some_list[-3] = some_list[-1][0], ab
    print(some_list, 'ugyasiud')
  else:
    print(some_list)
    ab.remove(lable)
    some_list[-3] = some_list[-1][0], ab


submenu = tk.Menu(manager.menu, tearoff=0)
labels = ["Дарья Гаврилова", "Святослав Лапшин", "Софья Макарова"]
some_list[-1] = [some_list[-1][0], labels]
ab = [].extend(labels)
manager.menu.add_checkbutton(label="Дарья Гаврилова",
                             command=lambda l=label: hendle_(l, ab))
manager.menu.add_checkbutton(label="Святослав Лапшин",
                             command=lambda l=label: hendle_(l, ab))
manager.menu.add_checkbutton(label="Софья Макарова",
                             command=lambda l=label: hendle_(l, ab))


def handle_click_(event):
  clear_treeview()
  data = utils.fillRoles("data.xlsx")
  filling_table(data)


button_restart_frame = tk.Frame(root)
button_restart = tk.Button(button_restart_frame,
                           text="Распределить",
                           relief="raised")
button_restart.pack(side="top", fill="x")
button_restart_frame.pack(side="top", fill="x")
button_frame = tk.Frame(root)
button_frame.pack(side="left", fill="y")
button_restart.bind('<Button-1>', handle_click_)

print(some_list)

root.mainloop()
