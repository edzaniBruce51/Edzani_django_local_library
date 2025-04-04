from django.test import TestCase # type: ignore
from catalog.models import Author

# Create your tests here.
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)       # Get an author object to test
        field_label = author._meta.get_field('first_name').verbose_name         # # Get the metadata for the required field and use it to query the required field data
        self.assertEqual(field_label, 'first name')     # Compare the value to the expected result

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

#We also need to test our custom methods a few listed below.

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

#Note: You should not normally include print() functions in your tests as shown above.
# We do that here only so that you can see the order that the setup functions are called in the console (in the following section).

#The interesting things to note are:

#We can't get the verbose_name directly using author.first_name.verbose_name, because author.first_name is a string (not a handle to the first_name object that we can use
# to access its properties). Instead we need to use the author's _meta attribute to get an instance of the field and use that to query for the additional information.
#We chose to use assertEqual(field_label,'first name') rather than assertTrue(field_label == 'first name'). The reason for this is that if the test fails the output for 
# the former tells you what the label actually was, which makes debugging the problem just a little easier