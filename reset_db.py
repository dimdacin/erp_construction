# reset_db.py
# Script pour supprimer TOUTES les tables et les recréer avec le bon schéma

from database import Base, engine
from models import *  # Importe tous les modèles

def reset_database():
    """Supprime toutes les tables puis les recrée."""
    print("⚠️  ATTENTION : Suppression de TOUTES les tables...")
    
    # Supprime toutes les tables
    Base.metadata.drop_all(bind=engine)
    print("✅ Toutes les tables ont été supprimées.")
    
    # Recrée toutes les tables
    print("🔄 Recréation de toutes les tables avec le nouveau schéma...")
    Base.metadata.create_all(bind=engine)
    print("✅ SUCCESS: Toutes les tables ont été recréées avec le bon schéma!")

if __name__ == "__main__":
    confirmation = input("⚠️  ATTENTION : Cette opération supprimera TOUTES vos données. Continuer ? (oui/non) : ")
    if confirmation.lower() in ['oui', 'yes', 'o', 'y']:
        reset_database()
    else:
        print("❌ Opération annulée.")
