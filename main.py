from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Центр дополнительного образования", version="1.0.0")


class ProgramInput(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    min_age: int = Field(ge=0, le=18)
    max_age: int = Field(ge=0, le=18)
    duration_hours: int = Field(gt=0)


class Program(ProgramInput):
    id: int


class GroupInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    program_id: int
    capacity: int = Field(gt=0)
    enrollment_open: bool = True


class Group(GroupInput):
    id: int


class ApplicationInput(BaseModel):
    student_name: str = Field(min_length=1, max_length=150)
    parent_name: str = Field(min_length=1, max_length=150)
    program_id: int


class Application(ApplicationInput):
    id: int
    status: str = "new"



programs: dict[int, Program] = {
    1: Program(id=1, name="Робототехника", min_age=8, max_age=15, duration_hours=72),
    2: Program(id=2, name="Программирование Python", min_age=12, max_age=17, duration_hours=96),
}
groups: dict[int, Group] = {
    1: Group(id=1, name="Робототехника-1", program_id=1, capacity=15),
    2: Group(id=2, name="Python-1", program_id=2, capacity=12),
}
applications: dict[int, Application] = {}


# 1. GET — список образовательных программ
@app.get("/programs", response_model=list[Program], tags=["Программы"])
def list_programs():
    return list(programs.values())


# 2. GET — одна образовательная программа
@app.get("/programs/{program_id}", response_model=Program, tags=["Программы"])
def get_program(program_id: int):
    if program_id not in programs:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    return programs[program_id]


# 3. POST — создание программы
@app.post("/programs", response_model=Program, status_code=status.HTTP_201_CREATED, tags=["Программы"])
def create_program(data: ProgramInput):
    if data.min_age > data.max_age:
        raise HTTPException(status_code=422, detail="Минимальный возраст больше максимального")
    new_id = max(programs, default=0) + 1
    program = Program(id=new_id, **data.model_dump())
    programs[new_id] = program
    return program


# 4. PUT — обновление программы
@app.put("/programs/{program_id}", response_model=Program, tags=["Программы"])
def update_program(program_id: int, data: ProgramInput):
    if program_id not in programs:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    if data.min_age > data.max_age:
        raise HTTPException(status_code=422, detail="Минимальный возраст больше максимального")
    program = Program(id=program_id, **data.model_dump())
    programs[program_id] = program
    return program


# 5. DELETE — удаление программы
@app.delete("/programs/{program_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Программы"])
def delete_program(program_id: int):
    if program_id not in programs:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    if any(group.program_id == program_id for group in groups.values()) or any(
        application.program_id == program_id for application in applications.values()
    ):
        raise HTTPException(status_code=409, detail="Программа используется группой или заявкой")
    del programs[program_id]


# 6. GET — список учебных групп
@app.get("/groups", response_model=list[Group], tags=["Группы"])
def list_groups():
    return list(groups.values())


# 7. GET — одна учебная группа
@app.get("/groups/{group_id}", response_model=Group, tags=["Группы"])
def get_group(group_id: int):
    if group_id not in groups:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return groups[group_id]


# 8. POST — создание заявки
@app.post("/applications", response_model=Application, status_code=status.HTTP_201_CREATED, tags=["Заявки"])
def create_application(data: ApplicationInput):
    if data.program_id not in programs:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    new_id = max(applications, default=0) + 1
    application = Application(id=new_id, **data.model_dump())
    applications[new_id] = application
    return application


# 9. GET — получение заявки
@app.get("/applications/{application_id}", response_model=Application, tags=["Заявки"])
def get_application(application_id: int):
    if application_id not in applications:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return applications[application_id]


# 10. DELETE — удаление заявки
@app.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Заявки"])
def delete_application(application_id: int):
    if application_id not in applications:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    del applications[application_id]
