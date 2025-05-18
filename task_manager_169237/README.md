# 📝 Task CLI – Prosty menedżer zadań w terminalu

Task CLI to prosty program do zarządzania zadaniami (to-do list) z poziomu terminala. Pozwala dodawać zadania, oznaczać je jako zakończone oraz przeglądać aktualną listę. Dane są przechowywane w pliku JSON.

## 🚀 Funkcje

* ✅ Dodawanie zadań z tytułem, opisem i datą w formacie `YYYY-MM-DD`
* 📋 Wyświetlanie wszystkich zadań wraz ze statusem (`pending`, `done`)
* 🟢 Oznaczanie zadań jako wykonane
* 📀 Trwałość danych dzięki zapisowi do pliku `tasks.json`
* 🧪 Zestaw testów jednostkowych pokrywających wiele przypadków (w tym brzegowe)

---

## 📦 Struktura projektu

```
.
├── src/
│   ├── __init__.py
│   ├── cli.py         # Obsługa interfejsu CLI
│   ├── task.py        # Klasa Task
│   └── storage.py     # Operacje na pliku JSON
├── tests/
|	├── __init__.py		
|	├── tasks.csv
│   ├── test_cli.py         # testy jednostkowe klasy cli
│   ├── test_task.py        # testy jednostkowe klasy task
│   └── test_storage.py		# testy jednostkowe klasy storage
├── .coverage 
├── large_tasks.json       
├── README.md
├── requirements.txt
└── setup.cfg
```

---

## ▶️ Jak uruchomić

1. **Wymagania**:

* Python 3.7+
* requirements.txt

2. **Uruchomienie programu**:

```bash
  python -m src
```

3. **Dostępne opcje w menu**:

   ```
   1 - Dodaj zadanie
   2 - Pokaż zadania
   3 - Zakończ
   4 - Oznacz zadanie jako zakończone
   ```

---

## ✅ Jak uruchomić testy

```bash
python -m unittest discover tests
```

---


## ✍️ Autorzy i podziękowania

* 👨‍💻 Autor: **Jakub Filipiak**
* ⚙️ Główne klasy  (task, cli, storage), oraz komentarze do testów zostały częściowo wygenerowane i zrefaktoryzowane przy pomocy [ChatGPT](https://openai.com/chatgpt).
* 📆 Kod jest modularny, testowalny i prosty do rozbudowy.

---

## 📄 Licencja

Ten projekt udostępniany jest na licencji MIT. Możesz go swobodnie używać, modyfikować i dystrybuować.

---
