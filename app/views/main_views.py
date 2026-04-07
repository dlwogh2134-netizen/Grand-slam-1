# app/views/main_views.py
from flask import Blueprint, render_template
from constants import KBO_TEAMS

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    # 메인 페이지에 구단 리스트를 던져줍니다.
    return render_template('index.html', teams=KBO_TEAMS)
