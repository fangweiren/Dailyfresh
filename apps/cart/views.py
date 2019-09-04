from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU


# 添加商品到购物车
# 1.请求方式，采用ajax post
# 如果涉及到数据的修改(新增、更新、删除),采用post
# 如果只涉及到数据的获取，采用get
# 2.传递参数：商品id(sku_id) 商品数量(count)
# /cart/add
class CartAddView(View):
    """购物车记录添加"""

    def post(self, request):
        """购物车记录添加"""
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理：添加购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # 先尝试获取sku_id的值 -> hget
        # 如果sku_id在hash中不存在，hget返回None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            count += int(cart_count)

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 设置hash中sku_id对应的值
        # hset->如果sku_id已经存在，更新数据；如果sku_id不存在，添加数据
        conn.hset(cart_key, sku_id, count)

        # 返回应答
        return JsonResponse({'res': 5, 'errmsg': '购物车添加成功'})
