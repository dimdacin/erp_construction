# reset_db.py
# Script pour réinitialiser complètement la base de données
"""
Ce script permet de :
1. Supprimer toutes les tables existantes
2. Recréer toutes les tables selon les modèles définis
3. Optionnellement, insérer des données de test

ATTENTION : Ce script supprime TOUTES les données de la base de données !
Utilisez-le uniquement en développement ou après avoir fait une sauvegarde.
"""

from database import engine, Base
from models import *
import sys

def reset_database(drop_all=True, create_all=True):
    """
    Réinitialise la base de données.
    
    Args:
        drop_all: Si True, supprime toutes les tables existantes
        create_all: Si True, crée toutes les tables selon les modèles
    """
    try:
        if drop_all:
            print("⚠️  Suppression de toutes les tables existantes...")
            Base.metadata.drop_all(bind=engine)
            print("✅ Toutes les tables ont été supprimées.")
        
        if create_all:
            print("🔨 Création de toutes les tables...")
            Base.metadata.create_all(bind=engine)
            print("✅ Toutes les tables ont été créées avec succès.")
            
            # Afficher la liste des tables créées
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"\n📋 Tables créées ({len(tables)}):")
            for table in sorted(tables):
                print(f"   - {table}")
        
        print("\n✅ Réinitialisation de la base de données terminée avec succès !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("  RÉINITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print("\n⚠️  ATTENTION : Cette opération va supprimer toutes les données !")
    
    # Demander confirmation
    confirmation = input("\nÊtes-vous sûr de vouloir continuer ? (oui/non): ").strip().lower()
    
    if confirmation in ['oui', 'o', 'yes', 'y']:
        success = reset_database()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("❌ Opération annulée.")
        sys.exit(0)

