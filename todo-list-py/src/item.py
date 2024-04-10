from datetime import datetime


class Item:
    # ATTRIBUTES
    def __init__(self, description=None, id=None, done=False, date=None):
        # NEW ITEM CONSTRUCTOR
        if description is not None:
            self.description = description
            self.done = done
            self.date = date if date is not None else datetime.now().date()
            self.id = id
        else:
            raise ValueError("DESCRIPTION CANNOT BE EMPTY.")

    # METHODS
    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def is_done(self):
        return self.done

    def get_date(self):
        return self.date
