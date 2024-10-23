from tkinter import *
from tkinter import ttk
import yt_dlp
import subprocess
import os

# Configurar ventana principal
root = Tk()
root.geometry('500x500')
root.resizable(0, 0)
root.title("Tu Conversor de YouTube: Descarga y Transforma")
root.configure(bg="#F7E7CE")

# Título
Label(root, text='YouTube Video Downloader', font=('Helvetica', 20, 'bold'), bg="#F7E7CE", fg="#3E2723").pack(pady=10)

# Campo para el link de YouTube
link = StringVar()
Label(root, text='Ingresa un link de YouTube:', font=('Helvetica', 15, 'bold'), bg="#F7E7CE", fg="#5D4037").place(x=40, y=60)
link_enter = Entry(root, width=50, textvariable=link).place(x=32, y=100)

# Opciones de formato
format_var = StringVar(value="mp3")
Label(root, text='Formato de salida:', font=('Helvetica', 15, 'bold'), bg="#F7E7CE", fg="#5D4037").place(x=40, y=160)
ttk.Combobox(root, textvariable=format_var, values=["mp3", "flac", "aac", "mp4"]).place(x=250, y=165)

# Directorio de salida
output_dir = "Descargas"

# Crear el directorio si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función para descargar el video de YouTube
def downloader():
    video_url = str(link.get())
    select_format = format_var.get()

    # Si se selecciona MP4, descargamos video y audio
    if select_format == "mp4":
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Descargar el video y el audio en la mejor calidad
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Guardar el archivo descargado
            'merge_output_format': 'mp4'  # Unir video y audio en formato mp4
        }
    else:
        # Descargar solo el audio en el mejor formato posible excluyendo OPUS
        ydl_opts = {
            'format': 'bestaudio[ext!=opus]/bestaudio',  # Excluir OPUS
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Guardar el archivo descargado
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': select_format,  # Usar el formato seleccionado (mp3, flac, aac)
                'preferredquality': '192',  # Calidad preferida del audio
            }]
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            downloaded_file = os.path.join(output_dir, f"{video_title}.{select_format}")
        
        Label(root, text='DESCARGADO', font='Helvetica 12 bold', bg="#F7E7CE", fg="#00796B").place(x=180, y=260)
        return downloaded_file
    except Exception as e:
        Label(root, text='ERROR EN DESCARGA', font='Helvetica 12 bold', bg="#F7E7CE", fg="#E53935").place(x=150, y=200)
        return None

# Función para convertir el archivo descargado al formato deseado
def converter():
    input_file = downloader()
    if input_file and format_var.get() != "mp4":  # Solo convertir si no es mp4
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_converted.{format_var.get()}")
        
        # Comando para convertir usando ffmpeg
        command = [
            'ffmpeg', '-i', input_file, output_file
        ]

        try:
            subprocess.run(command, check=True)
            Label(root, text='CONVERTIDO', font='Helvetica 12 bold', bg="#F7E7CE", fg="#00796B").place(x=180, y=300)
        except Exception as e:
            Label(root, text='ERROR EN CONVERSIÓN', font='Helvetica 12 bold', bg="#F7E7CE", fg="#E53935").place(x=150, y=300)

# Botón para descargar y convertir
download_btn = Button(root, text='DESCARGAR Y CONVERTIR', font='Helvetica 15 bold', bg='#D32F2F', fg='white', command=converter).place(x=120, y=220)

root.mainloop()
