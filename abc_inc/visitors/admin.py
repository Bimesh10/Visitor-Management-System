from django.contrib import admin
from .models import Visitor, Contact, UserProfile

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'status')  # Fields to display in the admin list view
    list_filter = ('status', 'department')          # Filter options in the sidebar
    search_fields = ('name', 'department', 'status') # Fields to search in the admin

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date_of_visit', 'status', 'contact')  # Add relevant fields
    list_filter = ('status', 'date_of_visit')  # Add filters for visitor status and date
    search_fields = ('name', 'email', 'phone') # Enable search functionality
    ordering = ('-date_of_visit',)             # Order by most recent visit

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')           # Display user and their role
    list_filter = ('role',)                   # Filter by role
    search_fields = ('user__username', 'role') # Search by username or role
