from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
#from django.contrib.auth.models import User
def quiz_processor(request):
    if request.user.is_authenticated:
        var = request.user.userId
        #quiz = Quiz.objects.filter(classroom=ClassRoom.objects.get(id=User.objects.get(userId=var).studentYear))
        #return {'quiz': quiz}
    else:
        return ''

