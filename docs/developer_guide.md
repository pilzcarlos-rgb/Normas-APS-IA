# Developer Documentation

## System Architecture

### Overview
The APS Normative Graph System is designed with modularity and extensibility in mind. It consists of several independent components that can be used separately or together.

### Components

#### 1. Data Models (`src/models/`)
SQLAlchemy-based ORM models for the normative database.

**Key Classes:**
- `Norm`: Represents a normative document
- `Relationship`: Represents relationships between norms
- `Article`: Individual articles within norms
- `Program`: APS programs with their regulatory ecosystem

**Usage:**
```python
from src.models import init_database, Norm

# Initialize database
engine, Session = init_database()
session = Session()

# Create a new norm
norm = Norm(
    id_norma='PORTARIA_123_2024',
    tipo='Portaria',
    orgao='SAPS',
    numero='123',
    ano=2024,
    # ... other fields
)
session.add(norm)
session.commit()
```

#### 2. Scrapers (`src/scrapers/`)
Web scraping tools for data collection following the 3-layer strategy.

**Layer 1: BVSMSScraper**
Broad temporal sweep of BVSMS for years 2010-2025.

```python
from src.scrapers import BVSMSScraper

scraper = BVSMSScraper()
results = scraper.scrape(start_year=2020, end_year=2024)
scraper.save_to_jsonl(results, 'output.jsonl')
```

**Layer 2: ConsolidationParser**
Parses consolidation ordinances to extract cited norms.

```python
from src.scrapers import ConsolidationParser

parser = ConsolidationParser()
results = parser.scrape()
```

**Layer 3: ProgramScraper**
Specialized collection for programs with extensive micro-legislation.

```python
from src.scrapers import ProgramScraper

scraper = ProgramScraper()
program_data = scraper.scrape_program('previne_brasil')
```

#### 3. Utilities (`src/utils/`)

**QualityChecker**
Validates completeness and consistency of the normative collection.

```python
from src.utils import QualityChecker

checker = QualityChecker(norms_list)
report = checker.run_all_checks()
print(f"Quality score: {report['quality_score']}%")
```

**NormativeGraph**
Graph analysis tools for relationship mapping.

```python
from src.utils import build_graph_from_norms

graph = build_graph_from_norms(norms_list)
active = graph.find_active_norms()
revoked = graph.find_revoked_norms()
path = graph.find_shortest_path('norm_a', 'norm_b')
```

#### 4. Web Portal (`src/portal/`)
Flask-based web interface for navigation and visualization.

```python
from src.portal.app import run_portal

run_portal(host='0.0.0.0', port=5000, debug=True)
```

## Database Schema

### Tables

**norms**
- Primary normative documents
- Fields: id, id_norma, tipo, orgao, numero, ano, ementa, status_vigencia, etc.
- Indexes on: ano, data_publicacao, tema_principal, status_vigencia

**relationships**
- Relationships between norms
- Fields: id, source_norm_id, target_norm_id, relationship_type, description
- Foreign keys to norms table

**articles**
- Individual articles/sections within norms
- Fields: id, norm_id, article_number, content, topic
- Foreign key to norms table

**programs**
- APS programs with regulatory ecosystems
- Fields: id, name, description, establishing_norm_id, is_active
- Foreign key to norms table

## Configuration

### config.yaml Structure

```yaml
sources:
  planalto:
    base_url: "..."
  bvsms:
    base_url: "..."
    search_terms: [...]
  key_norms: [...]

temporal_range:
  start_year: 2010
  end_year: 2025

themes: [...]
relationship_types: [...]

database:
  type: "sqlite"
  path: "data/normas_aps.db"

output:
  formats: [jsonl, sqlite, html]
  portal:
    enabled: true
    port: 5000
```

## API Endpoints

### Web Portal API

**GET /api/norms**
Query parameters:
- `theme`: Filter by theme
- `year`: Filter by year
- `status`: Filter by validity status
- `search`: Search term

Response:
```json
{
  "norms": [...],
  "total": 123
}
```

**GET /api/stats**
Response:
```json
{
  "total_norms": 500,
  "active_norms": 450,
  "revoked_norms": 50
}
```

**GET /api/graph**
Response:
```json
{
  "nodes": [...],
  "edges": [...],
  "stats": {...}
}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py
```

### Test Structure

```
tests/
├── test_models.py          # Database model tests
├── test_scrapers.py        # Scraper tests
├── test_utils.py           # Utility tests
└── test_portal.py          # Portal tests
```

## Adding New Features

### Adding a New Scraper

1. Create a new file in `src/scrapers/`
2. Inherit from `BaseScraper`
3. Implement the `scrape()` method
4. Add to `__init__.py`

Example:
```python
from .base_scraper import BaseScraper

class NewScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url='...')
    
    def scrape(self):
        # Implementation
        return results
```

### Adding a New Theme

1. Update `config.yaml` themes list
2. Add theme to database enum in `src/models/database.py`
3. Update validation in `src/utils/quality_checker.py`
4. Add theme card to portal templates

### Adding a New Relationship Type

1. Update `config.yaml` relationship_types list
2. Update graph analysis logic in `src/utils/graph_analysis.py`
3. Update visualization in portal

## Performance Considerations

### Database Optimization
- Use indexes on frequently queried fields
- Consider PostgreSQL for production
- Implement connection pooling

### Scraping Best Practices
- Respect rate limits (use `delay` parameter)
- Implement retry logic
- Cache responses when possible
- Use async scraping for large collections

### Portal Optimization
- Implement pagination for large result sets
- Cache static data
- Use CDN for static assets
- Consider Redis for session management

## Security

### Best Practices
- Never commit credentials to version control
- Use environment variables for sensitive data
- Sanitize user input in portal
- Implement CSRF protection
- Use HTTPS in production

### Data Validation
- Validate all input data against schema
- Sanitize HTML content before display
- Implement rate limiting on API endpoints

## Deployment

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up logging
- [ ] Configure HTTPS
- [ ] Set up monitoring
- [ ] Implement backup strategy
- [ ] Configure caching
- [ ] Set up error tracking

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "src.portal.app"]
```

## Troubleshooting

### Common Issues

**Database locked error**
- Use connection pooling
- Implement retry logic
- Consider PostgreSQL

**Scraping timeouts**
- Increase timeout values
- Check network connectivity
- Verify target site availability

**Memory issues with large datasets**
- Implement batch processing
- Use generators instead of lists
- Consider streaming responses

## Contributing

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small

### Commit Messages
Format: `type: description`

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Tests
- chore: Maintenance

### Pull Request Process
1. Create feature branch
2. Write tests
3. Update documentation
4. Submit PR with clear description
5. Address review comments

## Resources

### Official Sources
- [BVSMS](https://bvsms.saude.gov.br/bvs/saudelegis)
- [Planalto](http://www.planalto.gov.br)
- [Ministério da Saúde](https://www.gov.br/saude)

### Technical Documentation
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Flask Docs](https://flask.palletsprojects.com/)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
