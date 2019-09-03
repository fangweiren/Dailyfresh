from haystack import indexes
# 导入模型类
from .models import GoodsSKU


# 指定对于某个类的某些数据建立索引
# 索引类名格式：模型类名+Index
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # document=True表示建立的索引数据存储到文件中
    # use_template=True表示通过模板指定表中的字段，用于查询 /templates/search/indexes/goods/goodssku_text.txt
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
