from __future__ import annotations
import copy
from pathlib import Path
import clr,os
from pythonnet import set_runtime
from clr_loader import get_coreclr
clr.AddReference("System")
import System
from System import Int32, Tuple,Math

#from System.Linq.Enumerable import MaxBy
from System.Collections.Generic import List


import pandas as pd
import numpy as np

pathDLL = os.getcwd() + "\\TestPythonnet3.dll"
clr.AddReference(pathDLL)
import TestPythonnet


def parseProjects(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Проекты")


def parseEmployees(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Сотрудники")


def parseTasks(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Задачи")


def parseTasksAsMatrix(path: Path) -> list[list[str]]:
    m = []
    raw_data = parseTasks(path)
    raw_data = raw_data.drop(columns=["Заголовок", "Описание", "SP анализ", "SP разработка",
                                      "SP тестирование", "SP релиз",
                                      "Заблокирована задачей с номером", "Блокирует задачу с номером"])
    for i, row in raw_data.iterrows():
        m.append(list(row))
    # "Номер", "Приоритет", "Заказчик", "Приёмщик", "Проект",
    # "Команда", "Тип задачи", "Статус", "Состояние", "Аналитик",
    # "Разработчик",  "Тестировщик", "Релиз менеджер"
    return m

class Employee:
    def __init__(self, name: str, role: str, group: str):
        self.name = name
        self.role = role
        self.group = group

    def getList(self) -> Tuple[str, str, str]:
        return Tuple[str, str, str](self.name, self.role, self.group)

def getEmployees(df: pd.DataFrame) -> list[Employee]:
    employees = []
    for index, row in df.iterrows():
        employee = Employee(row["Имя"] + " " + row["Фамилия"], row["Должность"], row["Команда"])
        employees.append(employee)
    return employees

def getEmployeesAsList(employees: list[Employee]) -> List[Tuple[str, str, str]]:
    employees_as_list = List[Tuple[str, str, str]]()
    for i in range(len(employees)):
        employees_as_list.Add(employees[i].getList())
    return employees_as_list

class Task:
    def __init__(
            self, task_num: int, priority: str, customer: str, project_num: str, team_num: str, task_type: str, \
            status: str, state: str,  \
            sp_analysis: int, sp_dev: int, sp_test: int, sp_release: int, creation_date: str, \
            blocked_by_task: int, blocking_task: int, analytic: str = "", dev: str = "", tester: str = "", release_manager: str = "",
                 ):
        self.task_num: int = task_num
        self.priority: str = priority
        self.customer: str = customer
        self.project_num: str = project_num
        self.team_num: str = team_num
        self.task_type: str = task_type
        self.status: str = status
        self.state: str = state
        self.analytic: str = analytic
        self.dev: str = dev
        self.tester: str = tester
        self.release_manager: str = release_manager
        self.sp_analysis: int = sp_analysis
        self.sp_dev: int = sp_dev
        self.sp_test: int = sp_test
        self.sp_release: int = sp_release
        self.creation_date: str = creation_date
        self.blocked_by_task: int = 0 if type(blocked_by_task) == float else blocked_by_task
        self.blocking_task: int = blocking_task
        self.sp = 0

    def toList(self) -> Tuple:
        # return Tuple[int, str, str, str, str, int, Tuple[str, str, str, str], Tuple[int, str]](self.task_num, self.priority, self.status, self.task_type, self.team_num, self.sp, Tuple[str, str, str, str](self.analytic, self.dev, self.tester, self.release_manager), Tuple[int, str](self.blocked_by_task, self.project_num))
        return Tuple[int, str, str, str, str, int, int,Tuple[str, str, str, str]](self.task_num, self.priority, self.status, self.task_type, self.team_num, self.sp, self.blocked_by_task,Tuple[str, str, str, str](self.analytic, self.dev, self.tester, self.release_manager))

def splitTaskByStatus(task: Task, current_status: str, tasks: list[Task]) -> list[Task]:
    if current_status == "Релиз":
        _task = copy.deepcopy(task)
        _task.sp = task.sp_release
        tasks.append(_task)
        return tasks
    if current_status == "Тестирование":
        _task = copy.deepcopy(task)
        _task.sp = task.sp_test
        tasks.append(_task)
        return splitTaskByStatus(_task, "Релиз", tasks)
    if current_status == "Разработка":
        _task = copy.deepcopy(task)
        _task.sp = task.sp_dev
        tasks.append(_task)
        return splitTaskByStatus(_task, "Тестирование", tasks)
    if current_status == "Анализ":
        _task = copy.deepcopy(task)
        _task.sp = task.sp_analysis
        tasks.append(_task)
        return splitTaskByStatus(_task, "Разработка", tasks)
    if current_status == "Оценка" or current_status == "Новая":
        _task = copy.deepcopy(task)
        _task.sp = task.sp_analysis + 8
        tasks.append(_task)
        return splitTaskByStatus(_task, "Анализ", tasks)

    raise Exception(f"Some error: task {task.status}")

def taskRowToTask(row: pd.Series) -> Task:
    analytic = "" if row["Аналитик"] is np.nan else row["Аналитик"]
    dev = "" if row["Разработчик"] is np.nan else row["Разработчик"]
    test = "" if row["Тестировщик"] is np.nan else row["Тестировщик"]
    release_manager = "" if row["Релиз менеджер"] is np.nan else row["Релиз менеджер"]

    task = Task(row["Номер"], row["Приоритет"], row["Заказчик"], row["Проект"], row["Команда"], row["Тип задачи"],
                row["Статус"], row["Состояние"], \
                row["SP анализ"], row["SP разработка"], row["SP тестирование"], row["SP релиз"], row["Дата создания"],
                row["Заблокирована задачей с номером"], \
                row["Блокирует задачу с номером"], analytic, dev, test, release_manager)

    return task

def getAllTasks(df: pd.DataFrame) -> list[Task]:
    tasks = []
    for index, row in df.iterrows():
        task = taskRowToTask(row)
        tasks.append(task)

    return tasks

def getAllTasksAsLists(tasks: list[Task]) -> list[list]:
    tasks_as_list = []
    for task in tasks:
        splitted_tasks = splitTaskByStatus(task, task.status, [])
        for splitted_task in splitted_tasks:
            tasks_as_list.append(splitted_task.toList())
    tmp = List[Tuple[int, str, str,str, str, int, int,Tuple[str, str, str, str]]]()

    for i in range(len(tasks_as_list)):
        tmp.Add(tasks_as_list[i])
    return tmp

def getFilteredTasks(filter_rules: list[tuple[str, tuple[str]]], path: Path) -> list[list[str]]:
    tasks = parseTasks(path)

    filtered_tasks = []
    for index, row in tasks.iterrows():
        is_passing_filter = True
        for filter_rule in filter_rules:
            column_to_filter_by, criteria = filter_rule

            if not(row[column_to_filter_by] in criteria):
                is_passing_filter = False

        if is_passing_filter:
            row = row.drop(["Заголовок", "Описание", "SP анализ", "SP разработка",
                            "SP тестирование", "SP релиз",
                            "Заблокирована задачей с номером", "Блокирует задачу с номером"])

            filtered_tasks.append(list(row))

    return filtered_tasks

def _sortTasks(task: Task) -> list:
    res = []

    if task.state == "В работе":
        res.append(0)
    elif task.state == "В очереди":
        res.append(1)
    elif task.state == "Завершена":
        res.append(2)

    if task.task_type == "Ошибка":
        res.append(0)
    else:
        res.append(1)

    if task.priority == "Высокий":
        res.append(0)
    elif task.priority == "Средний":
        res.append(1)
    elif task.priority == "Низкий":
        res.append(2)

    return res

def sortTasks(tasks: list[Task]) -> list:
    sorted_tasks = sorted(tasks, key=_sortTasks)
    return sorted_tasks

def fillRoles(path) -> list[list]:
    tasks = parseTasks(path)
    tasks_as_lists = getAllTasksAsLists(getAllTasks(tasks))

    employees = getEmployees(parseEmployees(path))
    employees_as_lists = getEmployeesAsList(employees)

    roles_managed = TestPythonnet.Program.ManageEmployees(tasks_as_lists,employees_as_lists)

    _tasks = []
    tasks = tasks.drop(columns=["Заголовок", "Описание", "SP анализ", "SP разработка",
                                      "SP тестирование", "SP релиз",
                                      "Заблокирована задачей с номером", "Блокирует задачу с номером"])
    for index, row in tasks.iterrows():
        for task in roles_managed:
            if task.Number == row["Номер"]:
                #print(task.Analytic,"d" ,task.Tester, task.Developer,"k",task.ReleaseManager)
                row["Аналитик"] = task.Analytic
                row["Тестировщик"] = task.Tester
                row["Разработчик"] = task.Developer
                row["Релиз менеджер"] = task.ReleaseManager
                _tasks.append(list(row))
                break
        else:

            _tasks.append(list(row))

    return _tasks


if __name__ == "__main__":
    path = "data.xlsx"

    _sorted = sortTasks(getAllTasks(parseTasks(path)))
    #for task in _sorted:
        #print(task.state, task.status, task.priority)

    # for i in getFilteredTasks([("Приоритет", ("Низкий", "Высокий")), ("Тип задачи", ("Новая функциональность"))], path):
    #     print(i)

    res = fillRoles(path)
    #print(res[0])

    # print(parseTasksAsMatrix(path))

    raw_employees = parseEmployees(path)
    employees = getEmployees(raw_employees)
    employees_as_lists = getEmployeesAsList(employees)
    print(employees_as_lists)

    raw_tasks = parseTasks(path)
    tasks = getAllTasks(raw_tasks)
    tasks_as_lists = getAllTasksAsLists(tasks)
    # print(tasks_as_lists)
    result = TestPythonnet.Program.ManageEmployees(tasks_as_lists,employees_as_lists)
    print(TestPythonnet.Program.OverallTime)
    print(TestPythonnet.Program.CompletionTime)

