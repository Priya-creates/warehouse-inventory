from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Product, Transaction
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    total_skus  = products.count()
    total_units = products.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'inventory/product_list.html', {
        'products':    products,
        'total_skus':  total_skus,
        'total_units': total_units,
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()

            # Snapshot name into transaction
            Transaction.objects.create(
                product=product,
                product_name=product.name,
                action='A',
                quantity=product.quantity
            )

            messages.success(request, "✅ Product added successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'inventory/add_product.html', {
        'form':    form,
        'is_edit': False,
    })


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated = form.save()

            Transaction.objects.create(
                product=updated,
                product_name=updated.name,
                action='U',
                quantity=updated.quantity
            )

            messages.success(request, f"✏️ “{updated.name}” updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/add_product.html', {
        'form':     form,
        'is_edit':  True,
        'product':  product,
    })


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Snapshot name before deletion
        Transaction.objects.create(
            product=product,
            product_name=product.name,
            action='D',
            quantity=product.quantity
        )

        product.delete()
        messages.success(request, f"🗑️ “{product.name}” deleted successfully!")
        return redirect('product_list')

    return render(request, 'inventory/delete_confirm.html', {
        'product': product
    })


def transaction_list(request):
    transactions = (
        Transaction.objects
        .order_by('-timestamp')
    )

    return render(request, 'inventory/transaction_list.html', {
        'transactions': transactions
    })
