from flask_restplus import Resource, Namespace
from eshiBlood.models.models import DonationCenter
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import donationCenter, donationCenterSchema
from eshiBlood.utils.role_jwt import role_required, getTokenUserId

donation_centers_admin_ns = Namespace('admin/donation-centers')


@donation_centers_admin_ns.route('/<int:id>')
class DonationCenterResource(Resource):
    @role_required('SuperAdmin')
    @donation_centers_admin_ns.expect(donationCenter)
    def get(self, id):
        '''
        Show a single donation center
        '''
        data = DonationCenter.query.filter_by(DonationCenterId=id).first()
        print(data)
        return donationCenterSchema.dump([data])

    @role_required('SuperAdmin')
    @donation_centers_admin_ns.expect(donationCenter)
    def put(self, id):
        '''
        Updates an appointment
        '''
        result = DonationCenter.query.filter_by(DonationCenterId=id).first()
        payload = api.payload
        result.Address = payload["Address"]
        result.DonationCenterName = payload["DonationCenterName"]
        result.Status = payload["Status"]
        result.AppointmentDescription = payload["AppointmentDescription"]

        return donationCenterSchema.dump([result])

    @role_required('SuperAdmin')
    def delete(self, id):
        '''
        Deletes a request
        '''
        result = DonationCenter.query.filter_by(DonationCenterId=id).first()
        result.IsDeleted = 1
        db.session.commit()
        return {"message": "deleted successfully"}


@donation_centers_admin_ns.route('')
class DonationCentersResource(Resource):
    @role_required('SuperAdmin')
    def get(self):
        '''
        Show all donation centers
        '''
        data = DonationCenter.query.filter_by(IsDeleted=0).all()
        return donationCenterSchema.dump(data)

    @role_required('SuperAdmin')
    @donation_centers_admin_ns.expect(donationCenter)
    def post(self):
        '''
        Creates a donation center
        '''
        payload = api.payload
        newDonationCenter = DonationCenter(
            DonationCenterName=payload["DonationCenterName"],
            Status=payload["Status"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow(),
            IsDeleted=0
        )
        db.session.add(newDonationCenter)
        db.session.commit()
        return {"message": "donation center created successfully"}, 201
