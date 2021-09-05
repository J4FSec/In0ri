from crontab import CronTab
from hashlib import md5
from os import environ

my_cron = CronTab(user=environ.get("USER"))


def create(domain, time, email):
    command = f"python3 /opt/In0ri/main.py {domain} {email}"
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
    if check == 1:
        print("This domain avaliable!")
    else:
        job = my_cron.new(command=command, comment=comment)
        job.minute.every(time)
        my_cron.write(user=environ.get("USER"))
        print(job.is_valid())


def edit(domain, time, email):
    command = f"python3 /opt/In0ri/main.py {domain} {email}"
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
            my_cron.remove(job)
            job = my_cron.new(command=command, comment=comment)
            job.minute.every(time)
            my_cron.write(user=environ.get("USER"))
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
            my_cron.write(user=environ.get("USER"))
            print("Sucessfull!")
    if check == 0:
        print("Domain not found!")

