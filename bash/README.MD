# 🐧 Linux Systems Automation (Bash)

Kolekcja natywnych skryptów Bash wspierających administrację systemami Linux, diagnostykę sieciową oraz zarządzanie kontenerami Docker.

## 📜 Spis skryptów

### 1. Docker Janitor (`docker_janitor.sh`)
Narzędzie do zwalniania zasobów środowiska uruchomieniowego Docker.
* **Funkcje:** * Zlicza i wyświetla liczbę zatrzymanych kontenerów (`status=exited`).
  * Raportuje aktualne zużycie dysku przez obiekty Dockera (`docker system df`).
  * Wykonuje automatyczne czyszczenie (`prune -f`), jeżeli liczba wyłączonych kontenerów przekroczy próg 5 sztuk.

### 2. Server Health Guardian (`health_check.sh`)
Skrypt monitorujący kondycję serwera z systemem ostrzegania.
* **Funkcje:**
  * Monitoruje obciążenie głównej partycji (`/`) z progiem alarmowym zdefiniowanym w zmiennej środowiskowej.
  * Analizuje użycie pamięci RAM przy pomocy polecenia `free -m`, generując alert po przekroczeniu 80% użycia.
  * Symuluje i parsuje logi aplikacyjne (`grep -c "ERROR"`), wskazując potencjalne błędy i timeouty usług.

### 3. Diagnostyka Sieci (`net_diag.sh`)
Narzędzie CLI w stylu "Scyzoryka Szwajcarskiego" do błyskawicznej weryfikacji problemów z łącznością.
* **Funkcje:**
  * Weryfikuje poprawne rozwiązywanie nazw DNS przy użyciu komendy `dig`.
  * Sprawdza domyślną trasę routingu (Gateway) (`ip route`).
  * Weryfikuje kody odpowiedzi HTTP (200, 301, 302) dla podanego adresu przy użyciu ukrytego zapytania `curl`.

### 4. Network Ports Scanner (`ports_check.sh`)
Skaner otwartych portów ułatwiający mapowanie aktywnych procesów.
* **Funkcje:**
  * Wykorzystuje narzędzie `ss` do wylistowania wszystkich nasłuchujących gniazd.
  * Za pomocą strumieniowego edytora `awk` parsuje output, wyodrębniając sam numer portu oraz powiązany z nim proces.
  * Generuje formatowaną, kolorowaną tabelę wyjściową.

### 5. SSL Certificate Expiry Checker (`ssl_expiry_checker.sh`)
Automatyczny czytnik terminów ważności certyfikatów SSL/TLS.
* **Funkcje:** * Wymusza połączenie OpenSSL z docelową domeną na porcie 443.
  * Przechwytuje i izoluje pole `notAfter` (`-enddate`), aby zwrócić surową datę wygaśnięcia certyfikatu w czytelnej formie.