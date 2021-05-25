"""Initial Migration

Revision ID: 072b6452eda6
Revises: 
Create Date: 2021-05-21 15:25:10.682803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '072b6452eda6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Address',
    sa.Column('AddressId', sa.Integer(), nullable=False),
    sa.Column('State', sa.String(), nullable=True),
    sa.Column('City', sa.String(), nullable=True),
    sa.Column('SubCity', sa.String(), nullable=True),
    sa.Column('Woreda', sa.String(), nullable=True),
    sa.Column('Kebele', sa.String(), nullable=True),
    sa.Column('Zone', sa.String(), nullable=True),
    sa.Column('AddressLine', sa.String(), nullable=True),
    sa.Column('PostCode', sa.String(), nullable=True),
    sa.Column('PhoneNumber', sa.String(), nullable=True),
    sa.Column('Email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('AddressId')
    )
    op.create_table('BloodType',
    sa.Column('BloodTypeId', sa.Integer(), nullable=False),
    sa.Column('BloodTypeName', sa.String(), nullable=True),
    sa.Column('BloodTypeDescription', sa.String(), nullable=True),
    sa.Column('BloodTypeCreatedAt', sa.String(), nullable=True),
    sa.Column('BloodTypeUpdatedAt', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('BloodTypeId')
    )
    op.create_table('UserCredential',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(), nullable=True),
    sa.Column('PhoneNumber', sa.String(), nullable=True),
    sa.Column('Password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('UserId')
    )
    op.create_table('EmergencyContact',
    sa.Column('EmergencyContactId', sa.Integer(), nullable=False),
    sa.Column('ContactName', sa.String(), nullable=True),
    sa.Column('ContactPhone', sa.String(), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('EmergencyContactId')
    )
    op.create_table('Request',
    sa.Column('RequestId', sa.Integer(), nullable=False),
    sa.Column('UnitsNeeded', sa.Integer(), nullable=True),
    sa.Column('RequestReason', sa.String(), nullable=True),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('RequestId')
    )
    op.create_table('User',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(), nullable=True),
    sa.Column('LastName', sa.String(), nullable=True),
    sa.Column('UserName', sa.String(), nullable=True),
    sa.Column('BirthDate', sa.Date(), nullable=True),
    sa.Column('RegisteredAt', sa.Date(), nullable=True),
    sa.Column('CreatedAt', sa.Date(), nullable=True),
    sa.Column('UpdatedAt', sa.Date(), nullable=True),
    sa.Column('Gender', sa.Enum('Male', 'Female', name='gender'), nullable=True),
    sa.Column('Check', sa.String(), nullable=True),
    sa.Column('MartialStatus', sa.Enum('Single', 'Married', name='martialstatus'), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('UserId')
    )
    op.create_table('DonationCenter',
    sa.Column('DonationCenterId', sa.Integer(), nullable=False),
    sa.Column('AddressId', sa.Integer(), nullable=True),
    sa.Column('DonationCenterName', sa.String(), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AddressId'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('DonationCenterId')
    )
    op.create_table('Event',
    sa.Column('EventId', sa.Integer(), nullable=False),
    sa.Column('EventName', sa.String(), nullable=True),
    sa.Column('EventGoal', sa.String(), nullable=True),
    sa.Column('EventOrganizer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['EventOrganizer'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('EventId')
    )
    op.create_table('UserRole',
    sa.Column('UserRoleId', sa.Integer(), nullable=False),
    sa.Column('UserRoleName', sa.Integer(), nullable=True),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['User'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('UserRoleId')
    )
    op.create_table('Appointment',
    sa.Column('AppointmentId', sa.Integer(), nullable=False),
    sa.Column('StartDate', sa.Date(), nullable=True),
    sa.Column('EndDate', sa.Date(), nullable=True),
    sa.Column('StartTime', sa.Date(), nullable=True),
    sa.Column('EndTime', sa.Date(), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('AppointmentDescription', sa.String(), nullable=True),
    sa.Column('DonationCenter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['DonationCenter'], ['DonationCenter.DonationCenterId'], ),
    sa.PrimaryKeyConstraint('AppointmentId')
    )
    op.create_table('TimeSlot',
    sa.Column('TimeSlotId', sa.Integer(), nullable=False),
    sa.Column('Weekday', sa.Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', name='weekday'), nullable=True),
    sa.Column('StartTime', sa.Date(), nullable=True),
    sa.Column('EndTime', sa.Date(), nullable=True),
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