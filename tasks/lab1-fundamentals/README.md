# Laboratorium 1: przygotowanie środowiska do pracy

Na tym laboratorium skonfigurujesz środowisko do pracy z językiem Python. W tym celu, konieczne jest zainstalowanie zależności oraz wymaganej wersji Pythona w środowisku wirtualnym `.venv/` oraz konfiguracja systemu kontroli wersji Git. To za jego pośrednictwem będziesz zapisywać efekty swojej pracy, oraz wersjonować wprowadzane zmiany w kodzie. 

## Konfiguracja

### 1. Zainstaluj zależności

```bash
uv sync
```

### 2. Skonfiguruj Git

```bash
git config user.name "Twoje Imię i Nazwisko"
git config user.email "twoj.email@example.com"
```

Zweryfikuj konfigurację:
```bash
git config user.name
git config user.email
```

### 3. Utwórz gałąź roboczą

```bash
git checkout -b lab
```

**Ważne:** Wszyscy studenci pracują na gałęzi `lab`. Nigdy nie commituj bezpośrednio do `main`!

## Codzienny przepływ pracy

### Pobieranie aktualizacji od prowadzącego

Gdy prowadzący opublikuje nowe materiały:

```bash
git checkout main
git pull origin main
git checkout lab
git merge main
```

### Praca nad zadaniami

Całą swoją pracę wykonuj w katalogu `tasks/`:

```bash
cd tasks/
uv run python your_script.py
```

### Uruchamianie skryptów z uv

**uv** to nowoczesny menedżer pakietów i środowisk dla Pythona. Oto najważniejsze komendy:

```bash
# Uruchomienie pojedynczego skryptu
uv run python nazwa_skryptu.py

# Uruchomienie skryptu z argumentami
uv run python nazwa_skryptu.py arg1 arg2

# Uruchomienie interaktywnej konsoli Python
uv run python3

# Sprawdzenie zainstalowanych pakietów
uv pip list
```

**Uwaga:** `uv run` automatycznie aktywuje wirtualne środowisko projektu, więc nie musisz ręcznie aktywować środowiska przed uruchomieniem skryptów.

### Commitowanie pracy

```bash
git add .
git commit -m "Wykonanie zadania XYZ"
```

**Uwaga:** Twoja praca pozostaje lokalna. Nie wypychasz zmian do zdalnego repozytorium.
