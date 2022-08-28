from tkinter import E
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm 
from .models import Board
from user.models import User
from user.decorators import login_required

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

    return render(request, 'board/board_detail.html', context)

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