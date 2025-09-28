"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision if down_revision else None}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql  # needed if autogen uses JSONB/UUID/ARRAY, etc.

# revision identifiers, used by Alembic.
revision = '${up_revision}'
down_revision = ${repr(down_revision) if down_revision is not None else 'None'}
branch_labels = ${repr(branch_labels) if branch_labels is not None else 'None'}
depends_on = ${repr(depends_on) if depends_on is not None else 'None'}


def upgrade() -> None:
    ${upgrades if upgrades else 'pass'}


def downgrade() -> None:
    ${downgrades if downgrades else 'pass'}
