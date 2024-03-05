from ast import If
from asyncio.windows_events import NULL
from contextvars import Context
from django.utils import timezone
from django.http import HttpResponse
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Role, Department, Announcement
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q

#logout
def myLogout(request):
    logout(request)
    return redirect('login')

# login
def myLogin(request):

    if request.method == 'POST':
        username = request.POST['loginUsername']
        password = request.POST['loginPassword']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'myapp/login.html')

    else:
        return render(request, 'myapp/login.html')




# Home Page
def index(request):

    totalEmployees = Employee.objects.filter(status='employee').count()
    totalManagers = Employee.objects.filter(status='manager').count()
    totalDepartments = Department.objects.all().count()
    
    user = Employee.objects.get(user=request.user)
    if user.status == 'employee':
        userSalary = user.salary
        userBonus = user.bonus
        context = {
            'authUser': user,
            'totalEmp': totalEmployees,
            'totalMan': totalManagers,
            'userSalary': userSalary,
            'userBonus': userBonus,
            'photo': user.photo,
            'totalDep': totalDepartments,
        }
    elif user.status == 'manager':
        userSalary = user.salary
        userBonus = user.bonus
        userExtraBonus = user.extra_bonus
        context = {
            'authUser': user,
            'totalEmp': totalEmployees,
            'totalMan': totalManagers,
            'userSalary': userSalary,
            'userBonus': userBonus,
            'userExtraBonus': userExtraBonus,
            'photo': user.photo,
            'totalDep': totalDepartments,
        }

    return render(request, 'myapp/index.html', context)


# display all Employees
def all_emp(request):

    user = Employee.objects.get(user=request.user)
    if 'searchButton' in request.GET:
        searchedEmp = request.GET['search']
        employee = Employee.objects.filter(first_name__icontains = searchedEmp)
        #employee = Employee.objects.filter(Q(first_name__icontains = searchedEmp) | Q(last_name__icontains = searchedEmp))

        context = {
            'authUser': user,
            'emps': employee,
            'photo': user.photo,
        }

    else:
        emps = Employee.objects.all()
        context = {
            'authUser': user,
            'emps': emps,
            'photo': user.photo,
        }
    # print(context)
    return render(request, 'myapp/all_emp.html', context)


# Add Employees
def add_emp(request):

    user = Employee.objects.get(user=request.user)

    if request.method == 'POST':

        #----------------
        departement_name = get_object_or_404(Department, id=request.POST['dept'])
        role_name = get_object_or_404(Role, id=request.POST['role'])

        first_name = request.POST['first_name']
        last_name = request.POST['second_name']
        dept = departement_name
        salary = request.POST['salary']
        bonus = request.POST['bonus']
        status = request.POST['status']
        extra_bonus = request.POST['extra_bonus']
        role = role_name
        hire_date = request.POST['hire_date']
        new_employee = Employee(first_name=first_name, last_name=last_name, dept=dept, salary=salary, bonus=bonus, status=status, extra_bonus=extra_bonus, role=role, hire_date=hire_date)
        new_employee.save()

        context = {
            'authUser': user,
            'photo': user.photo,
        }

        return render(request, 'myapp/add_emp.html', context)

    elif request.method == 'GET':

        department = Department.objects.all()
        role = Role.objects.all()

        context = {
            'authUser': user,
            'photo': user.photo,
            'department': department,
            'roles':role,
        }

        return render(request, 'myapp/add_emp.html', context)

    else:
        return HttpResponse('Exception : Employee has not been added!')


# remove Employee
def remove_emp(request, emp_id):
    empDelete = Employee.objects.get(id=emp_id)
    empDelete.delete()
    return all_emp(request)



# update Employee
def update_emp(request, emp_id = 0):

    user = Employee.objects.get(user=request.user)

    if request.method == 'POST':

        emp = Employee.objects.get(id=emp_id)

        departement_name = Department.objects.get(id=request.POST['dept'])
        role_name = Role.objects.get(id=request.POST['role'])

        emp.first_name = request.POST['first_name']
        emp.last_name = request.POST['second_name']
        emp.dept = departement_name
        emp.salary = request.POST['salary']
        emp.bonus = request.POST['bonus']
        emp.status = request.POST['status']
        emp.extra_bonus = request.POST['extra_bonus']
        emp.role = role_name
        emp.hire_date = request.POST['hire_date']
        emp.save()

        return redirect('all_emp')

    elif request.method == 'GET':

        department = Department.objects.all()
        role = Role.objects.all()
        employee = Employee.objects.get(id=emp_id)
        context = {
            'authUser': user,
            'photo': user.photo,
            'employee' : employee,
            'department' : department,
            'roles' : role
        }

        return render(request, 'myapp/update_emp.html', context)


# displays announcements
def announcements(request):

    user = Employee.objects.get(user=request.user)

    anounc = Announcement.objects.all().order_by('-anc_date')
    context = {
        'authUser': user,
        'anouncements': anounc,
        'photo': user.photo
    }

    return render(request, 'myapp/announcement.html', context)


# add announcement
def add_announcement(request):

    user = Employee.objects.get(user=request.user)

    if request.method == 'POST':
        admin = request.user
        title = request.POST['anouncTitle']
        description = request.POST['anouncDescription']

        new_announcement = Announcement(anc_title=title, anc_description=description, anc_date=timezone.now(), anc_admin=admin)
        new_announcement.save()

        return redirect('announcements');

    elif request.method == 'GET':

        context = {
            'authUser': user,
            'photo':user.photo,
        }
        return render(request, 'myapp/add_announcement.html', context)


# Departements
def departments(request):

    user = Employee.objects.get(user=request.user)

    departments = Department.objects.all()
    context = {
        'authUser': user,
        'departs': departments,
        'photo': user.photo,
    }

    return render(request, 'myapp/departments.html', context)


# Department
def department(request, dep):

    user = Employee.objects.get(user=request.user)

    department = Department.objects.get(dep_name=dep)
    employeeDepartment = Employee.objects.filter(dept=department)
    context = {
        'authUser': user,
        'emps': employeeDepartment,
        'department': department,
        'photo': user.photo,
    }

    return render(request, 'myapp/department.html', context)


# Salary
def salary(request):

    user = Employee.objects.get(user=request.user)

    totalSalary = user.bonus + user.extra_bonus + user.salary
    context = {
        'authUser': user,
        'baseSalary': user.salary,
        'bonus': user.bonus,
        'extraBonus': user.extra_bonus,
        'totalSalary': totalSalary,
        'photo': user.photo,
    }

    return render(request, 'myapp/salary.html', context)