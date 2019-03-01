import tkinter as tk
import tkinter.font as tkFont
import time
import iPill

# Declare global variables
dfont = None
dtime = None
font_size = 24
fullscreen = False

######################################################
class SampleApp(tk.Tk):
    
    def __init__(self):
        global time_dfont
        global button_dfont
        global label_dfont
        global dtime
        global pill
        global dispensed
        root = tk.Tk.__init__(self)
        time_dfont = tkFont.Font(family='Courier New', size=font_size, weight=tkFont.BOLD)
        button_dfont = tkFont.Font(size=font_size)
        label_dfont = tkFont.Font(size=font_size)
        dtime = tk.StringVar()
        pill = iPill.pillInfo()
        dispensed = False
        self._frame = None
        self.switch_frame(StartPage)
        self.bind('<F11>', self.toggle_fullscreen)
        self.bind('<Escape>', self.end_fullscreen)
        self.bind('<Configure>', self.resize)
        self.after(20,self.update)

    def toggle_fullscreen(self, event=None):

        global root
        global fullscreen

        # Toggle between fullscreen and windowed modes
        fullscreen = not fullscreen
        self.attributes('-fullscreen', fullscreen)
        self.resize

    # Return to windowed mode
    def end_fullscreen(self,event=None):

        global root
        global fullscreen

        # Turn off fullscreen mode
        fullscreen = False
        self.attributes('-fullscreen', False)
        self.resize
    
    # Automatically resize font size based on window size
    def resize(self,event=None):

        global time_dfont
        global button_dfont
        global label_dfont
        new_size = -max(12, int((self._frame.winfo_height() / 6)))
        time_dfont.configure(size=new_size)
        new_size = -max(12, int((self._frame.winfo_height() / 12)))
        label_dfont.configure(size=new_size)
        new_size = -max(12, int((self._frame.winfo_height() / 8)))
        button_dfont.configure(size=new_size)
        
    
    # Read values from the sensors at regular intervals
    def update(self):
        global dtime
        global dispensed
        # Get local time
        local_time = time.localtime()
        # Convert time to 12 hour clock
        hours = local_time.tm_hour
        if hours > 12:
            hours -= 12

        # Add leading 0s
        shours = str(hours)
        smin = str(local_time.tm_min)
        ssec = str(local_time.tm_sec)
        if hours < 10:
            shours = '0' + shours
        if local_time.tm_min < 10:
            smin = '0' + smin
        if local_time.tm_sec < 10:
            ssec = '0' + ssec

        # Construct string out of time
        if dispensed == False:
            dtime.set(shours + ':' + smin + ':' + ssec)   
        self.after(700, self.update)
    
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH, expand=1)

class StartPage(tk.Frame):
    def __init__(self, master):
        global time_dfont
        global button_dfont
        sp = tk.Frame.__init__(self, master)
        tk.Label(self, text="Choose User Mode",font=time_dfont,highlightthickness=0).grid(row=0, column=0, padx=0, pady=0)
        tk.Button(self, text="Pharmacist", font=button_dfont,highlightthickness=0,
                  command=lambda: master.switch_frame(pharmframe)).grid(row=1, column=0, padx=0, pady=0)
        tk.Button(self, text="User", font=button_dfont,highlightthickness=0,
                  command=lambda: master.switch_frame(userframe)).grid(row=2, column=0, padx=0, pady=0)
        tk.Button(self, text="Quit", font=button_dfont,highlightthickness=0,
                  command=lambda: master.destroy()).grid(row=3, column=0, padx=0, pady=0)

