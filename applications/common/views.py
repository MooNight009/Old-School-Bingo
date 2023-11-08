from django.db.models import Q
from django.views.generic import TemplateView

from applications.bingo.models import Bingo
from applications.player.models import Player

class HomePageView(TemplateView):
    template_name = 'pages/common/homepage.html'

class BingosView(TemplateView):
    template_name = 'pages/common/bingos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if self.request.user.is_anonymous:
            public_bingos = Bingo.objects.all().filter(is_public=True, is_over=False)
            context['public_bingos'] = public_bingos
        else:
            player = Player.objects.get(user=user)
            bingos = Bingo.objects.all()

            moderating_bingos = bingos.filter(Q(moderator_bingo__player=player)|Q(creator=player))
            joined_bingo = bingos.filter(playerbingodetail__player=player)
            public_bingos = bingos.filter(is_public=True).exclude(pk__in=moderating_bingos).exclude(
                pk__in=joined_bingo)

            context['moderating_bingos'] = moderating_bingos
            context['joined_bingos'] = joined_bingo
            context['public_bingos'] = public_bingos
        return context

class handle404(TemplateView):
    template_name = 'pages/common/404.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(handle404, self).render_to_response(context, **response_kwargs)
        response.status_code = 404
        return response

class HandleNoPermission(TemplateView):
    template_name = 'pages/common/403.html'