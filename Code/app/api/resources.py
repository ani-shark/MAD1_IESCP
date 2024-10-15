from flask_restful import Resource, reqparse
from flask_login import current_user, login_required
from app.models import User, Campaign, AdRequest
from app import db

class SecureResource(Resource):
    method_decorators = [login_required]

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')
user_parser.add_argument('role', type=str, required=True, help='Role is required')

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}

    def post(self):
        args = user_parser.parse_args()
        user = User(username=args['username'], email=args['email'], password=args['password'], role=args['role'])
        db.session.add(user)
        db.session.commit()
        return {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}, 201

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        args = user_parser.parse_args()
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        user.role = args['role']
        db.session.commit()
        return {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument('name', type=str, required=True, help='Name is required')
campaign_parser.add_argument('description', type=str, required=True, help='Description is required')
campaign_parser.add_argument('start_date', type=str, required=True, help='Start date is required')
campaign_parser.add_argument('end_date', type=str, required=True, help='End date is required')
campaign_parser.add_argument('budget', type=float, required=True, help='Budget is required')
campaign_parser.add_argument('visibility', type=str, required=True, help='Visibility is required')
campaign_parser.add_argument('category', type=str, required=True, help='Category is required')
campaign_parser.add_argument('goals', type=str, required=True, help='Goals are required')

class CampaignResource(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        return {'id': campaign.id, 'name': campaign.name, 'description': campaign.description, 'start_date': campaign.start_date, 'end_date': campaign.end_date, 'budget': campaign.budget, 'visibility': campaign.visibility, 'category': campaign.category, 'goals': campaign.goals}

    def post(self):
        args = campaign_parser.parse_args()
        campaign = Campaign(name=args['name'], description=args['description'], start_date=args['start_date'], end_date=args['end_date'], budget=args['budget'], visibility=args['visibility'], category=args['category'], goals=args['goals'])
        db.session.add(campaign)
        db.session.commit()
        return {'id': campaign.id, 'name': campaign.name, 'description': campaign.description, 'start_date': campaign.start_date, 'end_date': campaign.end_date, 'budget': campaign.budget, 'visibility': campaign.visibility, 'category': campaign.category, 'goals': campaign.goals}, 201

    def put(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        args = campaign_parser.parse_args()
        campaign.name = args['name']
        campaign.description = args['description']
        campaign.start_date = args['start_date']
        campaign.end_date = args['end_date']
        campaign.budget = args['budget']
        campaign.visibility = args['visibility']
        campaign.category = args['category']
        campaign.goals = args['goals']
        db.session.commit()
        return {'id': campaign.id, 'name': campaign.name, 'description': campaign.description, 'start_date': campaign.start_date, 'end_date': campaign.end_date, 'budget': campaign.budget, 'visibility': campaign.visibility, 'category': campaign.category, 'goals': campaign.goals}

    def delete(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        db.session.delete(campaign)
        db.session.commit()
        return '', 204

ad_request_parser = reqparse.RequestParser()
ad_request_parser.add_argument('campaign_id', type=int, required=True, help='Campaign ID is required')
ad_request_parser.add_argument('influencer_id', type=int, required=True, help='Influencer ID is required')
ad_request_parser.add_argument('messages', type=str, required=True, help='Messages are required')
ad_request_parser.add_argument('requirements', type=str, required=True, help='Requirements are required')
ad_request_parser.add_argument('payment_amount', type=float, required=True, help='Payment amount is required')
ad_request_parser.add_argument('status', type=str, required=True, help='Status is required')

class AdRequestResource(Resource):
    def get(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        return {'id': ad_request.id, 'campaign_id': ad_request.campaign_id, 'influencer_id': ad_request.influencer_id, 'messages': ad_request.messages, 'requirements': ad_request.requirements, 'payment_amount': ad_request.payment_amount, 'status': ad_request.status}

    def post(self):
        args = ad_request_parser.parse_args()
        ad_request = AdRequest(campaign_id=args['campaign_id'], influencer_id=args['influencer_id'], messages=args['messages'], requirements=args['requirements'], payment_amount=args['payment_amount'], status=args['status'])
        db.session.add(ad_request)
        db.session.commit()
        return {'id': ad_request.id, 'campaign_id': ad_request.campaign_id, 'influencer_id': ad_request.influencer_id, 'messages': ad_request.messages, 'requirements': ad_request.requirements, 'payment_amount': ad_request.payment_amount, 'status': ad_request.status}, 201

    def put(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        args = ad_request_parser.parse_args()
        ad_request.campaign_id = args['campaign_id']
        ad_request.influencer_id = args['influencer_id']
        ad_request.messages = args['messages']
        ad_request.requirements = args['requirements']
        ad_request.payment_amount = args['payment_amount']
        ad_request.status = args['status']
        db.session.commit()
        return {'id': ad_request.id, 'campaign_id': ad_request.campaign_id, 'influencer_id': ad_request.influencer_id, 'messages': ad_request.messages, 'requirements': ad_request.requirements, 'payment_amount': ad_request.payment_amount, 'status': ad_request.status}

    def delete(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        db.session.delete(ad_request)
        db.session.commit()
        return '', 204
