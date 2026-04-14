from flask import Blueprint, render_template, request
from app.models import Ticket
from constants import KBO_TEAMS

bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp.route('/list')
def ticket_list():
  
    #  URL에서 값 받아오기 (검색/필터용)
   
    awayteam = request.args.get('awayteam', '')
    seat = request.args.get('seat', '')
    quantity = request.args.get('quantity', '')
    team = request.args.get('team', '')
    option = request.args.get('option', '')
    page = request.args.get('page', 1, type=int)   #  현재 페이지 (페이징 핵심)

    
    #  기본 쿼리 생성
   
    query = Ticket.query

    
    #  필터 조건 적용 (검색 기능)
    
    if awayteam:
        query = query.filter(Ticket.awayteam_name == awayteam)

    if seat:
        query = query.filter(Ticket.seat.contains(seat))

    if quantity:
        #  숫자일 때만 적용 (에러 방지)
        if quantity.isdigit():
            query = query.filter(Ticket.quantity == int(quantity))

    
    #  정렬 + 페이징 
  
    tickets = query.order_by(Ticket.created_at.desc()).paginate(
        page=page,        # 현재 페이지 번호
        per_page=10,      # 한 페이지당 10개
        error_out=False   # 에러 방지
    )
    #  created_at.desc() → 최신 등록순 정렬

    
    #  선택한 팀 정보 찾기 (UI용)
    
    selected_team_data = None
    for t in KBO_TEAMS:
        if t['name'] == team:
            selected_team_data = t
            break

    #  템플릿으로 데이터 전달
    
    return render_template(
        'ticket.html',
        tickets=tickets,                     # 티켓 리스트 데이터
        team=team,                           # 선택된 팀
        option=option,                       # 선택된 옵션
        kbo_teams=KBO_TEAMS,                 # 팀 전체 데이터
        selected_team_data=selected_team_data  # 선택된 팀 상세
    )