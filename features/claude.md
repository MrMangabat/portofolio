Claude Code CLI Instructions - Service Template
Interactive Development Principles
Focus on Small, Incremental Changes

Maximum 1-4 files per session
One function/method at a time
Always ask before creating new files
Show plan before implementing

Test-Driven Development Flow

Discuss Feature → Break down complexity, identify intended behavior
Write Tests → Define expected behavior in executable tests
Implement Code → Write minimal code to pass tests
Human Review → User reviews and approves before moving on

Compliance Handling

NEVER auto-implement compliance code
Add TODO comments for compliance considerations
Flag when personal data is involved but let human decide implementation
Compliance requires human oversight and understanding

Example:
pythondef process_user_data(user_id):
    # TODO: GDPR consideration - processing personal data
    # TODO: Add audit logging after human review of requirements
    # Human must understand GDPR implications before implementation
    return process_data(user_id)

EXACT Directory Structure
service_{domain}/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies/
│   │   ├── middleware/
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── requests/
│   │   │   │   ├── __init__.py
│   │   │   └── responses/
│   │   │       ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   ├── compliance/
│   │   ├── __init__.py
│   │   ├── gdpr/
│   │   │   └── __init__.py
│   │   ├── nis2/
│   │   │   └── __init__.py
│   │   ├── ai_act/
│   │   │   └── __init__.py
│   │   └── audit/
│   │       └── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base_config.py
│   │   ├── security_config.py
│   │   ├── compliance_config/
│   │   │   ├── __init__.py
│   │   │   ├── gdpr/
│   │   │   │   └── __init__.py
│   │   │   ├── nis2/
│   │   │   │   └── __init__.py
│   │   │   └── ai_act/
│   │   │       └── __init__.py
│   │   ├── database_config/
│   │   │   ├── __init__.py
│   │   │   ├── postgresql/
│   │   │   │   └── __init__.py
│   │   │   ├── neo4j/
│   │   │   │   └── __init__.py
│   │   │   ├── redis/
│   │   │   │   └── __init__.py
│   │   │   └── qdrant/
│   │   │       └── __init__.py
│   │   ├── logging_config.py
│   │   └── environment/
│   │       ├── __init__.py
│   ├── core_business_logic/
│   │   └── __init__.py
│   │
│   ├── database_integrations/
│   │   ├── __init__.py
│   │   ├── postgresql/
│   │   │   └── __init__.py
│   │   ├── neo4j/
│   │   │   └── __init__.py
│   │   ├── redis/
│   │   │   └── __init__.py
│   │   └── qdrant/
│   │       └── __init__.py
│   ├── external_service_integrations/
│   │   └── __init__.py
├── messaging_integrations/
│   ├── __init__.py
│   ├── kafka/
│   │   ├── __init__.py
│   │   ├── producer/
│   │   │   ├── __init__.py
│   │   │   ├── base_producer.py        # Common producer functionality
│   │   │   ├── user_event_producer.py  # User-related events
│   │   │   ├── audit_producer.py       # Compliance audit events
│   │   │   └── notification_producer.py # Notification events
│   │   ├── consumer/
│   │   │   ├── __init__.py
│   │   │   ├── base_consumer.py        # Common consumer functionality
│   │   │   ├── user_event_consumer.py  # Processes user events
│   │   │   ├── audit_consumer.py       # Processes audit events
│   │   │   └── notification_consumer.py # Processes notifications
│   │   └── event_handlers/
│   │       ├── __init__.py
│   │       ├── base_handler.py         # Common handler functionality
│   │       ├── user_handlers.py        # User event processing logic
│   │       ├── audit_handlers.py       # Audit event processing logic
│   │       └── notification_handlers.py # Notification processing logic
│   └── event_store.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── database/
│   │       ├── __init__.py
│   │       ├── postgresql/
│   │       │   ├── __init__.py
│   │       ├── neo4j/
│   │       │   ├── __init__.py
│   │       ├── redis/
│   │       │   ├── __init__.py
│   │       └── qdrant/
│   │           ├── __init__.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   ├── postgresql/
│   │   │   ├── __init__.py
│   │   ├── neo4j/
│   │   │   ├── __init__.py
│   │   ├── redis/
│   │   │   ├── __init__.py
│   │   └── qdrant/
│   │       ├── __init__.py
│   ├── security/
│   │   └── __init__.py
│   │
│   ├── monitoring/
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       ├── validation/
│       │   └── __init__.py
│       ├── exceptions/
│       │   └── __init__.py
│       ├── decorators/
│       │   └── __init__.py
│       ├── date_utils/
│       │   └── __init__.py
│       └── process_mining/
│           └── __init__.py
├── notebooks/                          # ADD THIS
│   ├── __init__.py
│   ├── exploratory/                    # Data exploration, prototyping
│   │   └── __init__.py
│   ├── analysis/                       # Data analysis, insights
│   │   └── __init__.py
│   ├── experiments/                    # A/B tests, feature experiments
│   │   └── __init__.py
│   └── documentation/                  # Process documentation, tutorials
│       └── __init__.py
├── tests/
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── compliance/
│   │   ├── gdpr_assessment.md
│   │   ├── nis2_compliance.md
│   │   └── ai_act_conformity.md
│   └── security/
│       ├── security_policy.md
│       └── threat_model.md
├── deployment_infrastructure/
├── scripts/
├── migrations/
├── .env.example
├── .gitignore
├── .dockerignore
├── pyproject.toml
├── requirements-dev.txt
├── Makefile
├── README.md
└── api_{domain}_main.py

