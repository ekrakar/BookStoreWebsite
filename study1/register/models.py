from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
import uuid
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItems(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('BookInstance', on_delete=models.CASCADE)


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailing_Address = models.CharField(max_length=200, blank=True)
    billing_Address = models.CharField(max_length=200, blank=True)


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CARD_TYPES = {
        ("V", "Visa"),
        ("M", "MasterCard"),
        ("D", "Discover"),
        ("A", "American Express"),
    }
    credit_Card_Type = models.CharField(max_length=1, choices=CARD_TYPES, blank=True)
    credit_Card_Number = models.CharField(max_length=20, blank=True)
    expiration_Date = models.DateField(blank=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    SUBJECT_LIST = (
        ('M', 'Math'),
        ('H', 'History'),
        ('C', 'Computer Science'),
        ('E', 'English'),
    )
    subject = models.CharField(max_length=1, choices=SUBJECT_LIST, blank=True, default='M')
    course_number = models.CharField(max_length=7, null=True)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='book_covers', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    CONDITION_LIST = (
        ('N', 'New'),
        ('G', 'Good'),
        ('A', 'Acceptable'),
    )
    condition = models.CharField(max_length=1, choices=CONDITION_LIST, blank=True, default='N')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Professor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


def create_info(sender, **kwargs):
    if kwargs['created']:
        user_info = UserInfo.objects.create(user=kwargs['instance'])


post_save.connect(create_info, sender=User)