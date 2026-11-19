from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from. models import*
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from cloudinary.uploader import upload
import cloudinary.uploader
from cloudinary.exceptions import Error
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import CharField
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.contrib import messages as django_messages
from django.urls import reverse

# Create your views here.
def base(request):
    return render(request, 'base.html')
def home(request):
    testimonials = Testimonial.objects.all()
    return render(request, "index.html", {"testimonials": testimonials})

# def message(request):
#     if request.method == "POST":
#         try:
#             Enquiry.objects.create(
#                 full_name=request.POST.get("full_name"),
#                 email=request.POST.get("email"),
#                 phone=request.POST.get("phone"),
#                 business_name=request.POST.get("business_name"),
#                 business_category=request.POST.get("business_category"),
#                 subject=request.POST.get("subject"),
#                 message=request.POST.get("message"),
#             )
#             return JsonResponse({"success": True})

#         except Exception as e:
#             return JsonResponse({
#                 "success": False,
#                 "errors": {"server": str(e)}
#             }, status=400)

#     return render(request, "message.html")

import re

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Enquiry


def message(request):

    if request.method == "POST":

        submitted_values = {
            "full_name": request.POST.get("full_name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "business_name": request.POST.get("business_name", "").strip(),
            "business_category": request.POST.get("business_category", "").strip(),
            "subject": request.POST.get("subject", "").strip(),
            "message": request.POST.get("message", "").strip(),
        }

        errors = {}

        # Full name validation
        if len(submitted_values["full_name"]) < 2:
            errors["full_name"] = ["Name must contain at least 2 characters."]
        elif not re.fullmatch(r"[A-Za-z\s.'-]+", submitted_values["full_name"]):
            errors["full_name"] = [
                "Name can contain only letters, spaces, dots, apostrophes and hyphens."
            ]

        # Email validation
        try:
            validate_email(submitted_values["email"])
        except ValidationError:
            errors["email"] = ["Enter a valid email address."]

        # Phone validation
        if not re.fullmatch(r'^\+?[0-9]{10,13}$', submitted_values["phone"]):
            errors["phone"] = [
                "Enter a valid phone number with 10 to 13 digits."
            ]

        # Business name validation
        if len(submitted_values["business_name"]) < 2:
            errors["business_name"] = [
                "Business name must contain at least 2 characters."
            ]
        elif "<" in submitted_values["business_name"] or ">" in submitted_values["business_name"]:
            errors["business_name"] = [
                "HTML tags and scripts are not allowed."
            ]

        # Business category validation
        if len(submitted_values["business_category"]) < 2:
            errors["business_category"] = [
                "Business category must contain at least 2 characters."
            ]
        elif "<" in submitted_values["business_category"] or ">" in submitted_values["business_category"]:
            errors["business_category"] = [
                "HTML tags and scripts are not allowed."
            ]

        # Subject validation
        if len(submitted_values["subject"]) < 3:
            errors["subject"] = [
                "Subject must contain at least 3 characters."
            ]
        elif "<" in submitted_values["subject"] or ">" in submitted_values["subject"]:
            errors["subject"] = [
                "HTML tags and scripts are not allowed."
            ]

        # Message validation
        if len(submitted_values["message"]) < 10:
            errors["message"] = [
                "Message must contain at least 10 characters."
            ]
        elif "<" in submitted_values["message"] or ">" in submitted_values["message"]:
            errors["message"] = [
                "HTML tags and scripts are not allowed."
            ]

        # Prevent control characters
        for field, value in submitted_values.items():
            if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', value):
                errors[field] = ["Invalid characters are not allowed."]

        # Return to same page if validation fails
        if errors:
            return render(
                request,
                "message.html",
                {
                    "errors": errors,
                    "submitted_values": submitted_values,
                },
                status=400
            )

        # Save only after successful validation
        try:
            enquiry_obj = Enquiry.objects.create(**submitted_values)

            AdminNotification.objects.create(
                notification_type="enquiry",
                object_id=enquiry_obj.id,
                title="New Website Enquiry",
                message=f"New enquiry from {enquiry_obj.full_name}"
            )

            messages.success(
                request,
                "Your enquiry has been submitted successfully!"
            )

            return redirect("message")

        except Exception:
            messages.error(
                request,
                "Something went wrong. Please try again."
            )

            return render(
                request,
                "message.html",
                {"submitted_values": submitted_values},
                status=500
            )

    return render(request, "message.html")

def about(request):
    # Get all team members from database
    team_members = TeamMember.objects.all()

    context = {
        "team_members": team_members
    }

    return render(request, 'about.html', context)
def register(request):
    return render (request,'register.html')
def services(request):
    return render (request,'services.html')

def faq(request):
    return render (request,'faq.html')

def privacy(request):
    return render (request,'privacy_nmeapp.html')



# def sitemap(request):
#     return render (request,'sitemap.xml')

def blogs(request):
    query = request.GET.get('q', '').strip()

    blogs = Post.objects.all().order_by('-created_at')

    if query:
        date_filter = Q()

        # Try parsing date formats safely
        date_formats = [
    "%Y-%m-%d",      # 2026-01-09
    "%d-%m-%Y",      # 09-01-2026
    "%d/%m/%Y",      # 09/01/2026

    "%b %d %Y",      # Jan 09 2026
    "%b %d, %Y",     # Jan 09, 2026 ✅ NEW

    "%B %d %Y",      # January 09 2026
    "%B %d, %Y",     # January 09, 2026 ✅ NEW

    "%Y",            # 2026
]


        parsed_date = None
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(query, fmt)
                break
            except ValueError:
                continue

        # If a valid date is found → filter created_at
        if parsed_date:
            if len(query) == 4:  # year only
                date_filter = Q(created_at__year=parsed_date.year)
            else:
                date_filter = Q(created_at__date=parsed_date.date())

        blogs = blogs.filter(
            Q(card_head__icontains=query) |
            Q(card_paragraph__icontains=query) |
            Q(keyword__icontains=query) |
            Q(modal_head__icontains=query) |
            Q(modal_paragraph__icontains=query) |
            Q(date__icontains=query) |   # text date (optional)
            date_filter
        ).distinct()

    paginator = Paginator(blogs, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {
        'page_obj': page_obj,
        'query': query
    })


def blog_detail(request, id):
    post = get_object_or_404(Post, id=id)

    # 👉 Latest 3 blogs (excluding current one – optional but recommended)
    latest_blogs = Post.objects.exclude(id=post.id).order_by('-created_at')[:3]

    return render(request, 'blog_detail.html', {
        'post': post,
        'latest_blogs': latest_blogs
    })






from django.http import JsonResponse
from .forms import ContactForm
# def contact(request):

#     if request.method == "POST":
#         name = request.POST.get('name')
#         subject = request.POST.get('subject')
#         email = request.POST.get('email')
#         message = request.POST.get('message')

#         contact_data=Contact(name=name,subject=subject,email=email,message=message)
#         contact_data.save()
#     return render (request,'contact.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
        else:
            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# def contact(request):

#     if request.method == "POST":

#         form = ContactForm(request.POST)

#         if form.is_valid():

#             # Save contact form
#             contact_obj = form.save()

#             # Create admin notification
#             AdminNotification.objects.create(
#                 notification_type="contact",
#                 object_id=contact_obj.id,
#                 title="New Contact Message",
#                 message="A new contact form has been submitted."
#             )

#             return render(
#                 request,
#                 'contact.html',
#                 {
#                     'form': ContactForm(),
#                     'success': True
#                 }
#             )

#         else:
#             return render(
#                 request,
#                 'contact.html',
#                 {
#                     'form': form
#                 }
#             )

#     else:
#         form = ContactForm()

#     return render(
#         request,
#         'contact.html',
#         {
#             'form': form
#         }
#     )


# def contact_submit(request):
#     if request.method == "POST":
#         Contact.objects.create(
#             name=request.POST.get("name"),
#             email=request.POST.get("email"),
#             phone=request.POST.get("phone"),
#             subject=request.POST.get("subject"),
#             message=request.POST.get("message"),
#         )
#         # redirect to your custom admin panel instead of contact page
#         # return redirect("dashboard")  # your admin_panel URL name

#         messages.success(request, "Your message has been submitted successfully!")
#         return redirect("contact")
#     return redirect("contact")


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Contact


def contact_submit(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        try:
            contact_obj = Contact.objects.create(
                name=name,
                email=email,
                phone=phone or None,
                subject=subject,
                message=message,
            )

            AdminNotification.objects.create(
                notification_type="contact",
                object_id=contact_obj.id,
                title="New Contact Message",
                message=f"New contact message from {name}"
            )

            messages.success(
                request,
                "Your message has been submitted successfully!"
            )

            return redirect("contact")

        except ValidationError as e:

            field_errors = getattr(e, "message_dict", {})

            submitted_values = {
                "name": name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            }

            return render(
                request,
                "contact.html",
                {
                    "submitted_values": submitted_values,
                    "field_errors": field_errors,
                }
            )

    return redirect("contact")


# def delete_enquiry(request, id):
#     if request.method == "POST":
#         Contact.objects.filter(id=id).delete()  # delete the enquiry
#     return redirect("dashboard")  # redirect to admin panel
 # reload admin panel

from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact


def admin_enquiry(request):
    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )
    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect("login")

    contact = Contact.objects.all().order_by("-id")

    return render(request, "admin/enquiry.html", {
        "contact": contact,
        "selected_enquiry_id": request.GET.get("enquiry_id", "")
    })


def enquiry_detail(request, id):
    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )
    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect("login")

    enquiry = get_object_or_404(Contact, id=id)

    return render(request, "admin/enquiry_detail.html", {
        "enquiry": enquiry,
    })


