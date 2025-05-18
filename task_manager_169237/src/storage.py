from datetime import datetime
import json
from datetime import date


def save_tasks(tasks, filename):
    try:
        def date_serializer(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            raise TypeError(f"Typ {obj.__class__.__name__} nie może być zserializowany")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [task.__dict__ for task in tasks],
                f,
                ensure_ascii=False,
                indent=2,
                default=date_serializer
            )
    except IOError as e:
        raise RuntimeError(f"Błąd zapisu pliku: {e}")


def load_tasks(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []

            from .task import Task
            allowed_keys = {"title", "description", "due_date", "status"}
            return [
                Task(**{
                    k: (
                        datetime.strptime(v, "%Y-%m-%d").date()
                        if k == "due_date" and isinstance(v, str)
                        else v if v is not None
                        else "" if k != "due_date"
                        else None
                    )
                    for k, v in item.items() if k in allowed_keys
                })
                for item in data if isinstance(item, dict)
            ]
    except (IOError, json.JSONDecodeError):
        return []


def task_to_dict(task):
    task_dict = task.__dict__.copy()
    if isinstance(task.due_date, datetime.date):
        task_dict['due_date'] = task.due_date.isoformat()

    return task_dict
