# import lib
import tkinter, base64
# -- python 2
# import urllib
from urllib.parse import quote_plus
from urllib.request import urlopen

def getAddress(location, width, height, zoom):
    locationnospaces = quote_plus(location)
    # -- python 2
    # locationnospaces = urllib.quote_plus(location)
    address = "http://maps.googleapis.com/maps/api/staticmap?center={0}&zoom={1}&size={2}x{3}&format=gif&sensor=true".format(locationnospaces, zoom, width, height)
    return address

def getMap(location, width, height, zoom):
    address = getAddress(location, width, height, zoom)
    # read the url
    # -- python 2
    # urlreader = urllib.urlopen(address)
    urlreader = urlopen(address)
    data = urlreader.read()
    # close url reader
    urlreader.close()
    base64data = base64.encodestring(data)

    image = tkinter.PhotoImage(data=base64data)
    return image

def getLabelName():
    popup = tkinter.Toplevel()
    popup.title("New Marker")

    label = tkinter.Label(popup, text="Please enter a label for your marker")
    label.pack()

    label_name = tkinter.StringVar()
    textbox = tkinter.Entry(popup, textvariable=label_name)
    textbox.pack()
    textbox.focus_force()

    button = tkinter.Button(popup, text="Done", command=popup.destroy)
    button.pack()

    popup.wait_window()
    text = label_name.get()
    return text

# handling on map clicks
def canvasClick(event):
    x, y = event.x, event.y
    widget = event.widget
    size = 10
    widget.create_oval(x-size, y-size, x+size, y+size, width=2)
    label = getLabelName()
    widget.create_text(x, y+2*size, text=label)

def main():
    # init window,location and map zoom
    location = "-7.9682132,112.6305035"
    width       = 720
    height      = 480
    zoom        = 16
        
    # init tkinter
    window = tkinter.Tk()
    window.option_add('*font', ('Arial', 11, 'bold'))
    # set window title
    window.title("Travel Track (Beta)")
    # set minimum size
    window.minsize(width, height)
    # call getmap function
    mapimage = getMap(location, width, height, zoom)
    canvas = tkinter.Canvas(window, width=540, height=height)
    canvas.create_image(0, 0, image=mapimage, anchor=tkinter.NW)
    canvas.bind("<Button-1>",canvasClick)
    canvas.pack(side="left", fill="y")

    # button tracking
    btn_track = tkinter.Button(text="Track", height=2,
                               bd='1px', bg="#2962FF", fg="white", relief="solid")
    btn_track.pack(anchor='n', fill='x', padx=6, pady=2)

    # button exit
    btn_exit = tkinter.Button(text="Exit", height=2,
                              bd='1px', bg="#DD2C00", fg="white", relief="solid",
                              command=window.destroy)
    btn_exit.pack(anchor="e", fill='x', padx=6, pady=2)


    window.mainloop()

if __name__ == "__main__":
    main()
