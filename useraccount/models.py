from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager 
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = None
    
    objects = MyAccountManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]

    
# models for all tribes
class Tribe(models.Model):
    tribe = models.CharField(max_length=50)

    def __str__(self):
        return self.tribe

# models for all genders
class Gender(models.Model):
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.gender

# models for all incometypes
class Incometype(models.Model):
    highincometype = models.DecimalField(max_digits=8, decimal_places=2)
    lowincometype = models.DecimalField(max_digits=8, decimal_places=2)
    incometype = models.CharField(max_length=300)

    def __str__(self):
        return self.incometype

# this is used for authentication perposes


# models for all users
class UserProfile(models.Model):
    username  = models.CharField(max_length=200)
    dateOfBirth = models.DateField()
    email =models.OneToOneField(User,on_delete=models.CASCADE,related_name="useremail")
    city = models.CharField(max_length=100)
    phonenumber = models.IntegerField()
    description = models.CharField(max_length=100)
    userGender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    userIncome = models.ForeignKey(Incometype,on_delete=models.CASCADE)
    userTribe = models.ForeignKey(Tribe,on_delete=models.CASCADE)
    zodiacSign = models.CharField(blank=True, max_length=50)

    # method to get zodiac sign for a user 
    def save(self):
        day = int(self.dateOfBirth.strftime('%d'))
        month = str(self.dateOfBirth.strftime('%B'))
        if (day < 10):
            day=10
            
        if month == 'December':
            zodiac = 'Sagittarius' if (day < 22) else 'capricorn'
        elif month == 'January':
            zodiac = 'Capricorn' if (day < 20) else 'aquarius'
        elif month == 'February':
            zodiac = 'Aquarius' if (day < 19) else 'pisces'
        elif month == 'March':
            zodiac = 'Pisces' if (day < 21) else 'aries'
        elif month == 'April':
            zodiac = 'Aries' if (day < 20) else 'taurus'
        elif month == 'May':
            zodiac = 'Taurus' if (day < 21) else 'gemini'
        elif month == 'June':
            zodiac = 'Gemini' if (day < 21) else 'cancer'
        elif month == 'July':
            zodiac = 'Cancer' if (day < 23) else 'leo'
        elif month == 'August':
            zodiac = 'Leo' if (day < 23) else 'virgo'
        elif month == 'September':
            zodiac = 'Virgo' if (day < 23) else 'libra'
        elif month == 'October':
            zodiac = 'Libra' if (day < 23) else 'scorpio'
        elif month == 'November':
            zodiac = 'scorpio' if (day < 22) else 'sagittarius'
        else:
            zodiac = 'no zodiac sign found'  
        self.zodiacSign= zodiac
        super().save()

    def __str__(self):
        return self.username