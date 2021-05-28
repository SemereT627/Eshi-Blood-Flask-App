"""Initial Migration

Revision ID: 25460ca5b2be
Revises: 
Create Date: 2021-05-27 15:34:57.183719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25460ca5b2be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Address',
    sa.Column('AddressId', sa.Integer(), nullable=False),
    sa.Column('State', sa.String(length=30), nullable=True),
    sa.Column('City', sa.String(length=30), nullable=True),
    sa.Column('SubCity', sa.String(length=30), nullable=True),
    sa.Column('Woreda', sa.String(length=30), nullable=True),
    sa.Column('Kebele', sa.String(length=30), nullable=True),
    sa.Column('Zone', sa.String(length=30), nullable=True),
    sa.Column('AddressLine', sa.String(length=30), nullable=True),
    sa.Column('PostCode', sa.String(length=30), nullable=True),
    sa.Column('PhoneNumber', sa.String(length=30), nullable=True),
    sa.Column('Email', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('AddressId')
    )
    op.create_table('BloodType',
    sa.Column('BloodTypeId', sa.Integer(), nullable=False),
    sa.Column('BloodTypeName', sa.String(length=30), nullable=True),
    sa.Column('BloodTypeDescription', sa.String(length=30), nullable=True),
    sa.Column('BloodTypeCreatedAt', sa.String(length=30), nullable=True),
    sa.Column('BloodTypeUpdatedAt', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('BloodTypeId')
    )
    op.create_table('UserCredential',
    sa.Column('UserCredentialId', sa.Integer(), nullable=False),
    sa.Column('Email', sa.String(length=30), nullable=False),
    sa.Column('Password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('UserCredentialId')
    )
    op.create_table('EmergencyContact',
    sa.Column('EmergencyContactId', sa.Integer(), nullable=False),
    sa.Column('ContactName', sa.String(length=30), nullable=True),
    sa.Column('ContactPhone', sa.String(length=30), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('EmergencyContactId')
    )
    op.create_table('Request',
    sa.Column('RequestId', sa.Integer(), nullable=False),
    sa.Column('UnitsNeeded', sa.Integer(), nullable=True),
    sa.Column('RequestReason', sa.String(length=30), nullable=True),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('RequestId')
    )
    op.create_table('User',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(length=30), nullable=False),
    sa.Column('LastName', sa.String(length=30), nullable=True),
    sa.Column('UserName', sa.String(length=30), nullable=True),
    sa.Column('BirthDate', sa.DateTime(), nullable=True),
    sa.Column('RegisteredAt', sa.DateTime(), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), nullable=True),
    sa.Column('Gender', sa.String(), nullable=True),
    sa.Column('check', sa.String(length=30), nullable=True),
    sa.Column('MartialStatus', sa.String(length=30), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('UserId')
    )
    op.create_table('DonationCenter',
    sa.Column('DonationCenterId', sa.Integer(), nullable=False),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.Column('DonationCenterName', sa.String(length=30), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('DonationCenterId')
    )
    op.create_table('Event',
    sa.Column('EventId', sa.Integer(), nullable=False),
    sa.Column('EventName', sa.String(length=30), nullable=True),
    sa.Column('EventGoal', sa.String(length=30), nullable=True),
    sa.Column('EventOrganizer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['EventOrganizer'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('EventId')
    )
    op.create_table('UserRole',
    sa.Column('UserRoleId', sa.Integer(), nullable=False),
    sa.Column('RoleName', sa.Integer(), nullable=True),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['User'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('UserRoleId')
    )
    op.create_table('Appointment',
    sa.Column('AppointmentId', sa.Integer(), nullable=False),
    sa.Column('StartDate', sa.DateTime(), nullable=True),
    sa.Column('EndDate', sa.DateTime(), nullable=True),
    sa.Column('StartTime', sa.DateTime(), nullable=True),
    sa.Column('EndTime', sa.DateTime(), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('AppointmentDescription', sa.String(length=30), nullable=True),
    sa.Column('DonationCenter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['DonationCenter'], ['DonationCenter.DonationCenterId'], ),
    sa.PrimaryKeyConstraint('AppointmentId')
    )
    op.create_table('TimeSlot',
    sa.Column('TimeSlotId', sa.Integer(), nullable=False),
    sa.Column('Weekday', sa.Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', name='weekday'), nullable=True),
    sa.Column('StartTime', sa.DateTime(), nullable=True),
    sa.Column('EndTime', sa.DateTime(), nullable=True),
    sa.Column('DonationCenter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['DonationCenter'], ['DonationCenter.DonationCenterId'], ),
    sa.PrimaryKeyConstraint('TimeSlotId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TimeSlot')
    op.drop_table('Appointment')
    op.drop_table('UserRole')
    op.drop_table('Event')
    op.drop_table('DonationCenter')
    op.drop_table('User')
    op.drop_table('Request')
    op.drop_table('EmergencyContact')
    op.drop_table('UserCredential')
    op.drop_table('BloodType')
    op.drop_table('Address')
    # ### end Alembic commands ###