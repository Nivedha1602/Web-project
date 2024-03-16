from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .models import FormData,FieldData
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from .models import User
from django.contrib import messages


@csrf_exempt
def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            project_name = form.cleaned_data['project_name']
            password = form.cleaned_data['password']
            User.objects.create(name=name, project_name=project_name, password=password)
            
            messages.success(request, 'Signed up successfully!')
            
            return redirect('signup' ) 
    
    return render(request, 'signup.html', {'form': form})

@csrf_exempt
def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            password = login_form.cleaned_data['password']
            username = login_form.cleaned_data['username']
            user = User.objects.filter(username=username, password=password).first()
            if user:
                
                return redirect('home') 
            else:
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    login_form.add_error('password', 'Invalid password.')
                else:
                    login_form.add_error('username', 'User is not registered.')

    return render(request, 'login.html', {'login_form': login_form})

def home(request):
    
    return render (request,'home.html')

from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Project, FormData, FieldData

@csrf_exempt
def submit_form_data(request):
    if request.method == 'POST':
        try:
            form_data_list = []
            items_list = list(request.POST.items())
            
            project_name = request.POST.get('project_name', '')  # Get project name from request data

            # Check if the project name already exists in the database
            if Project.objects.filter(name=project_name).exists():
                return JsonResponse({'success': False, 'error': 'Project name already exists'})

            project = Project.objects.create(name=project_name)  # Create a new project
            
            for (key1, value1), (key2, value2) in zip(items_list[::2], items_list[1::2]):
                if key1.startswith('form') and key2.endswith('path'):
                    form_key = key1
                    forms_name = value1 
                    Rediretpath_name = value2
                 
                    form_data = {
                        'project': project,
                        #'project_name': project_name,
                        'form_key': form_key,
                        'forms_name': forms_name,
                        'Rediretpath_name': Rediretpath_name,
                    }

                    form_instance = FormData.objects.create(**form_data)
                    form_id = form_instance.id

                    for i, (key, value) in enumerate(items_list):
                        if 'field' in key and key.startswith(form_key) and 'field' in key and 'required' not in key and  'readable' not in key:
                            field_key = key
                            field_value = value
                            selection_value = items_list[i + 1][1] if i + 1 < len(items_list) else None

                            required = False
                            readable = False
                            for k, value in items_list[i:]:
                                if 'required' in k:
                                    required = value
                                    
                                if 'readable' in k:
                                    readable = value
                                
                                if required and readable:
                                    break

                            field_data = {
                                #'form_data': form_instance,
                                'form_id': form_id,
                                'project': project,
                                #'project_name': project_name,
                                'field_key': field_key,
                                'field_value': field_value,
                                'selection_value': selection_value,
                                'required': required,
                                'readable': readable,
                            }
                            form_data_list.append(field_data)

            for field_data in form_data_list:
                FieldData.objects.create(**field_data)

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def check_project_name(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name', '')
        exists = Project.objects.filter(name=project_name).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})
def fetch_data(request):
    project = Project.objects.all().values()
    form_data = FormData.objects.all().values()
    field_data = FieldData.objects.all().values()
    return JsonResponse({'form_data': list(form_data), 'field_data': list(field_data),'project': list(project)})



def delete_data(request):
    project_name = request.POST.get('project_name')
    try:
        project = Project.objects.get(name=project_name)
        form_data = FormData.objects.filter(project=project).delete()
        field_data = FieldData.objects.filter(project=project).delete()
        project.delete()
        return JsonResponse({'success': True})
    except Project.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Project not found'})