def delete_enquiry(request, id):
    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )
    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect("login")

    if request.method == "POST":
        enquiry = get_object_or_404(Contact, id=id)
        enquiry.delete()

        request.session["enquiry_notification"] = {
            "message": "Enquiry deleted successfully!",
            "type": "success"
        }

    return redirect("dashboard")

def blog_post(request):
    if request.method == "POST":
        card_head = request.POST.get('card_head')
        modal_head = request.POST.get('modal_head')
        card_paragraph = request.POST.get('card_paragraph')
        modal_paragraph = request.POST.get('modal_paragraph')
        keyword = request.POST.get('keyword')
        image = request.FILES.get('image')
        date = request.POST.get('date')

        cloudinary_response = cloudinary.uploader.upload(image)
        cloudinary_url = cloudinary_response.get("secure_url")

        blog_data = Post(
            card_head=card_head,
            modal_head=modal_head,
            card_paragraph=card_paragraph,
            modal_paragraph=modal_paragraph,
            keyword=keyword,
            image=cloudinary_url,
            date=date
        )
        blog_data.save()

        # Add message
        request.session["blog_notification"] = {
            "message": "Blog added successfully!",
            "type": "success"
        }
        return redirect('dashboard')  

# def admin_panel(request):
#     is_superuser = (
#         request.user.is_authenticated and
#         request.user.is_superuser
#     )
#     # if "name" not in request.session:
#     #     return render(request, 'login.html')

