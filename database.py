# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Charger les variables d'environnement (y compris DATABASE_URL)
load_dotenv()

# Récupérer la chaîne de connexion de votre .env
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Créer le moteur de connexion (Engine)
# 'echo=True' est utile pour le débogage, il montre le code SQL généré
engine = create_engine(DATABASE_URL, echo=False)

# 3. Créer une session locale (LocalSession) pour les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Déclarer la base (Base) pour les modèles
Base = declarative_base()

# Fonction d'utilité pour FastAPI : fournir une session de BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()