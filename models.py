# models.py
from sqlalchemy import Column, Integer, String, Numeric, Text, Date, ForeignKey, BigInteger, SmallInteger, Boolean, Enum, Time, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal
import enum
from datetime import date
from typing import Optional

# Assurez-vous d'importer Base depuis database.py dans votre structure réelle,
# ou décommentez la ligne suivante si vous exécutez ce fichier seul pour le test :
# Base = declarative_base() 
from database import Base # Utilise l'importation prévue dans votre projet

# ============================================================
# 1. RÉFÉRENTIELS (ENUMS, ORGANISATION ET SITES)
# ============================================================

# Définition des types ENUM pour la cohérence PostgreSQL
class CentreAnalytique(str, enum.Enum):
    PROD = 'PROD'
    CHANTIER = 'CHANTIER'
    ADMIN = 'ADMIN'
    LOCATION = 'LOCATION'
    
class TypeMouvement(str, enum.Enum):
    ACHAT_MP = 'ACHAT_MP'
    PRODUCTION_IN = 'PRODUCTION_IN'
    VENTE_OUT = 'VENTE_OUT'
    TRANSFERT_INTERNE = 'TRANSFERT_INTERNE'
    CONSOMMATION_CHANTIER = 'CONSOMMATION_CHANTIER'

class StatutPlanning(str, enum.Enum):
    BROUILLON = 'BROUILLON'
    VALIDE = 'VALIDE'
    ARCHIVE = 'ARCHIVE'

# 1.1 Référentiels RH
class Division(Base):
    __tablename__ = "division"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False, unique=True)
    
class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False, unique=True)
    division_id = Column(Integer, ForeignKey("division.id"))
    
class Fonction(Base):
    __tablename__ = "fonction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    code = Column(String(30))

class MotifJour(Base):
    __tablename__ = "motif_jour"
    code = Column(String(30), primary_key=True)
    libelle = Column(Text, nullable=False)
    est_productif = Column(Boolean, nullable=False)

# 1.2 Référentiel Sites (Lieu unifié)
class Site(Base):
    __tablename__ = "site"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, unique=True)
    nom = Column(Text, nullable=False)
    type_site = Column(String(20), nullable=False) # USINE, CHANTIER, DEPOT, BUREAU
    centre_analytique = Column(Enum(CentreAnalytique), nullable=False)
    
    # Informations de projet/chantier
    client_id = Column(BigInteger, ForeignKey("client.id"))
    localisation = Column(Text)
    date_debut = Column(Date)
    date_fin = Column(Date)
    chef_chantier_id = Column(BigInteger, ForeignKey("personne.id"))  # Référence au responsable
    statut = Column(String(20))  # EN_COURS, TERMINE, PLANIFIE, SUSPENDU
    
    actif = Column(Boolean, default=True)
    
    # Relations
    client = relationship("Client")
    chef_chantier = relationship("Personne", foreign_keys=[chef_chantier_id])

# 1.3 Autres Référentiels
class Produit(Base):
    __tablename__ = "produit"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    libelle = Column(Text, nullable=False)
    unite = Column(String(10), nullable=False)

class Fournisseur(Base):
    __tablename__ = "fournisseur"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom_entreprise = Column(Text, nullable=False)

class Client(Base):
    __tablename__ = "client"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nom = Column(Text, nullable=False)
    type_client = Column(String(50))  # PUBLIC, PRIVE, INSTITUTIONNEL
    contact = Column(Text)
    actif = Column(Boolean, default=True)
    
class EquipementCategorie(Base):
    __tablename__ = "equipement_categorie"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, unique=True)
    libelle = Column(Text, nullable=False)

class Activite(Base):
    __tablename__ = "activite"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, unique=True)
    libelle = Column(Text, nullable=False)
    type_activite = Column(String(30))  # PRODUCTION, MAINTENANCE, TRANSPORT, etc.

# ============================================================
# 2. RESSOURCES (PERSONNES & ÉQUIPEMENTS)
# ============================================================

class Personne(Base):
    __tablename__ = "personne"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    matricule = Column(String(30), unique=True)
    nom_prenom = Column(Text, nullable=False)
    
    # Organisation hiérarchique
    secteur = Column(String(100))  # Secteur d'activité
    
    # FKs de rattachement
    division_id = Column(Integer, ForeignKey("division.id"))
    service_id = Column(Integer, ForeignKey("service.id"))
    fonction_id = Column(Integer, ForeignKey("fonction.id"))

    # Données de Coût
    salaire_tarif = Column(Numeric(14, 2))
    accord_supplementaire = Column(Numeric(14, 2))  # Accord sup
    taux_horaire_cout = Column(Numeric(14, 2)) # Coût chargé utilisé dans les calculs
    
    actif = Column(Boolean, default=True)

