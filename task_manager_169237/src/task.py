from datetime import datetime, date


class Task:
    VALID_STATUSES = {"pending", "completed", "in_progress", "done"}

    def __init__(self, title: str, description: str = None, due_date: str | date = None, status: str = "pending"):
        if not title or not title.strip():
            raise ValueError("Tytuł nie może być pusty.")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Niepoprawny status: {status}")

        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.status = status

        if due_date:
            if isinstance(due_date, str):
                try:
                    self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Niepoprawny format daty. Oczekiwany format: YYYY-MM-DD")
            elif isinstance(due_date, date):
                self.due_date = due_date
            else:
                raise TypeError("Due date musi być ciągiem znaków w formacie 'YYYY-MM-DD' lub obiektem datetime.date.")
        else:
            self.due_date = None

    def complete(self):
        self.status = "completed"

    def edit(self, title=None, description=None, due_date=None):
        if title:
            self.title = title.strip()
        if description is not None:
            self.description = description.strip()
        if due_date is not None:
            if isinstance(due_date, str):
                try:
                    self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Niepoprawny format daty. Oczekiwany format: YYYY-MM-DD")
            elif isinstance(due_date, date):
                self.due_date = due_date
            else:
                raise TypeError("Due date musi być ciągiem znaków w formacie 'YYYY-MM-DD' lub obiektem datetime.date.")

    def is_overdue(self):
        if not self.due_date:
            return False
        return self.due_date < date.today()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
            "status": self.status
        }

    # tworzy obiekt ze slownika
    @classmethod
    def from_dict(cls, data):
        due_date = data.get("due_date")
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        return cls(
            title=data.get("title", ""),
            description=data.get("description"),
            due_date=due_date,
            status=data.get("status", "pending")
        )
