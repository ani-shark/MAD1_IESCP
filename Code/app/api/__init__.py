from flask import Blueprint
from flask_restful import Api
from .resources import UserResource, CampaignResource, AdRequestResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(CampaignResource, '/campaigns', '/campaigns/<int:campaign_id>')
api.add_resource(AdRequestResource, '/ad_requests', '/ad_requests/<int:ad_request_id>')
