from flask_restplus import Resource, Namespace
from eshiBlood.models.models import DonationCenter
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import donationCenter, donationCenterSchema

donation_center_ns = Namespace('donation-centers')


@donation_center_ns.route('/<int:id>')
class DonationCenterResource(Resource):
    @donation_center_ns.expect(donationCenter)
    def get(self,id):
        '''
        Show a single donation center
        '''
        data = DonationCenter.query.filter_by(DonationCenterId=id).first()
        print(data)
        return donationCenterSchema.dump([data])

    @donation_center_ns.expect(donationCenter)
    def put(self, id):
        '''
        Updates an appointment
        '''
        result = DonationCenter.query.filter_by(DonationCenterId=id).first()
        payload = api.payload
        result.Address = payload["Address"]
        result.DonationCenterName=payload["DonationCenterName"]
        result.Status= payload["Status"]
        result.AppointmentDescription = payload["AppointmentDescription"]

        return donationCenterSchema.dump([result])

@donation_center_ns.route('')
class DonationCentersResource(Resource):
    def get(self):
        '''
        Show all donation centers
        '''
        data = DonationCenter.query.all()
        return donationCenterSchema.dump(data)

    @donation_center_ns.expect(donationCenter)
    def post(self):
        '''
        Creates a donation center
        '''
        payload = api.payload
        newDonationCenter = DonationCenter(
            DonationCenterName=payload["DonationCenterName"],
            Status=payload["Status"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow()
        )
        db.session.add(newDonationCenter)
        db.session.commit()
        return {"message":"donation center created successfully"}, 201