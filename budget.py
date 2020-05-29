from reportlab.pdfgen import canvas
from datetime import date
from os import listdir, stat, mkdir


##########################################
#   Create timestamp

now = date.today()
ts = f'{now.year}{str(now.month).zfill(2)}{now.day}'


##########################################
#   Create the "budgets" directory if it doesn't exist

path = './presupuestos/'

try:
    stat(path)
except:
    mkdir(path)


##########################################
#   Find last quote and generate next id

files = listdir(path)
if len(files)>0:
    id = 0
    for obj in files:
        obj = obj.replace('.pdf', '')
        obj = obj.replace(f'PRESUPUESTO_{ts}-', '')
        if id < int(obj):
            id = int(obj)
    id += 1
else:
    id = 1

id = str(id).zfill(4)


##########################################
#   Generate the PDF file

filename = f'PRESUPUESTO_{ts}-{id}.pdf'
filename
pdf = canvas.Canvas(f'{path}{filename}')

##########################################
#   Save the PDF file

pdf.save()
