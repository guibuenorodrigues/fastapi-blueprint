# fastapi-blueprint
Holds the blueprint of a FastAPI project for large scale

# Content

├── .github/                     # GitHub specific configs (CI/CD, Issue Templates, etc.)
│   ├── workflows/               # GitHub Actions workflows
│   │   ├── ci.yml               # Main CI pipeline (lint, test, build)
│   │   ├── deploy-api.yml       # CD for the main API service
│   │   ├── deploy-frontend.yml  # CD for the frontend
│   │   └── release.yml          # Automated release workflows
│   └── CODEOWNERS               # Define ownership for specific parts of the codebase
│
├── config/                      # Global configuration files (e.g., for Helm, Terraform, environment config)
│   ├── environments/
│   │   ├── dev.env
│   │   ├── staging.env
│   │   └── prod.env
│   ├── logging.ini              # Centralized logging configuration
│   └── alembic.ini              # Alembic configuration
│
├── docs/                        # Project documentation (API docs, architecture, onboarding, runbooks)
│   ├── architecture/
│   │   ├── decision_records/    # ADRs (Architectural Decision Records)
│   │   └── diagrams/
│   ├── dev_setup.md
│   └── api_spec.yaml            # OpenAPI spec for external tools
│
├── scripts/                     # Utility scripts (setup, migration, maintenance, data seeding)
│   ├── local_setup.sh
│   ├── run_migrations.sh
│   ├── seed_data.py
│   └── health_check.py
│
├── src/                         # Core source code for all services/applications
│   ├── ezconstruct_app/         # Main FastAPI application (modular monolith)
│   │   ├── api/                 # FastAPI routers and endpoint definitions
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/   # Thin endpoint handlers
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── projects.py
│   │   │   │   │   ├── expenses.py
│   │   │   │   │   └── categories.py
│   │   │   │   └── __init__.py
│   │   │   └── dependencies/    # FastAPI common dependencies (e.g., get_db, get_current_user, service injections)
│   │   │   │   ├── common.py    # General dependencies (e.g., pagination)
│   │   │   │   ├── security.py  # Auth related dependencies
│   │   │   │   └── service_dependencies.py # Factory functions for injecting services
│   │   │   └── middleware/      # Custom FastAPI middleware
│   │   │   │   ├── request_logging.py
│   │   │   │   └── error_handling.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── core/                # Core application utilities, settings, and base components
│   │   │   ├── config.py        # Centralized settings management (Pydantic Settings)
│   │   │   ├── exceptions.py    # Custom application-specific exceptions
│   │   │   ├── logging.py       # Custom logging setup
│   │   │   ├── security.py      # Hashing, JWT encoding/decoding utilities (not dependencies)
│   │   │   └── __init__.py
│   │   │
│   │   ├── db/                  # Database specific configurations and models
│   │   │   ├── session.py       # Database engine and session setup
│   │   │   ├── base.py          # SQLAlchemy declarative base
│   │   │   └── __init__.py
│   │   │
│   │   ├── crud/                # **Domain-agnostic database operations**
│   │   │   ├── base.py          # Generic CRUD operations for any model
│   │   │   ├── user_crud.py     # Specific CRUD for User model
│   │   │   ├── project_crud.py
│   │   │   ├── expense_crud.py
│   │   │   ├── category_crud.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── domain/              # **Core business domain logic and models (DDD influence)**
│   │   │   ├── users/           # User-related domain objects and logic
│   │   │   │   ├── models.py    # SQLAlchemy User model (moved from app/models)
│   │   │   │   ├── schemas.py   # Pydantic schemas for User (moved from app/schemas)
│   │   │   │   └── services.py  # User-specific business logic (UserService)
│   │   │   ├── projects/        # Project-related domain objects and logic
│   │   │   │   ├── models.py    # Project SQLAlchemy model
│   │   │   │   ├── schemas.py   # Project Pydantic schemas
│   │   │   │   └── services.py  # ProjectService (budget calculations, project lifecycle)
│   │   │   ├── expenses/        # Expense-related domain objects and logic
│   │   │   │   ├── models.py    # Expense SQLAlchemy model, PaymentMethodEnum
│   │   │   │   ├── schemas.py   # Expense Pydantic schemas
│   │   │   │   └── services.py  # ExpenseService (budget checks, expense aggregations)
│   │   │   ├── categories/
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── services.py
│   │   │   ├── shared/          # Shared domain-level entities, enums, or value objects
│   │   │   │   ├── enums.py
│   │   │   │   └── util.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── main.py              # Main FastAPI application instance, router inclusion
│   │   ├── __init__.py
│   │
│   ├── background_tasks/        # Celery or other background job definitions
│   │   ├── workers.py           # Celery worker configuration
│   │   ├── tasks/               # Individual task definitions
│   │   │   ├── email_tasks.py   # Password reset emails, notifications
│   │   │   ├── receipt_processing.py # Image processing, OCR etc.
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │
│   ├── integrations/            # External service integrations (e.g., payment gateways, external APIs)
│   │   ├── s3_storage.py        # Receipt storage (AWS S3, GCP Cloud Storage)
│   │   ├── email_provider.py    # SendGrid, Mailgun etc.
│   │   ├── payment_gateway.py   # Stripe, PayPal etc.
│   │   └── __init__.py
│   │
│   ├── tests/                   # Centralized tests for all backend components
│   │   ├── unit/
│   │   │   ├── services/
│   │   │   ├── crud/
│   │   │   └── core/
│   │   ├── integration/         # Tests involving DB, services, multiple components
│   │   │   ├── api_tests.py     # FastAPI endpoint tests
│   │   │   └── db_integration.py
│   └── └── e2e/                 # End-to-end tests (requires frontend/mocks)
│
├── migrations/                  # Global Alembic migrations environment for all shared models
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                # Generated migration scripts
│       └── <timestamp>_initial_tables.py
│
├── infrastructure/              # Infrastructure as Code (IaC) - Terraform, Helm Charts
│   ├── terraform/               # Cloud infrastructure (VPC, RDS, EKS, etc.)
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── kubernetes/              # K8s manifests / Helm charts
│   │   ├── ezconstruct-api/
│   │   │   ├── values.yaml
│   │   │   └── templates/
│   │   ├── ezconstruct-workers/
│   │   └── ingress.yaml
│   └── monitoring/              # Prometheus, Grafana configurations
│       ├── prometheus.yml
│       └── grafana_dashboards/
│
├── Dockerfile                   # Main API Dockerfile
├── docker-compose.yml           # For local development orchestration
├── pyproject.toml               # Poetry config for the main FastAPI app
├── poetry.lock
├── Makefile                     # Common dev/ops commands (e.g., `make run`, `make test`, `make deploy`)
├── README.md
├── .env.example
├── .gitignore