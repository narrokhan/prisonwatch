from django.db import models

# Create your models here.
class prison(models.Model):
    prison_name = models.CharField(max_length=200)
    prison_domain_name = models.CharField(max_length=200)
    prison_BBS = models.CharField(max_length=200)
    prison_area = models.CharField(max_length=200)
    class Meta:
        ordering = ['-prison_name']
        verbose_name_plural = "已鎖定的監所"
    def __str__(self):
        return self.prison_name
class news(models.Model):
    topic = models.CharField(max_length=2000, verbose_name  = "公告")
    post_date = models.CharField(max_length=200 , verbose_name = "日期")
    news_url = models.CharField(max_length=1000)
    attach_filename = models.CharField(max_length=200)
    news_detail_text = models.CharField(max_length=2000)
    prison_related = models.ForeignKey('prison', on_delete = models.CASCADE, blank = True, default = None, verbose_name ="監所名稱")
    class Meta:
        ordering = ['-post_date']
        verbose_name_plural = "已發布的監所公告"
    def __str__(self):
        return self.topic
#class polling_process(models.Model):
#    prison_name = models.CharField(max_length=200)
#    crawlering_count_now = models.CharField(max_length=200)
#    limit_date = models.CharField(max_length=200)
#    def __str__(self):
#        return self.prison_name    
class FeatureCategory(models.Model):
    name = models.CharField(max_length=30)

class Feature(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(FeatureCategory, on_delete = models.CASCADE)

class Widget(models.Model):
    name = models.CharField(max_length=30)
    features = models.ManyToManyField(Feature, blank=True)