from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse as json
from django.db.models import F, Q
from django.views.decorators.http import require_GET as re_ge
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required as l_g
from . import models
from PIL import Image
from django.contrib import messages
from user_agents import parse

# Create your views here.
@re_ge
def home(request):
    return render(request, 'home.html', )

@re_ge
def about(request):
    return render(request, 'about.html', )

@re_ge
def faq(request):
    return render(request, 'faq.html',)

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        return render(request, 'login.html', )
    
def useregister(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        return render(request, 'register.html', )

def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        current_uer = models.newfile.objects.filter(holder=user).first()
        image = models.userimage.objects.filter(profile=current_uer).first()
        account = models.account.objects.filter(user=current_uer).first()
        context = {
            'user': current_uer,
            'img': image,
            'account': account,
        }
        return render(request, 'dashboard.html', context=context)
    else:
        return redirect('/login/')
    
def deposite(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'deposite.html',)
    else:
        return redirect('/login/')
    
def withdraw(request): 
    if request.user.is_authenticated:
        user = request.user
        current_uer = models.newfile.objects.filter(holder=user).first()
        image = models.userimage.objects.filter(profile=current_uer).first()
        account = models.account.objects.filter(user=current_uer).first()
        active_widrawal = models.transaction.objects.filter(accont=account).filter(t_typ='withdraw').filter(status='success').order_by('-date')
        pending_withdrawal = models.transaction.objects.filter(accont=account).filter(t_typ='withdraw').filter(status='pending').order_by('-date')
        context = {
            'user': current_uer,
            'img': image,
            'account': account,
            'active': active_widrawal,
            'pending': pending_withdrawal,
        }
        return render(request, 'withdraw.html', context=context)
    else:
        return redirect('/login/')
    
def history(request): 
    if request.user.is_authenticated:
        user = request.user
        current_uer = models.newfile.objects.filter(holder=user).first()
        image = models.userimage.objects.filter(profile=current_uer).first()
        account = models.account.objects.filter(user=current_uer).first()
        history = models.transaction.objects.filter(accont=account).all().order_by('-date')
        try:
            if request.method == 'POST':
                typ = request.POST['transact_type']
                status = request.POST['transact_status']
                day = request.POST['day']
                month = request.POST['month']
                year = request.POST['year']
                user = request.user
                print(month)
                current_uer = models.profile.objects.filter(user=user).first()
                image = models.userimage.objects.filter(profile=current_uer).first()
                account = models.account.objects.filter(user=current_uer).first()
                history = models.transaction.objects.filter(accont=account).filter(t_typ__contains=typ).filter(status__contains=status).filter(date__contains=day).filter(date__contains=year).all().order_by('-date')
                context = {
                'user': current_uer,
                'img': image,
                'account': account,
                'transact': history,
                }
                return render(request, 'transaction.html', context=context)
        except BaseException as e:
            print(e)
        context = {
            'user': current_uer,
            'img': image,
            'account': account,
            'transact': history,
        }
        return render(request, 'transaction.html', context=context)
    else:
        return redirect('/login/')
    
def referral(request):
    if request.user.is_authenticated:
        user = request.user
        current_uer = models.newfile.objects.filter(holder=user).first()
        image = models.userimage.objects.filter(profile=current_uer).first()
        account = models.account.objects.filter(user=current_uer).first()
        context = {
            'user': current_uer,
            'img': image,
            'account': account,
        }
        return render(request, 'referral.html', context=context)
    else:
        return redirect('/login/')
    
def setting(request):
    if request.user.is_authenticated:
        user = request.user
        current_uer = models.newfile.objects.filter(holder=user).first()
        image = models.userimage.objects.filter(profile=current_uer).first()
        account = models.account.objects.filter(user=current_uer).first()
        context = {
            'user': current_uer,
            'img': image,
            'account': account,
        }
        return render(request, 'setting.html', context=context)
    else:
        return redirect('/login/')
    
def planpay(request, plantype, price):
    if request.user.is_authenticated:
        user = request.user
        prices = models.price.objects.filter().first()
        admin = models.newfile.objects.filter(account_type='Admin').first()
        admim_account = models.account.objects.filter(user=admin).first()
        print(admim_account.bit_wallet)
        print(price)
        print(prices.btc_price)
        context = {
            'account': admim_account,
            'price': price,
            'meter': prices
        }
        return render(request, 'payment.html', context=context)
    else:
        return redirect('/login/')

def place_with(request):
    if request.user.is_authenticated:
        return render(request, 'place_withdraw.html')
    else:
        return redirect('/login/')
    
##################################################
## ajax data countrols
####################################################

def sub_plan(request):
    try:
        if request.method == 'POST':
            plan = request.POST['plan']
            percent = request.POST['percent']
            price = request.POST['price']
            
            #new_invetment = models.plansubs.objects.create(plantype=plan, percent=int(percent), price=int(price))
            #new_invetment.save()    
            return json({'S': 'new investment created'}, safe=False)  
        else:
            return json({'S': 'this is not post request'}, safe=False)      
    except BaseException as e:
        print(e)
        
        
def add_img(request):
    if request.user.is_authenticated:
        user = request.user
        current_uer = models.newfile.objects.filter(holder=user).first()
        try: 
            if request.method == 'POST':
                new_img = request.FILES['image']
                currentimg = models.userimage.objects.filter(profile=current_uer).first()
                if currentimg:
                    currentimg.delete()
                    newimage = models.userimage.objects.create(profile=current_uer, pics=new_img)
                    newimage.save()
                    return json({'S': 'New image added successful'}, safe=False)
                else:
                    newimage = models.userimage.objects.create(profile=current_uer, pics=new_img)
                    newimage.save()
                    return json({'S': 'New image added successful'}, safe=False)
            else:
                return json({'E': 'Sorry image cloud not not be addedd'}, safe=False)
        except BaseException as e:
            print(e)
    else:
        return redirect('/login/')
    
def update_pro(request):
    try:
        if request.method == 'POST':
            user = request.user
            full_name = request.POST['fname']
            phone = request.POST['phone']
            newemail = request.POST['email']
            country = request.POST['country']
            c_code = request.POST['code']
            bitcoin = request.POST['bit']
            litcoin = request.POST['lit']
            etherum = request.POST['eth']
            tron = request.POST['tron']
            trc20 = request.POST['trc']
            erc20 = request.POST['erc']
            current_user = models.newfile.objects.filter(holder=user).first()
            main_user = User.objects.filter(username=current_user.holder.username).first()
            user_account = models.account.objects.filter(user=current_user).first()
            if current_user:
                models.newfile.objects.filter(holder=user).update(phone_number=phone, place=country, c_code=c_code)
                User.objects.filter(username=current_user.holder.username).update(email=newemail, first_name=full_name)
                models.account.objects.filter(user=current_user).update(bit_wallet=bitcoin, lit_wallet=litcoin, eth_wallet=etherum, tron_wallet=tron, trc20_wallet=trc20, erc20_wallet=erc20) 
                current_user.refresh_from_db()
                main_user.refresh_from_db()
                user_account.refresh_from_db()    
                return json({'S': 'Profile updated successful'}, safe=False)
            else:
                return json({'E': 'User does not exist'}, safe=False)
        else:
            return json({'E': 'Post request error'}, safe=False)  
    except BaseException as e:
        print(e)
        
        
def update_pass(request):
    try:
        if request.method == 'POST':
            newpassword = request.POST['passwd']
            user = request.user
            main_user = User.objects.filter(username=user.username).first()
            current_user = models.newfile.objects.filter(holder=user).first()
            if main_user:
                main_user.set_password(raw_password=newpassword)
                models.newfile.objects.filter(holder=user).update(password=newpassword)
                main_user.save()
                main_user.refresh_from_db()
                current_user.refresh_from_db()
                return json({'S': 'Password updated successful'}, safe=False)
            else:
                return json({'E': 'Sorry this user is not loged in'}, safe=False)
        else:
            return json({'E': 'Post error occurd'}, safe=False)
    except BaseException as e:
        print(e)
    
def user_register(request):
    try:
        if request.method == 'POST':
            username = request.POST['uname']
            full_name = request.POST['fname']
            phone = request.POST['phone'] 
            email = request.POST['email']
            country = request.POST['country']
            _code = request.POST['code']
            bitcoin = request.POST['bit'] 
            litecoin = request.POST['lit'] 
            etherum = request.POST['eth']
            tron = request.POST['tron']
            trc20 = request.POST['trc']
            erc20 = request.POST['erc']
            password = request.POST['passwd']
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
            browser = user_agent.browser.family
            browser_version = user_agent.browser.version_string
            os = user_agent.os.family
            device = user_agent.device.family
            device_brand = user_agent.device.brand
            x_forward = request.META.get('HTTP_X_FORWARDER_FOR')
            if x_forward is not None:
                ip = x_forward.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            validate_user = User.objects.filter(username=username).first()
            validate_email = User.objects.filter(email=email).first()
            if validate_user:
                return json({'E': 'Sorry this username is already taken'}, safe=False)
            elif validate_email:
                return json({'E': 'Sorry this email is already taken'}, safe=False)
            else:
                pass
            new_user = User.objects.create_user( username=username, email=email, password=password)
            new_user.first_name = full_name
            new_user.save()
            auth_user = User.objects.filter(username=username).first()
            if auth_user:
                new_holder = models.newfile.objects.create(holder=auth_user, password=password, is_verified=True, place=country, phone_number=phone, ip_adress=ip, c_code=_code, user_browser=f'{browser}, {browser_version}', user_device=device)
                new_holder.save()
                get_newholder = models.newfile.objects.filter(holder=auth_user).first()
                new_account = models.account.objects.create(user=get_newholder, bit_wallet=bitcoin, lit_wallet=litecoin, eth_wallet=etherum, tron_wallet=tron, trc20_wallet=trc20, erc20_wallet=erc20)
                new_account.save()
                print('User login succesfully!!!')
                this_user = authenticate(request, username=username, password=password)
                login(request, this_user)
                ### send mail here #########################
                ############################################
                return json({'S': 'User created successful'}, safe=False)
            else:
               return json({'E': 'Sorry user could not be created'}, safe=False)
        else:
            return json({'E': 'Sorry not post request'}, safe=False)
    except BaseException as e:
        print(e)
        return json({'E': 'Sorry user could not be created'}, safe=False)
    
    
def login_user(request):
    try:
        if request.method == 'POST':
            user_name = request.POST['uname']
            passwd = request.POST['passwd']

            valid = User.objects.filter(username__exact=user_name).first()
            if valid is not None:
                this_user = authenticate(request, username=user_name, password=passwd)
                login(request, this_user)
                print('\n============\n  you are now logged in \n=============\n')
                return(json({'S':'Logged in sucessfully'}, safe=False))
            else:
                print('\n============\n  sorry this user is invalid \n=============\n')
                return(json({'E': 'sorry this user is invalid'}, safe=False))
        else:
            print('\n============\n  sorry this user is invalid \n=============\n')
            return(json({'E':'Post error ocurred'}, safe=False))
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, AttributeError) as err:
         print(err)
         return(json({'E': 'Invalid email or password!'}, safe=False))


