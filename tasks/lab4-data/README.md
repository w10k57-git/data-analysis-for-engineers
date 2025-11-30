# Laboratorium 4: Ładowanie i przetwarzanie danych

Na tym laboratorium nauczysz się wczytywać i przetwarzać duże zbiory danych na przykładzie pomiarów systemu hydraulicznego. Czujniki mają różne częstotliwości próbkowania (1 Hz, 10 Hz, 100 Hz). Twoim zadaniem jest zunifikowanie wszystkich czujników do wspólnej częstotliwości i zapisanie w formacie pickle. Przed przystąpienie do zadań, pobierz dane i zapisz je w folderze `~/data/external`

---

**Zadanie 1**. Zaimplementuj funkcję, która redukuje częstotliwość próbkowania przez wybór co N-tej próbki.

```python
import numpy as np

def downsample_decimation(data: np.ndarray, original_hz: int, target_hz: int = 1) -> np.ndarray:
    """
    Downsampling przez decymację - wybór co N-tej próbki
    
    Args:
        data: tablica numpy z danymi (np. [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        original_hz: częstotliwość oryginalna (np. 10)
        target_hz: częstotliwość docelowa (np. 1)
    
    Returns:
        tablica numpy po downsamplingu (np. [1, 11, 21, ...])
    
    Przykład:
        data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        result = downsample_decimation(data, 10, 2)
        # result = [0, 5] (co 5. próbka, bo 10/2=5)
    """
    # TODO: Oblicz krok (co która próbka)
    # TODO: Zwróć co N-tą próbkę używając slicingu data[::step]
    pass

test_data = np.arange(100)  # [0, 1, 2, ..., 99]
result = downsample_decimation(test_data, 100, 1)
print(f"Z {len(test_data)} próbek → {len(result)} próbek")  # Oczekiwane: 100 → 1
print(f"Wartość: {result}")  # Oczekiwane: [0]
```

---

**Zadanie 2**. Zaimplementuj funkcję, która redukuje częstotliwość próbkowania przez uśrednianie okien.

```python
import numpy as np

def downsample_averaging(data: np.ndarray, original_hz: int, target_hz: int = 1) -> np.ndarray:
    """
    Downsampling przez uśrednianie okien
    
    Args:
        data: tablica numpy z danymi
        original_hz: częstotliwość oryginalna (np. 10)
        target_hz: częstotliwość docelowa (np. 1)
    
    Returns:
        tablica numpy po downsamplingu
    
    Przykład:
        data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        result = downsample_averaging(data, 10, 2)
        # result = [2.0, 7.0] (średnia z [0,1,2,3,4] i [5,6,7,8,9])
    """
    # TODO: Oblicz rozmiar okna (ile próbek uśredniać)
    # TODO: Oblicz liczbę okien
    # TODO: Dla każdego okna oblicz średnią i zwróć jako tablicę
    pass

test_data = np.arange(100)  # [0, 1, 2, ..., 99]
result = downsample_averaging(test_data, 100, 10)
print(f"Z {len(test_data)} próbek → {len(result)} próbek")  # Oczekiwane: 100 → 10
print(f"Pierwsze okno (średnia z 0-9): {result[0]}")  # Oczekiwane: 4.5
```

**Wizualizacja różnicy (opcjonalnie):**

```python
import matplotlib.pyplot as plt

# Wygeneruj zaszumiony sygnał
time = np.linspace(0, 60, 6000)  # 100 Hz przez 60 sekund
signal = np.sin(time * 0.5) + np.random.normal(0, 0.1, 6000)

# Zastosuj obie metody
dec = downsample_decimation(signal, 100, 1)
avg = downsample_averaging(signal, 100, 1)

# Wykres
plt.figure(figsize=(12, 4))
plt.plot(time, signal, 'gray', alpha=0.3, linewidth=0.5, label='Oryginał (100 Hz)')
plt.plot(np.arange(60), dec, 'ro-', markersize=3, label='Decymacja')
plt.plot(np.arange(60), avg, 'bs-', markersize=3, label='Uśrednianie')
plt.xlabel('Czas (s)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

**Zadanie 3**. Stwórz generator, który czyta plik linia po linii bez ładowania całości do pamięci.

```python
from typing import Iterator

def read_sensor_file(filepath: str) -> Iterator[np.ndarray]:
    """
    Generator czytający plik czujnika linia po linii
    
    Args:
        filepath: ścieżka do pliku (np. 'data/PS1.txt')
    
    Yields:
        np.ndarray: dane dla jednego cyklu pomiarowego
    
    Dlaczego generator?
    - Plik z 2205 cyklami × 6000 próbek = ~13 milionów liczb
    - Generator przetwarza po jednym cyklu, oszczędzając pamięć
    """
    # TODO: Otwórz plik używając 'with open(filepath, 'r') as f:'
    # TODO: Dla każdej linii:
    #   - Podziel po tabulatorze: line.strip().split('\t')
    #   - Przekonwertuj na floaty i stwórz tablicę numpy
    #   - Użyj 'yield' zamiast 'return'
    pass

DATA_PATH = '/path/to/data/'  # ZMIEŃ NA SWOJĄ ŚCIEŻKĘ

gen = read_sensor_file(DATA_PATH + 'PS1.txt')
first_cycle = next(gen)
second_cycle = next(gen)

