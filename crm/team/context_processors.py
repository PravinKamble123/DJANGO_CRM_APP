from .models import Team

def active_team(request):
    if request.user.is_authenticated:
        active_team= Team.objects.filter(created_by=request.user)
        if active_team.exists():
            active_team = active_team.first()
        else:
            active_team = None
    else:
        active_team = None
    return {'active_team':active_team}