#     is_custom_user = "name" in request.session

#     if not is_superuser and not is_custom_user:
#         return redirect('login')

#     blog = Post.objects.all()
#     contact = Contact.objects.all()
#     messages = Enquiry.objects.all().order_by("-created_at")
#     team_members = TeamMember.objects.all()
#     testimonials = Testimonial.objects.all().order_by('-id')

#     # Get the page parameter from URL (default: dashboard)
#     page = request.GET.get('page', 'dashboard')

#     context = {
#         "blog": blog,
#         "contact": contact,
#         "messages": messages,
#         "team_members": team_members,
#         "testimonials": testimonials,
#         "page": page,
#     }

#     # ✅ THIS LINE WAS MISSING
#     return render(request, "admin/dashboard.html", context)

from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone

def admin_panel(request):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect('login')

    # Existing dashboard data
    blog = Post.objects.all()
    contact = Contact.objects.all()
    messages = Enquiry.objects.all().order_by("-created_at")
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all().order_by('-id')

    # =====================================
    # ENQUIRY ANALYTICS
    # =====================================

    current_date = timezone.localdate()
    current_year = current_date.year

    # Get selected year
    try:
        selected_year = int(request.GET.get('year', current_year))
    except (ValueError, TypeError):
        selected_year = current_year

    # Available years from enquiry records
    available_years = list(
        Enquiry.objects
        .dates('created_at', 'year')
    )

    year_options = sorted(
        {date.year for date in available_years} | {current_year},
        reverse=True
    )

    # Prevent selecting an unavailable year
    if selected_year not in year_options:
        selected_year = current_year

    # Total enquiries
    total_enquiries = Enquiry.objects.count()

    # Current month's enquiries
    this_month_enquiries = Enquiry.objects.filter(
        created_at__year=current_date.year,
        created_at__month=current_date.month
    ).count()

    # Enquiries received in the selected year
    yearly_enquiries = (
        Enquiry.objects
        .filter(created_at__year=selected_year)
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(total=Count('pk'))
        .order_by('month')
    )

    # Create all 12 months, including months with zero enquiries
    monthly_counts = [0] * 12

    for item in yearly_enquiries:
        monthly_counts[item['month'] - 1] = item['total']

    # Total enquiries for selected year
    selected_year_total = sum(monthly_counts)

    # =====================================
    # DASHBOARD CONTEXT
    # =====================================

    page = request.GET.get('page', 'dashboard')
    team_notification = request.session.pop("team_notification", None)
    blog_notification = request.session.pop("blog_notification", None)
    enquiry_notification = request.session.pop("enquiry_notification", None)
    testimonial_notification = request.session.pop("testimonial_notification", None)
    message_notification = request.session.pop("message_notification", None)
    context = {
        "blog": blog,
        "contact": contact,
        "messages": messages,
        "team_members": team_members,
        "testimonials": testimonials,
        "page": page,
        "team_notification": team_notification,
        "blog_notification": blog_notification,
        "enquiry_notification": enquiry_notification,
        "testimonial_notification": testimonial_notification,
        "message_notification": message_notification,
        # Enquiry analytics
        "today": current_date,
        "total_enquiries": total_enquiries,
        "this_month_enquiries": this_month_enquiries,
        "selected_year": selected_year,
        "selected_year_total": selected_year_total,
        "year_options": year_options,
        "monthly_counts": monthly_counts,
    }

    return render(request, "admin/dashboard.html", context)

