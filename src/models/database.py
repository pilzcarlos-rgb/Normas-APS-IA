"""
Database models for the APS Normative Graph System.

This module defines the core data structures for storing and managing
Brazilian Primary Health Care regulations and their relationships.
"""

from sqlalchemy import (
    Column, Integer, String, Text, Date, Boolean, 
    ForeignKey, Table, JSON, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


# Association table for many-to-many relationships between norms
norm_relationships = Table(
    'norm_relationships',
    Base.metadata,
    Column('source_id', Integer, ForeignKey('norms.id'), primary_key=True),
    Column('target_id', Integer, ForeignKey('norms.id'), primary_key=True),
    Column('relationship_type', String(50), nullable=False),
    Column('notes', Text),
    Column('created_at', Date, default=datetime.now)
)


class Norm(Base):
    """
    Represents a normative document in the APS regulatory framework.
    
    Nodes in the normative graph include:
    - Constitution, laws, complementary laws, decrees
    - GM/MS and SAPS ordinances
    - Consolidation ordinances (critical for completeness)
    - CIT resolutions (when structuring for APS)
    - Technical notes and operational manuals
    """
    __tablename__ = 'norms'
    
    # Primary identification
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_norma = Column(String(100), unique=True, nullable=False, index=True)
    
    # Type and classification
    tipo = Column(String(100), nullable=False)  # Lei, Decreto, Portaria, etc.
    orgao = Column(String(100), nullable=False)  # GM/MS, SAPS, etc.
    numero = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False, index=True)
    data_publicacao = Column(Date, nullable=False, index=True)
    
    # Content
    ementa = Column(Text, nullable=False)
    texto_completo = Column(Text)
    
    # Classification
    tema_principal = Column(String(100), index=True)
    temas_secundarios = Column(JSON)  # List of additional themes
    
    # Status
    status_vigencia = Column(
        String(50), 
        nullable=False, 
        default='vigente',
        index=True
    )  # vigente, revogada, alterada_parcial
    
    # Financial effects
    efeitos_financeiros_partir_de = Column(Date)
    
    # URLs for reference
    url_html = Column(String(500))
    url_pdf = Column(String(500))
    
    # Metadata
    fonte = Column(String(100))  # planalto, bvsms, etc.
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)
    
    # Relationships - norms this one affects
    altera = relationship(
        'Norm',
        secondary=norm_relationships,
        primaryjoin=id == norm_relationships.c.source_id,
        secondaryjoin=id == norm_relationships.c.target_id,
        backref='alterada_por',
        foreign_keys=[norm_relationships.c.source_id, norm_relationships.c.target_id]
    )
    
    def __repr__(self):
        return f"<Norm {self.tipo} {self.numero}/{self.ano} - {self.orgao}>"
    
    def to_dict(self):
        """Convert to dictionary for JSON export."""
        return {
            'id_norma': self.id_norma,
            'tipo': self.tipo,
            'orgao': self.orgao,
            'numero': self.numero,
            'ano': self.ano,
            'data_publicacao': self.data_publicacao.isoformat() if self.data_publicacao else None,
            'ementa': self.ementa,
            'tema_principal': self.tema_principal,
            'temas_secundarios': self.temas_secundarios,
            'status_vigencia': self.status_vigencia,
            'efeitos_financeiros_partir_de': self.efeitos_financeiros_partir_de.isoformat() if self.efeitos_financeiros_partir_de else None,
            'url_html': self.url_html,
            'url_pdf': self.url_pdf,
            'fonte': self.fonte
        }


class Relationship(Base):
    """
    Represents relationships between normative documents.
    
    Relationship types:
    - institui: creates or establishes
    - altera: modifies
    - revoga: revokes
    - regulamenta: regulates
    - consolida: consolidates
    - efeitos_financeiros: financial effects from
    """
    __tablename__ = 'relationships'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_norm_id = Column(Integer, ForeignKey('norms.id'), nullable=False)
    target_norm_id = Column(Integer, ForeignKey('norms.id'), nullable=False)
    relationship_type = Column(String(50), nullable=False, index=True)
    
    # Additional context
    description = Column(Text)
    article_reference = Column(String(100))  # Which article establishes this relationship
    
    # Metadata
    created_at = Column(Date, default=datetime.now)
    
    # Relationships to norm objects
    source_norm = relationship('Norm', foreign_keys=[source_norm_id], backref='outgoing_relationships')
    target_norm = relationship('Norm', foreign_keys=[target_norm_id], backref='incoming_relationships')
    
    def __repr__(self):
        return f"<Relationship {self.relationship_type}: {self.source_norm_id} -> {self.target_norm_id}>"
    
    def to_dict(self):
        """Convert to dictionary for JSON export."""
        return {
            'source_norm_id': self.source_norm_id,
            'target_norm_id': self.target_norm_id,
            'relationship_type': self.relationship_type,
            'description': self.description,
            'article_reference': self.article_reference
        }


class Article(Base):
    """
    Represents individual articles or sections within a normative document.
    Useful for granular analysis and Q&A generation.
    """
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    norm_id = Column(Integer, ForeignKey('norms.id'), nullable=False)
    
    # Article identification
    article_number = Column(String(50))
    section_number = Column(String(50))
    annex_number = Column(String(50))
    
    # Content
    content = Column(Text, nullable=False)
    
    # Classification
    topic = Column(String(200))
    
    # Relationship to norm
    norm = relationship('Norm', backref='articles')
    
    def __repr__(self):
        return f"<Article {self.article_number} of Norm {self.norm_id}>"


class Program(Base):
    """
    Represents specific programs with their own regulatory ecosystem.
    Examples: Previne Brasil, PMAQ, Informatiza APS
    """
    __tablename__ = 'programs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text)
    
    # Main establishing norm
    establishing_norm_id = Column(Integer, ForeignKey('norms.id'))
    establishing_norm = relationship('Norm', backref='established_programs')
    
    # Status
    is_active = Column(Boolean, default=True)
    start_date = Column(Date)
    end_date = Column(Date)
    
    def __repr__(self):
        return f"<Program {self.name}>"


def init_database(db_path='data/normas_aps.db'):
    """
    Initialize the database with all tables.
    
    Args:
        db_path: Path to SQLite database file
    
    Returns:
        engine, Session: SQLAlchemy engine and session maker
    """
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session


if __name__ == '__main__':
    # Create database with all tables
    engine, Session = init_database()
    print("Database initialized successfully!")
    print(f"Tables created: {', '.join(Base.metadata.tables.keys())}")
