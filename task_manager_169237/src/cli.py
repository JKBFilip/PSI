from datetime import datetime
from src.task import Task
from src.storage import load_tasks, save_tasks


class CLIHandler:
    def __init__(self, input_func=input, output_func=print, filename="tasks.json"):
        self.input = input_func
        self.output = output_func
        self.filename = filename
        self.tasks = load_tasks(self.filename)

    def run(self):
        while True:
            choice = self.input("Wybierz: ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.show_tasks()
            elif choice == "3":
                break
            elif choice == "4":
                self.mark_task_done()
            else:
                self.output("Nieprawidłowy wybór")

    def add_task(self):
        title = self.input("Tytuł: ")
        description = self.input("Opis: ")
        due_date = self.input("Termin (YYYY-MM-DD): ")

        if not title.strip() or not description.strip() or not due_date.strip():
            self.output("Wszystkie pola muszą być wypełnione.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            self.output("Niepoprawny format daty. Użyj YYYY-MM-DD.")
            return

        task = Task(title, description, due_date)
        self.tasks.append(task)
        save_tasks(self.tasks, self.filename)

    def show_tasks(self):
        for i, task in enumerate(self.tasks):
            self.output(f"{i + 1}. {task.title} - {task.status}")

    def mark_task_done(self):
        try:
            index = int(
                self.input("Numer zadania do oznaczenia jako zakończone: ")
            ) - 1
        except ValueError:
            self.output("Nieprawidłowy numer zadania")
            return

        if 0 <= index < len(self.tasks):
            self.tasks[index].status = "done"
            save_tasks(self.tasks, self.filename)
        else:
            self.output("Nieprawidłowy numer zadania")


def main():
    cli = CLIHandler()
    cli.run()