def deleteuser(request):
    if request.user.is_authenticated:
        user = request.user
        get_user = User.objects.filter(username=user.username).first()
        if get_user:
            User.objects.filter(username=user.username).delete()
            return redirect('/')
        else:
            pass
    else:
        return redirect('/login/')
    
def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('/')
    else:
        pass
    

def comfirm_d(request):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                amount = request.POST['amount']
                user = request.user
                profile = models.newfile.objects.filter(holder=user).first()
                new_deposite = models.deposite.objects.create(machant=profile, amount=amount)
                new_deposite.save()
                return json({'S': 'Please wait why we confirm payment'}, safe='False')
            else:
                return json({'E': 'Post error occured'}, safe=False)
        except BaseException as e:
            print(e)
            return json({'E': 'Deposite Failed'}, safe=False)
    else:
        return redirect('/login/')
    
def place_wit(request):
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                user = request.user
                coin_type = request.POST['coin']
                network = request.POST['network']
                amount = request.POST['amount']
                address = request.POST['address']
                profile = models.newfile.objects.filter(holder=user).first()
                new_withdraw = models.withdraw.objects.create(machant=profile, amount=amount, address=address, network=network, coin=coin_type)
                new_withdraw.save()
                return json({'S': 'Withdrawal place whill be send in 15min'}, safe=False)
            else:
                return json({'E': 'Post error occured'}, safe=False)
        except BaseException as e:
            print(e)
            return json({'E': 'Withdrawal Failed'}, safe=False)
    else:
        return redirect('/login/')