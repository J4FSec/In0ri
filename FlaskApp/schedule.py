from hashlib import md5
from os import environ

from crontab import CronTab

user = environ.get("USER")
my_cron = CronTab(user=user)


def create(domain, email, hours=None, minutes=None):
    command = f"python3 /opt/In0ri/main.py {domain} {email} >> /var/log/cron.log 2>&1"
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
    if check == 1:
        print("This domain is avaliable!")
    else:
        job = my_cron.new(command=command, comment=comment)
        if hours is not None:
            job.hour.every(hours)
        if minutes is not None:
            job.minute.every(minutes)
        my_cron.write(user='root')
        print(job.is_valid())


def edit(domain, email, hours=None, minutes=None):
    command = f"python3 /opt/In0ri/main.py {domain} {email} >> /var/log/cron.log 2>&1"
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
            my_cron.remove(job)
            job = my_cron.new(command=command, comment=comment)
            if hours is not None:
                job.hour.every(hours)
            if minutes is not None:
                job.minute.every(minutes)
            my_cron.write(user='root')
            print("Sucessfull!")
    if check == 0:
        print("Domain not found!")


def delete(domain):
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
            my_cron.remove(job)
            my_cron.write(user='root')
            print("Sucessfull!")
    if check == 0:
        print("Domain not found!")

