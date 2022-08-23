from itertools import count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Entry, Sku, Supplier
from .forms import EntryForm, NameForm, SkuForm, PartialCompleteForm
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.db.models import Count, Sum
from django.db.models import Q
import datetime
from django.contrib import messages

# Test 

def partial_confirm(request, pk):

    my_entry = Entry.objects.get(id=pk)
    sku_list = Sku.objects.all()

    my_sku = my_entry.code
    my_qty = my_entry.qty
    my_price = my_entry.price
    my_total_price = my_entry.total_price

    if request.method == "POST":
        form = PartialCompleteForm(request.POST, request.FILES)

        if form.is_valid():
            p_qty = form.cleaned_data['qty']
            print(p_qty)

            my_entry.qty = my_entry.qty - p_qty
            my_entry.save()

            new_complete_emtry = Entry(
                code = my_sku,
                qty= p_qty,
                price = my_price,
                order_date = my_entry.order_date,
                delivery_date = my_entry.delivery_date,
                supplier = my_entry.supplier,
                status = 'Complete',
                note = my_entry.note,
            )
            new_complete_emtry.save()

            messages.add_message(request, messages.INFO, 'Partial Confirm Successful')

            return redirect('products')
    my_entry = Entry.objects.get(id=pk)
    form = PartialCompleteForm()
    context = {
        # 'form': form,
        'sku_list': sku_list,
        'my_sku': my_sku,
        'my_qty': my_qty,
        'my_price': my_price,
        'my_total_price': my_total_price,
        'my_entry': my_entry,
        'form': form,
    }
    return render(request, 'partial_confirm.html', context)

def products(request):
    all_entries = Entry.objects.all()

    # test_entry = all_entries.get(pk=46)
    # test_sku = Sku.objects.get(code='B606')
    # test_entry.code = test_sku
    # test_entry.save()

    all_entries_recent = all_entries.order_by('-updated_at')[:5]
    Initials = all_entries.filter(status='Initial')
    assigne_orders = all_entries.filter(status='Assigned')
    pending_orders = all_entries.filter(status='Pending')
    complete_orders = all_entries.filter(status='Complete')

    suppliers = Supplier.objects.all()

    supplier_order_count = suppliers.annotate(sup_order_count = Count('entry'))
    
    initails_orders_count = Initials.count()
    assigne_orders_count = assigne_orders.count()
    pending_orders_count = pending_orders.count()
    complete_orders_count = complete_orders.count()

    initails_sku_orders_count = Count(
        'entry', filter=Q(entry__status='Initial'))
    initails_sku_orders_sum = Sum(
        'entry__qty', filter=Q(entry__status='Initial'))
    assigned_sku_orders_count = Count(
        'entry', filter=Q(entry__status='Assigned'))
    assigned_sku_orders_sum = Sum(
        'entry__qty', filter=Q(entry__status='Assigned'))
    pending_sku_orders_count = Count(
        'entry', filter=Q(entry__status='Pending'))
    pending_sku_orders_sum = Sum(
        'entry__qty', filter=Q(entry__status='Pending'))
    complete_sku_orders_count = Count(
        'entry', filter=Q(entry__status='Complete'))
    complete_sku_orders_sum = Sum(
        'entry__qty', filter=Q(entry__status='Complete'))
    total_sku_orders_count = Count('entry')
    total_sku_orders_sum = Sum('entry__qty',)


    sku_count = Sku.objects.annotate(initails_sku_orders_count=initails_sku_orders_count, assigned_sku_orders_count=assigned_sku_orders_count, assigned_sku_orders_sum=assigned_sku_orders_sum, total_sku_orders_count=total_sku_orders_count, initails_sku_orders_sum=initails_sku_orders_sum,
                                     total_sku_orders_sum=total_sku_orders_sum, pending_sku_orders_count=pending_sku_orders_count, pending_sku_orders_sum=pending_sku_orders_sum, complete_sku_orders_count=complete_sku_orders_count, complete_sku_orders_sum=complete_sku_orders_sum).order_by('-total_sku_orders_count')[:5]

    form = EntryForm()

    if request.method == "POST":
        form = EntryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('products')

    context = {
        'all_entries': all_entries,
        'all_entries_recent': all_entries_recent,
        'Initials': Initials,
        'assigne_orders': assigne_orders,
        'pending_orders': pending_orders,
        'complete_orders': complete_orders,
        'form': form,
        'assigne_orders_count': assigne_orders_count,
        'initails_orders_count': initails_orders_count,
        'pending_orders_count': pending_orders_count,
        'complete_orders_count': complete_orders_count,
        'sku_count': sku_count,
        'suppliers': suppliers,
        'supplier_order_count': supplier_order_count,


    }

    return render(request, "home3.html", context)


