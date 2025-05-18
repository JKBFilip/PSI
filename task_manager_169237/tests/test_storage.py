import json
import unittest
import os

from src.storage import load_tasks, save_tasks
from src.task import Task
from src import storage
from datetime import date


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.filename = "test_tasks.json"
        self.sample_tasks = [
            Task("Zadanie 1", "opis 1", "2099-01-01"),
            Task("Zadanie 2", "opis 2", "2100-01-01", "completed"),
        ]

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    # Sprawdza, czy zapisanie zadań tworzy plik.
    def test_save_creates_file(self):
        storage.save_tasks(self.sample_tasks, self.filename)
        self.assertTrue(os.path.exists(self.filename))

    # Sprawdza, czy zapisane zadania można poprawnie wczytać.
    def test_save_and_load_tasks(self):
        storage.save_tasks(self.sample_tasks, self.filename)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Zadanie 1")
        self.assertEqual(loaded[1].status, "completed")

    # Sprawdza, czy brak pliku skutkuje zwróceniem pustej listy.
    def test_load_returns_empty_on_missing_file(self):
        result = storage.load_tasks("nonexistent_file.json")
        self.assertEqual(result, [])

    # Sprawdza, czy nieprawidłowy JSON skutkuje pustą listą.
    def test_load_returns_empty_on_invalid_json(self):
        with open(self.filename, "w") as f:
            f.write("{ invalid json")
        result = storage.load_tasks(self.filename)
        self.assertEqual(result, [])

    # Sprawdza, czy zapisanie pustej listy tworzy pusty plik JSON.
    def test_save_handles_empty_list(self):
        storage.save_tasks([], self.filename)
        with open(self.filename, "r") as f:
            content = json.load(f)
        self.assertEqual(content, [])

    # Sprawdza spójność danych zadania po zapisaniu i wczytaniu.
    def test_task_data_integrity_after_save_and_load(self):
        storage.save_tasks(self.sample_tasks, self.filename)
        loaded = storage.load_tasks(self.filename)
        for original, loaded_task in zip(self.sample_tasks, loaded):
            self.assertEqual(original.title, loaded_task.title)
            self.assertEqual(original.description, loaded_task.description)
            self.assertEqual(original.due_date, loaded_task.due_date)
            self.assertEqual(original.status, loaded_task.status)

    # Sprawdza format zapisu zadań do pliku JSON.
    def test_save_tasks_format(self):
        storage.save_tasks(self.sample_tasks, self.filename)
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertTrue(all('title' in task and 'description' in task for task in data))

    # Sprawdza zachowanie ładowania pustego pliku.
    def test_load_returns_empty_on_empty_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('')
        tasks = storage.load_tasks(self.filename)
        self.assertEqual(tasks, [])

    # Sprawdza zgodność tytułów wczytanych zadań.
    def test_load_tasks(self):
        storage.save_tasks(self.sample_tasks, self.filename)
        tasks = storage.load_tasks(self.filename)
        self.assertEqual(len(tasks), len(self.sample_tasks))
        self.assertEqual(tasks[0].title, self.sample_tasks[0].title)

    # Sprawdza, czy pusta nazwa zadania powoduje wyjątek.
    def test_save_task_with_empty_title(self):
        with self.assertRaises(ValueError):
            Task(title="", description="Description", due_date="2025-12-31", status="pending")

    # Sprawdza, czy data typu date jest poprawnie obsługiwana.
    def test_task_with_date(self):
        task = Task(title="Task with date", description="Description", due_date=date(2099, 1, 1), status="pending")
        storage.save_tasks([task], self.filename)
        loaded_tasks = storage.load_tasks(self.filename)
        self.assertEqual(loaded_tasks[0].due_date, date(2099, 1, 1))

    # Sprawdza obsługę zadania bez daty.
    def test_task_without_due_date(self):
        task = Task(title="Task without date", description="Description", due_date=None, status="pending")
        storage.save_tasks([task], self.filename)
        loaded_tasks = storage.load_tasks(self.filename)
        self.assertIsNone(loaded_tasks[0].due_date)

    # Sprawdza, czy pusta lista nie generuje błędów.
    def test_save_empty_task_list(self):
        storage.save_tasks([], self.filename)
        loaded_tasks = storage.load_tasks(self.filename)
        self.assertEqual(len(loaded_tasks), 0)

    # Sprawdza, czy błąd IO rzuca wyjątek RuntimeError.
    def test_save_raises_runtime_error_on_io_error(self):
        invalid_path = "/invalid_path/test.json"
        with self.assertRaises(RuntimeError):
            storage.save_tasks(self.sample_tasks, invalid_path)

    # Sprawdza, czy dodatkowe pola w JSON są ignorowane.
    def test_load_ignores_extra_fields_in_json(self):
        data_with_extra = [{
            "title": "Zadanie X",
            "description": "Opis X",
            "due_date": "2099-01-01",
            "status": "pending",
            "unexpected": "surprise"
        }]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data_with_extra, f)
        tasks = storage.load_tasks(self.filename)
        self.assertEqual(tasks[0].title, "Zadanie X")
        self.assertFalse(hasattr(tasks[0], "unexpected"))

    # Sprawdza, czy tekstowa data jest konwertowana na obiekt date.
    def test_load_parses_string_date_correctly(self):
        data = [{
            "title": "Zadanie",
            "description": "Opis",
            "due_date": "2099-12-31",
            "status": "pending"
        }]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        tasks = storage.load_tasks(self.filename)
        self.assertIsInstance(tasks[0].due_date, date)
        self.assertEqual(tasks[0].due_date, date(2099, 12, 31))

    # Sprawdza, czy data jest zapisywana w formacie ISO.
    def test_save_serializes_date_to_iso(self):
        storage.save_tasks(self.sample_tasks, self.filename)
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertRegex(data[0]["due_date"], r"\d{4}-\d{2}-\d{2}")

    # Sprawdza obsługę zapisu zadania z None jako data.
    def test_save_handles_task_with_none_fields(self):
        task = Task("T", "D", None)
        storage.save_tasks([task], self.filename)
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsNone(data[0]["due_date"])

    # Sprawdza poprawność zapisu znaków Unicode.
    def test_save_preserves_unicode_characters(self):
        task = Task("Zadanie ś", "Opis ł", "2099-01-01", "pending")
        storage.save_tasks([task], self.filename)
        with open(self.filename, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Zadanie ś", content)
        self.assertIn("Opis ł", content)

    # Sprawdza obsługę zadania z pustym opisem.
    def test_save_and_load_task_with_empty_description(self):
        task = Task(title="Task without description", description="", due_date=None, status="pending")
        storage.save_tasks([task], self.filename)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(loaded[0].description, "")

    # Sprawdza, czy nieznany status zadania jest zachowany.
    def test_load_task_with_unknown_status(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([{
                "title": "Task",
                "description": "Desc",
                "due_date": None,
                "status": "in_progress"
            }], f)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(loaded[0].status, "in_progress")

    # Sprawdza zapis i odczyt zadania z bardzo długim tytułem.
    def test_save_and_load_long_title(self):
        long_title = "A" * 1000
        task = Task(title=long_title, description="desc", due_date=None, status="pending")
        storage.save_tasks([task], self.filename)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(loaded[0].title, long_title)

    # Sprawdza zapis i odczyt zadań o tym samym tytule.
    def test_multiple_tasks_same_title(self):
        tasks = [
            Task(title="Duplicate", description="1", due_date=None),
            Task(title="Duplicate", description="2", due_date=None)
        ]
        storage.save_tasks(tasks, self.filename)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Duplicate")
        self.assertEqual(loaded[1].description, "2")

    # Sprawdza konwersję None w opisie na pusty string.
    def test_task_with_none_description(self):
        task = Task(title="Task", description=None, due_date=None)
        storage.save_tasks([task], self.filename)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(loaded[0].description, "")

    # Sprawdza zapis i odczyt 100 zadań.
    def test_save_and_load_100_tasks(self):
        tasks = [Task(title=f"T{i}", description="desc", due_date=None) for i in range(100)]
        storage.save_tasks(tasks, self.filename)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(len(loaded), 100)
        self.assertEqual(loaded[-1].title, "T99")

    # Sprawdza, czy pusty JSON jako lista zwraca pustą listę zadań.
    def test_load_empty_json_list(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([], f)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(loaded, [])

    # Sprawdza, czy zagnieżdżone dane są ignorowane przy wczytywaniu.
    def test_load_task_with_nested_data(self):
        data = [{
            "title": "Nested Test",
            "description": "Has nested",
            "due_date": None,
            "status": "pending",
            "extra": {"note": "ignore this"}
        }]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
        loaded = storage.load_tasks(self.filename)
        self.assertEqual(loaded[0].title, "Nested Test")
        self.assertFalse(hasattr(loaded[0], "extra"))

    # Sprawdza, czy niepoprawna struktura JSON zwraca pustą listę.
    def test_load_tasks_with_non_list_json(self):
        wrong_structure = {
            "title": "Niepoprawne dane",
            "description": "To nie jest lista zadań",
            "due_date": None,
            "status": "pending"
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(wrong_structure, f)
        tasks = storage.load_tasks(self.filename)
        self.assertEqual(tasks, [])

    # brak pliku wejsciowego
    def test_loading_nonexistent_file_returns_empty_list(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        tasks = storage.load_tasks(self.filename)
        self.assertEqual(tasks, [])

    # wprowadzneie pustego pliku
    def test_loading_empty_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('')
        tasks = storage.load_tasks(self.filename)
        self.assertEqual(tasks, [])

    # duzy plik json
    def test_saving_and_loading_large_number_of_tasks(self):
        tasks = [Task(f"Task {i}", "Desc", "2099-12-31", "pending") for i in range(10_000)]
        filename = "large_tasks.json"
        save_tasks(tasks, filename)
        loaded = load_tasks(filename)
        self.assertEqual(len(loaded), len(tasks))
