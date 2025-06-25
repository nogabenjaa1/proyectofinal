import sys
try:
    import patch_bcrypt
except ImportError as e:
    print(f"⚠️ Error aplicando parche bcrypt: {e}", file=sys.stderr)

from app.database import SessionLocal
from app.models import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

db.query(Usuario).filter(Usuario.email == 'nogabenstudent@owner.io').delete()

hashed_password = pwd_context.hash('notbenjaa1')
db.add(Usuario(
    email='nogabenstudent@owner.io',
    hashed_password=hashed_password,
    es_admin=True
))
db.commit()
print('✅ Usuario recreado con hash bcrypt compatible')
