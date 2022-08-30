from pickle import EMPTY_DICT
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm, CommentForm
from .models import Board, Comment
from user.models import User
from user.decorators import login_required
from datetime import date, datetime, timedelta
from .pagination import pagination

def board_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}
    
    boards = Board.objects.all().order_by('-id')
    page = pagination(request, Board)
    context['boards'] = boards
    context.update(page)

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


def board_write(request):
    login_session = request.session.get('login_session')
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

# 댓글
def commnet_detail(request, pk) : 

    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}
    
    comment = get_object_or_404(Board, pk=pk)
    comment_form = CommentForm()
    context['comment'] = comment
    context['comment_form'] = comment_form

    return render(request, 'board/board_detail.html', context)

def create_comment(request, pk) : 

    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    if request.method =='GET' :
        filled_form = CommentForm()
        context['temp_form'] = filled_form
        return render(request, 'board/board_detail.html', context)

    elif request.method == 'POST':
        filled_form = CommentForm(request.POST)

        if filled_form.is_valid() :
            temp_form = filled_form.save(commit=False)
            temp_form.post=Board.objects.get(id=pk)
            temp_form.save()
        
        return redirect(f'/board/detail/{pk}/')
