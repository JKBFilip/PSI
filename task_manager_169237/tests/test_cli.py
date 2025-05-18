from datetime import datetime
import unittest
import os
from src.cli import CLIHandler
from src.storage import save_tasks
from src.task import Task


class TestCLI(unittest.TestCase):
    # czyszczenie plik json jezeli jest juz zapisany
    def setUp(self):
        self.test_filename = "test_tasks.json"
        self.tasks = []
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    # Testuje dodanie poprawnego zadania i zapis
    def test_add_task_successful(self):
        inputs = iter(["1", "Nowe zadanie", "Opis testowy", "2025-12-31", "3"])
        outputs = []

        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename="test_tasks.json")
        cli.run()

        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].title, "Nowe zadanie")
        self.assertEqual(cli.tasks[0].description, "Opis testowy")
        self.assertEqual(cli.tasks[0].due_date.isoformat(), "2025-12-31")

    # Testuje wyświetlanie zadań (czy odpowiedni format wypisany)
    def test_show_tasks(self):
        inputs = iter(["2", "3"])
        outputs = []
        task = Task("Zadanie X", "Opis", "2025-12-31", status="pending")

        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename="test_tasks.json")
        cli.tasks = [task]  # wstrzykujemy istniejące zadanie
        cli.run()

        self.assertIn("1. Zadanie X - pending", outputs)

    # Testuje zakończenie programu po wybraniu opcji 3
    def test_quit_option(self):
        inputs = iter(["3"])
        outputs = []

        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append)
        cli.run()

        self.assertEqual(cli.tasks, [])

    # Testuje obsługę nieprawidłowej opcji menu
    def test_invalid_menu_choice(self):
        inputs = iter(["9", "3"])
        outputs = []

        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append)
        cli.run()

        self.assertIn("Nieprawidłowy wybór", outputs)

    # Testuje odrzucenie zadania z pustym tytułem
    def test_add_task_empty_title(self):
        inputs = iter(["1", "   ", "Opis", "2025-12-31", "3"])
        outputs = []

        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename="test_tasks.json")
        cli.run()

        self.assertEqual(len(cli.tasks), 0)
        self.assertIn("Wszystkie pola muszą być wypełnione.", outputs)

    # Test: Dodanie zadania z niepoprawnym formatem daty
    def test_add_task_invalid_date_format(self):
        inputs = iter(["1", "Zadanie A", "Opis A", "31-12-2025", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()

        self.assertEqual(len(cli.tasks), 0)
        self.assertIn("Niepoprawny format daty. Użyj YYYY-MM-DD.", outputs)

    # Test: Dodanie zadania z pustym opisem
    def test_add_task_empty_description(self):
        inputs = iter(["1", "Zadanie A", "  ", "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()

        self.assertEqual(len(cli.tasks), 0)
        self.assertIn("Wszystkie pola muszą być wypełnione.", outputs)

    # Test: Pokazanie wielu zadań
    def test_show_multiple_tasks(self):
        inputs = iter(["2", "3"])
        outputs = []
        tasks = [
            Task("Task1", "Desc1", "2025-12-31"),
            Task("Task2", "Desc2", "2025-12-31", status="done"),
        ]
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = tasks
        cli.run()

        self.assertIn("1. Task1 - pending", outputs)
        self.assertIn("2. Task2 - done", outputs)

    # Test: Oznaczenie zadania jako zakończone
    def test_mark_task_done(self):
        inputs = iter(["4", "1", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = [Task("Do zrobienia", "opis", "2025-12-31")]
        cli.run()

        self.assertEqual(cli.tasks[0].status, "done")

    # Test: Oznaczenie zadania z nieprawidłowym indeksem
    def test_mark_task_invalid_index(self):
        inputs = iter(["4", "10", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = [Task("Zadanie", "Opis", "2025-12-31")]
        cli.run()

        self.assertIn("Nieprawidłowy numer zadania", outputs)

    # Test: Oznaczenie zadania z nieprawidłowym wejściem (np. tekst zamiast liczby)
    def test_mark_task_invalid_input(self):
        inputs = iter(["4", "abc", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = [Task("Zadanie", "Opis", "2025-12-31")]
        cli.run()

        self.assertIn("Nieprawidłowy numer zadania", outputs)

    # Test: Dodanie zadania z białymi znakami wokół danych
    def test_add_task_with_whitespace(self):
        inputs = iter(["1", "  Tytuł  ", "  Opis  ", "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()

        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].title.strip(), "Tytuł")
        self.assertEqual(cli.tasks[0].description.strip(), "Opis")

    # Test: Program nie dodaje zadania jeśli brakuje daty
    def test_add_task_missing_date(self):
        inputs = iter(["1", "Zadanie", "Opis", "   ", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()

        self.assertEqual(len(cli.tasks), 0)
        self.assertIn("Wszystkie pola muszą być wypełnione.", outputs)

    # Test: Program działa poprawnie przy pustej liście zadań
    def test_show_tasks_empty_list(self):
        inputs = iter(["2", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = []
        cli.run()

        self.assertEqual(len([o for o in outputs if " - " in o]), 0)

    # Test: Dodanie wielu zadań w jednej sesji
    def test_add_multiple_tasks(self):
        inputs = iter([
            "1", "T1", "D1", "2025-12-31",
            "1", "T2", "D2", "2025-12-30",
            "3"
        ])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()

        self.assertEqual(len(cli.tasks), 2)
        self.assertEqual(cli.tasks[0].title, "T1")
        self.assertEqual(cli.tasks[1].title, "T2")

    # Test: Nie dodaje zadania jeśli wszystkie pola są puste
    def test_add_task_all_fields_empty(self):
        inputs = iter(["1", "   ", "   ", "   ", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 0)
        self.assertIn("Wszystkie pola muszą być wypełnione.", outputs)

    # Test: Dodanie zadania z minimalnym poprawnym tytułem i opisem
    def test_add_task_minimal_valid(self):
        inputs = iter(["1", "a", "b", "2025-01-01", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].title, "a")

    # Test: Wielokrotne błędne wybory w menu, zanim użytkownik wyjdzie
    def test_multiple_invalid_choices(self):
        inputs = iter(["0", "abc", "", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append)
        cli.run()
        self.assertEqual(outputs.count("Nieprawidłowy wybór"), 3)

    # Test: Dodanie zadania z datą z przeszłości — dozwolone (logicznie tak)
    def test_add_task_past_due_date(self):
        inputs = iter(["1", "T", "D", "2000-01-01", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].due_date.isoformat(), "2000-01-01")

    # Test: Lista zadań pokazuje poprawnie indeksy po oznaczeniu zakończenia
    def test_show_tasks_after_done(self):
        inputs = iter(["4", "1", "2", "3"])
        outputs = []
        task = Task("Do zrobienia", "opis", "2025-12-31")
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = [task]
        cli.run()
        self.assertIn("1. Do zrobienia - done", outputs)

    # Test: Dodanie zadania z bardzo długim tytułem i opisem
    def test_add_task_long_title_description(self):
        long_text = "x" * 1000
        inputs = iter(["1", long_text, long_text, "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].title, long_text)

    # Test: Użytkownik wybiera opcję oznaczenia zakończonego zadania, gdy nie ma zadań
    def test_mark_done_no_tasks(self):
        inputs = iter(["4", "1", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = []
        cli.run()
        self.assertIn("Nieprawidłowy numer zadania", outputs)

    # Test: Pokazuje, że oznaczenie jako "done" nie usuwa zadania
    def test_mark_done_task_still_exists(self):
        inputs = iter(["4", "1", "3"])
        outputs = []
        task = Task("Zadanie", "Opis", "2025-12-31")
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = [task]
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].status, "done")

    # Test: Dodanie zadania, a następnie ponowne uruchomienie CLI odczytuje je poprawnie z pliku
    def test_persisted_task_after_reload(self):
        inputs = iter(["1", "Tytuł", "Opis", "2025-12-31", "3"])
        outputs = []
        cli1 = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli1.run()

        cli2 = CLIHandler(input_func=lambda _: "3", output_func=lambda x: None, filename=self.test_filename)
        self.assertEqual(len(cli2.tasks), 1)
        self.assertEqual(cli2.tasks[0].title, "Tytuł")

    # Test: Dodanie zadania i natychmiastowe jego oznaczenie jako zakończone
    def test_add_and_immediately_mark_done(self):
        inputs = iter(["1", "Nowe", "Opis", "2025-12-31", "4", "1", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].status, "done")

    # Test: Dodanie zadania z datą dzisiejszą
    def test_add_task_today_date(self):
        today = datetime.now().strftime("%Y-%m-%d")
        inputs = iter(["1", "Dzisiejsze", "Opis", today, "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].due_date.strftime("%Y-%m-%d"), today)

    # Test: Dodanie zadania ze spacjami i nową linią w opisie
    def test_add_task_multiline_description(self):
        desc = "Linia 1\nLinia 2\nLinia 3"
        inputs = iter(["1", "Tytuł", desc, "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(cli.tasks[0].description, desc)

    # Test: Wpisanie znaku specjalnego jako wyboru z menu
    def test_special_character_menu_choice(self):
        inputs = iter(["$", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append)
        cli.run()
        self.assertIn("Nieprawidłowy wybór", outputs)

    # Test: Dodanie zadania z numerami w tytule i opisie
    def test_add_task_with_numbers(self):
        inputs = iter(["1", "Zadanie 123", "Opis 456", "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(cli.tasks[0].title, "Zadanie 123")

    # Test: Wpisanie dużej liczby jako indeksu do oznaczenia zakończonego
    def test_mark_task_huge_index(self):
        inputs = iter(["4", "9999", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.tasks = [Task("Test", "Opis", "2025-12-31")]
        cli.run()
        self.assertIn("Nieprawidłowy numer zadania", outputs)

    # Test: Dodanie zadania z datą maksymalną
    def test_add_task_max_date(self):
        inputs = iter(["1", "Daleka przyszłość", "Opis", "9999-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(cli.tasks[0].due_date.isoformat(), "9999-12-31")

    # Test: Dodanie zadania z bardzo długim tytułem i opisem (~10k znaków)
    def test_add_task_very_long_fields(self):
        long_text = "x" * 10000
        inputs = iter(["1", long_text, long_text, "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(cli.tasks[0].title, long_text)
        self.assertEqual(cli.tasks[0].description, long_text)

    # Test: Naciśnięcie ENTER bez podania wyboru w menu
    def test_empty_menu_input(self):
        inputs = iter(["", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append)
        cli.run()
        self.assertIn("Nieprawidłowy wybór", outputs)

    # Test: Brak pliku JSON przy starcie – CLI powinien ruszyć z pustą listą
    def test_missing_file_starts_empty(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        cli = CLIHandler(input_func=lambda _: "3", output_func=lambda _: None, filename=self.test_filename)
        self.assertEqual(cli.tasks, [])

    # Test: Dodanie zadania i sprawdzenie, że po ponownym uruchomieniu dalej istnieje
    def test_data_persistence_between_sessions(self):
        inputs = iter(["1", "Trwałość", "Test", "2025-12-31", "3"])
        outputs = []
        cli1 = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli1.run()

        cli2 = CLIHandler(input_func=lambda _: "3", output_func=lambda _: None, filename=self.test_filename)
        self.assertEqual(len(cli2.tasks), 1)
        self.assertEqual(cli2.tasks[0].title, "Trwałość")

    # Test: Dodanie bardzo wielu zadań (1000) – test masowy
    def test_bulk_add_tasks(self):
        title_base = "Task"
        for i in range(1000):
            task = Task(f"{title_base} {i}", "Opis", "2025-12-31")
            self.tasks.append(task)
        save_tasks(self.tasks, self.test_filename)

        cli = CLIHandler(input_func=lambda _: "3", output_func=lambda _: None, filename=self.test_filename)
        self.assertEqual(len(cli.tasks), 1000)

    # Test: Oznaczenie jako done dwa razy z rzędu
    def test_double_mark_done(self):
        task = Task("Podwójne DONE", "Test", "2025-12-31")
        self.tasks = [task]
        save_tasks(self.tasks, self.test_filename)
        inputs = iter(["4", "1", "4", "1", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(cli.tasks[0].status, "done")  # nadal "done", nie zmienia się na coś dziwnego

    # Test: Zadanie z datą nieistniejącą (np. 2025-02-30)
    def test_add_task_invalid_day(self):
        inputs = iter(["1", "Test", "Opis", "2025-02-30", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append)
        cli.run()
        self.assertIn("Niepoprawny format daty. Użyj YYYY-MM-DD.", outputs)

    # Test: Dodanie zadania z nazwą zawierającą unicode (emoji, znaki spoza ASCII)
    def test_add_task_with_unicode(self):
        inputs = iter(["1", "🧪 Zadanie 🚀", "Opis z emoji 💬", "2025-12-31", "3"])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(cli.tasks[0].title, "🧪 Zadanie 🚀")

    # Test: Dużo błędnych prób zanim uda się dodać poprawne zadanie
    def test_multiple_failed_then_successful_add(self):
        inputs = iter([
            "1", "", "", "",   # niepoprawne
            "1", "   ", "a", "2025-13-01",  # też nie
            "1", "OK", "Opis", "2025-12-31",  # w końcu dobrze
            "3"
        ])
        outputs = []
        cli = CLIHandler(input_func=lambda _: next(inputs), output_func=outputs.append, filename=self.test_filename)
        cli.run()
        self.assertEqual(len(cli.tasks), 1)
        self.assertEqual(cli.tasks[0].title, "OK")
