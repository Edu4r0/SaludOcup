from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import client, file, tools
from pydrive.drive import GoogleDrive
from apiclient import discovery
from httplib2 import Http
from datetime import date
import customtkinter
from PIL import Image
import tkinter
import wget
import os


#------------------VENTANA-----------------
ventana = customtkinter.CTk()

ancho = 358
alto = 521
x=ventana.winfo_screenwidth() // 2 - ancho // 2
y=ventana.winfo_screenheight() // 2 - alto // 2

posicion = str(ancho)+"x"+str(alto)+"+"+str(x)+"+"+str(y)

ventana.geometry(posicion)
ventana.overrideredirect(True)

curr_date = str(date.today())
print(curr_date)

imagen_1 = customtkinter.CTkImage(light_image=Image.open("image/ergonomico1.png"), 
                                  dark_image=Image.open("image/ergonomico1.png"), size=(88, 85))

dowload = customtkinter.CTkImage(light_image=Image.open("image/image 3.png"),
                                       dark_image=Image.open("image/image 3.png"), size=(40,40))

google = customtkinter.CTkImage(light_image=Image.open("image/image 5.png"),
                                       dark_image=Image.open("image/image 5.png"), size=(30,30))

find = customtkinter.CTkImage(light_image=Image.open("image/buscar.png"),
                                       dark_image=Image.open("image/buscar.png"), size=(40,40))

unpload = customtkinter.CTkImage(light_image=Image.open("image/image 8.png"),
                                       dark_image=Image.open("image/image 8.png"), size=(40,40))

exit = customtkinter.CTkImage(light_image=Image.open("image/exit_black.png"),
                                       dark_image=Image.open("image/exit_black.png"), size=(40,40))

banner = customtkinter.CTkImage(light_image=Image.open("image/Vector.png"),
                                       dark_image=Image.open("image/Vector.png"), size=(279,646))
#------------------FRAME-----------------
frame = customtkinter.CTkFrame(ventana,width=331, height=495, corner_radius=10)
frame.pack(padx=5, pady=15,anchor=tkinter.CENTER)

##------------------PANEL-----------------
def panel():
    user = (usuario.get())
    print(user)

    passw = (contraseña.get())
    print(passw)

    if (user,passw) == ('e','e'):
        print('CONTRASEÑA CORRECTA')
        ventana.destroy()
        ventana_1 = customtkinter.CTk()
        alto = 683
        ancho = 958
        y=ventana_1.winfo_screenwidth() // 2 - ancho // 2
        h=ventana_1.winfo_screenheight() // 2 - alto // 2
        posicion1 = str(ancho)+"x"+str(alto)+"+"+str(y)+"+"+str(h)
        ventana_1.geometry(posicion1)
        ventana_1.title('SaludOcup')
        ventana_1.maxsize(958,683)
        ventana_1.minsize(958,683)
        

        #--------------CONSULT FORMS ---------------------------------
        def consult_forms():

            def authenticate():
                SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
                flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
                credentials = flow.run_local_server(port=0)
                return credentials

            def get_forms():
                try:
                    credentials = authenticate()
                    service = build('drive', 'v3', credentials=credentials)
                    query = "mimeType='application/vnd.google-apps.form'"
                    results = service.files().list(q=query, fields='nextPageToken, files(id, name)').execute()
                    forms_list = results.get('files', [])
                    return forms_list
                except HttpError as error:
                    print(f'An error occurred: {error}')
                    return None
                
            forms = get_forms()
            global respuest
            if forms is not None:
                for form in forms:
                    result=(f'Form Name: {form["name"]}\nForm Id: {form["id"]}\n\n')
                    respuest = str(result)
                    tex_name_id.insert("0.0",respuest)

#-------------------------------------------------------------------------------------
        def unpload_form():
        
            form = form_unpload.get()

            fech = fecha1.get()

            file = open('hello.txt', 'w')
            file.write('{}\n'.format(form))
            file.write('{}'.format(fech))
            file.close()

            drive = GoogleDrive()
            file1 = drive.CreateFile({'id':'1UJhTa7V5vgx00hmpS6fr9ZJTJoQqMKAn'})
            file1.SetContentFile("hello.txt")
            file1.Upload()

        def unpload_image():
            username = os.getenv("USERNAME")
            dir = os.path.isdir(f'C:/Users/{username}/Documents/IMAGE')
            
            if dir == True:
                drive = GoogleDrive()
                file = drive.CreateFile({'id': '1NEqWZtm67a56OlBaQGy05PPP48Nedb_a'})
                file.SetContentFile(f'C:/Users/{username}/Documents/IMAGE/font.jpg')
                file.Upload()
