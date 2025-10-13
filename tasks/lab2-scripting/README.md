# Laboratorium 2: ćwiczenia z programowania

Na tym laboratorium, nauczysz się programować proste skrypty wspomagające obliczenia inżynierskie z zakresu projektowania i analizy belek zginanych. Celem laboratorium jest przygotowanie dwóch funkcji, `analyze_3p` oraz `analyze_4p`, które umożliwią wyznaczenie sił reakcji, maksymalnego momentu gnącego i siły tnącej, oraz ugięcia i naprężenia gnącego w belce zginanej trzy i czteropunktowo. Każda funkcja powinna zwracać obiekt typu `BeamResults`.

**Do zaliczenia laboratorium, konieczne jest przygotowanie sprawozdania dokumentującego działanie funkcji `analyze_3p` oraz `analyze_4p`, wraz z przykładem użycia na wybranych przykładach.**

## Definicja Klasy Danych

Dodaj to na początku pliku Python:

```python
from dataclasses import dataclass

@dataclass
class BeamResults:
    """Wyniki analizy belki"""
    R1: float                    # Siła reakcji w lewej podporze [N]
    R2: float                    # Siła reakcji w prawej podporze [N]
    M_max: float                 # Maksymalny moment gnący [N·mm]
    V_max: float                 # Maksymalna siła tnąca [N]
    L: float                     # Rozpiętość [mm]
    P: float                     # Obciążenie przyłożone [N]
    max_deflection: float | None = None       # Maksymalne ugięcie [mm]
    max_bending_stress: float | None = None   # Maksymalne napr. gnące [MPa]
```

---

## Podstawowe obliczenia dla belek

**Zadanie 1.1**. Belka swobodnie podparta o rozpiętości `L` ma przyłożoną pojedynczą siłę skupioną `F` w środku belki (obciążenie symetryczne). Napisz funkcję `max_moment_3p_symmetric(F, L)`, która oblicza maksymalny moment gnący w belce.

```python
# Dla F = 1000 N, L = 1000 mm
M_max = max_moment_3p_symmetric(1000, 1000)
# Oczekiwany wynik: M_max = 250000 N·mm
print(f"Maksymalny moment: {M_max} N·mm")
```

---

**Zadanie 1.2**. Belka swobodnie podparta o rozpiętości `L` ma pojedynczą siłę skupioną `F` w środku. Napisz funkcję `analyze_3p_symmetric(F, L)`, która przeprowadza pełną analizę belki i zwraca obiekt `BeamResults`.

```python
# Dla F = 1000 N, L = 1000 mm
result = analyze_3p_symmetric(1000, 1000)
print(f"R1 = {result.R1} N")
print(f"R2 = {result.R2} N")
print(f"M_max = {result.M_max} N·mm")
print(f"V_max = {result.V_max} N")
# Oczekiwane: R1 = 500 N, R2 = 500 N, M_max = 250000 N·mm, V_max = 500 N
```

---

**Zadanie 1.3**. Belka swobodnie podparta o rozpiętości `L` ma pojedynczą siłę skupioną `F`. Obciążenie może być umieszczone w dowolnym miejscu wzdłuż belki za pomocą parametru `offset`, który przesuwa obciążenie od pozycji środkowej. Napisz funkcję `analyze_3p(F, L, offset=0)`, która przeprowadza pełną analizę belki i zwraca obiekt `BeamResults`. Funkcja musi walidować dane wejściowe: sprawdzić, że `L > 0` oraz że pozycja obciążenia `a = L/2 + offset` spełnia warunek `0 < a < L`. Jeśli walidacja się nie powiedzie, zgłoś `ValueError`.

```python
# Przypadek symetryczny (offset = 0)
result = analyze_3p(1000, 1000)
print(f"R1 = {result.R1} N, R2 = {result.R2} N")
# Oczekiwane: R1 = 500 N, R2 = 500 N

# Przypadek asymetryczny (offset = -100 mm, obciążenie przesunięte w lewo od środka)
result = analyze_3p(1000, 1000, offset=-100)
print(f"R1 = {result.R1} N")
print(f"R2 = {result.R2} N")
print(f"M_max = {result.M_max} N·mm")
print(f"V_max = {result.V_max} N")
# Oczekiwane: R1 = 600 N, R2 = 400 N, M_max = 240000 N·mm, V_max = 600 N

# Nieprawidłowe dane wejściowe powinny zgłosić błąd
try:
    result = analyze_3p(1000, 1000, offset=600)  # Obciążenie poza belką!
except ValueError as e:
    print(f"Błąd: {e}")
```

---

**Zadanie 1.4**. Belka swobodnie podparta o rozpiętości `L` ma dwie równe siły skupione `F`. Obciążenia są oddzielone odległością `spacing` i mogą być przesuwane wzdłuż belki za pomocą parametru `offset`. Napisz funkcję `analyze_4p(F, L, spacing, offset=0)`, która przeprowadza pełną analizę belki i zwraca obiekt `BeamResults`. Funkcja musi walidować dane wejściowe: sprawdzić, że `L > 0`, `spacing > 0` oraz że obie pozycje obciążeń `a = L/2 - spacing/2 + offset` i `b = L/2 + spacing/2 + offset` spełniają warunek `0 < a < b < L`. Jeśli walidacja się nie powiedzie, zgłoś `ValueError`.

