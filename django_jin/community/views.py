import profile
from django.shortcuts import render, redirect
from .forms import BoardWriteForm 
from .models import Board
from users.models import Profile
from users.decorators import login_required

def board_list(request):
    login_session = request.session.get('user')
    context = {'login_session' : login_session}

    boards = Board.objects.all().order_by('-id')
    
    if login_session != None:
            user=Profile.objects.get(id=login_session)
            context={'user_name':user.user_name}
            context['boards'] = boards
            return render(request,'community/board_list.html',context)
    if login_session == None:
            context['boards'] = boards
            return render(request,'community/board_list.html',context)

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
            return redirect('community:board_list')
        else : 
            context['forms']= write_form
            if write_form.errors : 
                for value in write_form.errors.values():
                    context['error'] = value
                return render(request, 'community/board_write.html', context)