from django.shortcuts import render,redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm, UserInfoForm , LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import UserInfo

def user_login(request):
    # If POST Validate data, if GET, send a login page
    if request.method == 'POST':
        # Get POST data from frontend
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # cleaned_data will return valid data as a dict, ignore invalid property
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    messages.success(request, "با موفقیت وارد شدید")
                    return redirect(reverse("articles:list"))
            else:
                messages.error(request, "نام کاربری یا رمز عبور نادرست است")
                return redirect(reverse('login'))
        else:
            return HttpResponse("Invalid login")

    if request.method == 'GET':
        # Create a empty login form
        login_form = LoginForm()
        return render(request, "users/login.html", {"form": login_form})


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('articles:list')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            
        return super(RegisterView, self).form_valid(form)

@login_required(login_url='/accounts/login/')
def edit_info(request):
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') \
        else UserInfo.objects.create(user=request.user)

    if request.method == 'POST':
        userinfo_form = UserInfoForm(request.POST, request.FILES)
        if userinfo_form.is_valid():
            userprofile = userinfo_form.save(commit=False)
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('articles:list')
    else:
        userinfo_form = UserInfoForm(initial={"about": userinfo.about,
                                                "phone": userinfo.phone,
                                                "photo": userinfo.photo})
        return render(request, "users/edit_info.html", {"userinfo_form": userinfo_form})

# class MyLoginView(LoginView):
#     template_name = 'users/login.html'
#     redirect_authenticated_user = True
    
#     def get_success_url(self):
#         return reverse_lazy('bloghome') 
    
#     def form_invalid(self, form):
#         messages.error(self.request,'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))