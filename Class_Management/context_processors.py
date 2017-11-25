from .models import ClassRoom,Quiz
from django.contrib.auth.models import User
def quiz_processor(request):
    if request.user.is_authenticated:
        var = request.user.username
        quiz = Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year))
        return {'quiz': quiz}
    else:
        return ''