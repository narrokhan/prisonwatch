from django.contrib import admin
from django.utils import timezone
import datetime
from django_admin_extras import InputFilter, custom_titled_filter, custom_view_field
# Register your models here.
from .models import prison,news
from django.contrib.admin.filters import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

class MyDateTimeFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(MyDateTimeFilter, self).__init__(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()

        self.links += ((
            (_('Next 7 days'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
        ))
        self.title = "日期"
#admin.site.register(prison)
#admin.site.register(news)
class MyRelatedDropdownFilter(RelatedDropdownFilter):
    def __init__(self, *args, **kwargs):
        super(MyRelatedDropdownFilter, self).__init__(*args, **kwargs)
        self.title = "監所名稱"
class MyDateRangeFilter(DateRangeFilter):
    def __init__(self, *args, **kwargs):
        super(MyDateRangeFilter, self).__init__(*args, **kwargs)
        self.title = "日期區間"   
#@admin.register(prison)
class prisonAdmin(admin.ModelAdmin):
    pass
admin.site.register(prison, prisonAdmin)
# Register the Admin classes for BookInstance using the decorator
@admin.register(news)

class newsAdmin(admin.ModelAdmin):
    list_display = ('topic','prison_related','post_date','show_topic_link')
    list_filter = ( ('post_date', MyDateTimeFilter),('prison_related',MyRelatedDropdownFilter  ),
        ('post_date', MyDateRangeFilter))
    change_list_template = "crawler_list.html"
    search_fields = ("topic",)
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
          #  '../polls/js/myscript.js',       # project static folder
           # 'app/js/myscript.js',   # app static folder
        )
    def show_topic_link(self, obj):
        return obj.news_url
        #return ('<a href=\"%s\">%s</a>' % (obj.news_url, obj.topic) )
    show_topic_link.allow_tags = True
    show_topic_link.short_description = "連結"
def get_urls(self):
    urls = super().get_urls()
    my_urls = [
        path('immortal/', self.set_immortal),
        path('mortal/', self.set_mortal),
    ]
    return my_urls + urls

def set_immortal(self, request):
    self.model.objects.all().update(is_immortal=True)
    self.message_user(request, "All heroes are now immortal")
    return HttpResponseRedirect("../")

def set_mortal(self, request):
    self.model.objects.all().update(is_immortal=False)
    self.message_user(request, "All heroes are now mortal")
    return HttpResponseRedirect("../")


admin.site.site_header = "監所公告資料庫"
admin.site.site_title = "UAdmin Portal"
admin.site.index_title = "爬蟲 自動抓取公告"

