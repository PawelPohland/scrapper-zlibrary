class Library:
    def __init__(self):
        # contains all books (with or without isbn)
        self._books = []

        # contains mapping: book_isbn ==> book_index
        # where: book_isbn is book's isbn number
        # and book_index is index from self._books
        self._books_isbn = {}

    @property
    def books(self):
        return self._books

    @books.setter
    def books(self, book):
        self.add_book(book)

    # returns index of book in library or -1 if the book cannot be find
    def find_book(self, book):
        # if book has isbn and is already in library
        if book.isbn and self._books_isbn.get(book.isbn):
            return self._books_isbn.get(book.isbn)

        # book doesn't have isbn or it's a new book
        # search for possible duplicates
        for index, library_book in enumerate(self._books):
            if library_book == book:
                return index

        # book not found
        return -1

    # add book to library
    def add_book(self, book):
        index = self.find_book(book)

        if index != -1:
            self._books[index].add_file(book)
        else:
            self._books.append(book)
            index = len(self._books) - 1

        if book.isbn and not self._books_isbn.get(book.isbn):
            self._books_isbn[book.isbn] = index

    def print_books(self):
        for book in self._books:
            book.print()

    def serialize(self):
        return [book.serialize() for book in self._books]

    def clear_books(self):
        self._books.clear()
        self._books_isbn.clear()

    def count(self):
        return len(self._books)
