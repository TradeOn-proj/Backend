from flask import Blueprint, render_template

bp_chat = Blueprint('chat', __name__, url_prefix= '/api/v1/chat')

@bp_chat.route('/')
def chat():
    return render_template('chat.html')