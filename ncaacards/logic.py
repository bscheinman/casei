from casei.ncaacards.models import UserEntry, NcaaGame

def get_game(game_id):
    try:
        return NcaaGame.objects.get(id=game_id)
    except NcaaGame.DoesNotExist:
        return None


def get_leaders(game):
    return UserEntry.objects.filter(game=game).order_by('-score')
