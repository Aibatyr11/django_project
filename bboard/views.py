from .models import Bb, Rubric, BbImage
from .forms import  SearchForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from .models import
from .models import ShopPrice
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .forms import BbForm, BbImageForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def rubric(request):
    rubrics = Rubric.objects.all()
    return render(request, 'index.html', {"rubrics": rubrics})

def rubric_detail(request, slug):
    rubric = get_object_or_404(Rubric, slug=slug)
    items = Bb.objects.filter(rubric=rubric)

    sort = request.GET.get('sort')
    brand = request.GET.get('brand')

    if sort == 'cheap':
        items = items.order_by('price')
    elif sort == 'expensive':
        items = items.order_by('-price')

    if brand:
        items = items.filter(title__icontains=brand)

    # Пагинация
    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'rubric_detail.html', {
        'rubric': rubric,
        'page_obj': page_obj,
        'selected_sort': sort,
        'selected_brand': brand,
    })

def product_detail(request, slug):
    product = get_object_or_404(Bb, slug=slug)
    shop_prices = product.shopprice_set.select_related('shop')  # Получаем связанные магазины и их цены

    return render(request, 'product_detail.html', {
        "product": product,
        "shop_prices": shop_prices,
    })


def search(request):
    context = {}
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric = sf.cleaned_data['rubric']
            bbs = Bb.objects.filter(
                title__iregex=keyword,
                rubric=rubric
            )
            context['bbs'] = bbs
    else:
        sf = SearchForm()

    context['form'] = sf
    return render(request, 'search.html', context)

# КОРЗИНА
def add_to_cart(request, sp_id):
    cart = request.session.get('cart', {})
    if isinstance(cart, list):
        cart = {}
    sp_id_str = str(sp_id)
    cart[sp_id_str] = cart.get(sp_id_str, 0) + 1
    request.session['cart'] = cart
    return redirect('bboard:view')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if isinstance(cart, list):
        cart = {}
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    return redirect('bboard:view')


def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if isinstance(cart, list):
            cart = {}
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                sp_id = key.split('_')[1]
                try:
                    qty = int(value)
                    if qty > 0:
                        cart[sp_id] = qty
                    else:
                        cart.pop(sp_id, None)
                except ValueError:
                    pass
        request.session['cart'] = cart
    return redirect('bboard:view')

def cart_view(request):
    if isinstance(request.session.get('cart'), list):
        request.session['cart'] = {}
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for sp_id, quantity in cart.items():
        try:
            item = ShopPrice.objects.get(pk=sp_id)
            item.quantity = quantity
            item.total_price = item.price * quantity
            total += item.total_price
            items.append(item)
        except ShopPrice.DoesNotExist:
            continue
    return render(request, 'cart.html', {'items': items, 'total': total})

@staff_member_required
def add_product(request):
    ImageFormSet = modelformset_factory(BbImage, form=BbImageForm, extra=3)

    if request.method == 'POST':
        form = BbForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=BbImage.objects.none())

        if form.is_valid() and formset.is_valid():
            bb = form.save()
            for img_form in formset.cleaned_data:
                if img_form:
                    BbImage.objects.create(bb=bb, image=img_form['image'])

            return redirect('bboard:rubric')
    else:
        form = BbForm()
        formset = ImageFormSet(queryset=BbImage.objects.none())

    return render(request, 'add_product.html', {
        'form': form,
        'formset': formset,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bboard:rubric')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
