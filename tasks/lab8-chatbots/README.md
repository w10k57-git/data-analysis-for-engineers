# Laboratorium 6: programowanie z użyciem dużych modeli językowych (LLM)

Na tym laboratorium nauczysz się wykorzystywać duże modele językowe (LLM) do rozwiązywania praktycznych problemów inżynierskich. Celem laboratorium jest przygotowanie dwóch funkcji: `classify_technical_problem` do klasyfikacji opisów jako problemów technicznych oraz `extract_machine_log` do wyodrębniania ustrukturyzowanych danych z dzienników maszynowych. Będziesz pracować z lokalnymi modelami Ollama, co pozwoli Ci na eksperymenty bez kosztów API.

**Do zaliczenia laboratorium konieczne jest przygotowanie sprawozdania dokumentującego działanie funkcji `classify_technical_problem` oraz `extract_machine_log`, wraz z przykładem użycia na wybranych przykładach.**

---

## Zadania do zrobienia

**Zadanie 1.1**. Napisz funkcję `classify_technical_problem(description: str) -> bool`, która używa LLM do klasyfikacji opisu jako problem techniczny (`True`) lub nie (`False`). Funkcja powinna połączyć się z lokalnym modelem Ollama i zwrócić wynik klasyfikacji.

---

**Zadanie 1.2**. Napisz funkcję `extract_machine_log(log_text: str) -> ExtractionResult`, która wyodrębnia nazwę maszyny, opis usterki i poziom dotkliwości (Low, Medium, High) z naturalnego tekstu dziennika maszynowego. Funkcja powinna używać LLM do analizy tekstu i zwracać ustrukturyzowany obiekt `ExtractionResult`.

```python
import json

# Wczytaj dane testowe
with open("extraction_task.json") as f:
    logs = json.load(f)

# Testuj funkcję
for log_entry in logs:
    result = extract_machine_log(log_entry["log_text"])
    print(f"Maszyna: {result.machine}")
    print(f"Usterka: {result.malfunction}")
    print(f"Dotkliwość: {result.severity}")
    print("---")
# Oczekiwane: Funkcja poprawnie wyodrębnia wszystkie trzy pola z każdego dziennika
```

**Wskazówki**:

- Możesz użyć dwóch podejść: raw client z JSON mode lub Pydantic AI
- Dla raw client: użyj parametru `format="json"` w Ollama, aby wymusić format JSON
- Dla Pydantic AI: użyj `Agent` z `result_type=ExtractionResult` dla automatycznej walidacji
- Zdefiniuj jasne kryteria dla poziomów dotkliwości w system prompt:
  - Low: drobne problemy, brak bezpośredniego ryzyka, zaplanowana konserwacja
  - Medium: spadek wydajności, wymaga uwagi w ciągu kilku dni
  - High: krytyczne awarie, zagrożenia bezpieczeństwa, wstrzymanie produkcji
- Model powinien samodzielnie ocenić poziom dotkliwości na podstawie opisu w dzienniku

## Wskazówki dotyczące prompt engineering

1. **Bądź konkretny**: Jasno określ format wyjściowy i oczekiwania
2. **Podaj przykłady**: Jeśli model ma problemy, dodaj przykłady (few-shot prompting)
3. **Iteruj**: Testuj różne wersje promptów i porównuj wyniki
4. **Obsłuż błędy**: LLM mogą zwracać nieoczekiwane formaty - dodaj walidację
5. **Dokumentuj**: Zapisuj, które prompty działały najlepiej i dlaczego
