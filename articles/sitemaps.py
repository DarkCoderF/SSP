from django.contrib.sitemaps import Sitemap
from articles.models import Article

class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # return Article.objects.filter(status="PUBLISH")
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.date