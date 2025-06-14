from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm
from .models import Ad, Category
from .forms import AdForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404
from django.utils import timezone
from django.contrib.auth import get_user_model
import hashlib
from django.contrib.auth import logout


# Create your views here.
@login_required
def profile_view(request):
    user = request.user
    email = user.email.lower().encode('utf-8')
    gravatar_hash = hashlib.md5(email).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{gravatar_hash}?s=200&d=identicon"

    return render(request, "ads/profile.html", {
        "user": user,
        "gravatar_url": gravatar_url
    })


@login_required
def ad_list(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    ads = Ad.objects.all().order_by("-created_at") if request.user.is_staff else Ad.objects.filter(status="published", is_archived=False).filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())).order_by("-created_at")

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        ads = ads.filter(category_id=category_id)

    paginator = Paginator(ads, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(
        request,
        "ads/ad_list.html",
        {
            "ads": ads,
            "page_obj": page_obj,
            "query": query,
            "category_id": category_id,
            "categories": categories,
        },
    )


@login_required
def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug)

    if ad.status != "published":
        if not request.user.is_authenticated or ( 
            not request.user.is_staff and ad.owner != request.user
         ):
            raise Http404("No Ad matches the qiven query.")
        
    return render(request, "ads/ad_detail.html", {"ad": ad})


@login_required
def ad_create(request):
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad  = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            assign_perm("change_ad", request.user, ad)
            assign_perm("delete_ad", request.user, ad)
            messages.success(request, "Ad created successfully.")
            return redirect("ad_detail", slug=ad.slug)
    else:
        form = AdForm()
    return render(request, "ads/ad_form.html", {"form": form})


@login_required
def ad_update(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if not request.user.has_perm("change_ad", ad):
        raise PermissionDenied
    
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, "Ad updated")
            return redirect("ad_detail", slug=ad.slug)
    else:
        form = AdForm(instance=ad)
    return render(request, "ad/ad_form.html", {"form": form})

@login_required
def ad_delete(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if not request.user.has_perm("delete_ad", ad):
        raise PermissionDenied
    
    if request.method == "POST":
        ad.delete()
        messages.success(request, "Ad deleted")
        return redirect("ad_list")
    
    return render(request, "ads/ad_confirm_delete.html", {"ad": ad})


@login_required
def my_ads(request):
    ads = Ad.objects.filter(owner=request.user)
    return render(request, "ads/my_ads.html", {"ads": ads})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("ad_list")
    return render(request, "ads/delete_account.html")

