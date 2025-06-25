import bcrypt
import passlib.handlers.bcrypt

if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('obj', (object,), {'__version__': '4.1.2'})
passlib.handlers.bcrypt._bcrypt = bcrypt

