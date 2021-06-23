# Repozytorium
Repozytorium składa się z dwóch części:
* serwera, który jest podatny na ataki XSS
* skanera, który jest w stanie tego XSSa wykryć.

Zostało stworzony na potrzeby webinara [Hackowanie na Ekranie - Czy bezpiecznik musi programować?](https://youtu.be/E5fmivf1XBU), który rozpoczynał przedsprzedaż kursu "Python dla Bezpieczników". Możesz kupić go w przedsprzedaży w świetniej cenie 299PLN - tak tanio już nigdy nie będzie!

Zapoznaj się ze szczegółami na https://szkolasecurity.pl/python



# Serwer
## Uruchomienie
Do uruchomienia serwera najlepiej wykorzystać dockera.
```
cd server/
docker build -t xss .
docker run --rm -p 80:80 --name xss xss
```

Serwer będzie dostępny pod adresem `http://localhost/`.

## Działanie 
Serwer wyświetla na stronie wartość parametru `name`. Nie jest ona kodowana, więc serwer jest podatny na ataki XSS, jednak filtry pozwalają jedynie na użycie tagu `<input>` i tylko niektórych event handlerów. 


Zadaniem jest efektywne zidentyfikowanie, które event handlery nie są blokowane, a mogą być wykorzystane do ataku XSS.

# Skaner XSS
## Instalacja
1. Zainstaluj chromedriver podążając za instrukcjami dla Twojegu systemu ze strony https://chromedriver.chromium.org/getting-started
2. wejdź do katalogu `scanner` i zainstaluj wymagane biblioteki
    ```
    cd scanner/
    pip install -r requirements.txt
    ```

## Używanie 
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