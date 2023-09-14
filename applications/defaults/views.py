# Create your views here.
from django.views.generic import TemplateView

from applications.bingo.models import Bingo
from applications.player.models import Player


class HomePageView(TemplateView):
    template_name = 'pages/common/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if self.request.user.is_anonymous:
            public_bingos = Bingo.objects.all().filter(is_public=True)
            context['public_bingos'] = public_bingos
        else:
            player = Player.objects.get(user=user)
            bingos = Bingo.objects.all()

            moderating_bingos = bingos.filter(moderator_bingo__player=player)
            joined_bingo = bingos.filter(player=player)
            public_bingos = bingos.filter(is_public=True).exclude(pk__in=moderating_bingos).exclude(
                pk__in=joined_bingo)

            context['moderating_bingos'] = moderating_bingos
            context['joined_bingos'] = joined_bingo
            context['public_bingos'] = public_bingos
        return context
