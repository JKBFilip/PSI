import unittest
from datetime import datetime, timedelta, date
from src.task import Task
from parameterized import parameterized


class TestTask(unittest.TestCase):

    # Sprawdza podstawowe tworzenie zadania
    def test_basic_creation(self):
        t = Task("Zadanie A")
        self.assertEqual(t.title, "Zadanie A")
        self.assertEqual(t.status, "pending")
        self.assertEqual(t.description, "")
        self.assertIsNone(t.due_date)

# Sprawdza tworzenie zadania ze wszystkimi polami
    def test_creation_with_all_fields(self):
        t = Task("Zadanie B", "Opis", "2099-01-01", "completed")
        self.assertEqual(t.description, "Opis")
        self.assertEqual(t.due_date, date(2099, 1, 1))
        self.assertEqual(t.status, "completed")

# Sprawdza, czy pusty tytuł powoduje błąd
    def test_empty_title_raises_value_error(self):
        with self.assertRaises(ValueError):
            Task("")

# Sprawdza, czy oznaczenie zadania jako zakończone zmienia jego status
    def test_complete_changes_status(self):
        t = Task("Zadanie")
        t.complete()
        self.assertEqual(t.status, "completed")

# Sprawdza możliwość edycji tytułu zadania
    def test_edit_title(self):
        t = Task("Stary")
        t.edit(title="Nowy")
        self.assertEqual(t.title, "Nowy")

# Sprawdza możliwość edycji opisu zadania
    def test_edit_description(self):
        t = Task("Zadanie", "Stary opis")
        t.edit(description="Nowy opis")
        self.assertEqual(t.description, "Nowy opis")

# Sprawdza możliwość edycji daty wykonania
    def test_edit_due_date(self):
        t = Task("Zadanie")
        t.edit(due_date="2100-01-01")
        self.assertEqual(t.due_date, date(2100, 1, 1))

# Sprawdza, czy zadanie jest po terminie (przeszła data)
    def test_is_overdue_true(self):
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        t = Task("Zadanie", due_date=past_date)
        self.assertTrue(t.is_overdue())

# Sprawdza, czy zadanie nie jest po terminie (przyszła data)
    def test_is_overdue_false_future_date(self):
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        t = Task("Zadanie", due_date=future_date)
        self.assertFalse(t.is_overdue())

# Sprawdza, czy brak daty wykonania oznacza, że zadanie nie jest po terminie
    def test_is_overdue_false_no_due(self):
        t = Task("Zadanie")
        self.assertFalse(t.is_overdue())

# Sprawdza poprawność konwersji zadania na słownik
    def test_to_dict_returns_correct_dict(self):
        t = Task("Zadanie", "Opis", "2099-12-31", "completed")
        d = t.to_dict()
        self.assertEqual(d["title"], "Zadanie")
        self.assertEqual(d["status"], "completed")
        self.assertEqual(d["due_date"], "2099-12-31")

# Sprawdza tworzenie zadania na podstawie słownika
    def test_from_dict_creates_task(self):
        data = {
            "title": "Z 1",
            "description": "desc",
            "due_date": "2099-12-01",
            "status": "pending"
        }
        t = Task.from_dict(data)
        self.assertEqual(t.title, "Z 1")
        self.assertEqual(t.status, "pending")
        self.assertEqual(t.due_date, date(2099, 12, 1))

    @parameterized.expand([
        ("just_title", "Task 1", "", None, "pending"),
        ("with_due", "Task 2", "", "2099-01-01", "pending"),
        ("with_desc", "Task 3", "opis", None, "pending"),
        ("full", "Task 4", "opis", "2099-12-31", "completed"),
    ])
# Sprawdza tworzenie zadań z różnymi zestawami danych wejściowych
    def test_creation_param_cases(self, _, title, desc, due, status):
        t = Task(title, desc, due, status)
        self.assertEqual(t.title, title)
        self.assertEqual(t.description, desc)
        if due:
            self.assertEqual(t.due_date, datetime.strptime(due, "%Y-%m-%d").date())
        else:
            self.assertIsNone(t.due_date)
        self.assertEqual(t.status, status)

# Sprawdza, czy niepoprawny format daty powoduje błąd
    def test_invalid_date_format_does_not_raise(self):
        with self.assertRaises(ValueError):
            Task("Zadanie", due_date="wrong-format")

# Sprawdza edycję wielu pól jednocześnie
    def test_edit_multiple_fields(self):
        t = Task("T1", "D", "2020-01-01")
        t.edit(title="T2", description="D2", due_date="2099-01-01")
        self.assertEqual(t.title, "T2")
        self.assertEqual(t.description, "D2")
        self.assertEqual(t.due_date, date(2099, 1, 1))

# Sprawdza, czy status nie zmienia się automatycznie na 'completed'
    def test_status_not_automatically_completed(self):
        t = Task("Zadanie")
        self.assertEqual(t.status, "pending")

# Sprawdza, czy wielokrotne zakończenie zadania nie zmienia stanu po raz kolejny
    def test_complete_twice_idempotent(self):
        t = Task("Z")
        t.complete()
        t.complete()
        self.assertEqual(t.status, "completed")

