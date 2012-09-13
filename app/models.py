from google.appengine.ext import db

class Book(db.Model):
    username = db.StringProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    in_series = db.BooleanProperty()
    series_name = db.StringProperty()
    book_in_series = db.IntegerProperty()
    isbn = db.StringProperty()
    pub_year = db.IntegerProperty()
    was_read = db.BooleanProperty()
    completed_date = db.DateProperty()

    def get_formatted_completed_date(self):
        if self.completed_date:
            return self.completed_date.strftime('%m/%d/%Y')
        else:
            return ""
