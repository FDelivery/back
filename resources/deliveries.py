import mongoengine
from flask_restful import Resource
from database.models.Delivery import Delivery
from flask import Response, request
from flask_jwt_extended import jwt_required, get_current_user

# TODO: plan end-points and resource needed
# TODO: validate args (marshmallow?)

"""
cancel/delete delivery - need to make sure only the user whom added the delivery can delete it
"""


class Deliveries(Resource):


    def get(self, delivery_id: str):
        delivery = Delivery.objects(id=delivery_id).first_or_404('Delivery not found').to_json()
        return delivery, 200

    @jwt_required
    def put(self, delivery_id: str):
        req_body = request.get_json()
        delivery = Delivery.objects(id=delivery_id).update_one(req_body)
        return Response(delivery.id, mimetype="application/json", status=204)

    def delete(self, delivery_id: str):
        """ delete an delivery """
        pass


class DeliveriesList(Resource):
    def get(self):
        """ :return: json list of all deliveriesRef query from url query params"""
        args = request.args
        deliveries = Delivery.objects(**args).to_json()
        if not deliveries:
            return Response({'error': 'data not found'}, status=400)
        else:
            return Response(deliveries, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        """
        post a delivery to DB
        :return: id of new post delivery
        """
        user = get_current_user()  # get user object from jwt
        body = request.get_json()
        delivery = Delivery(**body, srcAddress=user.address)
        delivery = delivery.save()
        user.deliveriesRef.append(delivery)
        user.save()
        return str(delivery.id), 200