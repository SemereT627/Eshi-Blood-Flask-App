"""Second Migration(Working on Models)

Revision ID: c1ee15ac7f7b
Revises: 072b6452eda6
Create Date: 2021-05-25 13:31:16.956085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1ee15ac7f7b'
down_revision = '072b6452eda6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('DonationCenter', sa.Column('Address', sa.Integer(), nullable=True))
    op.drop_constraint('DonationCenter_AddressId_fkey', 'DonationCenter', type_='foreignkey')
    op.create_foreign_key(None, 'DonationCenter', 'Address', ['Address'], ['AddressId'])
    op.drop_column('DonationCenter', 'AddressId')
    op.add_column('User', sa.Column('check', sa.String(), nullable=True))
    op.alter_column('User', 'FirstName',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('User', 'Check')
    op.add_column('UserCredential', sa.Column('UserCredentialId', sa.Integer(), nullable=False))
    op.add_column('UserCredential', sa.Column('Email', sa.String(), nullable=True))
    op.drop_column('UserCredential', 'FirstName')
    op.drop_column('UserCredential', 'UserId')
    op.add_column('UserRole', sa.Column('RoleName', sa.Integer(), nullable=True))
    op.drop_column('UserRole', 'UserRoleName')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserRole', sa.Column('UserRoleName', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('UserRole', 'RoleName')
    op.add_column('UserCredential', sa.Column('UserId', sa.INTEGER(), server_default=sa.text('nextval(\'"UserCredential_UserId_seq"\'::regclass)'), autoincrement=True, nullable=False))
    op.add_column('UserCredential', sa.Column('FirstName', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('UserCredential', 'Email')
    op.drop_column('UserCredential', 'UserCredentialId')
    op.add_column('User', sa.Column('Check', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('User', 'FirstName',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('User', 'check')
    op.add_column('DonationCenter', sa.Column('AddressId', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'DonationCenter', type_='foreignkey')
    op.create_foreign_key('DonationCenter_AddressId_fkey', 'DonationCenter', 'Address', ['AddressId'], ['AddressId'])
    op.drop_column('DonationCenter', 'Address')
    # ### end Alembic commands ###
