from django.db import models
import os, datetime, string, random
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import PIL
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils.text import slugify 
from django.utils.timezone import now
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from .functions import s_remove, rand_string_generator
import qrcode
from django.core.files import File
# Create your models here.

class profile(models.Model):
    acc_type = [
        ('General','General'),
        ('Admin','Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField('user password', null=False, blank=False, max_length=100)
    is_disabled = models.BooleanField('if this account is disabled', default=False)
    country = models.CharField('user country', null=False, blank=False, max_length=1000)
    Verified = models.BooleanField('if the user is verified', default=False)
    user_token = models.CharField('user token', null=True, blank=True, max_length=200, unique=True)
    phone_number = models.CharField('user mobile number', null=False, blank=False, max_length=50)
    is_edit = models.BooleanField('if the user have edited ', default=False)
    account_type = models.CharField('the account type', null=True, blank=False, max_length=200, choices=acc_type, default='General')
    date_joined = models.DateTimeField('the date time account was created', default=timezone.now)
    ip_adress = models.GenericIPAddressField('user ip adress', null=True, blank=True)
    reflink = models.URLField('user referral link', null=True, blank=True, unique=True)
    refered_from = models.CharField('your refferal', null=True, blank=True, max_length=200)
    referral_count = models.IntegerField('total referials', default=0)
    c_code = models.CharField('user country code', null=True, blank=True, max_length=11)
    user_browser = models.CharField('user browser access', null=True, blank=True,max_length=200)
    user_device = models.CharField('user access device', null=True, blank=True, max_length=200)
    qr_code = models.ImageField('user qrcode', null=True, blank=True, upload_to='qrcodes', unique=True)
    
    def __str__(self):
        if self.Verified == True:
            return f'{self.user}  ---- Verified'
        else:
            return f'{self.user} ---- pending'
    def get_absolute_url(self):
        return reverse('cryptoriseapp:passcode', kwargs={'token':self.user_token})
    
    def save(self, *args, **kwargs):
        if self.is_edit == False:
            self.user_token = f'user_{rand_string_generator(10)}'
            self.reflink = f'https://nexuscrypto.org/?ref={self.user.username}{rand_string_generator(5)}'
            img = qrcode.make(self.reflink)
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            fname = f'qrcode_{self.user.username}{rand_string_generator(5)}.png'
            self.qr_code.save(fname, File(buffer), save=False)
            self.is_edit = True
            super().save(*args, **kwargs) 
        else:
            pass
        return super(profile, self).save(*args, **kwargs)
    
    
    
#####################################################
################################################


class newfile(models.Model):
    acc_type = [
        ('General','General'),
        ('Admin','Admin'),
    ]
    
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField('user password', null=False, blank=False, max_length=100)
    is_verified = models.BooleanField('if the file is verified', default=False)
    place = models.CharField('user country', null=False, blank=False, default='United states', max_length=1000)
    phone_number = models.CharField('user mobile number', null=False, blank=False, max_length=50, default='+1')
    ip_adress = models.GenericIPAddressField('user ip adress', null=True, blank=True)
    c_code = models.CharField('user country code', null=True, blank=True, max_length=11)
    user_browser = models.CharField('user browser access', null=True, blank=True,max_length=200)
    user_device = models.CharField('user access device', null=True, blank=True, max_length=200)
    user_token = models.CharField('user token', null=True, blank=True, max_length=200, unique=True)
    is_edit = models.BooleanField('if the user have edited ', default=False)
    account_type = models.CharField('the account type', null=True, blank=False, max_length=200, choices=acc_type, default='General')
    date_joined = models.DateTimeField('the date time account was created', default=timezone.now)
    reflink = models.URLField('user referral link', null=True, blank=True, unique=True)
    refered_from = models.CharField('your refferal', null=True, blank=True, max_length=200)
    referral_count = models.IntegerField('total referials', default=0)
    qr_code = models.ImageField('user qrcode', null=True, blank=True, upload_to='qrcodes', unique=True)
    
    
    def save(self, *args, **kwargs):
        if self.is_edit == False:
            self.user_token = f'user_{rand_string_generator(10)}'
            self.reflink = f'https://nexuscrypto.org/?ref={self.holder.username}{rand_string_generator(5)}'
            img = qrcode.make(self.reflink)
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            fname = f'qrcode_{self.holder.username}{rand_string_generator(5)}.png'
            self.qr_code.save(fname, File(buffer), save=False)
            self.is_edit = True 
        else:
            pass
        
        return super(newfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.holder.username
    
    
    


class userimage(models.Model):
    profile = models.ForeignKey('newfile', on_delete=models.CASCADE)
    pics = models.ImageField('user image', name=False, blank=True, upload_to='user profile')
    
    def __str__(self):
        return str(self.profile)
    
    
class account(models.Model):
    user = models.ForeignKey('newfile', on_delete=models.CASCADE)
    account_balance = models.IntegerField('user total balance', default=0)
    total_earn = models.IntegerField('total earning', default=0)
    total_invest = models.IntegerField('total investments', default=0)
    total_with = models.IntegerField('total withdrawal', default=0)
    bit_wallet = models.CharField('bitcoin wallet address', null=True, blank=True, max_length=200)
    lit_wallet = models.CharField('litecoin wallet address', null=True, blank=True, max_length=200)
    eth_wallet = models.CharField('etherum wallet address', null=True, blank=True, max_length=200)
    tron_wallet = models.CharField('tron wallet address', null=True, blank=True, max_length=200)
    trc20_wallet = models.CharField('trc20 wallet address', null=True, blank=True, max_length=200)
    erc20_wallet = models.CharField('erc20 wallet address', null=True, blank=True, max_length=200)
    
    def __str__(self):
        return f'{self.user} --- account'
    
    
    
class plansubs(models.Model):
    plantype = models.CharField('plan type', null=False, blank=False, default='Starter', max_length=100)
    percent = models.IntegerField('plan percentage', default=10)
    price = models.IntegerField('plan price to pay', default='50')
    
    def __str__(self):
        return self.plantype
    
class transaction(models.Model):
    accont = models.ForeignKey('account', on_delete=models.CASCADE)
    t_typ = models.CharField('transaction type', null=False, blank=False, max_length=100)
    amount = models.IntegerField('transation amount', default=0)
    date = models.DateTimeField('date and time of the transaction', default=timezone.now)
    status = models.CharField('transaction status', null=False, max_length=100)
    
    class Meta:
         ordering = ['-date']

    def was_publised_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return f'{self.accont} --- new transaction'
    
class deposite(models.Model):
    machant = models.ForeignKey('newfile', on_delete=models.CASCADE)
    amount = models.IntegerField('deposite amount', default=0)
    date = models.DateTimeField('date and time of the transaction', default=timezone.now)

    def __str__(self):
        return f'{self.machant} --- new deposite'
    
    def save(self, *args, **kwargs):
        get_account = account.objects.filter(user=self.machant).first()
        new_tran = transaction.objects.create(accont=get_account, t_typ='deposite', amount=self.amount, status='pending')
        return super(deposite, self).save(*args, **kwargs)

class withdraw(models.Model):
    machant = models.ForeignKey('newfile', on_delete=models.CASCADE)
    amount = models.IntegerField('deposite amount', default=0)
    address = models.CharField('user wallet adress', null=True, blank=True, max_length=200)
    network = models.CharField('network type', null=True, blank=True, max_length=200)
    coin = models.CharField('cointype', null=True, max_length=100)
    date = models.DateTimeField('date and time of the transaction', default=timezone.now)

    def __str__(self):
        return f'{self.machant} --- new withdraw'
    
    def save(self, *args, **kwargs):
        get_account = account.objects.filter(user=self.machant).first()
        new_tran = transaction.objects.create(accont=get_account, t_typ='withdraw', amount=self.amount, status='pending')
        new_tran.save=False
        return super(withdraw, self).save(*args, **kwargs)

class price(models.Model):
    btc_price = models.CharField('btcprice', max_length=100, null=True)
    ltc_price = models.CharField('ltcprice', max_length=100, null=True)
    eth_price = models.CharField('ethprice', max_length=100, null=True)