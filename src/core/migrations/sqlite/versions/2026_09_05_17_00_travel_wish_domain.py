"""travel wish domain

Revision ID: e8f91a2b3c4d
Revises: 102813a5499d
Create Date: 2026-09-05 17:00:00.000000

"""

from alembic import op

revision = "e8f91a2b3c4d"
down_revision = "102813a5499d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE travel_wish (
            ref_id INTEGER NOT NULL,
            version INTEGER NOT NULL,
            archived BOOLEAN NOT NULL,
            created_time DATETIME NOT NULL,
            last_modified_time DATETIME NOT NULL,
            archived_time DATETIME,
            name VARCHAR(100) NOT NULL,
            vacation_collection_ref_id INTEGER NOT NULL,
            archival_reason VARCHAR,
            CONSTRAINT pk_travel_wish PRIMARY KEY (ref_id),
            CONSTRAINT fk_travel_wish_vacation_collection_ref_id_vacation_collection
                FOREIGN KEY (vacation_collection_ref_id) REFERENCES vacation_collection (ref_id)
        )
        """
    )

    op.execute(
        """
        CREATE INDEX ix_travel_wish_vacation_collection_ref_id
            ON travel_wish (vacation_collection_ref_id)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX ix_travel_wish_vacation_collection_ref_id")
    op.execute("DROP TABLE travel_wish")