# def delete_message(request, id):
#     if request.method == "POST":
#         msg = get_object_or_404(Enquiry, id=id)
#         msg.delete()
#         return redirect("dashboard")
#     return redirect("dashboard")  # redirect for GET requests

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Testimonial


def admin_testimonials(request):
    testimonials = Testimonial.objects.all().order_by("-id")

    return render(
        request,
        "admin/admin_testimonials.html",
        {
            "testimonials": testimonials
        }
    )


@require_POST
def add_testimonial(request):

    name = request.POST.get("name", "").strip()
    rating = request.POST.get("rating")
    opinion = request.POST.get("opinion", "").strip()
    image = request.FILES.get("image")

    if name and rating and opinion and image:
        Testimonial.objects.create(
            name=name,
            rating=rating,
            opinion=opinion,
            image=image
        )
        request.session["testimonial_notification"] = {
            "message": "Testimonial added successfully!",
            "type": "success"
        }
    else:
        request.session["testimonial_notification"] = {
            "message": "Please fill in all testimonial fields!",
            "type": "error"
        }

    return redirect("dashboard")


@require_POST
def edit_testimonial(request, id):

    testimonial = get_object_or_404(Testimonial, id=id)

    name = request.POST.get("name", "").strip()
    rating = request.POST.get("rating")
    opinion = request.POST.get("opinion", "").strip()

    if name and rating and opinion:

        testimonial.name = name
        testimonial.rating = rating
        testimonial.opinion = opinion

        if request.FILES.get("image"):
            testimonial.image = request.FILES["image"]

        testimonial.save()

        request.session["testimonial_notification"] = {
            "message": "Testimonial updated successfully!",
            "type": "success"
        }

    else:
        request.session["testimonial_notification"] = {
            "message": "Please fill in all required testimonial fields!",
            "type": "error"
        }


    return redirect("dashboard")


