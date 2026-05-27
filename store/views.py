from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

import razorpay

from store.models import (
    Category,
    Product,
    Cart,
    Order,
    OrderItem,
    ShippingAddress
)

# ---------------- HOME ----------------
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


# ---------------- CATEGORY PRODUCTS ----------------
def category_products(request, id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {
        'products': products,
        'categories': categories,
        'category': category
    })


# ---------------- ADD TO CART ----------------
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# ---------------- CART VIEW ----------------
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ---------------- REMOVE CART ITEM ----------------
@login_required
def remove_from_cart(request, id):
    Cart.objects.filter(id=id, user=request.user).delete()
    return redirect('cart')


# ---------------- INCREASE QTY ----------------
@login_required
def increase_qty(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


# ---------------- DECREASE QTY ----------------
@login_required
def decrease_qty(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


# ---------------- PRODUCT DETAILS ----------------
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'view_details.html', {
        'product': product
    })


# ---------------- CHECKOUT + RAZORPAY ----------------
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )

        # Save shipping address
        ShippingAddress.objects.create(
            user=request.user,
            order=order,
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            pincode=request.POST['pincode']
        )

        # Save order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Razorpay client
        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        razorpay_order = client.order.create({
            "amount": int(total * 100),  # paise
            "currency": "INR",
            "payment_capture": 1
        })

        cart_items.delete()

        return render(request, 'payment.html', {
            'total':total,
            'order': order,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'amount_paise': int(total * 100)
})


    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required(login_url='/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})