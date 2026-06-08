import unittest
import sys

class Library:
    def __init__(self):
        self.books = {}  # isbn -> {'title': title, 'author': author, 'is_borrowed': False}
        self.users = {}  # user_id -> {'name': name, 'borrowed_books': set()}

    # 1. Dodawanie książki
    def add_book(self, title, author, isbn):
        if not title or not author:
            return "Błąd: Brak tytułu lub autora."
        if isbn in self.books:
            return "Błąd: Książka z tym ISBN już istnieje."
        self.books[isbn] = {'title': title, 'author': author, 'is_borrowed': False}
        return "Sukces: Książka dodana."

    # 2. Rejestracja użytkownika
    def register_user(self, name, user_id):
        if not name:
            return "Błąd: Imię nie może być puste."
        if not isinstance(user_id, str) or len(user_id) < 3:
            return "Błąd: Nieprawidłowy format ID."
        if user_id in self.users:
            return "Błąd: Użytkownik o tym ID już istnieje."
        self.users[user_id] = {'name': name, 'borrowed_books': set()}
        return "Sukces: Użytkownik zarejestrowany."

    # 3. Wypożyczanie książki
    def borrow_book(self, user_id, isbn):
        if user_id not in self.users:
            return "Błąd: Użytkownik nie istnieje."
        if isbn not in self.books:
            return "Błąd: Książka nie istnieje."
        if self.books[isbn]['is_borrowed']:
            return "Błąd: Książka jest już wypożyczona."
        
        self.books[isbn]['is_borrowed'] = True
        self.users[user_id]['borrowed_books'].add(isbn)
        return "Sukces: Książka wypożyczona."

    # 4. Zwracanie książki
    def return_book(self, user_id, isbn):
        if user_id not in self.users:
            return "Błąd: Użytkownik nie istnieje."
        if isbn not in self.books:
            return "Błąd: Książka nie istnieje."
        if isbn not in self.users[user_id]['borrowed_books']:
            return "Błąd: Użytkownik nie posiada tej książki."
        
        self.books[isbn]['is_borrowed'] = False
        self.users[user_id]['borrowed_books'].remove(isbn)
        return "Sukces: Książka zwrócona."

    # 5. Wyszukiwanie książki
    def search_book(self, search_term):
        if not search_term:
            return []
        term = search_term.lower()
        results = []
        for isbn, info in self.books.items():
            if term in info['title'].lower():
                results.append(info['title'])
        return results

