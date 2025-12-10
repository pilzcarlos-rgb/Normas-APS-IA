"""
Tests for database models.
"""

import pytest
from datetime import datetime
from src.models import init_database, Norm, Relationship, Article, Program


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine, Session = init_database(':memory:')
    session = Session()
    yield session
    session.close()


def test_norm_creation(db_session):
    """Test creating a Norm object."""
    norm = Norm(
        id_norma='TEST_PORTARIA_123_2024',
        tipo='Portaria',
        orgao='SAPS',
        numero='123',
        ano=2024,
        data_publicacao=datetime(2024, 1, 15),
        ementa='Norma de teste',
        tema_principal='financiamento',
        status_vigencia='vigente',
        fonte='bvsms'
    )
    
    db_session.add(norm)
    db_session.commit()
    
    # Retrieve and verify
    retrieved = db_session.query(Norm).filter_by(id_norma='TEST_PORTARIA_123_2024').first()
    assert retrieved is not None
    assert retrieved.tipo == 'Portaria'
    assert retrieved.numero == '123'
    assert retrieved.ano == 2024


def test_relationship_creation(db_session):
    """Test creating relationships between norms."""
    # Create two norms
    norm1 = Norm(
        id_norma='NORM_A',
        tipo='Lei',
        orgao='GM/MS',
        numero='1',
        ano=2020,
        data_publicacao=datetime(2020, 1, 1),
        ementa='Norma A',
        fonte='planalto'
    )
    
    norm2 = Norm(
        id_norma='NORM_B',
        tipo='Decreto',
        orgao='GM/MS',
        numero='2',
        ano=2021,
        data_publicacao=datetime(2021, 1, 1),
        ementa='Norma B',
        fonte='planalto'
    )
    
    db_session.add_all([norm1, norm2])
    db_session.commit()
    
    # Create relationship
    rel = Relationship(
        source_norm_id=norm2.id,
        target_norm_id=norm1.id,
        relationship_type='regulamenta',
        description='Norma B regulamenta Norma A'
    )
    
    db_session.add(rel)
    db_session.commit()
    
    # Verify
    retrieved_rel = db_session.query(Relationship).first()
    assert retrieved_rel is not None
    assert retrieved_rel.relationship_type == 'regulamenta'
    assert retrieved_rel.source_norm.id_norma == 'NORM_B'
    assert retrieved_rel.target_norm.id_norma == 'NORM_A'


def test_article_creation(db_session):
    """Test creating articles within a norm."""
    norm = Norm(
        id_norma='NORM_WITH_ARTICLES',
        tipo='Portaria',
        orgao='SAPS',
        numero='100',
        ano=2024,
        data_publicacao=datetime(2024, 1, 1),
        ementa='Norma com artigos',
        fonte='bvsms'
    )
    
    db_session.add(norm)
    db_session.commit()
    
    # Add articles
    article1 = Article(
        norm_id=norm.id,
        article_number='1',
        content='Art. 1º - Conteúdo do artigo 1',
        topic='Disposições gerais'
    )
    
    article2 = Article(
        norm_id=norm.id,
        article_number='2',
        content='Art. 2º - Conteúdo do artigo 2',
        topic='Financiamento'
    )
    
    db_session.add_all([article1, article2])
    db_session.commit()
    
    # Verify
    retrieved_norm = db_session.query(Norm).filter_by(id_norma='NORM_WITH_ARTICLES').first()
    assert len(retrieved_norm.articles) == 2
    assert retrieved_norm.articles[0].article_number == '1'


def test_program_creation(db_session):
    """Test creating a program."""
    # Create establishing norm
    norm = Norm(
        id_norma='PORTARIA_2979_2019',
        tipo='Portaria',
        orgao='GM/MS',
        numero='2979',
        ano=2019,
        data_publicacao=datetime(2019, 11, 12),
        ementa='Institui o Previne Brasil',
        tema_principal='financiamento',
        fonte='bvsms'
    )
    
    db_session.add(norm)
    db_session.commit()
    
    # Create program
    program = Program(
        name='Previne Brasil',
        description='Novo modelo de financiamento da APS',
        establishing_norm_id=norm.id,
        is_active=True,
        start_date=datetime(2020, 1, 1)
    )
    
    db_session.add(program)
    db_session.commit()
    
    # Verify
    retrieved = db_session.query(Program).filter_by(name='Previne Brasil').first()
    assert retrieved is not None
    assert retrieved.is_active is True
    assert retrieved.establishing_norm.id_norma == 'PORTARIA_2979_2019'


def test_norm_to_dict(db_session):
    """Test converting Norm to dictionary."""
    norm = Norm(
        id_norma='NORM_DICT_TEST',
        tipo='Portaria',
        orgao='SAPS',
        numero='999',
        ano=2024,
        data_publicacao=datetime(2024, 6, 1),
        ementa='Teste de conversão para dict',
        tema_principal='organizacao_aps',
        status_vigencia='vigente',
        fonte='bvsms'
    )
    
    norm_dict = norm.to_dict()
    
    assert norm_dict['id_norma'] == 'NORM_DICT_TEST'
    assert norm_dict['tipo'] == 'Portaria'
    assert norm_dict['numero'] == '999'
    assert norm_dict['ano'] == 2024
    assert norm_dict['tema_principal'] == 'organizacao_aps'
