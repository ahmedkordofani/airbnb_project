import re

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

        