# TESTY JEDNOSTKOWE

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.lib = Library()

    def test_add_book_success(self):
        self.assertEqual(self.lib.add_book("Wiedźmin", "Sapkowski", "111"), "Sukces: Książka dodana.")
    def test_add_book_duplicate(self):
        self.lib.add_book("Wiedźmin", "Sapkowski", "111")
        self.assertEqual(self.lib.add_book("Inna", "Autor", "111"), "Błąd: Książka z tym ISBN już istnieje.")
    def test_add_book_empty_title(self):
        self.assertEqual(self.lib.add_book("", "Sapkowski", "222"), "Błąd: Brak tytułu lub autora.")
    def test_add_book_empty_author(self):
        self.assertEqual(self.lib.add_book("Wiedźmin", "", "222"), "Błąd: Brak tytułu lub autora.")

    def test_register_user_success(self):
        self.assertEqual(self.lib.register_user("Jan", "U001"), "Sukces: Użytkownik zarejestrowany.")
    def test_register_user_duplicate(self):
        self.lib.register_user("Jan", "U001")
        self.assertEqual(self.lib.register_user("Anna", "U001"), "Błąd: Użytkownik o tym ID już istnieje.")
    def test_register_user_empty_name(self):
        self.assertEqual(self.lib.register_user("", "U002"), "Błąd: Imię nie może być puste.")
    def test_register_user_invalid_id(self):
        self.assertEqual(self.lib.register_user("Jan", "12"), "Błąd: Nieprawidłowy format ID.")

    def test_borrow_book_success(self):
        self.lib.add_book("Hobbit", "Tolkien", "123")
        self.lib.register_user("Jan", "U001")
        self.assertEqual(self.lib.borrow_book("U001", "123"), "Sukces: Książka wypożyczona.")
    def test_borrow_book_user_not_found(self):
        self.lib.add_book("Hobbit", "Tolkien", "123")
        self.assertEqual(self.lib.borrow_book("U999", "123"), "Błąd: Użytkownik nie istnieje.")
    def test_borrow_book_book_not_found(self):
        self.lib.register_user("Jan", "U001")
        self.assertEqual(self.lib.borrow_book("U001", "999"), "Błąd: Książka nie istnieje.")
    def test_borrow_book_already_borrowed(self):
        self.lib.add_book("Hobbit", "Tolkien", "123")
        self.lib.register_user("Jan", "U001")
        self.lib.register_user("Anna", "U002")
        self.lib.borrow_book("U001", "123")
        self.assertEqual(self.lib.borrow_book("U002", "123"), "Błąd: Książka jest już wypożyczona.")

    def test_return_book_success(self):
        self.lib.add_book("Hobbit", "Tolkien", "123")
        self.lib.register_user("Jan", "U001")
        self.lib.borrow_book("U001", "123")
        self.assertEqual(self.lib.return_book("U001", "123"), "Sukces: Książka zwrócona.")
    def test_return_book_not_borrowed_by_user(self):
        self.lib.add_book("Hobbit", "Tolkien", "123")
        self.lib.register_user("Jan", "U001")
        self.assertEqual(self.lib.return_book("U001", "123"), "Błąd: Użytkownik nie posiada tej książki.")
    def test_return_book_user_not_found(self):
        self.assertEqual(self.lib.return_book("U999", "123"), "Błąd: Użytkownik nie istnieje.")
    def test_return_book_book_not_found(self):
        self.lib.register_user("Jan", "U001")
        self.assertEqual(self.lib.return_book("U001", "999"), "Błąd: Książka nie istnieje.")

    def test_search_book_exact_match(self):
        self.lib.add_book("Dziady", "Mickiewicz", "111")
        self.assertEqual(self.lib.search_book("Dziady"), ["Dziady"])
    def test_search_book_partial_match(self):
        self.lib.add_book("Pan Tadeusz", "Mickiewicz", "222")
        self.assertEqual(self.lib.search_book("Tadeusz"), ["Pan Tadeusz"])
    def test_search_book_case_insensitive(self):
        self.lib.add_book("Krzyżacy", "Sienkiewicz", "333")
        self.assertEqual(self.lib.search_book("krzyżacy"), ["Krzyżacy"])
    def test_search_book_no_match(self):
        self.lib.add_book("Lalka", "Prus", "444")
        self.assertEqual(self.lib.search_book("Harry Potter"), [])

# MENU INTERAKTYWNE 

def main_menu():
    lib = Library()
    print("Witaj w Systemie Bibliotecznym!")
    
    while True:
        print("\n--- MENU GŁÓWNE ---")
        print("1. Dodaj książkę")
        print("2. Zarejestruj czytelnika")
        print("3. Wypożycz książkę")
        print("4. Zrób zwrot książki")
        print("5. Szukaj książki")
        print("6. Zakończ program")
        
        wybor = input("Wybierz opcję (1-6): ")
        
        if wybor == '1':
            tytul = input("Podaj tytuł: ")
            autor = input("Podaj autora: ")
            isbn = input("Podaj ISBN: ")
            print(">>", lib.add_book(tytul, autor, isbn))
        elif wybor == '2':
            imie = input("Podaj imię: ")
            user_id = input("Podaj ID czytelnika (np. U001): ")
            print(">>", lib.register_user(imie, user_id))
        elif wybor == '3':
            user_id = input("Podaj ID czytelnika: ")
            isbn = input("Podaj ISBN książki: ")
            print(">>", lib.borrow_book(user_id, isbn))
        elif wybor == '4':
            user_id = input("Podaj ID czytelnika: ")
            isbn = input("Podaj ISBN książki do zwrotu: ")
            print(">>", lib.return_book(user_id, isbn))
        elif wybor == '5':
            fraza = input("Podaj tytuł (lub fragment) do wyszukania: ")
            wyniki = lib.search_book(fraza)
            if wyniki:
                print(">> Znalezione książki:", ", ".join(wyniki))
            else:
                print(">> Brak wyników.")
        elif wybor == '6':
            print("Zamykanie systemu. Do widzenia!")
            break
        else:
            print(">> Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == '__main__':
    # Jeśli uruchomisz z flagą --test, odpala testy, w innym wypadku menu
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        sys.argv = sys.argv[:1]
        unittest.main()
    else:
        main_menu()