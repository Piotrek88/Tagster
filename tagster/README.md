# Tagster 
### Asystent Opisywania i Tagowania Zdjęć z FAQ

## Opis Rozwiązania

### Wykorzystane Technologie
- **Platforma Chmurowa**: AWS
  - AWS Rekognition do analizy obrazów
  - AWS DynamoDB (planowane) do przechowywania FAQ i historii analiz
  - AWS Lambda (planowane) do skalowania funkcji
  - AWS API Gateway (planowane) do zarządzania API

- **Modele Językowe**:
  - OpenAI GPT-4 do generowania opisów, tagów i odpowiedzi na FAQ
  - OpenAI Embeddings do wyszukiwania podobnych pytań w FAQ

- **Interfejs Użytkownika**:
  - Streamlit do szybkiego prototypowania
  - React (planowane) do produkcyjnego interfejsu

### Architektura
1. **Analiza Obrazów**:
   - Przesłanie obrazu do AWS Rekognition
   - Generowanie etykiet i scen
   - Przetwarzanie wyników przez GPT-4
   - Generowanie opisu (możliwa edycja przez użytkownika)
   - Generowanie tagów na podstawie zaakceptowanego opisu

2. **System FAQ**:
   - Przechowywanie pytań i odpowiedzi w pliku JSON
   - Wyszukiwanie podobnych pytań za pomocą embeddings
   - Generowanie odpowiedzi przez GPT-4, jeśli nie znaleziono wystarczająco podobnego pytania

## Instrukcje Wdrożenia

### Wymagania
- Python 3.8+
- Konto AWS z dostępem do Rekognition
- Konto OpenAI z dostępem do GPT-4

### Instalacja
1. Sklonuj repozytorium
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Utwórz plik `.env` z kluczami:
   ```
   OPENAI_API_KEY=twój_klucz_openai
   AWS_ACCESS_KEY_ID=twój_klucz_aws
   AWS_SECRET_ACCESS_KEY=twój_klucz_aws
   AWS_DEFAULT_REGION=region
   ```
4. Uruchom aplikację:
   ```bash
   streamlit run app/main.py
   ```

## Funkcjonalności

- Automatyczne zmniejszanie i kompresja zdjęć do limitu AWS Rekognition (5 MB)
- Generowanie opisu zdjęcia przez GPT-4 na podstawie etykiet z Rekognition
- Możliwość edycji i poprawiania opisu przez użytkownika
- Generowanie tagów na podstawie zaakceptowanego opisu (dopiero po akceptacji)
- FAQ z wyszukiwaniem podobnych pytań przez embeddings i fallbackiem do GPT-4
- Logowanie błędów do pliku `data/app.log`
- Prosty, nowoczesny interfejs w Streamlit

## Plan rozwoju

- **Skalowalność i wydajność**
  - Migracja do architektury serverless (AWS Lambda)
  - Implementacja systemu kolejkowania zadań
  - Dodanie cache'owania wyników i optymalizacja kosztów API

- **Rozszerzenie funkcjonalności**
  - Obsługa wielu zdjęć jednocześnie
  - Generowanie alternatywnych opisów i tagów
  - System sugestii tagów
  - Eksport wyników do różnych formatów (PDF, CSV, TXT)
  - Historia analiz i panel użytkownika

- **Ulepszenia interfejsu**
  - Migracja z Streamlit do React dla produkcyjnego UI
  - Responsywny design i tryb ciemny/jasny
  - Panel administracyjny

- **Integracja z bazą danych**
  - Migracja FAQ i historii analiz do AWS DynamoDB
  - System użytkowników i uprawnień
  - Statystyki użycia

- **Zaawansowane funkcje AI**
  - Wykrywanie twarzy i emocji
  - Rozpoznawanie tekstu na zdjęciach (OCR)
  - Generowanie alt-text dla dostępności
  - Automatyczne kategoryzowanie zdjęć

- **Bezpieczeństwo i monitoring**
  - Implementacja autentykacji i autoryzacji
  - Szyfrowanie danych
  - Logowanie i monitoring
  - System alertów

