from src import app, db, bcrypt
from flask import render_template, redirect
from flask_login import current_user, login_required
from src.models import User, Group_participants, Group, Message_in_group, Message
from src.form import CreateGroupForm, JoinGroupForm, MessageForm, GroupForm

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    formCreate = CreateGroupForm()
    formJoin = JoinGroupForm()
    form = GroupForm()
    print(form.validate_on_submit())

    if formCreate.identifier.data == 'FORMCREATE' and form.validate_on_submit():

        group_name = formCreate.group_name.data
        code = formCreate.code.data

        existing_group = Group.query.all()
        for group in existing_group:
            if bcrypt.check_password_hash(group.code, code):
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
        
    if formJoin.identifier.data == 'FORMJOIN' and form.validate_on_submit():

        print("działa")
        group_name = formJoin.group_name.data
        code = formJoin.code.data

        existing_group = Group.query.filter_by(group_name=group_name).all()

        print(existing_group)

        for group in existing_group:
            if bcrypt.check_password_hash(group.code, code):
                add_user_to_group = Group_participants(group_id=group.id, user_id=current_user.id)

                try:
                    db.session.add(add_user_to_group)
                    db.session.commit()
                except Exception as e:
                    return str(e)
                break

    groups = Group_participants.query.filter_by(user_id=current_user.id).all()

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