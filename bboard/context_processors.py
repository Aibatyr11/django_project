
from .models import Rubric

def rubrics_processor(request):
    return {'rubrics': Rubric.objects.all()}
