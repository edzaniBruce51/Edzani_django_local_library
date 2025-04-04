from django.contrib import admin


# Register your models here.
#This code imports the models and then calls admin.site.register to register each of them.
from .models import Author, Genre, Book, BookInstance, Language

#To associate book with book instances using TabularInline 
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0 # This removes the extra empty forms
    # can_delete = True  # Allows deletion of book instances
    # show_change_link = True  # Adds a link to edit the instance in detail
    # readonly_fields = ('id',)  # Makes the ID field read-only

#To change how a model is displayed in the admin interface you define a ModelAdmin class (which describes the layout) and register it with the model
#admin.site.register(Book)
#for the purpose of this demonstration, we'll instead use the @register decorator to register the models (this does exactly the same thing as the admin.site.register() syntax)
#Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    #pass
    list_display = ('title', 'author', 'display_genre')  #Unfortunately we can't directly specify the genre field in list_display because it is a ManyToManyField 
    #(Django prevents this because there would be a large database access "cost" in doing so).
    #Instead we'll define a display_genre function to get the information as a string 
    inlines = [BooksInstanceInline]

#Register the Admin classes for BookInstance using the decorator
#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    #pass
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = ((None, {'fields': ('book', 'imprint', 'id')}), ('Availability', {'fields': ('status', 'due_back', 'borrower')}),)


#Add this new class for Book inline display
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

#Register the admin class with the associated model
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    #pass
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]  # Add this line to include the inline Books display


admin.site.register(Genre)
admin.site.register(Language)



#A way to add a user using code and not the admin interface
    #from django.contrib.auth.models import User

# Create user and save to the database
    #user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Update fields and then save again
    #user.first_name = 'Tyrone'
    #user.last_name = 'Citizen'
    #user.save()

#OR USE THIS HIGHLY RECOMMENDED WAY TO SET UP A CUSTOMER USER MODEL ALLOW EASY CUSTOMIZING IN FUTURE
# Get current user model from settings
    #from django.contrib.auth import get_user_model
    #User = get_user_model()

# Create user from model and save to the database
    #user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Update fields and then save again
    #user.first_name = 'Tyrone'
    #user.last_name = 'Citizen'
    #user.save()
