import strawberry
from typing import List
from database import collection, collection2
from utils import get_next_id
from fastapi import HTTPException, status
from pymongo.collection import ReturnDocument

@strawberry.type
class Task:
    id: str | None = None
    title: str | None = None
    description: str | None = None
    created_at: str | None = None

@strawberry.type
class User:
    id: str
    name: str
    job: str
    position: str
    # task: List[Task]

# Query resolver
@strawberry.type
class Query:
    @strawberry.field
    def allUser(self) -> List[User]:
        users = list()
        
        for user_data in collection.find():
            user = User(
                id=user_data["id"],
                name=user_data["name"],
                job=user_data["job"],
                position=user_data["position"]
            )
            users.append(user)
        return users
    
    @strawberry.field
    def idUser(self, id: str) -> User | None:
        user_data = collection.find_one({"id": id})
        if user_data:
            return User(
                id=user_data["id"],
                name=user_data["name"],
                job=user_data["job"],
                position=user_data["position"]
            )
        
    @strawberry.field
    def allTask(self) -> List[Task]:
        tasks = list()
        
        for task_data in collection2.find():
            task = Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                created_at=task_data["created_at"],
            )
            tasks.append(task)
        return tasks
        
    @strawberry.field
    def idTask(self, id: str) -> Task | None:
        task_data = collection2.find_one({"id": id})

        if task_data:
            return Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                created_at=task_data["created_at"]
            )
        else:
            return None
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, job: str, position: str) -> User:
        user = {
            "id": get_next_id(), "name": name,
            "job": job, "position": position,
            # "task": task
        }
        collection.insert_one(user)
        return User(
            id=user['id'], name=user['name'], 
            job=user['job'], position=user['position']
        )
        
    @strawberry.mutation
    def delete_user(self, id: str) -> User | None:
        deleted_user = collection.find_one_and_delete({"id": id})
        if deleted_user:
            return None
        return None
    
    @strawberry.mutation
    def create_task(self, title: str, description: str, created_at: str) -> Task:
        task = {
            "id": get_next_id(),
            # "user": user,
            "title": title,
            "description": description,
            "created_at": created_at
        }
        collection2.insert_one(task)
        return Task (
            id=task['id'], title=task['title'],
            description=task['description'], created_at=task['created_at']
        )
    
    @strawberry.field
    def update_task(self, id: str, title: str, description: str) -> Task | None:
        updated_task = collection2.find_one_and_update(
            {"id": id}, {"$set": {"title": title, "description": description}},
            return_document=ReturnDocument.AFTER
        )

        if updated_task:
            return Task (
                id=updated_task['id'], title=updated_task['title'],
                description=updated_task['description'], created_at=updated_task['created_at']
            )
        else:
            return None
    
    @strawberry.field
    def delete_task(self, id: str) -> Task | None:
        deleted_task = collection2.delete_one({"id": id})
        if deleted_task:
            return None
        return None

schema = strawberry.Schema(query=Query, mutation=Mutation)