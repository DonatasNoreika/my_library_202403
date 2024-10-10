from datetime import datetime

def current_year(request):
    return {
        'now': datetime.now()
    }