@require_POST
def delete_testimonial(request, id):

    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    request.session["testimonial_notification"] = {
        "message": "Testimonial deleted successfully!",
        "type": "success"
    }

    return redirect("dashboard")

# def add_testimonial(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         rating = request.POST.get('rating')
#         opinion = request.POST.get('opinion')
#         image = request.FILES.get('image')

#         Testimonial.objects.create(
#             name=name,
#             rating=rating,
#             opinion=opinion,
#             image=image
#         )
#     return redirect('dashboard')  # or testimonials_page


# def edit_testimonial(request, id):
#     testimonial = Testimonial.objects.get(id=id)

#     if request.method == "POST":
#         testimonial.name = request.POST.get("name")
#         testimonial.rating = request.POST.get("rating")
#         testimonial.opinion = request.POST.get("opinion")

#         if request.FILES.get("image"):
#             testimonial.image = request.FILES.get("image")

#         testimonial.save()
#         return redirect("dashboard")  # change if needed



# # Delete testimonial
# def delete_testimonial(request, id):
#     testimonial = get_object_or_404(Testimonial, id=id)
#     testimonial.delete()
#     return redirect('dashboard')

def add_team_member(request):
    if request.method == "POST":
        TeamMember.objects.create(
            name=request.POST.get("name"),
            designation=request.POST.get("designation"),
            sentence=request.POST.get("sentence"),
            photo=request.FILES.get("photo"),
        )

        request.session["team_notification"] = {
            "message": "Team member added successfully!",
            "type": "success"
        }

    return redirect("dashboard")


def update_team_member(request, id):
    member = get_object_or_404(TeamMember, id=id)

    if request.method == "POST":
        member.name = request.POST.get("name")
        member.designation = request.POST.get("designation")
        member.sentence = request.POST.get("sentence")

        if request.FILES.get("photo"):
            member.photo = request.FILES.get("photo")

        member.save()

        request.session["team_notification"] = {
            "message": "Team member updated successfully!",
            "type": "success"
        }

    return redirect("dashboard")


def delete_team_member(request, id):
    member = get_object_or_404(TeamMember, id=id)

    if request.method == "POST":
        member_name = member.name
        member.delete()

        request.session["team_notification"] = {
            "message": f"{member_name} deleted successfully!",
            "type": "success"
        }

    return redirect("dashboard")

def update_blog(request):
    if request.method == 'POST':

        blog_id = request.POST.get('id')
        if not blog_id:
            return HttpResponse("Blog ID missing", status=400)

        blog = get_object_or_404(Post, id=blog_id)

        # Update text fields
        blog.card_head = request.POST.get('card_head')
        blog.modal_head = request.POST.get('modal_head')
        blog.card_paragraph = request.POST.get('card_paragraph')
        blog.modal_paragraph = request.POST.get('modal_paragraph')
        blog.keyword = request.POST.get('keyword')
        blog.date = request.POST.get('date')

        # Image update
        new_image = request.FILES.get('image')
        if new_image:
            # delete old image safely
            if blog.image:
                cloudinary.uploader.destroy(blog.image.public_id)

            uploaded = cloudinary.uploader.upload(new_image)
            blog.image = uploaded['secure_url']

        blog.save()
        request.session["blog_notification"] = {
            "message": "Blog updated successfully!",
            "type": "success"
        }
        return redirect('dashboard')

    return redirect('dashboard')
        

     

def delete_blog(request, id):
    blog = get_object_or_404(Post, id=id)

    # delete image from cloudinary
    if blog.image:
        public_id = blog.image.public_id
        cloudinary.uploader.destroy(public_id)

    blog.delete()
    request.session["blog_notification"] = {
        "message": "Blog deleted successfully!",
        "type": "success"
    }
    return redirect('dashboard')

def delete_contact(request,id):
    contact = Contact.objects.get(id = id)
    if contact:
        contact.delete()
    else:
        return HttpResponse("Can't delete this message!")
    return redirect('dashboard')


def admin_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        raw_password = request.POST.get('subject')

        hashed_password = make_password(raw_password)

        login = Login(username=username, password=hashed_password)
        login.save()

    return render(request, 'admin_register.html')


