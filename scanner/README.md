# Instalacja
1. Zainstaluj chromedriver podążając za instrukcjami dla Twojegu systemu ze strony https://chromedriver.chromium.org/getting-started
2. wejdź do katalogu `scanner` i zainstaluj wymagane biblioteki
    ```
    cd scanner/
    pip install -r requirements.txt
    ```

# Używanie 
Skrypt uruchom komendą
```
python xssscanner.py
```

Wczyta on listę event handlerów a pliku `events.txt` i wyśle do serwera żądanie z takim payloadem:
```
http://localhost/?name=<input {event}=alert(1)>
```
gdzie {event} zostanie zastąpione innym event handlerem podczas każdej iteracji. Dokładne działanie jest opisane wewnątrz skryptu komentarzami.

Skrypt możesz zmodyfikować i użyć w swojej pracy.