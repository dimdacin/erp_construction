# init_db.py
from database import Base, engine
from models import * # Importe toutes les classes que vous avez définies

def create_all_tables():
    print("Tentative de création de toutes les tables dans la base de données...")
    # Base.metadata.create_all lit tous les modèles importés et crée les tables
    Base.metadata.create_all(bind=engine)
    print("SUCCESS: Toutes les tables de l'ERP ont été créées avec succès!")

if __name__ == "__main__":
    create_all_tables()