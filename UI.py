import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image
from tkcalendar import Calendar
import print_text


class CalenderUI():
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=2016, month=6, day=11)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="ok", command=self.print_sel).pack()
        ttk.Button(self.top, text="exit", command=self.quit1).pack()

        self.date = ''

        self.top.grab_set()

    def print_sel(self):
        self.date = self.cal.selection_get()

    def quit1(self):
        self.top.destroy()


class App:
    def __init__(self, master):
        self.master = master
        master.title("PyTSI User Interface")

        s = ttk.Style(self.master)
        s.theme_use('clam')

        self.img_folder = '/nobackup/users/mos/data/TSI/DBASE/201606/20160611_tsi-cabauw_realtime/'

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

        self.date = '2016-06-11'
        self.time = '12:00'

        # image 1
        img = ImageTk.PhotoImage(Image.open('images/20170828112200.jpg'))
        self.panel1 = tk.Label(self.master, image=img)
        self.panel1.grid(row=3, column=1, rowspan=2, sticky='NSEW')

        # image 2
        img2 = ImageTk.PhotoImage(Image.open('images/20170828112200.png'))
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
        info = tk.Text(self.master, height=3, width=30)
        info.insert(tk.INSERT, 'Cloud cover:x \nAzimuth:x \nAltitude:x')
        info.grid(row=6, column=1, columnspan=1)

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
        self.update_image()

    def get_time(self, event=None):
        self.time = self.e.get()
        if self.time[2] != ':' or len(self.time) != 5:
            print('Error: time format needs to follow specific format -> something like \'13:37\'')
        else:
            self.update_image()

    def update_image(self, event=None):
        date_time = self.date + self.time
        date_time = date_time.replace(':', '')
        date_time = date_time.replace('-', '')
        filename1 = date_time + '00.jpg'
        filename2 = date_time + '00.png'

        img_new = ImageTk.PhotoImage(Image.open(self.img_folder + filename1))
        self.panel1.configure(image=img_new)
        self.panel1.image = img_new
        img_new2 = ImageTk.PhotoImage(Image.open(self.img_folder + filename2))
        self.panel2.configure(image=img_new2)
        self.panel2.image = img_new2

    @staticmethod
    def select_all(event=None):
        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')


root = tk.Tk()
app = App(root)
