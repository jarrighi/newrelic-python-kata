from random import randint
from os import environ

def run_django_commands(*args):
    environ.setdefault("DJANGO_SETTINGS_MODULE", "newrelic_python_kata.settings")
    from django.core.management import call_command
    for command in args:
        call_command(command, interactive=False)

def populate_db():
    environ.setdefault("DJANGO_SETTINGS_MODULE", "newrelic_python_kata.settings")
    from employees.models import Employee, BioData, Payroll
    with open('names.txt') as f: 
        es = []
        bs = []
        ps = []
        for idx, line in enumerate(f):
            name, sex, salary = line.rstrip('\r\n').split(',')
            e = Employee(name=name, employee_id=(idx+1))
            b = BioData(employee=e, age=randint(18, 40), sex=sex)
            p = Payroll(employee=e, salary=salary)
            es.append(e)
            bs.append(b)
            ps.append(p)

    Employee.objects.bulk_create(es)
    BioData.objects.bulk_create(bs)
    Payroll.objects.bulk_create(ps)
            
if __name__ == '__main__':
    print 'INFO: Setting up Django DB'
    run_django_commands('syncdb')
    print 'INFO: Populating the database.'
    populate_db()
    print 'INFO: All done!'
    print 'INFO: Start your server.'
    print 'newrelic-admin run-python manage.py run_gunicorn'
