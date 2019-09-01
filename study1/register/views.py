from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, BookInstance, CreditCard, UserInfo, Order, OrderItems
from django.views import generic
from django.db.models import Q
from .forms import RegistrationForm, EditUserAccountForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url='/accounts/login/')
def Pay(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    items = []
    for item in request.session['cart']:
        if BookInstance.objects.filter(id=item).count() == 0:
            items.append(item)
        elif not BookInstance.objects.get(id=item).available:
            items.append(item)
    if len(items) > 0:
        for item in items:
            request.session['cart'].remove(item)
    book_list = None
    total = 0
    for item in request.session['cart']:
        if book_list is None:
            book_list = BookInstance.objects.filter(id=item)
        else:
            book_list = book_list | BookInstance.objects.filter(id=item)
        total += BookInstance.objects.filter(id=item)[0].price
    if CreditCard.objects.filter(user__username__exact=request.user.username).count() > 0:
        if book_list.count() > 0:
            order = Order.objects.create(user=request.user)
            order.save()
            order_number = order.id
            for book in book_list:
                book.available = False
                book.save()
                obj = OrderItems.objects.create(order=order, item=book)
                obj.save()
            context = {
                'order_number': order_number,
            }
            return render(request, 'register/order_complete.html', context=context)
        else:
            context = {
                'book_list': book_list,
                'total': total,
            }
            return render(request, 'register/shopping_cart.html', context=context)
    else:
        context = {
            'book_list': book_list,
            'total': total,
        }
        return render(request, "register/contact.html", context=context)


def Help(request):
    return render(request, "register/help.html", {})


def Contact(request):
    return render(request, "register/contact.html", {})


def Register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = RegistrationForm()
    return render(request, "register/register.html", {"form": form})


@login_required(login_url='/accounts/login/')
def Profile(request):
    cards = CreditCard.objects.filter(user__username__exact=request.user.username)
    if cards.count() == 0:
        cards = None
    else:
        cards = cards[0]
    info = UserInfo.objects.filter(user__username__exact=request.user.username)
    if info.count() == 0:
        info = None
    else:
        info = info[0]
    context = {
        'user': request.user,
        'info': info,
        'cards': cards,
    }
    return render(request, "register/profile.html", context=context)


@login_required(login_url='/accounts/login/')
def UpdateProfile(request):
    if request.method == "POST":
        form = EditUserAccountForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['First_Name']
            request.user.last_name = form.cleaned_data['Last_Name']
            request.user.save()
            try:
                userInfo = UserInfo.objects.get(user__username__exact=request.user.username)
                userInfo.mailing_Address = form.cleaned_data['mailing_address']
                userInfo.billing_Address = form.cleaned_data['billing_address']
                userInfo.save()
            except UserInfo.DoesNotExist:
                userInfo = UserInfo.objects.create(user=request.user, mailing_Address=form.cleaned_data['mailing_address'],
                                                   billing_Address=form.cleaned_data['billing_address'])
                userInfo.save()
            try:
                cardInfo = CreditCard.objects.get(user__username__exact=request.user.username)
                cardInfo.credit_Card_Type = form.cleaned_data['card_type']
                cardInfo.credit_Card_Number = form.cleaned_data['credit_card_number']
                cardInfo.expiration_Date = form.cleaned_data['Expiration_Date']
                cardInfo.save()
            except CreditCard.DoesNotExist:
                cardInfo = CreditCard.objects.create(user=request.user, credit_Card_Type=form.cleaned_data['card_type'],
                                                     credit_Card_Number=form.cleaned_data['credit_card_number'],
                                                     expiration_Date=form.cleaned_data['Expiration_Date'])
                cardInfo.save()
            return redirect("/profile")
        else:
            form = EditUserAccountForm()
            return render(request, "register/update_profile.html", {"form": form})
    else:
        form = EditUserAccountForm()
        return render(request, "register/update_profile.html", {"form": form})


def home(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count()
    num_available = BookInstance.objects.filter(available=True).count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_available': num_available,
        'num_authors': num_authors,
    }
    return render(request, 'register/home.html', context=context)


class BookDetailView(generic.DetailView):
    model = Book


class BookListView(generic.ListView):
    model = Book


class BookSearchView(generic.ListView):
    model = Book
    template_name = 'book_list'

    def get_queryset(self): # new
        query = self.request.GET.get('book_search')
        object_list = Book.objects.filter(
            Q(isbn__icontains=query) | Q(title__icontains=query) | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query) | Q(professor__first_name__icontains=query) |
            Q(professor__last_name__icontains=query) | Q(subject__icontains=query)
            | Q(course_number__icontains=query)

        )
        return object_list


