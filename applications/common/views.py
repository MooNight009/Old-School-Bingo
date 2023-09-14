from django.views.generic import TemplateView


class handle404(TemplateView):
    template_name = 'pages/common/404.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(handle404, self).render_to_response(context, **response_kwargs)
        response.status_code = 404
        return response

class HandleNoPermission(TemplateView):
    template_name = 'pages/common/403.html'