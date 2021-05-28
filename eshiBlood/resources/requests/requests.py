from flask_restplus import Resource, Namespace
from eshiBlood.models.models import Appointment, BloodType, Request
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import requestSchema, request

request_ns = Namespace('requests')

@request_ns.route('/<int:id>')
class RequestResource(Resource):
    @request_ns.expect(request)
    def get(self,id):
        '''
        Show single request
        '''
        data = Request.query.filter_by(RequestId=id).first()
        print(data)
        return requestSchema.dump([data])

    @request_ns.expect(request)
    def put(self,id):
        '''
        Updates a request
        '''
        updateRequest= Request.query.filter_by(RequestId=id).first()
        payload=api.payload
        updateRequest.UnitsNeeded=payload["UnitsNeeded"]
        updateRequest.RequestReason=payload["RequestReason"]
        updateRequest.TotalDonation=payload["TotalDonation"]
        updateRequest.Status=payload["Status"]
        updateRequest.UpdatedAt=datetime.utcnow()        
        db.session.commit()
        return {"message":"Ok"}

@request_ns.route('')
class RequestsResource(Resource):
    def get(self):
        '''
        Show all requests
        '''
        data = Request.query.all()
        return requestSchema.dump(data)

    @request_ns.expect(request)
    def post(self):
        '''
        Creates new request
        '''
        payload = api.payload
        newRequest= Request(
            UnitsNeeded=payload["UnitsNeeded"],
            RequestReason=payload["RequestReason"],
            TotalDonation=payload["TotalDonation"],
            Status=payload["Status"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow()
        )
        db.session.add(newRequest)
        db.session.commit()
        return {"message":"Request created successfully"}, 201
