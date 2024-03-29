import tkinter as tk
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading
import os


# Backend---                                                                                                         ---
def close_window():
    """
    Function that and asks user to confirm when the x button is pressed and closes the window.
    """
    # asks the user to confirm
    if askokcancel(title='Close', message='Do you want to close MP3 downloader?'):
        window.destroy()


def download_audio():
    """
    Function that downloads audio from YouTube url entered in entry, converts it to MP3 and saves it to music directory.
    """
    # gets video url from entry
    mp3_link = url_entry.get()

    # if the entry is empty show an error
    if mp3_link == '':
        showerror(title='Error', message='Please enter the MP3 URL')

    else:
        try:
            def on_progress(stream, chunk, bytes_remaining):
                """
                Function that tracks the progress of downloading.
                :param stream: stream
                :param chunk: chunk
                :param bytes_remaining: remaining bytes
                """
                # the total size of the audio
                total_size = stream.filesize

                def get_formatted_size(total_size, factor=1024, suffix='B'):
                    """
                    Function that gets the total size of the audio
                    :param total_size: total size in bytes
                    :param factor: factor
                    :param suffix: suffix
                    :return: formatted audio file size
                    """
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if total_size < factor:
                            return f"{total_size:.2f}{unit}{suffix}"
                        total_size /= factor
                    return f"{total_size:.2f}Y{suffix}"

                # updating progress bar
                formatted_size = get_formatted_size(total_size)
                bytes_downloaded = total_size - bytes_remaining
                percentage_completed = round(bytes_downloaded / total_size * 100)
                progress_bar['value'] = percentage_completed
                progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                window.update()

            # create a music directory to store downloaded files
            music_folder = os.path.join(os.getcwd(), 'music')
            os.makedirs(music_folder, exist_ok=True)
            audio = YouTube(mp3_link, on_progress_callback=on_progress)
            audio_stream = audio.streams.get_audio_only()
            output = audio_stream.download(output_path=music_folder)
            base, ext = os.path.splitext(output)
            # convert to MP3
            new_file = base + '.mp3'
            os.rename(output, new_file)

            # popup for displaying the mp3 downloaded success message
            showinfo(title='Download Complete', message='MP3 has been downloaded successfully.')
            progress_label.config(text='')
            progress_bar['value'] = 0

        except:
            showerror(title='Download Error', message='An error occurred while trying to ' \
                                                      'download the MP3\nThe following could ' \
                                                      'be the causes:\n->Invalid link\n->No internet connection\n' \
                                                      'Make sure you have stable internet connection and the MP3 link is valid')
            progress_label.config(text='')
            progress_bar['value'] = 0


def download_thread():
    """
    Function that runs the download as a thread.
    """
    t1 = threading.Thread(target=download_audio)
    t1.start()


# GUI/Frontend---                                                                                                    ---
window = Tk()
window.protocol('WM_DELETE_WINDOW', close_window)
window.title('MP3 Downloader')
window.resizable(height=FALSE, width=FALSE)
canvas = Canvas(window, width=1132, height=743)
canvas.pack()

# loading the background
window.iconbitmap(window, 'assets/icon.ico')
background = PhotoImage(file='assets/background.png')
canvas.create_image(0, 0, anchor=tk.NW, image=background)

# url entry and label
url_label = ttk.Label(window, text='Enter YouTube URL:', style='TLabel', background='white')
url_entry = ttk.Entry(window, width=50, style='TEntry')
canvas.create_window(566, 530, window=url_label)
canvas.create_window(566, 560, window=url_entry)

# download progress bar
progress_label = Label(window, text='')
canvas.create_window(566, 600, window=progress_label)
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
canvas.create_window(566, 650, window=progress_bar)

# download button
download_button = ttk.Button(window, text='Download MP3', style='TButton', command=download_thread)
canvas.create_window(566, 600, window=download_button)

# style for the label
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))
# style for the entry
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
# style for the button
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe', background='white')

window.mainloop()
