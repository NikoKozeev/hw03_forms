from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_author'] = 'Это я'
        context['text_author'] = ('Ну что я могу про себя рассказать, '
                                  'не так и многое. Больше всего мне мешает '
                                  'мой около гуманитарный мозг для которого '
                                  'представить себе целую программу '
                                  'огромное достижение. То что ещё вчера было '
                                  'почти не возможно сегодня'
                                  'не вызывает трудностей, '
                                  'буду надеятся что всё получится')

        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tech'] = 'Вот что я использовал'
        context['text_tech'] = ('Ну собтсвенно без Питона, '
                                'Джанго и VSCode ничего бы не получилось')
        return context