# from django.utils import timezone
# from datetime import timedelta
# from datetime import datetime
# def login(request):
#     print("Login view HIT!", request.method)
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         raw_password = request.POST.get('password')

#         print(username, raw_password)
#         if "name" in request.session:
#             print('haaaaaaiiii')
#         else:
#             print('loggiinnn pageee')

#         holder = Login.objects.first()

#         current_time = timezone.now()
#         if holder.last_failed_login is not None:
#             if timezone.is_naive(holder.last_failed_login):
#                 # Assume naive datetime is in your current timezone (e.g., Asia/Kolkata)
#                 aware_last_failed_login = timezone.make_aware(holder.last_failed_login, timezone.get_current_timezone())
#             else:
#                 aware_last_failed_login = holder.last_failed_login

#             if current_time < aware_last_failed_login + timedelta(hours=2) and holder.rate_limit == 5:
#                 print('Wait for a 2 hour time period')
#                 return render(request, 'login.html', {'ratelimit': True})
        
#             else:
#                 if holder.rate_limit >=5:
#                     holder.rate_limit = 0
#                     holder.save()
                
#                 try:
#                     user = Login.objects.get(username=username)
#                 except Login.DoesNotExist:
#                     holder.rate_limit +=1
#                     holder.last_failed_login = timezone.now()
#                     holder.save()
#                     return render(request, 'login.html', {'show_alert': True})
#                     # return render(request, 'login.html', {'show_alert': True})

                
#                 if check_password(raw_password, user.password):
#                     request.session["name"] = username
#                     # print(request.session['name'],'nameeeeee')
#                     holder.rate_limit = 0
#                     holder.save()
#                     response = redirect('dashboard')
#                     response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
#                     response['Pragma'] = 'no-cache'
#                     response['Expires'] = '0'
#                     print("Login successful, session name:", request.session.get("name"))

#                     return redirect('dashboard')
#                 else:
#                     holder = Login.objects.first()
                    
#                     holder.rate_limit +=1
#                     holder.last_failed_login = timezone.now()
#                     holder.save()
#                     # print('the rate limit :',user.rate_limit)
#                     return render(request, 'login.html', {'error': 'Invalid credentials'})
#         else:
#             holder.last_failed_login = current_time
#             holder.save()
#             return redirect('login')

#     else:
#         if "name" in request.session:
#             return redirect('dashboard')
#         else:
#             print("Login attempt")
#             response = render(request, 'login.html')
#             response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
#             response['Pragma'] = 'no-cache'
#             response['Expires'] = '0'
#             return response

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta


def login(request):

    print("Login view HIT!", request.method)

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        raw_password = request.POST.get('password', '')

        # =====================================
        # 1. CHECK DJANGO SUPERUSER LOGIN
        # =====================================

        django_user = authenticate(
            request,
            username=username,
            password=raw_password
        )

        print("Submitted username:", username)
        print("Django authentication result:", django_user)

        if django_user is None:
            print("Django authentication failed")
        else:
            print("Is superuser:", django_user.is_superuser)
            print("Is staff:", django_user.is_staff)

        if django_user is not None and django_user.is_superuser:

            auth_login(request, django_user)

            print("Django superuser login successful!")

            response = redirect('dashboard')

            response['Cache-Control'] = (
                'no-store, no-cache, must-revalidate, proxy-revalidate'
            )
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

            return response

        # =====================================
        # 2. CHECK YOUR CUSTOM LOGIN MODEL
        # =====================================

        holder = Login.objects.first()

        if holder is None:
            return render(
                request,
                'login.html',
                {'error': 'Login configuration not found'}
            )

        current_time = timezone.now()

        # =====================================
        # 3. CHECK RATE LIMIT
        # =====================================

        if holder.rate_limit >= 5:

            if holder.last_failed_login is not None:

                last_failed = holder.last_failed_login

                if timezone.is_naive(last_failed):
                    last_failed = timezone.make_aware(
                        last_failed,
                        timezone.get_current_timezone()
                    )

                if current_time < last_failed + timedelta(hours=2):

                    return render(
                        request,
                        'login.html',
                        {'ratelimit': True}
                    )

            # Reset expired rate limit
            holder.rate_limit = 0
            holder.save()

        # =====================================
        # 4. CUSTOM USER AUTHENTICATION
        # =====================================

        try:
            user = Login.objects.get(username=username)

        except Login.DoesNotExist:

            holder.rate_limit += 1
            holder.last_failed_login = current_time
            holder.save()

            return render(
                request,
                'login.html',
                {'show_alert': True}
            )

        if check_password(raw_password, user.password):

            request.session['name'] = username

            holder.rate_limit = 0
            holder.last_failed_login = None
            holder.save()

            print("Custom login successful:", username)

            response = redirect('dashboard')

            response['Cache-Control'] = (
                'no-store, no-cache, must-revalidate, proxy-revalidate'
            )
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

            return response

        else:

            holder.rate_limit += 1
            holder.last_failed_login = current_time
            holder.save()

            return render(
                request,
                'login.html',
                {'error': 'Invalid credentials'}
            )

    # =====================================
    # 5. GET REQUEST
    # =====================================

    else:

        if request.user.is_authenticated or 'name' in request.session:
            return redirect('dashboard')

        response = render(request, 'login.html')

        response['Cache-Control'] = (
            'no-store, no-cache, must-revalidate, proxy-revalidate'
        )
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response