# Sprawdza integralność danych po konwersji do i ze słownika
    def test_dict_conversion_integrity(self):
        original = Task("T1", "Opis", "2099-01-01", "completed")
        copy = Task.from_dict(original.to_dict())
        self.assertEqual(copy.title, original.title)
        self.assertEqual(copy.status, original.status)
        self.assertEqual(copy.description, original.description)
        self.assertEqual(copy.due_date, original.due_date)

# Sprawdza, czy brak zmian nie modyfikuje zadania
    def test_edit_nothing_does_not_change(self):
        t = Task("Zadanie", "O", "2099-01-01")
        t.edit()
        self.assertEqual(t.title, "Zadanie")
        self.assertEqual(t.description, "O")
        self.assertEqual(t.due_date, date(2099, 1, 1))

# Sprawdza, czy obiekt jest instancją klasy Task
    def test_task_is_instance_of_task(self):
        t = Task("Z")
        self.assertIsInstance(t, Task)

# Sprawdza, czy tytuł jest typu tekstowego
    def test_title_type(self):
        t = Task("Z")
        self.assertIsInstance(t.title, str)

# Sprawdza, czy status należy do dozwolonych wartości
    def test_status_in_expected_values(self):
        t = Task("Z")
        self.assertIn(t.status, ["pending", "completed", "in_progress"])

# Sprawdza, czy edycja pustego tytułu jest ignorowana
    def test_edit_to_empty_title_is_ignored(self):
        t = Task("Zadanie")
        t.edit(title=None)
        self.assertEqual(t.title, "Zadanie")

# Sprawdza tworzenie minimalnego zadania
    def test_task_creation_minimal(self):
        t = Task("Test")
        self.assertEqual(t.title, "Test")
        self.assertEqual(t.status, "pending")
        self.assertEqual(t.description, "")

# Sprawdza tworzenie pełnego zadania
    def test_task_full(self):
        t = Task("Zad", "Opis", "2099-01-01", "completed")
        self.assertEqual(t.title, "Zad")
        self.assertEqual(t.description, "Opis")
        self.assertEqual(t.due_date, date(2099, 1, 1))
        self.assertEqual(t.status, "completed")

# Sprawdza, czy nieprawidłowy status powoduje błąd
    def test_task_invalid_status(self):
        with self.assertRaises(ValueError):
            Task("Zad", status="niewazne")

# Sprawdza, czy dwa identyczne zadania są sobie równe
    def test_task_equality(self):
        a = Task("A", "desc", "2099-01-01")
        b = Task("A", "desc", "2099-01-01")
        self.assertEqual(a.__dict__, b.__dict__)

# Sprawdza, czy pusty tytuł przy tworzeniu powoduje błąd
    def test_task_creation_empty_title(self):
        with self.assertRaises(ValueError):
            Task("")

# Sprawdza, czy nieprawidłowa data wykonania powoduje błąd
    def test_task_creation_invalid_due_date(self):
        with self.assertRaises(ValueError):
            Task("Test Task", due_date="invalid-date")

# Sprawdza działanie metody complete()
    def test_task_complete(self):
        task = Task("Test")
        task.complete()
        self.assertEqual(task.status, "completed")

# Sprawdza działanie metody edit()
    def test_task_edit(self):
        task = Task("Test")
        task.edit(title="Updated Title", description="Updated Description", due_date="2025-01-01")
        self.assertEqual(task.title, "Updated Title")
        self.assertEqual(task.description, "Updated Description")
        self.assertEqual(task.due_date, date(2025, 1, 1))

# Sprawdza działanie metody is_overdue()
    def test_task_is_overdue(self):
        task = Task("Test", due_date="2000-01-01")
        self.assertTrue(task.is_overdue())
        task = Task("Test", due_date="2099-01-01")
        self.assertFalse(task.is_overdue())

# Sprawdza poprawność metody to_dict()
    def test_task_to_dict(self):
        task = Task("Test", "Description", "2099-01-01", "pending")
        task_dict = task.to_dict()
        self.assertEqual(task_dict["title"], "Test")
        self.assertEqual(task_dict["description"], "Description")
        self.assertEqual(task_dict["due_date"], "2099-01-01")
        self.assertEqual(task_dict["status"], "pending")

# Sprawdza poprawność metody from_dict()
    def test_task_from_dict(self):
        data = {
            "title": "Test",
            "description": "Description",
            "due_date": "2099-01-01",
            "status": "pending"
        }
        task = Task.from_dict(data)
        self.assertEqual(task.title, "Test")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.due_date, date(2099, 1, 1))
        self.assertEqual(task.status, "pending")

# Sprawdza działanie zadania z tytułem zawierającym znaki Unicode
    def test_task_with_unicode_title(self):
        task = Task("Zadanie in Polish", "Opis", "2099-01-01", "pending")
        self.assertEqual(task.title, "Zadanie in Polish")

# minimalna dlugosc znaku
    def test_minimal_title_length(self):
        t = Task("A")
        self.assertEqual(t.title, "A")

# limi dlugosci tytulu
    def test_very_long_title(self):
        long_title = "A" * 10_000
        t = Task(long_title)
        self.assertEqual(t.title, long_title)

# zadanie z dzisiejsza data
    def test_due_today_not_overdue(self):
        today = datetime.now().strftime("%Y-%m-%d")
        t = Task("Test", due_date=today)
        self.assertFalse(t.is_overdue())
