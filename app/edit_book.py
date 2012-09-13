import webapp2
import jinja2
import os
import logging
import constants
from datetime import datetime, date
from models import Book
from google.appengine.api import users
from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class EditBookController(webapp2.RequestHandler):
    def get(self, book_id):
        iden = int(book_id)

        logging.info("EditBookController.get()")
        logging.info("editing book id : " + str(iden))

        user = users.get_current_user()

        if user:
           # path =

            book = db.get(db.Key.from_path('Bookshelf', user.nickname(), 'Book', iden))
            logging.info("book key : " + str(book.key()))

            template = jinja_environment.get_template('edit_book.html')
            template_values = {'book': book}
            self.response.out.write(template.render(template_values))

    def post(self):
        logging.info("Entered EditBookController.post()")
        user = users.get_current_user()

        if user:
            logging.info("Got user : " + user.nickname())
            book_id = int(self.request.get('book_id'))
            logging.info("Updating book id : " + str(book_id))

            book = db.get(db.Key.from_path('Bookshelf', user.nickname(), 'Book', book_id))
            #book = Book.get_by_id(book_id)
            if not book:
                logging.info("unable to retrieve book with id " + str(book_id))
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
            self.redirect(users.create_login_url('/books'))

