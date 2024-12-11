from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.http import HttpResponse
from .models import Visitor, Contact, UserProfile
from django.db.models import Count, Avg
from datetime import datetime

# Utility function to check if the user is an admin
def is_admin(user):
    return user.userprofile.is_admin()

# Utility function to check if the user is a gatekeeper
def is_gatekeeper(user):
    return user.userprofile.is_gatekeeper()

# Utility function to check if the user is a visitor
def is_visitor(user):
    return user.userprofile.is_visitor()

def index(request):
    return HttpResponse("This is the homepage")

def book_appointment(request):
    if is_visitor(request.user):  # Check if the user is a Visitor
        if request.method == "POST":
            form = AppointmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("appointment_success")
        else:
            form = AppointmentForm()

        return render(request, "visitors/book_appointment.html", {"form": form})
    else:
        return HttpResponse("Unauthorized", status=403)  # Return a 403 for non-visitors

def appointment_success(request):
    return render(request, "visitors/appointment_success.html")

def mark_completed(request, visitor_id):
    if is_gatekeeper(request.user):  # Only Gatekeepers can mark visits as completed
        visitor = Visitor.objects.get(id=visitor_id)
        visitor.release_slot()
        return redirect('appointment_success')
    else:
        return HttpResponse("Unauthorized", status=403)  # Return a 403 for non-gatekeepers

def dashboard(request):
    if is_admin(request.user):  # Only Admin can access the dashboard
        # Get the number of office employees (assuming 'Active' status in Contact model)
        num_employees = Contact.objects.filter(status='Active').count()

        # Get the monthly visitors
        current_month = datetime.now().month
        monthly_visitors = Visitor.objects.filter(date_of_visit__month=current_month).count()

        # Visitors frequency (number of visits per visitor)
        visitor_frequency = Visitor.objects.values('name').annotate(visit_count=Count('name')).order_by('-visit_count')

        # Time taken for each visit (assuming meeting_end_time and meeting_start_time are set)
        time_taken_for_visits = Visitor.objects.filter(meeting_start_time__isnull=False, meeting_end_time__isnull=False)
        total_time_taken = sum([(v.meeting_end_time - v.meeting_start_time).total_seconds() for v in time_taken_for_visits])
        average_time_taken = total_time_taken / len(time_taken_for_visits) if time_taken_for_visits else 0

        return render(request, "visitors/dashboard.html", {
            'num_employees': num_employees,
            'monthly_visitors': monthly_visitors,
            'visitor_frequency': visitor_frequency,
            'average_time_taken': average_time_taken / 60,  # Convert seconds to minutes
        })
    else:
        return HttpResponse("Unauthorized", status=403)  # Return a 403 for non-admin users
