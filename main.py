import PySimpleGUI as sg
import random
from PIL import Image
import os
import base64
from io import BytesIO
import numpy as np
import time
# Convert Image to Base64 

images=[Image.open('images/'+i).resize((128,128)) for i in os.listdir('images/')]

byte_im=[]
bio = BytesIO()
temp=Image.open('images/fon.jpg').resize((128,128))
temp.save(bio,format='PNG')
fon=bio.getvalue()
for i in images:
    bio = BytesIO()
    i.save(bio,format='PNG')
    byte_im.append(bio.getvalue())
    bio.close()

def prepare(k):
    if(k==13 or k==11 or k==17):
        k-=1
    seed=random.randint(0,10000000)
    temp8=random.sample(byte_im,k)
    mask=[i for i in range(len(temp8))]
    temp=temp8*2
    mask*=2
    random.Random(seed).shuffle(temp)
    random.Random(seed).shuffle(mask)
    gameImages=np.array(temp)
    if(k<5):
        k=int(k/2)
    elif(k%3==0):
        k=int(k/3)
    elif(k%4==0):
        k=int(k/2)
    elif(k%8==0):
        k=int(k/4)
    elif(k>10):
        k=int(k/4)
    gameImages=gameImages.reshape((-1,k))
    mask=np.array(mask)
    mask=mask.reshape((-1,k))
    print(mask)
    print(gameImages.shape)
    return temp8,mask,gameImages,gameImages.shape[1],gameImages.shape[0]

start_layout=[[sg.Text('Num pictures', size=(15, 1)), sg.Spin(values=[i for i in range(1, 19)], initial_value=4, size=(6, 1),key=0),      
               sg.Text('Show time', size=(18, 1)), sg.Spin(values=[i for i in range(0, 100)], initial_value=3, size=(6, 1),key=2)],[sg.Button('Start',key=1)]]
window = sg.Window('Start', start_layout)
choosen_size=False
start=False
was_first_pic=False
first_pic_ind=(-1,-1)
first_pic_val=-1
mistakes=0
is_over=False
num_dis=0
while True:
    event, values = window.read(timeout=100)
    if not start and choosen_size:
        time.sleep(wait)
        for i in range(MAX_ROWS):
           for j in range(MAX_COL):
               window[(i,j)].update(image_data=fon)  
        start=True
        timeout=200
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event not in (sg.TIMEOUT_EVENT,'E') and  choosen_size and event!='new':
        print(event)
        if(not was_first_pic):
            first_pic_ind=event
            first_pic_val=mask[event[0]][event[1]]
            window[event].update(image_data=temp8[mask[event[0]][event[1]]])
            was_first_pic=True
        else:
            was_first_pic=False
            second_pic_ind=event
            second_pic_val=mask[event[0]][event[1]]
            if(second_pic_val!=first_pic_val):
                mistakes+=1
                window[second_pic_ind].update(image_data=fon)
                window[first_pic_ind].update(image_data=fon)
            else:
                num_dis+=2
                window[second_pic_ind].update(image_data=temp8[second_pic_val],disabled=True)
                window[first_pic_ind].update(image_data=temp8[first_pic_val],disabled=True)

    if event == 1:
        choosen_size=True
        k=int(values[0])
        wait=int(values[2])
        temp8,mask,gameImages,MAX_COL,MAX_ROWS=prepare(k) 
        layout= [[sg.Button(image_data=gameImages[i,j], size=(128, 128), key=(i,j), pad=(0,0)) for j in range(MAX_COL)] for i in range(MAX_ROWS)]
        window.close()
        window=sg.Window(layout=layout,title='Puzzle')
    
    if(start and num_dis==MAX_ROWS*MAX_COL):
        num_dis=0
        result_layout=[[sg.Text(f'You got {mistakes} mistakes')],[sg.Button(button_text='New game',k='new')]]
        window.close()
        window=sg.Window(title='Results',layout=result_layout)
    if event=='new':
        window.close()
        new_lay=[[sg.Text('Num pictures', size=(15, 1)), sg.Spin(values=[i for i in range(1, 20)], initial_value=4, size=(6, 1),key=0),      
               sg.Text('Show time', size=(18, 1)), sg.Spin(values=[i for i in range(0, 100)], initial_value=3, size=(6, 1),key=2)],[sg.Button('Start',key=1)]]
        window = sg.Window(title='Start', layout=new_lay)
        choosen_size=False
        start=False
        was_first_pic=False
        first_pic_ind=(-1,-1)
        first_pic_val=-1
        mistakes=0
        is_over=False
        num_dis=0

    
window.close()