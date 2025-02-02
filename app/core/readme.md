# Core Configuration Guide

This directory contains core application configurations, including database setup, security settings, and other fundamental components.

## Database Configuration

The application supports multiple database backends through SQLAlchemy. Default configuration is for PostgreSQL, but SQLite and MySQL are also supported.

### SQLite Configuration

SQLite is great for development and testing due to its simplicity and zero-configuration nature.

1. Install requirements (none needed, SQLite is included in Python)

2. Configure .env file:
```env
DB_TYPE=sqlite
DB_NAME=./sql_app.db    # Path where the SQLite file will be created
```

Other database settings (DB_USER, DB_PASSWORD, etc.) can be omitted for SQLite.

### MySQL Configuration

MySQL is a good choice for production when you need a robust, full-featured database but prefer MySQL over PostgreSQL.

1. Install the MySQL driver:
```bash
pip install pymysql
```

2. Configure .env file:
```env
DB_TYPE=mysql
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fastapi_template
```

3. Create the database:
```sql
CREATE DATABASE fastapi_template CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Database Migration Notes

When using different databases, some SQL operations might need adjustment:

#### SQLite Limitations
- No ALTER TABLE DROP COLUMN support
- Limited ALTER TABLE functionality
- No DATETIME with timezone support

To handle these limitations in migrations:
```python
# In your Alembic migration file
from alembic import op
import sqlalchemy as sa
from sqlalchemy import engine_from_config
from alembic import context

def upgrade():
    # Get database type
    config = context.config
    url = config.get_main_option("sqlalchemy.url")
    is_sqlite = url.startswith('sqlite')

    # Handle different databases
    if is_sqlite:
        # SQLite-specific code
        with op.batch_alter_table('table_name') as batch_op:
            batch_op.add_column(sa.Column('new_column', sa.Integer()))
    else:
        # Code for other databases
        op.add_column('table_name', sa.Column('new_column', sa.Integer()))
```

#### MySQL Considerations
- Use utf8mb4 character set for full UTF-8 support
- Consider using InnoDB engine for transaction support
- Timestamp columns default to CURRENT_TIMESTAMP

### Connection Pooling

Connection pooling is configured automatically based on the database type:
- SQLite: No pooling (not needed)
- MySQL/PostgreSQL: QueuePool with:
  - pool_size=5
  - max_overflow=10
  - pool_timeout=30

You can adjust these in database.py if needed.

### Performance Monitoring

To enable SQL query logging, set in .env:
```env
DB_ECHO_LOG=True
```

This will log all SQL queries to help with debugging and performance optimization.