import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image
from tkcalendar import Calendar
import settings
import image_interface
import os


class CalenderUI:
    """Calendar interface. Example taken from the official documentation of tkcalendar."""

    def __init__(self, cal_root):
        """Construct widget with master as parent widget"""
        self.top = tk.Toplevel(cal_root)

        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=int(settings.year), month=int(settings.month), day=int(settings.day))
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="ok", command=self.print_sel).pack()
        ttk.Button(self.top, text="exit", command=self.quit1).pack()

        self.date = ''

        self.top.grab_set()

    def print_sel(self):
        """Callback function saving the date to a variable."""
        self.date = self.cal.selection_get()

    def quit1(self):
        """Callback function that saves the date to a variable and exits the calendar window"""
        self.date = self.cal.selection_get()
        self.top.destroy()


class App:
    """Main app."""
    def __init__(self, master):
        """All elements in the frame must be described in the __init__. """
        self.master = master
        master.title("PyTSI User Interface")

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
        self.initial_img = ImageTk.PhotoImage(Image.open('images/placeholders/placeholder.png'))
        self.panel1 = tk.Label(self.master, image=self.initial_img)
        self.panel2 = tk.Label(self.master, image=self.initial_img)
        self.panel3 = tk.Label(self.master, image=self.initial_img)
        self.panel4 = tk.Label(self.master, image=self.initial_img)

        # make self.date and self.time variables
        self.compose_date_time()

        # title
        self.title = tk.Text(master, height=1, width=30)
        self.update_title()

        # calendar
        self.cal_button = tk.Button(self.master, text='Select date', command=self.get_date,
                                    activebackground=self.button_color,
                                    activeforeground='white')

        # time entry
        self.time_entry = tk.Entry(self.master, width=8)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, self.time)

        # fixed clear/cloud threshold entry
        self.fixed_sunny_entry = tk.Entry(self.master, width=8)
        self.fixed_sunny_entry.delete(0, tk.END)
        self.fixed_sunny_entry.insert(0, settings.fixed_sunny_threshold)

        # fixed thin/opaque threshold entry
        self.fixed_thin_entry = tk.Entry(self.master, width=8)
        self.fixed_thin_entry.delete(0, tk.END)
        self.fixed_thin_entry.insert(0, settings.fixed_thin_threshold)

        # hybrid stdev threshold entry
        self.hybrid_stdev_entry = tk.Entry(self.master, width=8)
        self.hybrid_stdev_entry.delete(0, tk.END)
        self.hybrid_stdev_entry.insert(0, settings.deviation_threshold)

        # hybrid fixed threshold entry
        self.hybrid_fixed_sunny_entry = tk.Entry(self.master, width=8)
        self.hybrid_fixed_sunny_entry.delete(0, tk.END)
        self.hybrid_fixed_sunny_entry.insert(0, settings.fixed_threshold)

        # time button
        self.time_button = tk.Button(self.master, text='Select time', width=10, command=self.get_entries,
                                     activebackground=self.button_color, activeforeground='white')

        # fixed clear/cloud threshold box
        self.fixed_sunny_button = tk.Button(self.master, text='Select fixed', width=10, command=self.get_entries,
                                      activebackground=self.button_color, activeforeground='white')

        # fixed thin/opaque threshold box
        self.fixed_thin_button = tk.Button(self.master, text='Select fixed', width=10, command=self.get_entries,
                                      activebackground=self.button_color, activeforeground='white')

        # hybrid stdev threshold box
        self.hybrid_stdev_button = tk.Button(self.master, text='Select T(stdev)', width=10, command=self.get_entries,
                                             activebackground=self.button_color, activeforeground='white')

        # hybrid fixed threshold box
        self.hybrid_fixed_button = tk.Button(self.master, text='Select T(fixed)', width=10, command=self.get_entries,
                                             activebackground=self.button_color, activeforeground='white')
        # initialize info boxes
        info_width = 35
        self.info_orig = tk.Text(self.master, height=3, width=info_width)
        self.info_tsi_fixed = tk.Text(self.master, height=3, width=info_width)
        self.info_fixed = tk.Text(self.master, height=3, width=info_width)
        self.info_hybrid = tk.Text(self.master, height=3, width=info_width)

        self.initialize_info_boxes()

        # alignments
        self.organize_grid_elements()

        # binds
        self.setup_binds()

    def setup_binds(self):
        """Set up the binds, such as 'RETURN' to enter input or 'Ctrl-A' to select all text in entry box."""
        self.master.bind('<Return>', lambda evt: self.get_entries(evt))
        self.time_entry.bind('<Control-KeyRelease-a>', lambda evt: self.select_all(evt))

    def organize_grid_elements(self):
        """Structure all widgets into a grid with corresponding white space to accomodate for window scaling."""
        # title
        self.title.grid(row=1, column=1, columnspan=8, sticky='')

        # original image
        self.panel1.grid(row=3, column=1, rowspan=1, columnspan=2, sticky='NSEW')

        # old tsi software image
        self.panel2.grid(row=3, column=3, rowspan=1, columnspan=2, sticky='NSEW')

        # fixed image
        self.panel3.grid(row=3, column=5, rowspan=1, columnspan=2, sticky='NSEW')

        # hybrid image
        self.panel4.grid(row=3, column=7, rowspan=1, columnspan=2, sticky='NSEW')

        # time entry
        self.time_entry.grid(row=8, column=2, sticky='NESW')

        # fixed clear/cloud entry
        self.fixed_sunny_entry.grid(row=7, column=5, sticky='NESW')

        # fixed thin/opauqe entry
        self.fixed_thin_entry.grid(row=8, column=5, sticky='NESW')

        # hybrid stdev entry
        self.hybrid_stdev_entry.grid(row=7, column=7, sticky='NESW')

        # hybrid fixed entry
        self.hybrid_fixed_sunny_entry.grid(row=8, column=7, sticky='NESW')

        # time button
        self.time_button.grid(row=8, column=3, sticky='NESW')

        # fixed clear/cloud button
        self.fixed_sunny_button.grid(row=7, column=6, sticky='NESW')

        # fixed thin/opaque button
        self.fixed_thin_button.grid(row=8, column=6, sticky='NESW')

        # hybrid stdev button
        self.hybrid_stdev_button.grid(row=7, column=8, sticky='NESW')

        # hybrid fixed button
        self.hybrid_fixed_button.grid(row=8, column=8, sticky='NESW')

        # calendar button
        self.cal_button.grid(row=7, column=2, columnspan=2, sticky='NESW')

        # info boxes
        self.info_orig.grid(row=5, column=1, columnspan=2)
        self.info_tsi_fixed.grid(row=5, column=3, columnspan=2)
        self.info_fixed.grid(row=5, column=5, columnspan=2)
        self.info_hybrid.grid(row=5, column=7, columnspan=2)

        # empty rows, fixes window scaling
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_rowconfigure(9, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(9, weight=1)

    def initialize_info_boxes(self):
        """Initialize the text in the boxes below the shown images."""
        init_info_orig = 'Original Image \nSolar Azimuth: %s \nSolar Altitude: %s' % (str(self.azimuth), str(self.altitude))
        init_info_tsi_fixed = 'Old TSI software \nCloud cover: %s' % (str(self.cloud_cover))
        init_info_fixed = 'New software (fixed) \nCloud cover: %s' % (str(self.cloud_cover))
        init_info_hybrid = 'New software (hybrid) \nCloud cover: %s' % (str(self.cloud_cover))

        self.info_orig.insert(tk.INSERT, init_info_orig)
        self.info_tsi_fixed.insert(tk.INSERT, init_info_tsi_fixed)
        self.info_fixed.insert(tk.INSERT, init_info_fixed)
        self.info_hybrid.insert(tk.INSERT, init_info_hybrid)

        return init_info_orig, init_info_tsi_fixed, init_info_fixed, init_info_hybrid

    def update_title(self):
        """Set the title to the currently selected date/time."""
        self.title.delete('1.0', tk.END)
        self.title.tag_configure('center', justify='center')
        self.title.insert('1.0', self.date + ' ' + self.time + ' (UTC yyyy-mm-dd)')
        self.title.tag_add('center', '1.0', 'end')

    def get_date(self):
        """Get the date as a variable from the calendar widget."""
        cal = CalenderUI(self.master)
        self.master.wait_window(cal.top)
        self.date = str(cal.date)
        self.process()

    def get_entries(self, event=None):
        """Get the time as a variable from the time entry box and check for incorrect format."""
        self.time = self.time_entry.get()

        settings.fixed_sunny_threshold = float(self.fixed_sunny_entry.get())
        settings.fixed_thin_threshold = float(self.fixed_thin_entry.get())
        settings.deviation_threshold = float(self.hybrid_stdev_entry.get())
        settings.fixed_threshold = float(self.hybrid_fixed_sunny_entry.get())

        # check the length of the time string
        if len(self.time) != 5 or self.time[2] != ':':
            print('Error: time format needs to follow specific format -> something like \'13:37\'.')
        # check the ranges of the time string
        elif (int(self.time[0:2]) > 23 or int(self.time[0:2]) < 0 or
              int(self.time[3:5]) > 59 or int(self.time[3:5]) < 0):
            print('Error: hours need to be between 00 and 23, minutes need to be between 00 and 59')
        # check the ranges of the thresholds
        elif (settings.fixed_sunny_threshold < 0 or settings.fixed_sunny_threshold > 1 or
              settings.fixed_thin_threshold < 0 or settings.fixed_thin_threshold > 1 or
              settings.deviation_threshold < 0 or settings.deviation_threshold > 1 or
              settings.fixed_threshold < -1 or settings.fixed_threshold > 1):
            print('Error: Threshold values out of range.')
        else:
            self.process()

    def update_info_boxes(self):
        """Update the information in the text boxes underneath the images."""
        # clear the text boxes from beginning to end
        self.info_orig.delete('1.0', tk.END)
        self.info_tsi_fixed.delete('1.0', tk.END)
        self.info_fixed.delete('1.0', tk.END)
        self.info_hybrid.delete('1.0', tk.END)

        # new text
        new_info_orig = 'Original Image \nSolar Azimuth: %s \nSolar Altitude: %s' % (str(self.azimuth), str(self.altitude))
        new_info_tsi_fixed = 'Old TSI software \nCloud cover: %s' % (str(self.cover_total_tsi))
        new_info_fixed = 'New software (fixed) \nCloud cover: %s' % (str(self.cover_total_fixed))
        new_info_hybrid = 'New software (hybrid) \nCloud cover: %s' % (str(self.cover_total_hybrid))

        # insert new text into text boxes
        self.info_orig.insert(tk.INSERT, new_info_orig)
        self.info_tsi_fixed.insert(tk.INSERT, new_info_tsi_fixed)
        self.info_fixed.insert(tk.INSERT, new_info_fixed)
        self.info_hybrid.insert(tk.INSERT, new_info_hybrid)

    def process(self):
        """Call the processing underlying processing function and delete temporary files."""
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
        """Open the images produced by the processing functions and display them in the window."""
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
        """Compose the date and time from the settings file variables."""
        self.date = settings.year + '-' + settings.month + '-' + settings.day
        self.time = settings.hour + ':' + settings.minute

    def compose_filename(self):
        """Create the 'naked' filename (naked here means without any extension(s)) from the date and time variables."""
        self.filename = self.date + self.time + '00'
        self.filename = self.filename.replace(':', '')
        self.filename = self.filename.replace('-', '')

    def layout(self):
        """Set some variables and settings relating to layout of the main window (colors, fonts etc.)."""
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
        size_x = 1200
        size_y = 550
        self.master.geometry('{}x{}'.format(size_x, size_y))

    @staticmethod
    def select_all(event=None):
        """Select-all bind callback."""
        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
