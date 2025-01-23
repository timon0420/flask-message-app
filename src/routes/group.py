from src import app, db, bcrypt
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from src.models import User, Group_participants, Group, Message_in_group, Message
from src.form import CreateGroupForm, JoinGroupForm, MessageForm, GroupForm

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    formCreate = CreateGroupForm()
    formJoin = JoinGroupForm()
    form = GroupForm()

    if formCreate.identifier.data == 'FORMCREATE' and form.validate_on_submit():

        group_name = formCreate.group_name.data
        code = formCreate.code.data

        existing_group = Group.query.all()
        for group in existing_group:
            if bcrypt.check_password_hash(group.code, code):
                return "Sorry Something went wrong. Please try again"

        new_group = Group(group_name=group_name, code=code, admin=current_user.id)
        try:
            db.session.add(new_group)
            db.session.commit()
        except Exception as e:
            return str(e)
        
        add_user_to_group = Group_participants(group_id=new_group.id, user_id=current_user.id, participant=True)
        try:
            db.session.add(add_user_to_group)
            db.session.commit()
        except Exception as e:
            return str(e)
        
    if formJoin.identifier.data == 'FORMJOIN' and form.validate_on_submit():

        group_name = formJoin.group_name.data
        code = formJoin.code.data

        existing_group = Group.query.filter_by(group_name=group_name).all()

        for group in existing_group:
            if bcrypt.check_password_hash(group.code, code):
                if not Group_participants.query.filter_by(group_id=group.id, user_id=current_user.id).first():
                    add_new_user = Group_participants(group_id=group.id, user_id=current_user.id, participant=False)
                else:
                    return "You are already in this group"

        try:
            db.session.add(add_new_user)
            db.session.commit()
        except Exception as e:
            return str(e)

    groups = Group_participants.query.filter_by(user_id=current_user.id, participant=True).all()

    return render_template('profile.html', user=current_user, formCreate=formCreate, formJoin=formJoin, groups=groups, Group=Group)

@app.route('/group/<id>', methods=['GET', 'POST'])
@login_required
def group(id):

    existing_user = Group_participants.query.filter_by(group_id=id, user_id=current_user.id).first()

    if not existing_user:
        return "Sorry something went wrong. Please try again"
    
    form = MessageForm()

    if form.validate_on_submit():

        content = form.content.data
        form.content.data = ""

        new_message = Message(content=content, author=current_user.id)
        try:
            db.session.add(new_message)
            db.session.commit()
        except Exception as e:
            return str(e)
        
        new_message_in_group = Message_in_group(group_id=id, message_id=new_message.id)
        try:
            db.session.add(new_message_in_group)
            db.session.commit()
        except Exception as e:
            return str(e)

    messages_id = [message.message_id for message in Message_in_group.query.filter_by(group_id=id).all()]
    return render_template('group.html', group_id=id, messages_id=messages_id, Message=Message, User=User, form=form)

@app.route('/group/<id>/options', methods=['GET', 'POST'])
@login_required
def group_options(id):
    participants = Group_participants.query.filter_by(group_id=id, participant=False).all()
    return render_template('groupOptions.html', group_id=id, Group=Group, users=participants, User=User)

@app.route('/group/<id>/delete', methods=['GET', 'POST'])
@login_required
def group_delete(id):

    group = Group.query.get(id)

    try:
        db.session.delete(group)
        db.session.commit()
    except Exception as e:
        return str(e)
    
    return redirect('/profile')

@app.route('/group/group=<group_id>/user=<user_id>/add_user', methods=['GET', 'POST'])
@login_required
def add_user(group_id, user_id):

    add_user_to_group = Group_participants.query.filter_by(user_id=user_id, group_id=group_id).first()
    
    if add_user_to_group:
        add_user_to_group.participant = True
        try:
            db.session.commit()
        except Exception as e:
            return str(e)
    else:
        return "Sorry something went wrong. Please try again"
    
    return redirect(f"/group/{group_id}/options")

@app.route("/group/<group_id>/leave", methods=['GET', 'POST'])
@login_required
def leave_group(group_id):
    leave = Group_participants.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    try:
        db.session.delete(leave)
        db.session.commit()
    except Exception as e:
        return str(e)
    return redirect('/profile')
@app.route("/group/<group_id>/statics", methods=['GET', 'POST'])
@login_required
def statics(group_id):
    users = Group_participants.query.filter_by(group_id=group_id, participant=True).all()
    return render_template('statics.html', users=[user.user_id for user in users], User=User, group_id=group_id)