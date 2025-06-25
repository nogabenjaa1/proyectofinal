import bcrypt
import passlib.handlers.bcrypt
import sys

if not hasattr(bcrypt, '__about__'):
    class FakeAbout:
        __version__ = '4.1.2'
    bcrypt.__about__ = FakeAbout()

# Reforzar backend de passlib
passlib.handlers.bcrypt._bcrypt = bcrypt

print("✅ Parche bcrypt aplicado permanentemente", file=sys.stderr)