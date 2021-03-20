from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = 'Артём Вирютин'
        context['work'] = 'Начинающий backend-разработчик'
        context['contacts'] = [{'label': 'GitHub', 'url': 'https://github.com/ArtyomViryutin'},
                               {'label': 'Instagram', 'url': 'https://www.instagram.com/virytin_art/'}]
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = 'Технологии'
        context['description'] = 'Используемые технологии'
        context['technologies'] = [{'label': 'Django', 'url': 'https://www.djangoproject.com/'},
                               {'label': 'Python', 'url': 'https://www.python.org/'},
                               {'label': 'HTML, CSS', 'url': 'http://htmlbook.ru/html'}]
        return context
