import webapp2
import jinja2
import os
import logging
from datetime import datetime, date
import constants
from models import Book
from edit_book import EditBookController
from delete_book import DeleteBookController
from google.appengine.api import users
from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

def bookshelf_key(bookshelf_name=None):
    """
    Constructs a Datastore key for a Book entity with bookshelf_name.
    """
    return db.Key.from_path('Bookshelf', bookshelf_name or 'default_bookself')

class BooksController(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:

            books = db.GqlQuery("SELECT * FROM Book WHERE ANCESTOR IS :1",
                    bookshelf_key(user.nickname()))

            template_values = {
                'books': books,
                'user': user
            }
            template = jinja_environment.get_template('book_list.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()

        if user:
            # gather ip the pieces of data
            bookshelf_name = user.nickname()
            book = Book(parent=bookshelf_key(bookshelf_name))

            book.username = user.nickname()
            book.title = self.request.get('title')
            book.author = self.request.get('author')
            if self.request.get('in_series') == constants.CHECKED:
                book.in_series = True
            else:
                book.in_series = False
            book.series_name = self.request.get('series_name')
            try:
                book.book_in_series = int(self.request.get('book_in_series'))
            except:
                book.book_in_series = None
            book.isbn = self.request.get('isbn')
            try:
                book.pub_year = int(self.request.get('pub_year'))
            except:
                book.pub_year = None
            if self.request.get('was_it_read') == constants.CHECKED:
                book.was_read = True
            else:
                book.was_read = False
            try:
                cdt = datetime.strptime(self.request.get('date_read'), '%m/%d/%Y')
                cd = date(cdt.year, cdt.month, cdt.day)
                book.completed_date = cd
            except Exception, e:
                logging.info("exception getting read date : " + str(e))
                book.completed_date = None

            book.put()

            self.redirect('/books')

        else:
            self.redirect(users.create_login_url(self.request.uri))

class AddBookController(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('add_book.html')
        template_values = {}
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', BooksController),
    ('/books', BooksController),
    ('/books/add', AddBookController),
	('/books/edit', EditBookController),
    ('/books/edit/([\d]+)', EditBookController),
    ('/books/delete/([\d]+)', DeleteBookController)
    ],
    debug=True)
