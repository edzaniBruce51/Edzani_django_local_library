from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # Constraints fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
import uuid # Required for unique book instances
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # Fields
    # defined local to a method, it is a variable. If it is declared as part of a class, then it is a field.
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')

    # Metadata
    class Meta:
        ordering = ['-my_field_name']   #the minus reverses the sorting order(from newest to oldest)

    # Methods
    #  get_absolute_url (returns a URL for displaying individual model records on the website (if you
    #  define this method then Django will automatically add a "View on Site" button to the model's record editing screens in the Admin site). 
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    # __str__ (This string is used to represent individual records in the administration site (and 
    # anywhere else you need to refer to a model instance). Often this will return a title or name field from the model.)
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name

# Genre model
# unique=True on the field above prevents genres being created with exactly the same name, but not variations such as "fantasy", "Fantasy", or even "FaNtAsY"
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, unique=True,help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")


    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to acces a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
    
    # Introducing the definition of constraints 
    # specify that the lower case of the value in the name field must be unique in the database, and display the violation_error_message string if it isn't
    class Meta:
        constraints = [UniqueConstraint(Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message = "Genre already exists(case insensitive match)"),]

# Language model
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ] 

        
# Book model
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',on_delete=models.RESTRICT, null=True)
    # Foreign key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file
    # on_delete=models.RESTRICT, which will prevent the book's associated author being deleted if it is referenced by any book.
    # By default on_delete=models.CASCADE, which means that if the author was deleted, this book would be deleted too! We use RESTRICT here, but we could also use PROTECT to prevent the author being deleted while any book uses it


    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn''">ISBN number</a>')


# ManyToManyField used because genre can contain many books. Books can cover many genres.
# Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    # Represent a book record
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    # returns a URL that can be used to access a detail record for this
    #  model (we will have to define a URL mapping that has the name 
    # book-detail, and define an associated view and template
    def get_absolute_url(self):
        """Returns the url to access a detailed record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
 #This creates a string from the first three values of the genre field 
 # (if they exist) and creates a short_description that can be used in the admin site for this method.   
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'


#Book instance model
class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1, 
        choices=LOAN_STATUS, 
        blank=True, default='m', 
        help_text='Book availability',
        )
    
    #Defining permissions is done on the model class Meta section, using the permissions field
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),) #we might define a permission to allow a user to mark that a book has been returned as shown:

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
    #borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)
    

#Author model
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'   # this is interpolation remember its different from concatenation




# Notes  N.B.

# 1. CREATING AND MODIFYING RECORDS!! 

# Create a new record using the model's constructor.
#   record = MyModelName(my_field_name="Instance #1")

# Save the object into the database.
#   record.save()

# Access model field values using Python attributes.
#   print(record.id) # should return 1 for the first record.
#   print(record.my_field_name) # should print 'Instance #1'

# Change record by modifying the fields, then calling save().
#   record.my_field_name = "New Instance Name"
#   record.save()

# 2. SEARCHING FOR RECORDS!! QUERIES!!

# We can get all records for a model as a QuerySet, using objects.all().
#   all_books = Book.objects.all()

# Django's filter() method allows us to filter the returned QuerySet to match a specified text or numeric field against particular criteria
# example, to filter for books that contain "wild" in the title and then count them, we could do the following:
#   wild_books = Book.objects.filter(title__contains='wild')
#   number_wild_books = wild_books.count()

# So for example to filter for books with a specific genre pattern, you will have to index to the name through the genre field,
# Will match on: Fiction, Science fiction, non-fiction etc.
#   books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')


