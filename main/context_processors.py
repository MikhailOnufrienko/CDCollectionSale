from .models import Artist, Item


def cdcoll_objects(request):
    return {'artist_list': Artist.objects.all(), 'item_list': Item.objects.all()}
