# Uruchomienie
Do uruchomienia serwera najlepiej wykorzystać dockera.
```
cd server/
docker build -t xss .
docker run --rm -p 80:80 --name xss xss
```

Serwer będzie dostępny pod adresem `http://localhost/`.

# Działanie 
Serwer wyświetla na stronie wartość parametru `name`. Nie jest ona kodowana, więc serwer jest podatny na ataki XSS, jednak filtry pozwalają jedynie na użycie tagu `<input>` i tylko niektórych event handlerów. 


Zadaniem jest efektywne zidentyfikowanie, które event handlery nie są blokowane, a mogą być wykorzystane do ataku XSS.
