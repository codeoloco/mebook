import webapp2
import jinja2
import os
import logging
import constants
from models import Book
from google.appengine.api import users
from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class DeleteBookController(webapp2.RequestHandler):
# not the best way to handle this. delete should be handled with post but using
# get for now.
    def get(self, book_id):
        book_id = int(book_id)

        logging.info("DeleteBookController.get()")
        logging.info("deleting book id : " + str(book_id))

        user = users.get_current_user()

        if user:
           # path =

            book = db.get(db.Key.from_path('Bookshelf', user.nickname(), 'Book', book_id))
            book.delete()

            logging.info("book deleted")

            self.redirect("/books")
        else:
            self.redirect(users.create_login_url('/books'))