def AddToCart(request, pk):
    if 'cart' not in request.session:
        request.session['cart'] = [pk]
    else:
        if pk not in request.session['cart']:
            request.session['cart'].append(pk)
    items = []
    for item in request.session['cart']:
        if BookInstance.objects.filter(id=item).count() == 0:
            items.append(item)
        elif not BookInstance.objects.get(id=item).available:
            items.append(item)
    if len(items) > 0:
        for item in items:
            request.session['cart'].remove(item)
    request.session.modified = True
    book_list = None
    total = 0
    for item in request.session['cart']:
        if book_list is None:
            book_list = BookInstance.objects.filter(id=item)
        else:
            book_list = book_list | BookInstance.objects.filter(id=item)
        total += BookInstance.objects.filter(id=item)[0].price
    context = {
        'book_list': book_list,
        'total': total,
    }
    return render(request, 'register/shopping_cart.html', context=context)


def ShoppingCart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    items = []
    for item in request.session['cart']:
        if BookInstance.objects.filter(id=item).count() == 0:
            items.append(item)
        elif not BookInstance.objects.get(id=item).available:
            items.append(item)
    if len(items) > 0:
        for item in items:
            request.session['cart'].remove(item)
    book_list = None
    total = 0
    for item in request.session['cart']:
        if book_list is None:
            book_list = BookInstance.objects.filter(id=item)
        else:
            book_list = book_list | BookInstance.objects.filter(id=item)
        total += BookInstance.objects.filter(id=item)[0].price
    context = {
        'book_list': book_list,
        'total': total,
    }
    return render(request, 'register/shopping_cart.html', context=context)


def RemoveFromCart(request, pk):
    if 'cart' not in request.session:
        request.session['cart'] = []
    else:
        item = request.session['cart']
        if pk in item:
            item.remove(pk)
            request.session['cart'] = item
    items = []
    for item in request.session['cart']:
        if BookInstance.objects.filter(id=item).count() == 0:
            items.append(item)
        elif not BookInstance.objects.get(id=item).available:
            items.append(item)
    if len(items) > 0:
        for item in items:
            request.session['cart'].remove(item)
    request.session.modified = True
    book_list = None
    total = 0
    for item in request.session['cart']:
        if book_list is None:
            book_list = BookInstance.objects.filter(id=item)
        else:
            book_list = book_list | BookInstance.objects.filter(id=item)
        total += BookInstance.objects.filter(id=item)[0].price
    context = {
        'book_list': book_list,
        'total': total,
    }
    return render(request, 'register/shopping_cart.html', context=context)


@login_required(login_url='/accounts/login/')
def Checkout(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    items = []
    for item in request.session['cart']:
        if BookInstance.objects.filter(id=item).count() == 0 :
            items.append(item)
        elif not BookInstance.objects.get(id=item).available:
            items.append(item)
    if len(items) > 0:
        for item in items:
            request.session['cart'].remove(item)
    book_list = None
    total = 0
    for item in request.session['cart']:
        if book_list is None:
            book_list = BookInstance.objects.filter(id=item)
        else:
            book_list = book_list | BookInstance.objects.filter(id=item)
        total += BookInstance.objects.filter(id=item)[0].price
    context = {
        'book_list': book_list,
        'total': total,
    }
    return render(request, 'register/checkout.html', context=context)