```python
# Przypadek symetryczny (offset = 0, spacing = 600 mm)
result = analyze_4p(1000, 1200, 600)
print(f"R1 = {result.R1} N, R2 = {result.R2} N")
print(f"M_max = {result.M_max} N·mm")
# Oczekiwane: R1 = 1000 N, R2 = 1000 N, M_max = 300000 N·mm

# Przypadek asymetryczny (offset = 100 mm, obciążenia przesunięte w prawo)
result = analyze_4p(1000, 1200, 600, offset=100)
print(f"R1 = {result.R1} N")
print(f"R2 = {result.R2} N")
print(f"M_max = {result.M_max} N·mm")
print(f"V_max = {result.V_max} N")

# Nieprawidłowe dane wejściowe powinny zgłosić błąd
try:
    result = analyze_4p(1000, 1200, 1000)  # Rozstaw zbyt duży!
except ValueError as e:
    print(f"Błąd: {e}")
```

---

## Analiza naprężeń i ugięć belki

Opierając się na Grupie 1, zintegrujesz teraz właściwości materiałowe i geometrię przekroju z analizą belki. Wykorzystując programowanie obiektowe, stworzysz klasy przekrojów reprezentujące różne kształty belek. Pozwoli to na obliczanie ugięć i naprężeń, które są kluczowe dla określenia, czy projekt belki spełnia wymagania bezpieczeństwa. Ta grupa pokazuje, jak inżynierowie łączą różne aspekty (geometrię, materiały, obciążenia) w celu oceny właściwości konstrukcyjnych. Przed rozpoczęciem pracy, zdefiniuj **abstrakcyjną klasę bazową (ABC)**, która będzie stanowiła wzór dla dziedziczonych klas przekrojów.

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Section(ABC):
    """Abstrakcyjna klasa bazowa dla przekrojów belek"""
    E: float      # Moduł Younga [MPa]
    nu: float     # Współczynnik Poissona [-]
    rho: float    # Gęstość materiału [kg/m³]

    @abstractmethod
    def area(self) -> float:
        """Pole przekroju [mm²]"""
        pass

    @abstractmethod
    def I_xx(self) -> float:
        """Moment bezwładności względem osi x-x (poziomej) [mm⁴]"""
        pass

    @abstractmethod
    def W_xx(self) -> float:
        """Wskaźnik wytrzymałości przekroju względem osi x-x [mm³]"""
        pass
```

**Zadanie 2.1**. Zaimplementuj dwie różne klasy przekrojów dziedziczące po `Section`. Każda klasa musi implementować trzy metody abstrakcyjne: `area()`, `I_xx()` i `W_xx()`. Wybierz dowolne dwa kształty przekrojów (np. prostokątny, kołowy, dwuteownik, rura, itp.).

```python
# Przykład użycia z wybranymi przekrojami
section1 = TwojPierwszyPrzekroj(a=120, b=80, t=3, E=200000, nu=0.3, rho=7850)
print(f"Przekrój 1 - Pole: {section1.area()} mm²")
print(f"Przekrój 1 - I_xx: {section1.I_xx()} mm⁴")
print(f"Przekrój 1 - W_xx: {section1.W_xx()} mm³")

section2 = TwojDrugiPrzekroj(D=50, E=200000, nu=0.3, rho=7850)
print(f"Przekrój 1 - Pole: {section2.area()} mm²")
print(f"Przekrój 1 - I_xx: {section2.I_xx()} mm⁴")
print(f"Przekrój 1 - W_xx: {section2.W_xx()} mm³")
```

**Zadanie 2.2**. Zmodyfikuj funkcję `analyze_3p`, aby przyjmowała opcjonalny parametr `section`. Gdy przekrój jest podany, oblicz maksymalne ugięcie i maksymalne naprężenie gnące.

```python
# Z przekrojem (NOWE zachowanie)
steel_rect = RectangularSection(b=20, h=40, E=200_000, nu=0.3, rho=7850)
result = analyze_3p(F=1000, L=1000, offset=0, section=steel_rect)
print(f"M_max = {result.M_max} N·mm")
print(f"Ugięcie = {result.max_deflection:.4f} mm")
print(f"Naprężenie = {result.max_bending_stress:.2f} MPa")
```

**Zadanie 2.3**. Zmodyfikuj funkcję `analyze_4p`, aby przyjmowała opcjonalny parametr `section`. Gdy przekrój jest podany, oblicz maksymalne ugięcie i naprężenie gnące.

```python
# Z przekrojem
steel_rect = RectangularSection(b=30, h=50, E=200_000, nu=0.3, rho=7850)
result = analyze_4p(F=1000, L=1200, spacing=400, offset=0, section=steel_rect)
print(f"M_max = {result.M_max} N·mm")
print(f"Ugięcie = {result.max_deflection:.4f} mm")
print(f"Naprężenie = {result.max_bending_stress:.2f} MPa")
```