def new_entry(request):
    form = EntryForm()
    all_entries = Entry.objects.all()
    sku_list = Sku.objects.all()
    # my_sku = sku_list.get(id=1)
    # entry1 = all_entries.get(id=46)

    # entry1.code = Sku.objects.get(id=3)



    if request.method == "POST":
        form = EntryForm(request.POST, request.FILES)

        if form.is_valid():
            

            new_entry = form.save(commit=False)
            now = datetime.datetime.now()
            sku = request.POST.get('n_code')
            entry_sku = Sku.objects.get(code=sku)
            # print(sku)
            new_entry.updated_at = now
            new_entry.code = entry_sku
            new_entry.save()

            # form.code = code_sku
            # new_entry_id = form.id
            # print(f"form id: {new_entry_id}")
            # form.save()
            # test_entry = Entry.objects.latest('created_at')
            # sku = str(sku)
            # test_sku = Sku.objects.get(code=sku)
            # test_entry.code = test_sku
            # test_entry.updated_at = now
            # test_entry.save()

            
            messages.success(request, 'Entry Created')
            return redirect('products')

    context = {
        'all_entries': all_entries,
        'form': form,    
        'sku_list': sku_list,    
    }

    return render(request, 'new_entry.html', context)


def new_sku(request):
    print("works")
    if request.method == "POST":
        form = SkuForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'New Sku Added')
            form = SkuForm()
            context = {
                'form': form,
            }
            return render(request, "new_sku.html", context)
    form = SkuForm()

    context = {
        'form': form,

    }

    return render(request, "new_sku.html", context)



def update_status(request, pk):
    if request.method == "POST":
        my_status = Entry.objects.get(id=pk)
        my_status.status = 'Assigned'
        my_status.save()

    return redirect('products')


def edit_entry(request, pk):

    my_entry = Entry.objects.get(id=pk)
    sku_list = Sku.objects.all()

    if request.method == "POST":
        initial = Entry.objects.get(id=pk)
        form = EntryForm(request.POST, request.FILES, instance=my_entry)

        if form.is_valid():
            now = datetime.datetime.now()
            form.save(commit=False)
            form.updated_at = now
            form.save()
            return redirect('products')
    my_entry = Entry.objects.get(id=pk)
    form = EntryForm(instance=my_entry)
    context = {
        'form': form,
        'sku_list': sku_list,
    }
    return render(request, 'edit_entry.html', context)



def search(request):
    if request.POST:
        print("here post")
        sku = request.POST.get('sku')

        all_entries = Entry.objects.filter(code__iexact=sku)

        context = {
            'all_entries': all_entries,
        }

        return render(request, "search.html", context)

def suppler_orders(request, pk):
    all_entries = Entry.objects.all()
    sup = Supplier.objects.get(id=pk)
    entries = all_entries.filter(supplier__id=pk)
    total_sku_orders_count = entries.count()
    initials_orders = entries.filter(status='Initial')
    assigne_orders = entries.filter(status='Assigned')
    pending_orders = entries.filter(status='Pending')
    complete_orders = entries.filter(status='Complete')

    initials_orders_money = initials_orders.aggregate(Sum('total_price'))
    assigne_orders_money = assigne_orders.aggregate(Sum('total_price'))
    pending_orders_money = pending_orders.aggregate(Sum('total_price'))
    complete_orders_money = complete_orders.aggregate(Sum('total_price'))
    total_orders_money = entries.aggregate(Sum('total_price'))



    initails_orders_count = initials_orders.count()
    assigne_orders_count = assigne_orders.count()
    pending_orders_count = pending_orders.count()
    complete_orders_count = complete_orders.count()
    
    context = {
        'entries': entries,
        'sup': sup,
        'initails_orders_count': initails_orders_count,
        'assigne_orders_count': assigne_orders_count,
        'pending_orders_count': pending_orders_count,
        'complete_orders_count': complete_orders_count,
        'initials_orders_money': initials_orders_money,
        'assigne_orders_money': assigne_orders_money,
        'pending_orders_money': pending_orders_money,
        'complete_orders_money': complete_orders_money,
        'total_sku_orders_count': total_sku_orders_count,
        'total_orders_money': total_orders_money,
    }
    return render(request, 'supplier_orders.html', context)



