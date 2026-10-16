"""Модель данных приложения «Менеджер задач».

Содержит два класса:
    * Task        — описывает отдельную задачу;
    * TaskManager — управляет списком задач и файловыми операциями.
"""

import json
from datetime import datetime


class Task:
    """Одна задача.

    Атрибуты:
        title (str):       название задачи;
        description (str):  описание задачи;
        due_date (str):     срок выполнения в формате ГГГГ-ММ-ДД.
    """

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date

    def is_valid_date(self):
        """Проверяет, что срок выполнения задан в формате ГГГГ-ММ-ДД."""
        try:
            datetime.strptime(self.due_date, self.DATE_FORMAT)
            return True
        except ValueError:
            return False

    def to_dict(self):
        """Превращает задачу в словарь для сериализации в JSON."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Восстанавливает задачу из словаря."""
        return cls(data["title"], data["description"], data["due_date"])

    def __str__(self):
        return f"{self.title} (до {self.due_date})"


class TaskManager:
    """Управляет списком задач и их сохранением в файл."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_from_file()

    def add_task(self, task):
        """Добавляет задачу и сохраняет изменения в файл."""
        self.tasks.append(task)
        self.save_to_file()

    def delete_task(self, index):
        """Удаляет задачу по индексу и сохраняет изменения в файл."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()
            return True
        return False

    def save_to_file(self):
        """Записывает все задачи в JSON-файл."""
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_from_file(self):
        """Загружает задачи из JSON-файла при запуске приложения."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
