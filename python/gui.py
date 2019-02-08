import tkinter as tk
import tkinter.font as tkFont
import time
import iPill

###############################################################################
# Parameters and global variables

# Default font size
font_size = 10

# Declare global variables
root = None
dfont = None
frame = None
dtime = None
last = time.localtime()
flag = False

# Global variable to remember if we are fullscreen or windowed
fullscreen = False

###############################################################################
# Functions

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize()

# Automatically resize font size based on window size
def resize(event=None):

    global time_dfont
    global button_dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 2)))
    time_dfont.configure(size=new_size)
    new_size = -max(12, int((frame.winfo_height() / 30)))
    button_dfont.configure(size=new_size)


# Read values from the sensors at regular intervals
def update():

    global root
    global dtime
    global last
    global flag
    
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
    dtime.set(shours + ':' + smin + ':' + ssec)
    if abs(last.tm_sec - local_time.tm_sec) > 5:
        flag = True    
    
    if local_time.tm_sec%10 < 5 and flag == True:
        button_dispense.config(state="normal")
        button_dispense.grid(row=1, column=0, padx=5, pady=5)
    else:
        button_dispense.grid_forget()
        
    
    # Schedule the poll() function for another 500 ms from now
    root.after(500, update)

def dispense():
    global last
    global flag
    button_dispense.grid_forget()
    button_dispense.config(state="disabled")
    flag = False
    last = time.localtime()
    iPill.dispensePill()
    

###############################################################################
# Main script

# Create the main window
root = tk.Tk()
root.title("iPill")

# Create the main container
frame = tk.Frame(root, bg='blue')

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)
frame.config(cursor='none')
# Variables for holding temperature and light data
dtime = tk.StringVar()

# Create dynamic font for text
time_dfont = tkFont.Font(family='Courier New', size=font_size)
button_dfont = tkFont.Font(size=font_size)

# Create widgets
label_time = tk.Label(  frame, 
                        textvariable=dtime, 
                        font=("Courier", 60), 
                        fg='white', 
                        bg='blue')
button_quit = tk.Button(frame, 
                        text="Quit", 
                        font=button_dfont, 
                        command=root.destroy,
                        borderwidth=0,
                        highlightthickness=0, 
                        fg='gray10',
                        bg='white')
                        
button_dispense = tk.Button(frame, 
                        text="Dispense Pill", 
                        font=("Courier", 14), 
                        command=dispense,
                        #command=iPill.dispensePill,
                        borderwidth=2,
                        highlightthickness=0,
                        height=5,
                        width=20, 
                        fg='gray10',
                        bg='white')

# Lay out widgets in a grid in the frame
label_time.grid(row=0, column=0, padx=0, pady=20)
button_quit.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
button_dispense.grid(row=1, column=0, padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
frame.rowconfigure(0, weight=10)
frame.rowconfigure(1, weight=10)
frame.columnconfigure(0, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Schedule the poll() function to be called periodically
root.after(20, update)

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()