print(f"Pierwszy cykl: {len(first_cycle)} próbek")  # Oczekiwane: 6000
print(f"Drugi cykl: {len(second_cycle)} próbek")    # Oczekiwane: 6000
print(f"Pierwsze 5 wartości: {first_cycle[:5]}")
```

---

**Zadanie 4**. Stwórz funkcję, która przetwarza wszystkie czujniki i zwraca obiekt dataclass. Wczytaj i przetwórz tylko te pliki, które są uwzględnione w pliku `config.yaml`

```python
from dataclasses import dataclass

import numpy as np

@dataclass
class HydraulicData:
    """Zunifikowane dane z czujników hydraulicznych"""
    profile: np.ndarray                     # Etykiety stanów (2205, 5)
    temperature: dict[str, np.ndarray]      # {'TS1': array, 'TS2': array, ...}
    pressure: dict[str, np.ndarray]         # {'PS1': array, 'PS2': array, ...}
    flow: dict[str, np.ndarray]             # {'FS1': array, 'FS2': array}

def process_hydraulic_data(data_path: str,
                           config_file: str,
                           method: str = 'averaging',
                           target_hz: int = 1) -> HydraulicData:
    """
    Przetwarza dane hydrauliczne do zunifikowanej częstotliwości

    Args:
        data_path: ścieżka do folderu z danymi (z trailing slash)
        method: 'decimation' lub 'averaging'
        target_hz: docelowa częstotliwość (domyślnie 1 Hz)

    Returns:
        HydraulicData: obiekt z przetworzonymi danymi
    """

    # 1. Wybierz funkcję downsamplingu na podstawie parametru 'method'
    downsample_func = downsample_averaging if method == 'averaging' else downsample_decimation

    # 2. Załaduj konfigurację czujników z YAML
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # 3. Załaduj profile
    profile = np.loadtxt(data_path + 'profile.txt')

    # 4. Przetwarzaj czujniki temperatury
    print("Przetwarzanie czujników temperatury...")
    temp_data = {}
    for filename in config['temperature']['files']:
        # TODO: Wyciągnij nazwę czujnika (np. 'TS1' z 'TS1.txt')
        # TODO: Pobierz częstotliwość z config['temperature']['hz']
        # TODO: Użyj generatora read_sensor_file() do czytania cykli
        # TODO: Dla każdego cyklu:
        #       - Jeśli freq != target_hz, zastosuj downsample_func
        #       - Dodaj do listy cycles
        # TODO: Przekonwertuj listę na np.array() i zapisz w temp_data[sensor_name]
        # TODO: Wypisz nazwę czujnika i shape
        pass

    # 5. Przetwarzaj czujniki ciśnienia
    print("\nPrzetwarzanie czujników ciśnienia...")
    pressure_data = {}
    for filename in config['pressure']['files']:
        # TODO: Analogicznie jak dla temperatury
        pass

    # 6. Przetwarzaj czujniki przepływu
    print("\nPrzetwarzanie czujników przepływu...")
    flow_data = {}
    for filename in config['flow']['files']:
        # TODO: Analogicznie jak dla temperatury
        pass

    # 7. Stwórz i zwróć obiekt HydraulicData
    return HydraulicData(
        profile=profile,
        temperature=temp_data,
        pressure=pressure_data,
        flow=flow_data
    )

# Przykład użycia
data = process_hydraulic_data(DATA_PATH, method='averaging')

print("\n" + "="*60)
print("Załadowane dane:")
print("="*60)
print(f"Profile: {data.profile.shape}")
print(f"Temperature TS1: {data.temperature.TS1.shape}")
print(f"Temperature TS2: {data.temperature.TS2.shape}")
print(f"Pressure PS1: {data.pressure.PS1.shape}")
print(f"Flow FS1: {data.flow.FS1.shape}")

# Dostęp do konkretnego czujnika
first_cycle_ps1 = data.pressure.PS1[0]  # Pierwszy cykl z PS1
print(f"\nPierwszy cykl PS1: {first_cycle_ps1.shape}")  # (60,)
```

**Oczekiwany wynik:**

```text
Przetwarzanie czujników temperatury...
  TS1: (2205, 60)
  TS2: (2205, 60)
  TS3: (2205, 60)
  TS4: (2205, 60)

Przetwarzanie czujników ciśnienia...
  PS1: (2205, 60)
  PS2: (2205, 60)
  PS3: (2205, 60)
  PS4: (2205, 60)
  PS5: (2205, 60)
  PS6: (2205, 60)

Przetwarzanie czujników przepływu...
  FS1: (2205, 60)
  FS2: (2205, 60)

============================================================
Załadowane dane:
============================================================
Profile: (2205, 5)
Temperature TS1: (2205, 60)
Temperature TS2: (2205, 60)
Pressure PS1: (2205, 60)
Flow FS1: (2205, 60)

Pierwszy cykl PS1: (60,)
```

**Zapisywanie do pickle (opcjonalnie):**

```python
# Zapisz obiekt dataclass do pickle
with open('unified_data.pkl', 'wb') as f:
    pickle.dump(data, f)

# Załaduj z powrotem
with open('unified_data.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

print(f"Typ: {type(loaded_data)}")  # <class '__main__.HydraulicData'>
print(f"Pierwszy pomiar PS3: {loaded_data.pressure.PS3[0, 0]}")  # np. 152.4
```

---
