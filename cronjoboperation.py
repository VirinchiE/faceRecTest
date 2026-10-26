import os
from microface import microface
from m1cr0face.settings import GET_EMPLOYEE_DETAILS

def cronDeleteJobs():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm1cr0face.settings')
    microface.findStatusAndDelete(GET_EMPLOYEE_DETAILS)

if __name__ == '__main__':
    cronDeleteJobs()
