from fastapi import APIRouter


lesson_router = APIRouter(
    prefix='/lessons',
    tags=['Уроки'],
)