#-------------------------------------------------------------------------------------
        def consult_form_id():
            global respuest2
            obten = (entry_form.get())
            print(obten)
            SCOPES = "https://www.googleapis.com/auth/forms.body.readonly"
            DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

            store = file.Storage('token.json')
            creds = None
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
                creds = tools.run_flow(flow, store)
            service = discovery.build('forms', 'v1', http=creds.authorize(
                Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
            # Prints the title of the sample form:
            form_id= str(obten)
            result = service.forms().get(formId=form_id).execute()
            respuest = result['linkedSheetId']
            print(respuest)
            respuest2 = result['responderUri']
            print(respuest2)
            text = linsheet_id_entry.insert(0,respuest)
            textunploadform = form_id_entry.insert(0, respuest2) 
          
        #-------------- DOWLOAD RESPOSES----------------------------
        def response_get1():
            global read_invar
            read_invar=(int_variable.get())
            if read_invar==2:
                read_invar='xlsx'
            else:
                read_invar='csv'
        def response_get():
            file = (linsheet_Id.get())
            type_file= str(read_invar)
            descarga = wget.download(f'https://docs.google.com/spreadsheets/d/{file}/export?format={type_file}')
            print(descarga)
        #---------------------------FRAMES---------------------------

        frame_user = customtkinter.CTkFrame(ventana_1,height=646, width=279, corner_radius=10)
        frame_user.place(x=14, y=15)

        label_banner = customtkinter.CTkLabel(frame_user, height=646, width=279, image=banner, text='')
        label_banner.pack(padx=2, pady=2)

        appareance_button = customtkinter.CTkButton(frame_user, height=48, width=239, corner_radius=10,command=ventana_1.destroy,bg_color='#2A2A2A', text='', image=exit)
        appareance_button.place(x=20, y=570)

        #-------------------------- CONSULT FORMS  FRAMES -------------

        frame_consult= customtkinter.CTkFrame(ventana_1, height=154, width=301, corner_radius=10)
        frame_consult.place(x=326,y=63)

        frame_consult1= customtkinter.CTkFrame(ventana_1, height=95, width=301, corner_radius=10)
        frame_consult1.place(x=640,y=63)

        button_item1 = customtkinter.CTkButton(frame_consult, height=30, width=241, text='' ,corner_radius=10)
        button_item1.place(x=356, y=24)
        
        button_google_account = customtkinter.CTkButton(ventana_1, text='', height=48, width=154, corner_radius=10, image=google, command=consult_forms)
        button_google_account.place(x=640, y=169)

        button_consult = customtkinter.CTkButton(ventana_1, text='', height=48, width=134, corner_radius=10, image=find, command=consult_form_id)
        button_consult.place(x=807, y=169)

        entry_form = customtkinter.StringVar()
        entry_form_id = customtkinter.CTkEntry(frame_consult1, height=30, width=241, corner_radius=10, textvariable=entry_form, show='X')
        entry_form_id.place(x=30, y=40)

        form_id = customtkinter.CTkLabel(frame_consult1,height=17, width=49, text='FormID',font=('Bahnschrift SemiBold',14))
        form_id.place(x=30, y=10)

        tex_name_id = customtkinter.CTkTextbox(frame_consult, height=135, width=284,corner_radius=10, font=('Bahnschrift SemiBold',14))
        tex_name_id.place(x=8, y=10)

        #--------------------------DOWNLOAD RESPONSES FRAMES ---------------------------------

        frame_respomses= customtkinter.CTkFrame(ventana_1, height=154, width=304, corner_radius=10)
        frame_respomses.place(x=329,y=285)

        frame_respomses1= customtkinter.CTkFrame(ventana_1, height=95, width=301, corner_radius=10)
        frame_respomses1.place(x=640,y=285)

        linsheet_Id = customtkinter.StringVar()
        linsheet_id_entry = customtkinter.CTkEntry(frame_respomses1, height=30, width=241, corner_radius=10, textvariable=linsheet_Id, show = 'X')
        linsheet_id_entry.place(x=30, y=40)
        
        responses_button = customtkinter.CTkButton(ventana_1, height=48, width=301, corner_radius=10,text='', image=dowload, command=response_get, fg_color='#35BD73')
        responses_button.place(x=640, y=391)

        linkSheet = customtkinter.CTkLabel(frame_respomses1, height=17, width=49, text='LinkSheeID',font=('Bahnschrift SemiBold',14))
        linkSheet.place(x=30, y=10)

        csv = customtkinter.CTkLabel(frame_respomses, height=29, width=52, text='CSV', text_color='#35BD73',font=('Bahnschrift SemiBold',24))
        csv.place(x=25, y=40)

        xlsx = customtkinter.CTkLabel(frame_respomses, height=29, width=64, text='XLSX', text_color='#35BD73', font=('Bahnschrift SemiBold',24))
        xlsx.place(x=210, y=40)

        or_res = customtkinter.CTkLabel(frame_respomses, height=29, width=64, text='OR',font=('Bahnschrift SemiBold',14))
        or_res.place(x=120, y=50)


        int_variable = customtkinter.IntVar()
        csv_radio = customtkinter.CTkRadioButton(frame_respomses, height=25, width=25, text='', command=response_get1,hover_color='#35BD73', variable=int_variable, value=1) 
        csv_radio.place(x=40, y=100)

        xlsx_radio = customtkinter.CTkRadioButton(frame_respomses, height=25, width=25, text='', command=response_get1,hover_color='#35BD73', variable=int_variable, value=2) 
        xlsx_radio.place(x=230, y=100)

        #---------------------------FORMS------------------------------------------

        frame_send = customtkinter.CTkFrame(ventana_1,height=174, width=615, corner_radius=10)
        frame_send.place(x=326, y=487)

        form_unpload = customtkinter.StringVar()
        form_id_entry_label = customtkinter.CTkLabel(frame_send,text='FormID', height=17, width=49,font=('Bahnschrift SemiBold',14))
        form_id_entry_label.place(x=40,y=10)

        form_id_entry_label = customtkinter.CTkLabel(frame_send,text='Fecha', height=17, width=49,font=('Bahnschrift SemiBold',14))
        form_id_entry_label.place(x=300,y=10)

        form_id_entry = customtkinter.CTkEntry(frame_send,height=30, width=241, corner_radius=10, textvariable=form_unpload,font=('Bahnschrift SemiBold',14))
        form_id_entry.place(x=40, y=35)

        

        fecha1 = customtkinter.StringVar()
        fecha = customtkinter.CTkEntry(frame_send,height=30, width=85, corner_radius=10,font=('Bahnschrift SemiBold',14), textvariable=fecha1)
        fecha.place(x=300, y=35)

        form_id_entry_label = customtkinter.CTkLabel(frame_send,text='Image Location', height=17, width=49,font=('Bahnschrift SemiBold',14))
        form_id_entry_label.place(x=40,y=90)
        form_id_entry2 = customtkinter.CTkEntry(frame_send,height=30, width=241, corner_radius=10,placeholder_text='C:/USERS/DOCUMENTS/IMAGE',font=('Bahnschrift SemiBold',14))
        form_id_entry2.configure(state='disabled')
        form_id_entry2.place(x=40, y=115)

        unploadfromid = customtkinter.CTkButton(frame_send, height=48, width=200, corner_radius=10,text='', image=unpload,command=unpload_form)
        unploadfromid.place(x=400, y=20)

        unploadimage = customtkinter.CTkButton(frame_send, height=48, width=301, corner_radius=10,text='', image=unpload,command=unpload_image)
        unploadimage.place(x=300, y=100)

        consultforms = customtkinter.CTkLabel(ventana_1,height=25, width=194, text='CONSULTAR FORMULARIOS',font=('Bahnschrift SemiBold',14))
        consultforms.place(x=326, y=27)

        consultforms = customtkinter.CTkLabel(ventana_1,height=25, width=194, text='DESCARGAR RESPUESTAS',font=('Bahnschrift SemiBold',14))
        consultforms.place(x=334, y=249)
        
        consultforms = customtkinter.CTkLabel(ventana_1,height=25, width=194, text='FORMULARIO SEND/ IMAGEN SEND',font=('Bahnschrift SemiBold',14))
        consultforms.place(x=334, y=454)

        ventana_1.mainloop()   
    else:
        print('CONTRASEÑA INCORRECTA') 

#------------------LOGIN-----------------
login = customtkinter.CTkLabel(ventana, height=40, width=236, font=('Bahnschrift SemiBold',32), text='Inicio de Sesion', bg_color='#2A2A2A')
login.place(x=73, y=132)

login_2 = customtkinter.CTkLabel(ventana,  image=imagen_1, height=95, width=105, text='', bg_color='#2A2A2A')
login_2.place(x=127, y=26)

username = customtkinter.CTkLabel(frame, width=128, height=21, text='Username')
username.place(x=15, y=188)

usuario  = customtkinter.StringVar()
username_entry = customtkinter.CTkEntry(frame, width=241, height=30, textvariable=usuario)
username_entry.place(x=45, y= 209)

password = customtkinter.CTkLabel(frame, width=128, height=21, text='Password')
password.place(x=15, y=278)

contraseña  = customtkinter.StringVar()
password_entry = customtkinter.CTkEntry(frame, width=241, height=30, textvariable=contraseña, show='x')
password_entry.place(x=45, y= 299)

submi = customtkinter.CTkButton(frame, height=28, width=241, text='login', command=panel,font=('Bahnschrift SemiBold',20))
submi.place(x=50, y=396)
#---------------------------------------------
ventana.mainloop()