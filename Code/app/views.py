from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import AdRequestForm, CampaignForm, RegistrationForm, LoginForm, SearchInfluencerForm, NegotiateAdRequestForm, SearchPublicCampaignForm, UpdateSponsorProfileForm, UpdateInfluencerProfileForm
from .models import db, User, Sponsor, Influencer, Admin, Campaign, AdRequest, Conversation, Message
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('landing.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        if form.role.data == 'sponsor':
            sponsor = Sponsor(user_id=user.id)
            db.session.add(sponsor)
        elif form.role.data == 'influencer':
            influencer = Influencer(user_id=user.id)
            db.session.add(influencer)
        db.session.commit()
        flash('Your account has been created! Please complete your profile.', 'success')
        if form.role.data == 'sponsor':
            return redirect(url_for('main.complete_sponsor_profile'))
        elif form.role.data == 'influencer':
            return redirect(url_for('main.update_influencer_profile'))

    return render_template('register.html', form=form)

@main.route('/complete_sponsor_profile', methods=['GET', 'POST'])
@login_required
def complete_sponsor_profile():
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    form = UpdateSponsorProfileForm()
    if form.validate_on_submit():
        sponsor = Sponsor.query.filter_by(user_id=current_user.id).first_or_404()
        sponsor.name = form.name.data
        sponsor.company_name = form.company_name.data
        sponsor.industry = form.industry.data
        sponsor.budget = form.budget.data
        db.session.commit()
        flash('Profile completed successfully!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))

    return render_template('complete_sponsor_profile.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.is_on_hold:
                flash('Your account is currently on hold, please contact support.', 'danger')
                return redirect(url_for('main.index'))
            login_user(user, remember=False)
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'sponsor':
                return redirect(url_for('main.sponsor_dashboard'))
            elif user.role == 'influencer':
                return redirect(url_for('main.influencer_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@main.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Access Denied", 403

    users = User.query.filter(User.role != 'admin').all()
    sponsors = Sponsor.query.all()
    influencers = Influencer.query.all()
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()

    total_users = User.query.count()
    total_influencers = Influencer.query.count()
    total_sponsors = Sponsor.query.count()
    active_influencers = Influencer.query.join(User).filter(User.is_active == True).count()
    active_sponsors = Sponsor.query.join(User).filter(User.is_active == True).count()

    total_campaigns = Campaign.query.count()
    active_campaigns = Campaign.query.filter(Campaign.end_date >= date.today()).count()
    inactive_campaigns = Campaign.query.filter(Campaign.end_date <= date.today()).count()

    total_ad_requests = AdRequest.query.count()
    pending_ad_requests = AdRequest.query.filter_by(status='Pending').count()
    accepted_ad_requests = AdRequest.query.filter_by(status='Accepted').count()
    rejected_ad_requests = AdRequest.query.filter_by(status='Rejected').count()

    return render_template('admin_dashboard.html', users = users, sponsors = sponsors, influencers = influencers, campaigns = campaigns, ad_requests = ad_requests, total_users = total_users, total_influencers = total_influencers, total_sponsors = total_sponsors, active_influencers = active_influencers, active_sponsors = active_sponsors, total_campaigns = total_campaigns, active_campaigns = active_campaigns, inactive_campaigns = inactive_campaigns, total_ad_requests = total_ad_requests, pending_ad_requests = pending_ad_requests, accepted_ad_requests = accepted_ad_requests, rejected_ad_requests = rejected_ad_requests)

@main.route('/hold_user/<int:user_id>', methods=['POST'])
@login_required
def hold_user(user_id):
    if current_user.role != 'admin':
        return "Access Denied", 403

    user = User.query.get_or_404(user_id)
    user.is_on_hold = not user.is_on_hold
    db.session.commit()
    flash(f'User {"held" if user.is_on_hold else "released"} successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/hold_campaign/<int:campaign_id>', methods=['POST'])
@login_required
def hold_campaign(campaign_id):
    if current_user.role != 'admin':
        return "Access Denied", 403

    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.is_on_hold = not campaign.is_on_hold
    db.session.commit()
    flash(f'Campaign {"held" if campaign.is_on_hold else "released"} successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/hold_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def hold_ad_request(ad_request_id):
    if current_user.role != 'admin':
        return "Access Denied", 403

    ad_request = AdRequest.query.get_or_404(ad_request_id)
    ad_request.is_on_hold = not ad_request.is_on_hold
    db.session.commit()
    flash(f'Ad Request {"held" if ad_request.is_on_hold else "released"} successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/sponsor')
@login_required
def sponsor_dashboard():
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    campaigns = Campaign.query.filter_by(sponsor_id = current_user.id).all()
    ad_requests = AdRequest.query.filter_by(sponsor_id = current_user.id).all()
    return render_template('sponsor_dashboard.html', campaigns = campaigns, ad_requests = ad_requests)

@main.route('/create_campaign', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            sponsor_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data,
            goals=form.goals.data
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))

    return render_template('create_campaign.html', form=form)

@main.route("/sponsor/view_all_campaigns")
@login_required
def view_all_campaigns():
    if current_user.role != 'sponsor':
        return redirect(url_for('main.index'))
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    return render_template('view_all_campaigns.html', campaigns=campaigns)

@main.route("/sponsor/view_all_ad_requests")
@login_required
def view_all_ad_requests():
    if current_user.role != 'sponsor':
        return redirect(url_for('main.index'))
    ad_requests = AdRequest.query.filter_by(sponsor_id=current_user.id).all()
    return render_template('view_all_ad_requests.html', ad_requests=ad_requests)

@main.route('/update_campaign/<int:campaign_id>', methods = ['GET','POST'])
@login_required
def update_campaign(campaign_id):
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        return "Access Denied", 403

    form = CampaignForm(obj = campaign)
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.budget = form.budget.data
        campaign.visibility = form.visibility.data
        campaign.category = form.category.data
        campaign.goals = form.goals.data
        db.session.commit()

    return render_template('update_campaign.html')

@main.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        return "Access Denied", 403

    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('main.sponsor_dashboard'))

@main.route('/create_ad_request', methods=['GET', 'POST'])
@login_required
def create_ad_request():
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    form = AdRequestForm()
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.filter_by(sponsor_id=current_user.id).all()]
    form.influencer_id.choices = [(influencer.user_id, influencer.user.username) for influencer in Influencer.query.all()]

    if form.validate_on_submit():
        influencer_id = form.influencer_id.data
        influencer = Influencer.query.filter_by(user_id=influencer_id).first()
        if not influencer:
            flash('Invalid Influencer selected', 'danger')
            return render_template('create_ad_request.html', form=form)

        ad_request = AdRequest(
            sponsor_id=current_user.id,
            campaign_id=form.campaign_id.data,
            influencer_id=influencer.id,
            messages=form.messages.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status=form.status.data
        )
        db.session.add(ad_request)
        db.session.commit()
        flash('Ad request created successfully!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))

    return render_template('create_ad_request.html', form=form)

@main.route('/update_ad_request/<int:ad_request_id>', methods=['GET', 'POST'])
@login_required
def update_ad_request(ad_request_id):
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.campaign.sponsor_id != current_user.id:
        return "Access Denied", 403

    form = AdRequestForm(obj=ad_request)
    form.campaign_id.choices = [(campaign.id, campaign.name) for campaign in Campaign.query.filter_by(sponsor_id=current_user.id).all()]
    form.influencer_id.choices = [(influencer.user_id, influencer.user.username) for influencer in Influencer.query.all()]

    if form.validate_on_submit():
        influencer_id = form.influencer_id.data
        influencer = Influencer.query.filter_by(user_id=influencer_id).first()
        if not influencer:
            flash('Invalid Influencer selected', 'danger')
            return render_template('update_ad_request.html', form=form)

        ad_request.campaign_id = form.campaign_id.data
        ad_request.influencer_id = influencer.id
        ad_request.messages = form.messages.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = form.status.data
        db.session.commit()
        flash('Ad request updated successfully!', 'success')
        return redirect(url_for('main.sponsor_dashboard'))

    return render_template('update_ad_request.html', form=form)

@main.route('/delete_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def delete_ad_request(ad_request_id):
    if current_user.role != 'sponsor':
        return "Access Denied", 403

    ad_request = AdRequest.query.get_or_404(ad_request_id)
    if ad_request.campaign.sponsor_id != current_user.id:
        return "Access Denied", 403

    db.session.delete(ad_request)
    db.session.commit()
    flash('Ad request deleted successfully!', 'success')
    return redirect(url_for('main.sponsor_dashboard'))

@main.route('/search_influencers', methods=['GET', 'POST'])
@login_required
def search_influencers():
    form = SearchInfluencerForm()
    influencers = Influencer.query.order_by(Influencer.reach.desc()).all()

    if form.validate_on_submit():
        query = Influencer.query
        if form.category.data:
            query = query.filter(Influencer.category.ilike(f"%{form.category.data}%"))
        if form.min_reach.data:
            query = query.filter(Influencer.reach >= form.min_reach.data)
        if form.max_reach.data:
            query = query.filter(Influencer.reach <= form.max_reach.data)
        influencers = query.all()

    return render_template('search_influencers.html', form=form, influencers=influencers)

@main.route("/sponsor/<int:influencer_id>/profile")
@login_required
def view_influencer_profile(influencer_id):
    influencer = Influencer.query.get_or_404(influencer_id)
    return render_template('view_influencer_profile.html', influencer=influencer)

@main.route('/influencer')
@login_required
def influencer_dashboard():
    if current_user.role != 'influencer':
        return "Access Denied", 403

    form = UpdateInfluencerProfileForm()
    influencer = Influencer.query.filter_by(user_id=current_user.id).first_or_404()
    accepted_ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='Accepted').all()
    print(f"Accepted Ad Requests for Influencer {current_user.id}: {influencer.id} :{accepted_ad_requests}")
    return render_template('influencer_dashboard.html', accepted_ad_requests = accepted_ad_requests, form = form)

@main.route('/update_influencer_profile', methods=['GET', 'POST'])
@login_required
def update_influencer_profile():
    if current_user.role != 'influencer':
        return "Access Denied", 403

    form = UpdateInfluencerProfileForm()
    if form.validate_on_submit():
        current_user.influencer.name = form.name.data
        current_user.influencer.category = form.category.data
        current_user.influencer.niche = form.niche.data
        current_user.influencer.reach = form.reach.data
        current_user.influencer.instagram_handle = form.instagram_handle.data
        current_user.influencer.profile_picture = form.profile_picture.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.influencer_dashboard'))
    elif request.method == 'GET':
        form.name.data = current_user.influencer.name
        form.category.data = current_user.influencer.category
        form.niche.data = current_user.influencer.niche
        form.reach.data = current_user.influencer.reach
        form.instagram_handle.data = current_user.influencer.instagram_handle
        form.profile_picture.data = current_user.influencer.profile_picture

    return render_template('update_influencer_profile.html', form=form)

@main.route('/influencer/influencer_ad_requests')
@login_required
def influencer_ad_requests():
    if current_user.role != 'influencer':
        return "Access Denied", 403

    influencer = Influencer.query.filter_by(user_id=current_user.id).first_or_404()
    ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id).all()
    print(f"Fetched ad requests: {ad_requests}")  # Debug print
    return render_template('influencer_ad_requests.html', ad_requests=ad_requests)

@main.route('/accept_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def accept_ad_request(ad_request_id):
    if current_user.role != 'influencer':
        return "Access Denied", 403

    ad_request = AdRequest.query.get_or_404(ad_request_id)
    influencer = Influencer.query.filter_by(user_id = current_user.id).first_or_404()
    if ad_request.influencer.id != influencer.id:
        return f"Access Denied: Target ID: {ad_request.influencer_id}, Current ID: {current_user.id}", 403

    ad_request.status = 'Accepted'
    db.session.commit()
    flash('Ad request accepted successfully!', 'success')
    return redirect(url_for('main.influencer_ad_requests'))

@main.route('/reject_ad_request/<int:ad_request_id>', methods=['POST'])
@login_required
def reject_ad_request(ad_request_id):
    if current_user.role != 'influencer':
        return "Access Denied", 403

    ad_request = AdRequest.query.get_or_404(ad_request_id)
    influencer = Influencer.query.filter_by(user_id = current_user.id).first_or_404()
    if ad_request.influencer_id != influencer.id:
        return "Access Denied", 403

    ad_request.status = 'Rejected'
    db.session.commit()
    flash('Ad request rejected successfully!', 'success')
    return redirect(url_for('main.influencer_ad_requests'))

@main.route('/negotiate_ad_request/<int:ad_request_id>', methods=['GET', 'POST'])
@login_required
def negotiate_ad_request(ad_request_id):
    if current_user.role != 'influencer':
        return "Access Denied", 403

    ad_request = AdRequest.query.get_or_404(ad_request_id)
    influencer = Influencer.query.filter_by(user_id = current_user.id).first_or_404()
    if ad_request.influencer_id != influencer.id:
        return "Access Denied", 403

    form = NegotiateAdRequestForm(obj=ad_request)
    if form.validate_on_submit():
        ad_request.messages = form.messages.data
        ad_request.requirements = form.requirements.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.status = 'Pending'
        db.session.commit()
        flash('Ad request negotiation submitted successfully!', 'success')
        return redirect(url_for('main.influencer_ad_requests'))

    return render_template('negotiate_ad_requests.html', form=form)

@main.route('/influencer/search_public_campaigns', methods=['GET', 'POST'])
@login_required
def search_public_campaigns():
    form = SearchPublicCampaignForm()
    public_campaigns = []
    if form.validate_on_submit():
        public_campaigns = db.session.query(
            Campaign.name,
            Campaign.description,
            Campaign.budget,
            Campaign.start_date,
            Campaign.end_date,
            Sponsor.company_name.label('sponsor_name')
        ).join(Sponsor, Campaign.sponsor_id == Sponsor.user_id).filter(Campaign.visibility == 'public').all()


    return render_template('search_public_campaigns.html', form=form, campaigns=public_campaigns)

@main.route("/conversations", methods=['GET', 'POST'])
@login_required
def conversations():
    if request.method == 'POST':
        recipient_id = request.form['recipient_id']
        recipient = User.query.get_or_404(recipient_id)

        conversation = Conversation.query.filter(
            ((Conversation.user1_id == current_user.id) & (Conversation.user2_id == recipient.id)) |
            ((Conversation.user1_id == recipient.id) & (Conversation.user2_id == current_user.id))
        ).first()

        if not conversation:
            conversation = Conversation(
                user1_id=current_user.id,
                user2_id=recipient.id,
                last_message_at=datetime.utcnow()
            )
            db.session.add(conversation)
            db.session.commit()

        # Redirect to the chat page for this conversation
        return redirect(url_for('main.chat', conversation_id=conversation.id))

    user_conversations = Conversation.query.filter(
        (Conversation.user1_id == current_user.id) | (Conversation.user2_id == current_user.id)
    ).order_by(Conversation.last_message_at.desc()).all()
    users = User.query.filter(User.id != current_user.id).all()

    return render_template('conversations.html', conversations=user_conversations, users=users)

@main.route("/chat/<int:conversation_id>", methods=['GET', 'POST'])
@login_required
def chat(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)

    if current_user.id not in [conversation.user1_id, conversation.user2_id]:
        return redirect(url_for('main.conversations'))

    if conversation.user1_id == current_user.id:
        recipient = conversation.user2
    else:
        recipient = conversation.user1

    if request.method == 'POST':
        message = Message(
            conversation_id=conversation.id,
            sender_id=current_user.id,
            body=request.form['message']
        )
        db.session.add(message)
        conversation.last_message_at = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('main.chat', conversation_id=conversation.id))

    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', conversation = conversation, messages = messages, recipient = recipient)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
