from pickle import EMPTY_DICT
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm 
from .models import Board
from user.models import User
from user.decorators import login_required
from datetime import date, datetime, timedelta

def board_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}
    
    boards = Board.objects.all().order_by('-id')
    py_boards = Board.objects.filter(board_name = 'Python')
    js_boards = Board.objects.filter(board_name = 'JavaScript')
    
    context['boards'] = boards
    context['py_boards'] =py_boards
    context['js_boards'] = js_boards

    return render(request, 'board/board_list.html', context)

def board_detail(request, pk) :
    login_session = request.session.get('login_session')
    context = {'login_session' : login_session}

    board = get_object_or_404(Board, id=pk)

    context['board'] = board

    if board.writer.user_id == login_session:
        context['writer'] = True
    else :
        context['writer'] = False

    response = render(request, 'board/board_detail.html', context)

    # 쿠키 이용 조회수 기능
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date =expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitsboard', '_')

    if f'_{pk}_' not in cookie_value :
        cookie_value += f'{pk}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        board.hits +=1
        board.save()
    
    return response


@login_required
def board_write(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    if request.method =='GET' :
        write_form = BoardWriteForm()
        context['forms'] = write_form
        return render(request, 'board/board_write.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id = login_session)
            board = Board(
                title = write_form.title,
                contents = write_form.contents,
                writer = writer,
            )
            board.save()
            return redirect('/board')
        else : 
            context['forms']= write_form
            if write_form.errors : 
                for value in write_form.errors.values():
                    context['error'] = value
                return render(request, 'board/board_write.html', context)

def board_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(Board, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board')
    else : 
        return redirect(f'board/detail/{pk}/')

@login_required
def board_modify(request, pk) : 
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    if board.writer.user_id != login_session:
        return redirect(f'/board/detail/{pk}/')
    
    if request.method == 'GET' : 
        write_form = BoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board/board_modify.html', context)

    elif request.method =='POST' :
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid() : 
            board.title = write_form.title
            board.contents = write_form.contents
            board.board_name =write_form.board_name

            board.save()
            return redirect('/board')
        
        else :
            context['forms'] = write_form
            if write_form.errors :
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_modify.html', context)

# 페이지 이동
from django.core.paginator import Paginator

def pagination(request, Board, contents_num=10) -> dict:
    all_boards = Board.objects.all().order_by('-id') # 객체 불러오기
    board_page = int(request.GET.get('page', '1'))  # 페이지 가져오기 기본값 =1
    paginator = Paginator(all_boards, contents_num)  # 페이지당 10개씩 표시
    boards = paginator.page(board_page)

    now_page = boards.number 
    end_page = boards.paginator.num_pages

    # 페이지를 7개만 표기 
    if end_page >= 7 :
        min_page = 7
    else :
        min_page =end_page

    # 보여줄 페이지(min_page 수)
    display_page = {}
    if now_page <= 4 :
        for k in range (min_page):
            display_page[k] = k+1
    elif now_page >= end_page-3 :
        for k in range (min_page):
            display_page[k] = (end_page-7)+(k+1)
    else : 
        for k in range(min_page) :
            display_page[k] = (now_page-4) + (k+1)

    # 이전페이지
    previous_page_chunk = now_page-7
    if previous_page_chunk <1:
        previous_page_chunk =1

    # 이전페이지 활성화
    if 4< now_page : 
        active_previous_page_chunk = True
    else : 
        active_previous_page_chunk = False

    # 다음 페이지
    next_page_chunk = now_page + 7
    if next_page_chunk > end_page :
        next_page_chunk = end_page

    # 다음페이지 활성화
    if now_page < (end_page-3) : 
        active_next_page_chunk = True
    else : 
        active_next_page_chunk = False
    
    context = {
        'boards' : boards,
        'now_page' : now_page,
        'end_page' : end_page,
        'display_page' : display_page,
        'previous_page_chunk' : previous_page_chunk,
        'next_page_chunk' : next_page_chunk,
        'active_previous_page_chunk' : active_previous_page_chunk,
        'active_next_page_chunk' : active_next_page_chunk
    }

    return context