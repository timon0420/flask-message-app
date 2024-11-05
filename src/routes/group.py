from src import app, db, bcrypt
from flask import render_template, redirect
from flask_login import current_user, login_required
from src.models import Group_participants, Group, Message_in_group, Message
from src.form import CreateGroupForm

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = CreateGroupForm()
    groups = Group_participants.query.filter_by(user_id=current_user.id).all()
    print(groups)
    if form.validate_on_submit():

        group_name = form.group_name.data
        code = form.code.data

        existing_group = Group.query.all()
        for group in existing_group:
            if bcrypt.check_password_hash(group.password, code):
                return "Sorry Something went wrong. Please try again"

        new_group = Group(group_name=group_name, code=code)
        try:
            db.session.add(new_group)
            db.session.commit()
        except Exception as e:
            return str(e)
        
        add_user_to_group = Group_participants(group_id=new_group.id, user_id=current_user.id)
        try:
            db.session.add(add_user_to_group)
            db.session.commit()
        except Exception as e:
            return str(e)
        
    return render_template('profile.html', user=current_user, form=form, groups=groups, Group=Group)

@app.route('/group/<id>', methods=['GET', 'POST'])
@login_required
def group(id):
    messages_id = [message.message_id for message in Message_in_group.query.filter_by(group_id=id).all()]
    return render_template('group.html')