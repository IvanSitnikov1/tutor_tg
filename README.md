# EnglishTutor
Телеграм бот для репетиторов по иностранному языку и их учеников. Создан для более удобного взаимодействия преподавателя и ученика. Позволяет управлять учениками, уроками и файлами в одном месте.

## Возможности учителя
- Приглашение учеников
- Создание/удаление урока, смена статуса урока, назначение даты урока
- Добавление/удаление материалов к уроку
- Добавление/удаление домашних заданий
- Просмотр выполненных домашних заданий
- Возможность оставить комментарий к выполненному домашнему заданию

## Возможности ученика
- Просмотр материалов урока, домашних заданий, комментариев учителя к выполненному домашнему заданию
- Возможность добавить выполненное домашнее задание

## [Примеры использования](examples/)

## Где попробовать
[![EnglishTutor](https://img.shields.io/badge/%F0%9F%92%AC_Telegram-@YourBotName-blue)](https://t.me/EnglishTutor1Bot)

## Сваггер к АПИ
[Swagger](http://217.114.10.190:8000/docs)

## Структура проекта
.
├── api                      # Дирректория API c файлами зависимостей, запуска и настроек окружения
│   └── api
│       ├── alembic          # Файлы alembic
│       │   └── versions       # Версии миграций
│       ├── configs          # Конфигурационные файлы
│       ├── handlers         # Контроллеры
│       │   ├── lessons        # Контроллеры уроков
│       │   ├── students       # Контроллеры учеников
│       │   └── teachers       # Контроллеры учителей
│       ├── log              # Файлы логов
│       ├── models           # Sqlalchemy модели
│       ├── routers          # Роутеры
│       ├── schemas          # Pydantic схемы
│       └── utils            # Утилиты для выноса логики из контроллеров
│           ├── lessons        # Улилиты уроков
│           ├── students       # Утилиты учеников
│           └── teachers       # Утилиты учителей
├── static                   # Дирректория для хранения статических файлов
└── tg_bot                   # Дирректория бота с файлами зависимостей, запуска и настроек окружения
    └── bot                  
        ├── api_helpers      # Помошники для работы с API
        │   ├── lessons        # Запросы для уроков
        │   ├── students       # Запросы для учеников
        │   └── teachers       # Запросы для учителей
        ├── functions        # Функции для выноса логики из обработчиков
        │   ├── lessons        # Функции уроков
        │   ├── students       # Функции учеников
        │   └── teachers       # Функции учителей
        ├── handlers         # Обработчики событий
        │   ├── auth           # Обработчики для авторизации пользователей
        │   ├── students       # Обработчики для учеников
        │   └── teachers       # Обработчики для учителей
        └── keyboards        # Клавиатуры

## Стек
Python3.11, FastAPI, Aiogram3, PostgreSQL
