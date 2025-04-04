from django.urls import path, include # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),  #For Django class-based views we access an appropriate view function by calling the class method as_view()
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), #<int:pk>' to capture the book id
    #re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'), code can replace the immediate top line but thats if you prefer this regular expression primer
    #regular expressions should usually be declared using the raw string literal syntax. And they are powerful mapping tools.
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]
#A URL pattern, which is an empty string: ''. We'll discuss URL patterns in detail when working on the other views.
#A view function that will be called if the URL pattern is detected: views.index, which is the function named index() in the views.py file.
#The path() function also specifies a name parameter, which is a unique identifier for this particular URL mapping

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

#The URL configuration will redirect URLs with the format /catalog/book/<bookinstance_id>/renew/ to the function named renew_book_librarian() in views.py, 
# and send the BookInstance id as the parameter named pk. The pattern only matches if pk is a correctly formatted uuid.
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

urlpatterns += [
    path('borrowed/', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
]
