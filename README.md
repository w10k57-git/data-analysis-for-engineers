# Analiza danych inżynierskich z wykorzystaniem języka Python

Materiały do kursu Pythona dla studentów inżynierii na studiach magisterskich. Kurs zakłada brak lub bardzo małą znajomość Pythona na początku. Kurs rozpoczyna się od podstawowych koncepcji w Pythonie, a następnie przechodzi przez podstawowe skrypty i obliczenia numeryczne przy użyciu `math` i `numpy`. W późniejszej części kursu studenci uczą się, jak wczytywać dane z różnych źródeł, w tym scrapowania stron internetowych. Na piątych zajęciach laboratoryjnych studenci uczą się przeprowadzać eksploracyjną analizę danych, a następnie analizę statystyczną wyników. Poznają również interakcje z bazami danych. Kurs kończy się nauką podstawowej interakcji z chatbotami, w tym strategii promptowania.

## Przygotowanie repozytorium do zajęć laboratoryjnych

Przed rozpoczęciem upewnij się, że masz zainstalowane:

- **uv**
- **Visual Studio Code**
- **Git**

## Konfiguracja

### 1. Sklonuj repozytorium

Sklonuj to repozytorium do folderu nazwanego Twoim **numerem indeksu**.

Zamień `123456` na swój rzeczywisty numer indeksu:

```bash
git clone https://github.com/w10k57-git/data-analysis.git 123456
cd 123456
```

**Przykład:** Jeśli Twój numer indeksu to `987654`, wykonaj:

```bash
git clone https://github.com/w10k57-git/data-analysis.git 987654
cd 987654
```

### 2. Zainstaluj zależności

```bash
uv sync
```

### 3. Skonfiguruj Git

```bash
git config user.name "Twoje Imię i Nazwisko"
git config user.email "twoj.email@example.com"
```

Zweryfikuj swoją konfigurację:

```bash
git config user.name
git config user.email
```

### 4. Utwórz swoją gałąź roboczą

```bash
git checkout -b lab
```

**Ważne:** Wszyscy studenci pracują na gałęzi `lab`. Nigdy nie commituj do `main`!

## Codzienny workflow

### Pobieranie aktualizacji od prowadzącego

Gdy prowadzący opublikuje nowe materiały:

```bash
git checkout main
git pull origin main
git checkout lab
git merge main
```

### Praca nad zadaniami

Cała Twoja praca powinna odbywać się w katalogu `tasks/`:

```bash
cd tasks/
uv run python your_script.py
```

### Commitowanie swojej pracy

```bash
git add .
git commit -m "Ukończenie zadania XYZ"
```

**Uwaga:** Twoja praca pozostaje lokalna. Nie pushuj do zdalnego repozytorium.

## Przykłady

## Struktura repozytorium

```
123456/  (twój numer indeksu)
├── examples/       # Przykłady kodu i ćwiczenia
├── tasks/          # TWOJA przestrzeń robocza - pracuj tutaj!
├── src/            # Funkcje narzędziowe, których możesz używać
└── data/           # Pliki danych do kursu
```

## Podsumowanie workflow Git

- **`main`** - Materiały kursu od prowadzącego (tylko do odczytu)
- **`lab`** - Twoja gałąź robocza (wszyscy studenci używają tej nazwy)

### Kluczowe polecenia

```bash
# Sprawdź status
git status

# Zobacz historię
git log --oneline

# Zobacz zmiany
git diff
```

## Kompletna lista kontrolna konfiguracji

- [ ] Sklonuj repozytorium do folderu nazwanego swoim numerem indeksu
- [ ] Uruchom `uv sync` aby zainstalować zależności
- [ ] Skonfiguruj `git config user.name` i `git config user.email`
- [ ] Utwórz gałąź `lab` za pomocą `git checkout -b lab`

---

Miłego kodowania! 🚀
