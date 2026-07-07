# Powershell Scripts

Zbiór skryptów narzędziowych napisanych w języku PowerShell, służących do automatyzacji codziennych zadań administracyjnych, monitorowania infrastruktury. 

## 📜 Spis skryptów

### 1. SSL Monitor (`ssl_monitor.ps1`)
Monitoruje ważność certyfikatów SSL dla zdefiniowanej listy domen.
* **Działanie:** Wykorzystuje klasy `.NET` (`[Net.HttpWebRequest]`) do nawiązania połączeń i pobrania obiektu certyfikatu. Oblicza czas do wygaśnięcia i generuje odpowiednie alerty w konsoli (żółty dla <30 dni, zielony dla bezpiecznych).
* **Zastosowanie:** Proaktywne zapobieganie awariom wynikającym z wygaśnięcia certyfikatów.

### 2. Docker Janitor (`docker_janitor.ps1`)
Automatyzuje proces czyszczenia środowisk kontenerowych.
* **Działanie:** Wykonuje zapytania do CLI Dockera, filtruje obrazy typu *dangling* (porzucone) oraz zatrzymane kontenery, a następnie automatycznie zwalnia zajmowaną przez nie przestrzeń dyskową.
* **Zastosowanie:** Utrzymanie higieny na agentach CI/CD oraz maszynach deweloperskich.

### 3. System Watchdog (`system_watchdog.ps1`)
Lekki system monitoringu zasobów serwera.
* **Działanie:** Bada bieżące zużycie dysku systemowego (C:) oraz pamięci fizycznej (RAM) za pomocą instancji WMI/CIM. Jeżeli zużycie dysku spadnie poniżej 15%, skrypt generuje ostrzeżenie z możliwością łatwej integracji z Webhookami .
* **Zastosowanie:** Zastępstwo dla ciężkich systemów monitoringu (np. Zabbix) w małych projektach.

### 4. Service Checker (`service_checker.ps1`)
Asynchroniczny skaner dostępności usług i portów sieciowych.
* **Działanie:** Próbuje nawiązać połączenie TCP na określonych portach  dla listy obiektów `PSCustomObject`. Wyświetla przejrzystą tabelę ze statusem połączenia i czasem odpowiedzi (Ping).
* **Zastosowanie:** Szybka weryfikacja czy aplikacje i bazy danych wstały poprawnie po wdrożeniu infrastruktury.