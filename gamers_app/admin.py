from django.contrib import admin
from .models import Game, Borrow, Gamer

# Register your models here.
admin.site.register(Game)
admin.site.register(Borrow)
admin.site.register(Gamer)
