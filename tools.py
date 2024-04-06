  import dataclasses
  import hashlib
  from pathlib import Path
  import os

  import pandas
  import pandas as pd


  def parseProjects(path: Path) -> pandas.DataFrame:
      return pandas.read_excel(path, sheet_name="Проекты")


  def parseEmployees(path: Path) -> pandas.DataFrame:
      return pandas.read_excel(path, sheet_name="Сотрудники")


  def parseTasks(path: Path) -> pandas.DataFrame:
      return pandas.read_excel(path, sheet_name="Задачи")


  def searchInColumn(search_object: str,column: str, df: pd.DataFrame) ->list:
      found = []
      for index, row in df.iterrows():
          if row[column] == search_object:
              found.append(index)

      return found


  class App:
      def __init__(self):
          ...


  class ProjectManager:
      @staticmethod
      def getTasks(project_name: str, tasks: pd.DataFrame):
          _tasks = []
          for index, row in tasks.iterrows():
              if row["Проект"] == project_name:
                  _tasks.append([index, row["Номер"]])

          return _tasks

  class EmployeeManager:
      @staticmethod
      def getTasksRelatedToEmployee(employee_name: str, employee_last_name: str, tasks: pd.DataFrame, employees: pd.DataFrame) -> list:
          employee_role = EmployeeManager.getEmployeeRole(employee_name, employee_last_name, employees)
          employee_tasks = []
          for index, task in tasks.iterrows():
              if task[employee_role] == employee_name + ' ' + employee_last_name:
                  employee_tasks.append(task["Номер"])
          print(employee_tasks)

      @staticmethod
      def getEmployeeRole(employee_name: str, employee_last_name: str, employees: pd.DataFrame) -> list:
          for index, employee in employees.iterrows():
              if employee["Имя"] == employee_name and employee["Фамилия"] == employee_last_name:
                  employee_role = employee["Должность"]
                  break

          return(employee_role)



  if __name__ == "__main__":
      path = "data/data.xlsx"
      tasks = parseTasks(path)
      employees = parseEmployees(path)
      EmployeeManager.getTasksRelatedToEmployee("Эмилия","Игнатьева",tasks,employees)
      #project_1 = ProjectManager.getTasks("Проект 1", tasks)
      #print(project_1)
