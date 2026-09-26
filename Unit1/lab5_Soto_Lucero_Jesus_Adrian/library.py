class Library:
    def __init__(self):
        self.users = []
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def show_books(self):
        for book in self.books:
            print(book.show_book_info())

    def find_book(self, id_book):
        for book in self.books:
            if book.id_book == id_book:
                return book
        return None

    def find_user(self, id_user):
        for user in self.users:
            if user.id == id_user:
                return user
        return None

    def borrow_book(self, id_user, id_book):
        user = self.find_user(id_user)
        book = self.find_book(id_book)

        if not user:
            print(f"Error: User with ID '{id_user}' not found.")
            return
        if not book:
            print(f"Error: Book with ID '{id_book}' not found.")
            return

        if book.is_borrowed:
            print(f"Error: The book '{book.title}' is already borrowed.")
        else:
            book.is_borrowed = True
            print(f"Success: The book '{book.title}' has been borrowed by {user.name}.")

    def return_book(self, id_book):
        book = self.find_book(id_book)

        if not book:
            print(f"Error: Book with ID '{id_book}' not found.")
            return

        if not book.is_borrowed:
            print(f"Notice: The book '{book.title}' was not borrowed.")
        else:
            book.is_borrowed = False
            print(f"Success: The book '{book.title}' has been returned.")