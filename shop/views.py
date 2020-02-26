from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Item, Cart, Record, Myuser
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import F


def index(request):
    items = Item.objects.all()
    try:
        user_id = request.session['user_id']
    except KeyError:
        return render(
            request,
            'shop/index.html',
            {
                'items': items
            }
        )
    else:
        myuser = get_object_or_404(Myuser, pk=user_id)
        return render(
            request,
            'shop/index.html',
            {
                'items': items,
                'myuser': myuser,
            }
        )


def detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(
        request,
        'shop/detail.html',
        {'item': item}
    )


def cart(request):
    if request.POST.keys().__contains__('item_id'):
        item_id = request.POST['item_id']
        item_id = int(item_id)
        item = get_object_or_404(Item, pk=item_id)
        usercart = Cart.objects.filter(is_finished=False)
        if usercart.count() > 1:
            raise Http404("Cart more than one")
        elif usercart.count() == 0:
            newcart = Cart(is_finished=False)
            newcart.save()
        usercart = Cart.objects.filter(is_finished=False)[0]
        if usercart.record_set.filter(item__id=item_id).count() == 1:
            r1 = usercart.record_set.filter(item__id=item_id)[0]
            r1.num = F('num')+1
            r1.save()
        elif usercart.record_set.filter(item__id=item_id).count() == 0:
            usercart.record_set.create(cart=usercart, item=item, num=1)
        else:
            raise Http404("dumplicated item records in cart")
        return HttpResponseRedirect(reverse('shop:cart'))
    usercart = Cart.objects.filter(is_finished=False)[0]
    return render(
        request,
        'shop/cart.html',
        {
            'cart': usercart
        }
    )


def register(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        verify = request.POST['verify']
    except KeyError:
        return render(
            request,
            'shop/register.html',
        )
    else:
        if password != verify:
            return render(
                request,
                'shop/register.html',
                {
                    'message': 'password doesn\'t match'
                }
            )
        if Myuser.objects.filter(username=username).count() == 1:
            return render(
                request,
                'shop/register.html',
                {
                    'message': 'username already exists'
                }
            )
        user = Myuser(username=username, password=password)
        user.save()
        return render(
            request,
            'shop/login.html',
        )


def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return render(
            request,
            'shop/login.html',
            {
                'message': 'input both username and password'
            }
        )
    if Myuser.objects.filter(username=username).count() == 0:
        return render(
            request,
            'shop/login.html',
            {
                'message': 'no such user, you can register it'
            }
        )
    user = Myuser.objects.filter(username=username)[0]
    if user.password != password:
        return render(
            request,
            'shop/login.html',
            {
                'message': 'password incorrect'
            }
        )
    request.session['user_id'] = user.id
    return HttpResponseRedirect(reverse('shop:index'))


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('shop:index'))


def user(request, user_id):
    myuser = get_object_or_404(Myuser, pk=user_id)
    return render(
        request,
        'shop/user.html',
        {
            'myuser': myuser
        }
    )
