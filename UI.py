import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image
from tkcalendar import Calendar
import settings
import image_interface
import os


class CalenderUI:
    def __init__(self, cal_root):
        self.top = tk.Toplevel(cal_root)

        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=int(settings.year), month=int(settings.month), day=int(settings.day))
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

        style = ttk.Style(self.master)
        style.theme_use('clam')

        # initialize some variables
        self.filename = None
        self.button_color = None
        self.azimuth = self.altitude = self.cloud_cover = None
        self.date = self.time = None
        self.azimuth = self.altitude = None
        self.cover_total_hybrid = self.cover_total_tsi = self.cover_total_fixed = None

        # layout (fonts, colors etc)
        self.layout()

        # initialize image frames
        initial_img = ImageTk.PhotoImage(Image.open('images/placeholders/placeholder.png'))
        self.panel1 = tk.Label(self.master, image=initial_img)
        self.panel2 = tk.Label(self.master, image=initial_img)
        self.panel3 = tk.Label(self.master, image=initial_img)
        self.panel4 = tk.Label(self.master, image=initial_img)

        # make self.date and self.time variables
        self.compose_date_time()

        # title
        self.title = tk.Text(master, height=1, width=30)
        self.update_title()

        # calendar
        self.cal_button = tk.Button(self.master, text='Select date', command=self.get_date,
                                    activebackground=self.button_color,
                                    activeforeground='white')

        # time
        self.time_entry = tk.Entry(self.master, width=8)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, self.time)

        # time button
        self.time_button = tk.Button(self.master, text='Select time', width=10, command=self.get_time,
                                     activebackground=self.button_color, activeforeground='white')

        # initialize info boxes
        self.info_orig = tk.Text(self.master, height=3, width=30)
        self.info_tsi_fixed = tk.Text(self.master, height=3, width=30)
        self.info_fixed = tk.Text(self.master, height=3, width=30)
        self.info_hybrid = tk.Text(self.master, height=3, width=30)

        self.initialize_info_boxes()

        # alignments
        self.organize_grid_elements()

        # binds
        self.setup_binds()

    def setup_binds(self):
        self.master.bind('<Return>', lambda evt: self.get_time(evt))
        self.time_entry.bind('<Control-KeyRelease-a>', lambda evt: self.select_all(evt))

    def organize_grid_elements(self):
        # title
        self.title.grid(row=0, column=1, columnspan=5, sticky='')

        # original image
        self.panel1.grid(row=1, column=1, rowspan=2, sticky='NSEW')

        # old tsi software
        self.panel2.grid(row=1, column=2, rowspan=2, sticky='NSEW')

        # fixed
        self.panel3.grid(row=1, column=3, rowspan=2, sticky='NSEW')

        # hybrid
        self.panel4.grid(row=1, column=4, rowspan=2, sticky='NSEW')

        # time entry
        self.time_entry.grid(row=2, column=6)

        # time button
        self.time_button.grid(row=2, column=7)

        # calendar button
        self.cal_button.grid(row=1, column=6, columnspan=2, sticky='EW')

        # info boxes
        self.info_orig.grid(row=4, column=1, columnspan=1)
        self.info_tsi_fixed.grid(row=4, column=2, columnspan=1)
        self.info_fixed.grid(row=4, column=3, columnspan=1)
        self.info_hybrid.grid(row=4, column=4, columnspan=1)

        # empty rows, fixes window scaling
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(5, weight=1)
        self.master.grid_columnconfigure(8, weight=1)

    def initialize_info_boxes(self):
        init_info_orig = 'Original Image \nAzimuth: %s \nAltitude: %s' % (str(self.azimuth), str(self.altitude))
        init_info_tsi_fixed = 'Old TSI software \nCloud cover: %s' % (str(self.cloud_cover))
        init_info_fixed = 'New software (fixed) \nCloud cover: %s' % (str(self.cloud_cover))
        init_info_hybrid = 'New software (hybrid) \nCloud cover: %s' % (str(self.cloud_cover))

        self.info_orig.insert(tk.INSERT, init_info_orig)
        self.info_tsi_fixed.insert(tk.INSERT, init_info_tsi_fixed)
        self.info_fixed.insert(tk.INSERT, init_info_fixed)
        self.info_hybrid.insert(tk.INSERT, init_info_hybrid)

        return init_info_orig, init_info_tsi_fixed, init_info_fixed, init_info_hybrid

    def update_title(self):
        self.title.delete('1.0', tk.END)
        self.title.tag_configure('center', justify='center')
        self.title.insert('1.0', self.date + ' ' + self.time + ' (UTC yyyy-mm-dd)')
        self.title.tag_add('center', '1.0', 'end')

    def get_date(self):
        cal = CalenderUI(self.master)
        self.master.wait_window(cal.top)
        self.date = str(cal.date)
        self.process()

    def get_time(self, event=None):
        self.time = self.time_entry.get()
        if len(self.time) != 5 or self.time[2] != ':':
            print('Error: time format needs to follow specific format -> something like \'13:37\'.')
        elif 0 <= int(self.time[0:2]) <= 23 and 0 <= int(self.time[3:5]) <= 59:
            self.process()
        else:
            print('Error: hours need to be between 00 and 23, minutes need to be between 00 and 59')

    def update_info_boxes(self):
        # clear the text boxes from beginning to end
        self.info_orig.delete('1.0', tk.END)
        self.info_tsi_fixed.delete('1.0', tk.END)
        self.info_fixed.delete('1.0', tk.END)
        self.info_hybrid.delete('1.0', tk.END)

        # new text
        new_info_orig = 'Original Image \nAzimuth: %s \nAltitude: %s' % (str(self.azimuth), str(self.altitude))
        new_info_tsi_fixed = 'Old TSI software \nCloud cover: %s' % (str(self.cover_total_tsi))
        new_info_fixed = 'New software (fixed) \nCloud cover: %s' % (str(self.cover_total_fixed))
        new_info_hybrid = 'New software (hybrid) \nCloud cover: %s' % (str(self.cover_total_hybrid))

        # insert new text into text boxes
        self.info_orig.insert(tk.INSERT, new_info_orig)
        self.info_tsi_fixed.insert(tk.INSERT, new_info_tsi_fixed)
        self.info_fixed.insert(tk.INSERT, new_info_fixed)
        self.info_hybrid.insert(tk.INSERT, new_info_hybrid)

    def process(self):
        self.compose_filename()
        self.azimuth, self.altitude, self.cover_total_fixed, self.cover_total_hybrid, self.cover_total_tsi = \
            image_interface.single(self.filename)
        self.update_image()
        self.update_info_boxes()
        self.update_title()
        os.remove(settings.tmp + self.filename + '_original.png')
        os.remove(settings.tmp + self.filename + '_fixed_old.png')
        os.remove(settings.tmp + self.filename + '_fixed.png')
        os.remove(settings.tmp + self.filename + '_hybrid.png')
        os.remove(settings.tmp + self.filename + '.png')
        os.remove(settings.tmp + self.filename + '.jpg')
        os.remove(settings.tmp + self.filename + '.properties.gz')

    def update_image(self):
        filename1 = self.filename + '_original.png'
        filename2 = self.filename + '_fixed_old.png'
        filename3 = self.filename + '_fixed.png'
        filename4 = self.filename + '_hybrid.png'
        img_new = ImageTk.PhotoImage(Image.open(settings.tmp + filename1))
        self.panel1.configure(image=img_new)
        self.panel1.image = img_new
        img_new2 = ImageTk.PhotoImage(Image.open(settings.tmp + filename2))
        self.panel2.configure(image=img_new2)
        self.panel2.image = img_new2
        img_new3 = ImageTk.PhotoImage(Image.open(settings.tmp + filename3))
        self.panel3.configure(image=img_new3)
        self.panel3.image = img_new3
        img_new4 = ImageTk.PhotoImage(Image.open(settings.tmp + filename4))
        self.panel4.configure(image=img_new4)
        self.panel4.image = img_new4

    def compose_date_time(self):
        self.date = settings.year + '-' + settings.month + '-' + settings.day
        self.time = settings.hour + ':' + settings.minute

    def compose_filename(self):
        self.filename = self.date + self.time + '00'
        self.filename = self.filename.replace(':', '')
        self.filename = self.filename.replace('-', '')

    def layout(self):
        # background colors
        background_color = '#f4f4f4'
        self.master.configure(bg=background_color)

        # button colors
        self.button_color = '#bababa'

        # fonts
        default_font = font.nametofont('TkDefaultFont')
        default_font.configure(size=12)
        self.master.option_add("*Font", default_font)

        # sizes
        size_x = 1400
        size_y = 500
        self.master.geometry('{}x{}'.format(size_x, size_y))

    @staticmethod
    def select_all(event=None):
        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
