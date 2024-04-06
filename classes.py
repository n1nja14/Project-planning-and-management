import pydantic

class Project:





class Task:
  id: int
  name: str
  description: str
  project_id: int
  employee_id: int
  start_date: str
  end_date: str
  status: str
  priority: int