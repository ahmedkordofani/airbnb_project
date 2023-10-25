import re
from datetime import datetime

class Validator:
    def validate_signup(self, email, pw, pw_confirm):
        errors = []

        if email == '' or email.isspace():
            errors.append('Email cannot be blank')
        
        elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) == None:
            errors.append('Email must be valid')

        if len(pw) < 8:
            errors.append('Password must be at least 8 characters long')
        if any(char.isdigit() for char in pw) == False:
            errors.append('Password must contain at least one number')
        if any(char.isupper() for char in pw) == False:
            errors.append('Password must contain at least one uppercase letter')
        if any(char in '!?-_+£$%*#@' for char in pw) == False:
            errors.append('Password must contain at least one special character')
        
        if pw != pw_confirm:
            errors.append('Passwords must match')
        
        return errors
    
    def validate_listing(self, title, description, price, start_date, end_date):
        errors = []

        if title == '' or title.isspace():
            errors.append('Title cannot be blank')
        
        if description == '' or description.isspace():
            errors.append('Description cannot be blank')
        
        if price < 0:
            errors.append('Price cannot be negative')

        dates_valid = True

        try:
            st_date = datetime.strptime(start_date, '%d/%m/%Y')
        except:
            errors.append('Start date must be valid')
            dates_valid = False
        
        try:
            en_date = datetime.strptime(end_date, '%d/%m/%Y')
        except:
            errors.append('End date must be valid')
            dates_valid = False

        if dates_valid:
            if en_date < st_date:
                errors.append('End date must be after start date')

            if st_date < datetime.today():
                errors.append('Start date cannot be in the past')
        
        return errors
        