class Equipement(Base):
    __tablename__ = "equipement"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True) # Ton ID_M ou équivalent
    immatriculation = Column(String(50))
    categorie_id = Column(Integer, ForeignKey("equipement_categorie.id"))
    unite_compteur = Column(String(10)) 
    usage_source = Column(String(30)) # MANUEL, OMNICOMM
    
    # Coûts Théoriques pour l'imputation
    conso_h_l = Column(Numeric(10,2))
    cout_usage_1h_lei = Column(Numeric(12,2))
    cout_usage_100km_lei = Column(Numeric(12,2))
    
    site_rattachement_id = Column(BigInteger, ForeignKey("site.id")) # Dépôt maison
    actif = Column(Boolean, default=True)

class DepenseEquipement(Base):
    __tablename__ = "depenses_equipement"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    equipement_id = Column(BigInteger, ForeignKey("equipement.id"), nullable=False)
    fournisseur_id = Column(BigInteger, ForeignKey("fournisseur.id"))
    
    date_depense = Column(Date, nullable=False)
    type_depense = Column(String(50), nullable=False) # Assurance, Pneumatiques, Réparation Capitale
    montant_ht = Column(Numeric(14, 2), nullable=False)
    description = Column(Text)
    
    fournisseur = relationship("Fournisseur")

# ============================================================
# 3. PLANNING ET AFFECTATIONS (CŒUR DE L'ACTIVITÉ)
# ============================================================

class PlanningJour(Base):
    __tablename__ = "planning_jour"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_jour = Column(Date, nullable=False)
    site_id = Column(BigInteger, ForeignKey("site.id"), nullable=False)
    statut = Column(Enum(StatutPlanning), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('date_jour', 'site_id', name='uq_planning_jour_site'),
    )

class AffectationEquipement(Base):
    __tablename__ = "affectation_equipement"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Clés d'identification de l'usage
    date_jour = Column(Date, nullable=False)
    equipement_id = Column(BigInteger, ForeignKey("equipement.id"), nullable=False)
    site_id = Column(BigInteger, ForeignKey("site.id"), nullable=False)
    
    bloc_jour = Column(SmallInteger, nullable=False, default=1) # 1 ou 2 (Matin/APM)
    
    # Clés de Traçabilité
    operateur_id = Column(BigInteger, ForeignKey("personne.id"))
    activite_id = Column(Integer, ForeignKey("activite.id"))
    motif_jour_code = Column(String(30), ForeignKey("motif_jour.code"))

    # Données saisies ou lues
    heure_jour = Column(Numeric(10, 2), default=Decimal(0.0))
    km_effectue = Column(Numeric(12, 2), default=Decimal(0.0))
    carburant_litres = Column(Numeric(12, 2), default=Decimal(0.0))
    
    # Coûts CALCULÉS
    cout_usage_calc = Column(Numeric(14, 2))
    cout_operateur_calc = Column(Numeric(14, 2))
    
    # Contrainte UNIQUE CLÉ
    __table_args__ = (
        UniqueConstraint('date_jour', 'equipement_id', 'bloc_jour', name='uq_affectation_bloc'),
    )

# ============================================================
# 4. STOCKS ET MOUVEMENTS
# ============================================================

class Stock(Base):
    __tablename__ = "stock"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    site_id = Column(BigInteger, ForeignKey("site.id"), nullable=False)
    produit_id = Column(BigInteger, ForeignKey("produit.id"), nullable=False)
    quantite = Column(Numeric(18,4), nullable=False)
    cout_unitaire_moyen = Column(Numeric(18,6), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('site_id', 'produit_id', name='uq_stock_site_produit'),
    )

class MouvementStock(Base):
    __tablename__ = "mouvement_stock"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    site_id = Column(BigInteger, ForeignKey("site.id"), nullable=False)
    produit_id = Column(BigInteger, ForeignKey("produit.id"), nullable=False)
    date_mouvement = Column(TIMESTAMP(timezone=True), nullable=False)
    type_mouvement = Column(Enum(TypeMouvement), nullable=False)
    quantite = Column(Numeric(18,4), nullable=False)
    
    centre_analytique = Column(Enum(CentreAnalytique), nullable=False)
    equipement_id = Column(BigInteger, ForeignKey("equipement.id"))