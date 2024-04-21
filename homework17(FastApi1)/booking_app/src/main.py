from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from typing import Dict, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError, conint, constr
import random
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

'''
Создать объект класса FastAPI() . Создать один эндпоинт с get запросом, который будет возвращать 
список из 5 случайных чисел. Числа генерируются с помощью модуля random. 
'''

app = FastAPI()


response_model=Dict[str, Any]

@app.get("/get_random_numbers", response_model=response_model)
def generate_random_numbers() -> Dict[str, Any]:
    return {"random_numbers": [random.randint(1, 100) for _ in range(5)]}


'''
Создать 3 эндпоинта для get запросов, которые возвращают словари. 
1 возвращает данные которые прокидываются в качестве path params название {item_id} тип int. 
2 возвращает данные переданные в качестве query params. Имена произвольные двух типов int и str. 
3 возвращает 1 path params тип str и два query params тип int, int
'''

@app.get("/items/{item_id}", response_model=response_model)
def get_item_by_id(item_id: int) -> Dict[str, int]:
    return {"item_id": item_id}

@app.get("/query_params/", response_model=response_model)
def get_data_by_query_params(param1: int = Query(..., description="type: int"),
                              param2: str = Query(..., description="type: str")) ->  Dict[str, Any]:
    return {"param1": param1, "param2": param2}

@app.get("/mixed_params/{item}", response_model=response_model)
def get_mixed_params(item: str, param1: int = Query(..., description="type: int"),
                     param2: int = Query(..., description="type: int")) -> Dict[str, Any]:
    return {"item": item, "param1": param1, "param2": param2}


'''
Используя pydantic создайте класс Actor c полями (actor_id int, name str, surname str, age int, sex str) 
Создайте эндпоинт c post запросом который принимает в body (actor: Actors).  
и возвращает актёра с переданными полями в теле запроса.
'''

'''
Используйте возможности pydantic и провалидируйте поля класса Actor следующим образом: 
actor_id сделайте положительным числом, 
age определите от 0 до 100, 
name и surname сделайте не более 20 символов и не менее 2, 
sex добавьте возможность выбора только male и female .
'''

class ValidSex(str, Enum):
    m = "m"
    f = "f"



class Actor(BaseModel):
    actor_id: conint(ge=1)
    name: constr(min_length=2, max_length=20)
    surname: constr(min_length=2, max_length=20)
    age: conint(ge=0, le=100)
    sex: ValidSex


@app.post("/return_actor", response_model=Actor)
def return_actor(actor: Actor) -> Actor:
    return actor


'''
Создайте движок для подключения к Sqlite. И подключитесь к базе cinema. 
Измените эндпоинт созданный в 4 пункте, добавив в него сохранение в таблицу actors, 
данных об актёре полученных в body. Для сохранения в базу используйте на выбор или raw Sql или sqlalchemy orm.
'''

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../../../../"))
DATABASE_URL = f"sqlite:///{parent_dir}/db/sqlLite/example.db"

Base = declarative_base()

class DBActor(Base):
    __tablename__ = 'actors_2'

    actors_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    age = Column(Integer)
    sex = Column(String) 


class ActorsHandler():
        def __init__(self) -> None:
            self.engine = create_engine(DATABASE_URL)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

        def add_actor(self, actor: DBActor) -> None:
            self.session.add(actor)
            self.session.commit()
            self.session.close()

        def get_actor_by_id(self, actor_id: int) -> DBActor | None:
            actor = self.session.query(DBActor).filter(DBActor.actors_id == actor_id).first()
            self.session.close()
            return actor

        def __del__(self):
            self.session.close()

db_actors_handler = ActorsHandler()

class ActorCreate(BaseModel):
    name: constr(min_length=2, max_length=20)
    surname: constr(min_length=2, max_length=20)
    age: conint(ge=0, le=100)
    sex: ValidSex


@app.post("/actors/create", response_model=dict)
def create_actor(actor_data: ActorCreate) -> JSONResponse:
    try:
        actor = Actor(name=actor_data.name, surname=actor_data.surname, age=actor_data.age, sex=actor_data.sex)
        db_actors_handler.add_actor(actor)
        return JSONResponse(content={"errorInfo": 'success', "data": actor_data.dict()})
    except ValidationError as e:
        return JSONResponse(content={"errorInfo": str(e), "data": None}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"errorInfo": str(e), "data": None}, status_code=500)


'''
Cоздайте эндпоинт c get запросом, который будет принимать в path params параметр {actor_id}. 
И с помощью raw Sql или sqlalchemy orm  получите данные об актёре с полученным actor_id или выведите, что такого актёра нет в БД. 
'''

@app.get("/actors/{actor_id}", response_model=dict)
def get_actor_by_id(actor_id: int):
    try:
        actor = db_actors_handler.get_actor_by_id(actor_id)
        if actor:
            return JSONResponse(content={"errorInfo": 'success', "data": jsonable_encoder(actor)})
        else:
            return JSONResponse(content={"errorInfo": "Actor not found", "data": None}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"errorInfo": str(e), "data": None}, status_code=500)