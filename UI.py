import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image
from tkcalendar import Calendar
import settings
import image_interface
import os


class CalenderUI():
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=2016, month=6, day=1)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="ok", command=self.print_sel).pack()
        ttk.Button(self.top, text="exit", command=self.quit1).pack()

        self.date = ''

        self.top.grab_set()

    def print_sel(self):
        self.date = self.cal.selection_get()

    def quit1(self):
        self.date = self.cal.selection_get()
        self.top.destroy()


class App:
    def __init__(self, master):
        self.master = master
        master.title("PyTSI User Interface")

        s = ttk.Style(self.master)
        s.theme_use('clam')

        self.img_folder = settings.main_data

        self.azimuth = self.altitude = self.cloud_cover = '0'

        # background colors
        background_color = '#f4f4f4'
        self.master.configure(bg=background_color)

        # button colors
        button_color = '#bababa'

        # fonts
        default_font = font.nametofont('TkDefaultFont')
        default_font.configure(size=12)
        self.master.option_add("*Font", default_font)

        # sizes
        size_x = 800
        size_y = 500
        self.master.geometry('{}x{}'.format(size_x, size_y))

        self.date = '2016-06-01'
        self.time = '12:00'

        self.filename = self.compose_filename()

        # image 1
        img = ImageTk.PhotoImage(Image.open('images/placeholders/placeholder.png'))
        self.panel1 = tk.Label(self.master, image=img)
        self.panel1.grid(row=3, column=1, rowspan=2, sticky='NSEW')

        # image 2
        img2 = ImageTk.PhotoImage(Image.open('images/placeholders/placeholder.png'))
        self.panel2 = tk.Label(self.master, image=img2)
        self.panel2.grid(row=3, column=2, rowspan=2, sticky='NSEW')

        # calendar
        cal_button = tk.Button(self.master, text='Select date', command=self.get_date, activebackground=button_color,
                               activeforeground='white')
        cal_button.grid(row=3, column=4, columnspan=2, sticky='EW')

        # time
        self.e = tk.Entry(self.master, width=10)
        # self.e.focus_set()
        self.e.grid(row=4, column=4)
        self.e.delete(0, tk.END)
        self.e.insert(0, self.time)
        self.e.bind('<Control-KeyRelease-a>', lambda evt: self.select_all(evt))

        # time button
        time_button = tk.Button(self.master, text='Select time', width=10, command=self.get_time,
                                activebackground=button_color, activeforeground='white')
        time_button.grid(row=4, column=5)

        # title
        title = tk.Text(self.master, height=1)
        title.insert(tk.INSERT, 'Select a date and time')
        title.grid(row=1, column=1, columnspan=5)

        # info
        initial_info = 'Cloud cover: %s \nAzimuth: %s \nAltitude: %s' % (str(self.cloud_cover),
                                                                         str(self.azimuth),
                                                                         str(self.altitude))

        self.info = tk.Text(self.master, height=3, width=30)
        self.info.insert(tk.INSERT, initial_info)
        self.info.grid(row=6, column=1, columnspan=1)

        # alignments
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_rowconfigure(7, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        self.master.bind('<Return>', lambda evt: self.get_time(evt))

        root.mainloop()

    def get_date(self, event=None):
        cal = CalenderUI(self.master)
        self.master.wait_window(cal.top)
        self.date = str(cal.date)
        self.process()

    def get_time(self, event=None):
        self.time = self.e.get()
        if len(self.time) != 5 or self.time[2] != ':':
            print('Error: time format needs to follow specific format -> something like \'13:37\'.')
        elif 0 <= int(self.time[0:2]) <= 23 and 0 <= int(self.time[3:5]) <= 59:
            self.process()
        else:
            print('Error: hours need to be between 00 and 23, minutes need to be between 00 and 59')

    def update_info(self, event=None):
        self.info.delete('1.0', tk.END)
        new_info = 'Cloud cover: %s \nAzimuth: %s \nAltitude: %s' % (str(self.cloud_cover),
                                                                     str(self.azimuth),
                                                                     str(self.altitude))
        self.info.insert(tk.INSERT, new_info)

    def process(self, event=None):
        self.filename = self.compose_filename()
        self.azimuth, self.altitude, self.cloud_cover = image_interface.single(self.filename)
        self.update_image()
        self.update_info()
        os.remove(self.filename + '_processed.png')

    def update_image(self, event=None):
        filename1 = self.filename + '.jpg'
        filename2 = self.filename + '_processed.png'

        img_new = ImageTk.PhotoImage(Image.open(settings.main_data + filename1))
        self.panel1.configure(image=img_new)
        self.panel1.image = img_new
        img_new2 = ImageTk.PhotoImage(Image.open(filename2))
        self.panel2.configure(image=img_new2)
        self.panel2.image = img_new2

    def compose_filename(self, event=None):
        filename_no_ext = self.date + self.time + '00'
        filename_no_ext = filename_no_ext.replace(':', '')
        filename_no_ext = filename_no_ext.replace('-', '')

        return filename_no_ext

    @staticmethod
    def select_all(event=None):
        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')


root = tk.Tk()
app = App(root)
