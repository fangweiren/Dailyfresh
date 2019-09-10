from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from datetime import datetime
from apps.goods.models import GoodsSKU
from apps.user.models import Address
from apps.order.models import OrderInfo, OrderGoods
from utils.mixin import LoginRequiredMixin


# /order/place
class OrderPlaceView(LoginRequiredMixin, View):
    """提交订单页面显示"""

    def post(self, request):
        """提交订单页面显示"""
        user = request.user

        # 获取参数
        sku_ids = request.POST.getlist('sku_ids')

        if not sku_ids:
            return redirect(reverse('cart:show'))

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        skus = []
        total_count = 0
        total_price = 0

        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            count = conn.hget(cart_key, sku_id)
            amount = sku.price * int(count)
            sku.count = int(count)
            sku.amount = amount
            skus.append(sku)
            total_count += int(count)
            total_price += amount

        # 运费：实际开发时，属于一个子系统
        # 这里写死
        transit_price = 10

        # 实付款
        total_pay = total_price + transit_price

        # 获取用户的收件地址
        addrs = Address.objects.filter(user=user)

        sku_ids = ','.join(sku_ids)

        context = {
            'skus': skus,
            'total_count': total_count,
            'total_price': total_price,
            'transit_price': transit_price,
            'total_pay': total_pay,
            'addrs': addrs,
            'sku_ids': sku_ids
        }
        return render(request, 'place_order.html', context)


# /order/commit
class OrderCommitView(View):
    """订单创建"""

    def post(self, request):
        """订单创建"""
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')

        # 校验参数
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 2, 'errmsg': '非法的支付方式'})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '地址不存在'})

        # TODO：创建订单核心业务
        # 订单id: 20190910172020+用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # 运费
        transit_price = 10

        # 总数目和总金额
        total_count = 0
        total_price = 0

        # TODO：向df_order_info表中添加一条记录
        order = OrderInfo.objects.create(order_id=order_id,
                                         user=user,
                                         addr=addr,
                                         pay_method=pay_method,
                                         total_count=total_count,
                                         total_price=total_price,
                                         transit_price=transit_price)

        # TODO：用户的订单中有几个商品，就需要向df_order_goods表中添加几条记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        sku_ids = sku_ids.split(',')
        for sku_id in sku_ids:
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except:
                return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

            # 从redis中获取用户所要购买商品的数量
            count = conn.hget(cart_key, sku_id)

            # TODO：向df_order_goods表中添加一条记录
            OrderGoods.objects.create(order=order,
                                      sku=sku,
                                      count=count,
                                      price=sku.price)

            # TODO：更新商品的库存和销量
            sku.stock -= int(count)
            sku.sales += int(count)

            # TODO：累加计算订单商品的总数目和总价格
            amount = sku.price * int(count)
            total_count += int(count)
            total_price += amount

        # TODO：更新订单信息表中的商品的总数量和总价格
        order.total_count = total_count
        order.total_price = total_price
        order.save()

        # TODO：清除用户购物车中对应的商品 sku_ids=[1, 3, 4, 6]
        conn.hdel(cart_key, *sku_ids)

        # 返回应答
        return JsonResponse({'res': 5, 'message': '订单创建成功'})
