from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm
from .models import Ad
from .forms import AdForm
# Create your views here.

def ad_list(request):
    ads = Ad.objects.filter(status="published")
    return render(request, "ads/ad_list.html", {"ads": ads})

def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug, status="published")
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
