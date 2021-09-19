from hashlib import md5
from getpass import getuser


from crontab import CronTab

user = getuser()
my_cron = CronTab(user=user)


def create(domain, email, hours=None, minutes=None):
    command = f"python3 /opt/In0ri/main.py {domain} {email}"
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
        my_cron.write(user=user)
        print(job.is_valid())


def edit(domain, email, hours=None, minutes=None):
    command = f"python3 /opt/In0ri/main.py {domain} {email}"
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
            my_cron.write(user=user)
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
            my_cron.write(user=user)
            print("Sucessfull!")
    if check == 0:
        print("Domain not found!")