Essential Directory Explanations
Key Development Locations:

src/api/routes/ - HTTP endpoint implementations
src/api/schemas/requests|responses/ - API request/response models
src/core_business_logic/ - Business workflows and rules
src/repositories/{database_type}/ - Data access (CRUD operations)
src/models/database/{database_type}/ - Database schema definitions
src/external_service_integrations/ - Third-party API clients
src/config/ - Configuration settings and parameters

Database Selection Guide:

PostgreSQL: Transactional business data, user accounts, financial data
Neo4j: Relationships, social graphs, recommendations, network analysis
Redis: Sessions, caching, rate limiting, temporary data, fast lookups
Qdrant: Vector embeddings, semantic search, ML features, similarity matching

File Naming Conventions:

Services: {purpose}_service.py (e.g., user_registration_service.py)
Repositories: {entity}_repository.py (e.g., user_repository.py)
Models: {entity}_models.py (e.g., user_models.py)
Routes: {domain}_routes.py (e.g., user_routes.py)
Producers: {domain}_producer.py (e.g., user_event_producer.py)
Consumers: {domain}_consumer.py (e.g., user_event_consumer.py)
Event Handlers: {domain}_handlers.py (e.g., user_handlers.py)


Development Decision Tree
For ANY new functionality, ask:

HTTP endpoint? → src/api/routes/
Request/response model? → src/api/schemas/
Business logic? → src/core_business_logic/
Data access? → src/repositories/{database_type}/
Database schema? → src/models/database/{database_type}/
External API? → src/external_service_integrations/
Configuration? → src/config/
Personal data involved? → FLAG for human review (add TODO comments)
AI/ML feature? → FLAG for human review (add TODO comments)


Critical Instructions for Claude Code
ALWAYS:

Ask which service the user is working on
Show implementation plan before generating code (max 1-4 files)
Check existing files before creating new ones
Follow this directory structure exactly
Generate tests alongside implementation when requested
Use verbose, descriptive naming
Add comprehensive docstrings explaining purpose and reasoning
FLAG compliance considerations with TODO comments for human review

NEVER:

Auto-implement compliance code without explicit human instruction
Generate more than 4 files in single session
Mix API models with database models
Put business logic in repositories
Create files outside this structure
Skip the test-first approach when user requests TDD