class pharmframe(tk.Frame):
    global time_dfont
    global button_dfont
    global label_dfont
    global pill
    def __init__(self, master):
        pharm = tk.Frame.__init__(self, master)
        
        tk.Label(self, font=time_dfont,text="Pharmacist Mode",highlightthickness=0).grid(row=0, columnspan = 3,sticky=tk.E+tk.W)
        
        self.pname = tk.Entry(self, font =label_dfont, text="John Doe")
        self.pname.grid(row=1, column = 1, columnspan = 2, pady=15,sticky=tk.W+tk.E)
        tk.Label(self, text="Patient Name", font =label_dfont).grid(row=1, column = 0,sticky=tk.W+tk.E)
        self.pinfo = tk.Entry(self, font =label_dfont, text="Ibuprofen")
        self.pinfo.grid(row=2, column = 1, columnspan = 2,pady=15, sticky=tk.W+tk.E)
        tk.Label(self, text="Prescription Info", font =label_dfont).grid(row=2, column = 0, sticky=tk.W+tk.E)
        self.dinfo = tk.Entry(self, font =label_dfont, text="Two tablets three times a day")
        self.dinfo.grid(row=3, column = 1, columnspan = 2,pady=15, sticky=tk.W+tk.E)
        tk.Label(self, text="Dosage Info", font =label_dfont).grid(row=3, column = 0, sticky=tk.W+tk.E)
        self.numpills = tk.Spinbox(self, from_=1, to = 99, width=5,font = label_dfont)
        self.numpills.grid(row=4, column = 1, pady=15, sticky=tk.W)
        tk.Label(self, text="Number of Pills", font =label_dfont).grid(row=4, column = 0, sticky=tk.W+tk.E)
        tk.Button(self, text="Encode Info", font=button_dfont, command=lambda:self.setinfo()).grid(row=4,column=2)
        
        tk.Button(self, text="Return to start page", font=button_dfont,highlightthickness=0,
                  command=lambda: master.switch_frame(StartPage)).grid(row=5, columnspan = 3, sticky=tk.W+tk.E)
        
        self.pinfo.delete(0, tk.END)
        self.pname.delete(0, tk.END)
        self.dinfo.delete(0, tk.END)
        
        self.pname.insert(0,"John Doe")
        self.pinfo.insert(0,"Ibuprofen 400mg")
        self.dinfo.insert(0,"1 pill taken 3x per day")
        
        self.columnconfigure(1, weight=0)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(2, weight=10)
        
    def setinfo(self):
        pill.setinfo(self.pname.get(),self.pinfo.get(),self.dinfo.get(),self.numpills.get())
        
class userframe(tk.Frame):
    def __init__(self, master):
        global time_dfont
        global button_dfont
        global dtime
        global pill
        homeuser = tk.Frame.__init__(self, master)
        dtime = tk.StringVar()
        tk.Label(self, text="Home User Mode", font=time_dfont,highlightthickness=0).grid(row=0, columnspan=2,column=0, padx=0, pady=0)
        tk.Label(self, text = "Patient Name: "+pill.pname, font=label_dfont).grid(row=2,column=0)
        tk.Label(self, text = "Pill info: "+pill.pinfo, font=label_dfont).grid(row=3,column=0,columnspan=2)
        tk.Label(self, text = "Dosage: "+pill.dinfo, font=label_dfont).grid(row=4,column=0,columnspan=2)
        self.pill_label = tk.Label(self, text = "Pills left: "+pill.getpills(), font=label_dfont)
        self.pill_label.grid(row=2,column=1)
        button_quit = tk.Button(self, 
                        text="Quit", 
                        font=button_dfont, 
                        command=lambda: master.switch_frame(StartPage),
                        borderwidth=0,
                        highlightthickness=0, 
                        fg='gray10',
                        bg='white')
                        
        button_dispense = tk.Button(self, 
                        text="Dispense Pill", 
                        font=button_dfont, 
                        command=self.dispense,
                        borderwidth=0,
                        highlightthickness=0, 
                        fg='gray10',
                        bg='white')
        self.label_time = tk.Label(self, 
                        textvariable=dtime, 
                        font=time_dfont,
                        highlightthickness=0,
                        fg='black')
        
        
        
        self.label_time.grid(row=1, column=0,columnspan=2, padx=0, pady=0)
        button_quit.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        button_dispense.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(0, weight=10)

    def dispense(self):
        global dispensed
        global dtime
        dispensed = True
        dtime.set("Dispensing Pill")
        pill.dispense()
        iPill.dispensePill()
        self.pill_label.config(text="Pills left: "+pill.getpills())
        dispensed = False

if __name__ == "__main__":
    app = SampleApp()
    app.toggle_fullscreen()
    app.mainloop()
