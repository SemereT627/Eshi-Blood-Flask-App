"""Initial migration

Revision ID: d5b21e47db73
Revises: 
Create Date: 2021-06-01 01:59:09.388690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b21e47db73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Address',
    sa.Column('AddressId', sa.Integer(), nullable=False),
    sa.Column('State', sa.String(), nullable=True),
    sa.Column('City', sa.String(), nullable=True),
    sa.Column('Woreda', sa.String(), nullable=True),
    sa.Column('Kebele', sa.String(), nullable=True),
    sa.Column('Zone', sa.String(), nullable=True),
    sa.Column('AddressLine', sa.String(), nullable=True),
    sa.Column('PostCode', sa.String(), nullable=True),
    sa.Column('PhoneNumber', sa.String(), nullable=True),
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
    sa.Column('UserCredentialId', sa.Integer(), nullable=False),
    sa.Column('Email', sa.String(), nullable=False),
    sa.Column('Password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('UserCredentialId')
    )
    op.create_table('UserRole',
    sa.Column('UserRoleId', sa.Integer(), nullable=False),
    sa.Column('RoleName', sa.Enum('SuperAdmin', 'Admin', 'Donor', 'Nurse', name='role'), nullable=True),
    sa.PrimaryKeyConstraint('UserRoleId')
    )
    op.create_table('EmergencyContact',
    sa.Column('EmergencyContactId', sa.Integer(), nullable=False),
    sa.Column('ContactName', sa.String(), nullable=True),
    sa.Column('ContactPhone', sa.String(), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.PrimaryKeyConstraint('EmergencyContactId')
    )
    op.create_table('User',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(), nullable=False),
    sa.Column('LastName', sa.String(), nullable=True),
    sa.Column('UserName', sa.String(), nullable=True),
    sa.Column('Gender', sa.Enum('Male', 'Female', name='gender'), nullable=True),
    sa.Column('BirthDate', sa.DateTime(), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=True),
    sa.Column('MartialStatus', sa.Enum('Single', 'Married', name='martialstatus'), nullable=True),
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.Column('UserCredential', sa.Integer(), nullable=True),
    sa.Column('UserRole', sa.Integer(), nullable=True),
    sa.Column('EmergencyContact', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.ForeignKeyConstraint(['EmergencyContact'], ['EmergencyContact.EmergencyContactId'], ),
    sa.ForeignKeyConstraint(['UserCredential'], ['UserCredential.UserCredentialId'], ),
    sa.ForeignKeyConstraint(['UserRole'], ['UserRole.UserRoleId'], ),
    sa.PrimaryKeyConstraint('UserId')
    )
    op.create_table('DonationCenter',
    sa.Column('DonationCenterId', sa.Integer(), nullable=False),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.Column('DonationCenterName', sa.String(), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('UpdatedBy', sa.Integer(), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['UpdatedBy'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('DonationCenterId'),
    sa.UniqueConstraint('UpdatedBy'),
    sa.UniqueConstraint('UpdatedBy')
    )
    op.create_table('Event',
    sa.Column('EventId', sa.Integer(), nullable=False),
    sa.Column('EventName', sa.String(), nullable=True),
    sa.Column('EventGoal', sa.String(), nullable=True),
    sa.Column('EventOrganizer', sa.Integer(), nullable=True),
    sa.Column('TotalDonations', sa.Integer(), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['EventOrganizer'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('EventId')
    )
    op.create_table('Request',
    sa.Column('RequestId', sa.Integer(), nullable=False),
    sa.Column('UnitsNeeded', sa.Integer(), nullable=True),
    sa.Column('RequestReason', sa.String(), nullable=True),
    sa.Column('TotalDonation', sa.Integer(), nullable=True),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=True),
    sa.Column('CreatedBy', sa.Integer(), nullable=True),
    sa.Column('Address', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Address'], ['Address.AddressId'], ),
    sa.ForeignKeyConstraint(['CreatedBy'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('RequestId')
    )
    op.create_table('Appointment',
    sa.Column('AppointmentId', sa.Integer(), nullable=False),
    sa.Column('Status', sa.Enum('Active', 'Pending', 'Closed', name='status'), nullable=True),
    sa.Column('AppointmentDescription', sa.String(), nullable=True),
    sa.Column('DonationCenter', sa.Integer(), nullable=True),
    sa.Column('Discriminator', sa.String(), nullable=True),
    sa.Column('DiscriminatorId', sa.Integer(), nullable=True),
    sa.Column('User', sa.Integer(), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('UpdatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['DonationCenter'], ['DonationCenter.DonationCenterId'], ),
    sa.ForeignKeyConstraint(['User'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('AppointmentId')
    )
    op.create_table('Request_BloodType_Association',
    sa.Column('BloodType', sa.Integer(), nullable=True),
    sa.Column('Request', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['BloodType'], ['BloodType.BloodTypeId'], ),
    sa.ForeignKeyConstraint(['Request'], ['Request.RequestId'], )
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
    op.create_table('DonationHistory',
    sa.Column('DonationCenterId', sa.Integer(), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=True),
    sa.Column('AppointmentId', sa.Integer(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('NurseId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['AppointmentId'], ['Appointment.AppointmentId'], ),
    sa.ForeignKeyConstraint(['NurseId'], ['User.UserId'], ),
    sa.ForeignKeyConstraint(['UserId'], ['User.UserId'], ),
    sa.PrimaryKeyConstraint('DonationCenterId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DonationHistory')
    op.drop_table('TimeSlot')
    op.drop_table('Request_BloodType_Association')
    op.drop_table('Appointment')
    op.drop_table('Request')
    op.drop_table('Event')
    op.drop_table('DonationCenter')
    op.drop_table('User')
    op.drop_table('EmergencyContact')
    op.drop_table('UserRole')
    op.drop_table('UserCredential')
    op.drop_table('BloodType')
    op.drop_table('Address')
    # ### end Alembic commands ###