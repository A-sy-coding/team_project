import profile
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import BoardWriteForm 
from .models import Board
from users.models import Profile
from users.decorators import login_required
from datetime import date, datetime, timedelta
from .pagination import pagination

# 게시판
def board_list(request):
    login_session = request.session.get('user')
    context = {'login_session' : login_session}

    boards = Board.objects.all().order_by('-id')
    page = pagination(request, Board)

    if login_session != None:
            user=Profile.objects.get(id=login_session)
            context={'user_name':user.user_name}
            context['boards'] = boards
            context.update(page)
            return render(request,'community/board_list.html',context)
            
    if login_session == None:
            context['boards'] = boards
            context.update(page)
            return render(request,'community/board_list.html',context)

# 게시글 보기
def board_detail(request, pk) :
    login_session = request.session.get('user')
    context = {'login_session' : login_session}

    board = get_object_or_404(Board, id=pk)

    if login_session != None :
        user=Profile.objects.get(id=login_session)
        context={'user_name':user.user_name}
        context['board'] = board
        
        if board.writer.user_id == user.user_id:
            context['writer'] = True
        else :
            context['writer'] = False

        response = render(request,'community/board_detail.html',context)
            
    if login_session == None:
        context['board'] = board
        response = render(request,'community/board_detail.html',context)

    # 조회수
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

# 게시글 쓰기
@login_required
def board_write(request):
    login_session = request.session.get('user')
    context = {'login_session' : login_session}

    if request.method =='GET' :
        write_form = BoardWriteForm()
        context['forms'] = write_form
        return render(request, 'community/board_write.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = Profile.objects.get(id = login_session)
            board = Board(
                title = write_form.title,
                contents = write_form.contents,
                writer = writer,
            )
            board.save()
            return redirect('/community')
        else : 
            context['forms']= write_form
            if write_form.errors : 
                for value in write_form.errors.values():
                    context['error'] = value
                return render(request, 'community/board_write.html', context)

# 게시글 삭제
def board_delete(request, pk):
    login_session = request.session.get('user')
    board = get_object_or_404(Board, id=pk)

    if login_session != None :
        user=Profile.objects.get(id=login_session)

        if board.writer.user_id == user.user_id:
            board.delete()
            return redirect('/community')
        else : 
            return redirect(f'community/detail/{pk}/')

# 글 수정
@login_required
def board_modify(request, pk) : 
    login_session = request.session.get('user')
    context = {'login_session' : login_session}

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    if login_session != None :
        user=Profile.objects.get(id=login_session)

        if board.writer.user_id != user.user_id:
            return redirect(f'community/detail/{pk}/')

        if request.method == 'GET' : 
            write_form = BoardWriteForm(instance=board)
            context['forms'] = write_form
            return render(request, 'community/board_modify.html', context)

        elif request.method =='POST' :
            write_form = BoardWriteForm(request.POST)

            if write_form.is_valid() : 
                board.title = write_form.title
                board.contents = write_form.contents

                board.save()
                return redirect('/community')
            
            else :
                context['forms'] = write_form
                if write_form.errors :
                    for value in write_form.errors.values():
                        context['error'] = value
                return render(request, 'community/board_modify.html', context)