- **API i integracje**
  - REST API dla zewnętrznych integracji
  - Webhooki dla powiadomień
  - Integracja z systemami CMS

## Integracja Komponentów
Po wdrożeniu planowanych funkcjonalności i integracji z bazą FAQ, system zapewni kompleksową analizę obrazów z wykorzystaniem wszystkich dostępnych źródeł informacji:

### Pełna Analiza Obrazu
- **Analiza Wizualna przez AWS Rekognition**:
  - Szczegółowa detekcja obiektów i scen
  - Identyfikacja osób i ich liczby (planowane)
  - Analiza emocji i gestów (planowane)
  - Wykrywanie tekstu w obrazach (planowane)

- **Generowanie Opisu przez LLM**:
  - Naturalny, kontekstowy opis sceny
  - Możliwość edycji i dostosowania opisu przez użytkownika
  - Automatyczna korekta i ulepszanie opisów (planowane)
  - Wielojęzyczne opisy (planowane)

- **System Tagowania**:
  - Automatyczne generowanie tagów na podstawie analizy
  - Inteligentne sugestie tagów bazujące na kontekście
  - Hierarchiczna kategoryzacja tagów
  - System popularności i trendów tagów

### Integracja z Bazą Wiedzy FAQ
- **Automatyczne Powiązania**:
  - Generowanie kontekstowych pytań na podstawie wykrytych elementów
  - Dynamiczne łączenie tagów z odpowiednimi sekcjami FAQ
  - Proaktywne sugestie powiązanych informacji

- **Wzbogacanie Analizy**:
  - Dodawanie kontekstowej wiedzy dziedzinowej
  - Łączenie podobnych przypadków i analiz
  - Uczenie się na podstawie historycznych analiz
  - Personalizowane sugestie na podstawie preferencji użytkownika

### Końcowa Synteza przez LLM
- **Integracja Źródeł**:
  - Łączenie wyników analizy wizualnej z wiedzą z FAQ
  - Generowanie spójnej, kompleksowej analizy
  - Kontekstualne wykorzystanie wszystkich dostępnych informacji
  - Adaptacyjne dostosowanie poziomu szczegółowości

### Korzyści dla Użytkownika
- **Natychmiastowa Analiza**:
  - Szybkie przetwarzanie i analiza obrazów
  - Automatyczne generowanie wszystkich potrzebnych informacji
  - Możliwość interaktywnej modyfikacji wyników

- **Kontekstowa Wiedza**:
  - Dostęp do powiązanych informacji z bazy wiedzy
  - Automatyczne sugestie i podpowiedzi
  - Personalizowane rekomendacje

- **Spójna Prezentacja**:
  - Przejrzysty i intuicyjny interfejs
  - Hierarchiczna organizacja informacji
  - Możliwość dostosowania widoku do preferencji

- **Głębokie Zrozumienie**:
  - Kompleksowa analiza zawartości obrazu
  - Kontekstowe powiązania z bazą wiedzy
  - Możliwość eksploracji powiązanych tematów
  - Ciągłe uczenie się i doskonalenie systemu

## Ograniczenia Obecnego Rozwiązania
1. Ograniczenia dokładności analizy obrazów przez AWS Rekognition
2. Koszty związane z użyciem API
3. Brak systemu użytkowników i historii analiz
4. Brak zaawansowanego panelu administracyjnego
5. Brak eksportu wyników do plików

## Testowanie
1. Uruchom aplikację lokalnie
2. Prześlij przykładowe zdjęcie (JPG, JPEG, PNG, max 5 MB)
3. Sprawdź generowany opis, popraw go jeśli chcesz, zaakceptuj i wygeneruj tagi
4. Zadaj pytania do FAQ i sprawdź odpowiedzi
5. Sprawdź plik `data/app.log` w razie błędów

## Kontakt
W przypadku pytań lub sugestii, proszę o kontakt przez system rekrutacyjny.