def logout(request):
    request.session.flush()  # Clears all session data
    return redirect('login')

def admin_blogs(request):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect('login')

    blog = Post.objects.all().order_by('-date')

    return render(request, 'admin/added_blogs.html', {
        'blog': blog,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Enquiry


def admin_messages(request):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect("login")

    messages = Enquiry.objects.all().order_by("-id")

    return render(
        request,
        "admin/admin_messages.html",
        {
            "messages": messages,
            "selected_message_id": request.GET.get("message_id", "")
        }
    )


@require_POST
def delete_message(request, id):

    msg = get_object_or_404(Enquiry, id=id)

    msg.delete()
    request.session["message_notification"] = {
        "message": "Enquiry message deleted successfully!",
        "type": "success"
    }

    return redirect("dashboard")


def admin_notifications_api(request):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return JsonResponse(
            {"error": "Unauthorized"},
            status=403
        )

    notifications = AdminNotification.objects.filter(
        is_read=False
    ).order_by("-created_at")

    unread_count = notifications.count()

    latest_notifications = notifications[:10]

    data = []

    for notification in latest_notifications:

        notification_url = reverse(
            "open_admin_notification",
            args=[notification.id]
        )

        mark_read_url = reverse(
            "mark_admin_notification_read",
            args=[notification.id]
        )

        data.append({
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "url": notification_url,
            "mark_read_url": mark_read_url,
            "notification_type": notification.notification_type,
            "created_at": timezone.localtime(
                notification.created_at
            ).strftime("%d %b %Y, %I:%M %p")
        })

    return JsonResponse({
        "unread_count": unread_count,
        "notifications": data
    })


def open_admin_notification(request, id):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect("login")

    notification = get_object_or_404(
        AdminNotification,
        id=id
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    # CONTACT FORM MESSAGE
    if notification.notification_type == "contact":

        return redirect(
            f"{reverse('admin_enquiry')}?enquiry_id={notification.object_id}"
        )

    # WEBSITE ENQUIRY MESSAGE
    elif notification.notification_type == "enquiry":

        return redirect(
            f"{reverse('admin_messages')}?message_id={notification.object_id}"
        )

    return redirect("dashboard")

@require_POST
def mark_admin_notification_read(request, id):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return JsonResponse(
            {"error": "Unauthorized"},
            status=403
        )

    notification = get_object_or_404(
        AdminNotification,
        id=id
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    unread_count = AdminNotification.objects.filter(
        is_read=False
    ).count()

    return JsonResponse({
        "success": True,
        "unread_count": unread_count
    })


def message_enquiry_detail(request, id):

    is_superuser = (
        request.user.is_authenticated and
        request.user.is_superuser
    )

    is_custom_user = "name" in request.session

    if not is_superuser and not is_custom_user:
        return redirect("login")

    enquiry = get_object_or_404(
        Enquiry,
        id=id
    )

    return render(
        request,
        "admin/message_enquiry_detail.html",
        {
            "enquiry": enquiry
        }
    )