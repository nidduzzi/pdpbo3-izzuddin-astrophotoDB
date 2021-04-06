# Ahmad Izzuddin 1908919 C2
# using theme 'awdark' from https://sourceforge.net/projects/tcl-awthemes/

from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from CelestialObject import CelestialObject
from PIL import Image, ImageTk

root = Tk()
root.title("AstroPhotoDB")
s = ttk.Style()

try:
    root.tk.eval("""
        set base_theme_dir awthemes-10.3.0/

        package ifneeded awthemes 10.3.0 \
            [list source [file join $base_theme_dir awthemes.tcl]]
        package ifneeded colorutils 4.5 \
            [list source [file join $base_theme_dir colorutils.tcl]]
        package ifneeded awdark 7.11 \
            [list source [file join $base_theme_dir awdark.tcl]]
        # ... (you can add the other themes from the package if you want
        """)
    root.tk.call('package', 'require', 'awdark')
except:
    print("Couldn't load \'awdark\' theme")

if 'awdark' in s.theme_names():
    s.theme_use('awdark')
else:
    s.theme_use('clam')

celestialObjects = []

list_constellations = ["Andromeda", "Antlia", "Apus", "Aquarius", "Aquila", "Ara", "Aries", "Auriga", "Boötes", "Caelum", "Camelopardalis", "Cancer", "Canes Venatici", "Canis Major", "Canis Minor", "Capricornus", "Carina", "Cassiopeia", "Centaurus", "Cepheus", "Cetus", "Chamaeleon", "Circinus", "Columba", "Coma Berenices", "Corona Austrina", "Corona Borealis", "Corvus", "Crater", "Crux", "Cygnus", "Delphinus", "Dorado", "Draco", "Equuleus", "Eridanus", "Fornax", "Gemini", "Grus", "Hercules", "Horologium", "Hydra",
                       "Hydrus", "Indus", "Lacerta", "Leo", "Leo Minor", "Lepus", "Libra", "Lupus", "Lynx", "Lyra", "Mensa", "Microscopium", "Monoceros", "Musca", "Norma", "Octans", "Ophiuchus", "Orion", "Pavo", "Pegasus", "Perseus", "Phoenix", "Pictor", "Pisces", "Piscis Austrinus", "Puppis", "Pyxis", "Reticulum", "Sagitta", "Sagittarius", "Scorpius", "Sculptor", "Scutum", "Serpens", "Sextans", "Taurus", "Telescopium", "Triangulum", "Triangulum Australe", "Tucana", "Ursa Major", "Ursa Minor", "Vela", "Virgo", "Volans", "Vulpecula"]
inputMenu = Frame(root)
inputMenu.pack(side="left", padx=10, pady=10, fill="y")
input_lb_w = 25
input_tb_w = 25
input_tb_h = 1
lb_coordinates = LabelFrame(inputMenu, text="Coordinates")
lb_coordinates.grid(row=0, column=0, sticky="nsew", ipadx=5, ipady=5)
# Declination
lb_declination = Label(lb_coordinates, text="Declination δ(Radians)",
                       width=input_lb_w, anchor="w")
lb_declination.grid(row=0, column=0, padx=10, pady=5)

declination = StringVar()
tb_declination = Entry(lb_coordinates, width=input_tb_w,
                       textvariable=declination)
tb_declination.grid(row=0, column=1, padx=10, pady=5)

# RA
lb_ra = Label(lb_coordinates, text="Right Asscention α(Radians)",
              width=input_lb_w, anchor="w")
lb_ra.grid(row=1, column=0, padx=10, pady=5)

ra = StringVar()
tb_ra = Entry(lb_coordinates, width=input_tb_w, textvariable=ra)
tb_ra.grid(row=1, column=1, padx=10, pady=5)

# Datetime
lb_dt = Label(lb_coordinates, text="Datetime (GMT)", width=input_lb_w,
              borderwidth=0, anchor="w")
lb_dt.grid(row=2, column=0, padx=10, pady=5)

dt = StringVar()
tb_dt = Entry(lb_coordinates, width=input_tb_w, textvariable=dt)
tb_dt.grid(row=2, column=1, padx=10, pady=5)

# Constellation
lb_constellation = Label(lb_coordinates, text="Constellation",
                         width=input_lb_w, anchor="w")
lb_constellation.grid(row=3, column=0, padx=1, pady=1)

constellation = StringVar()
cb_constellation = ttk.Combobox(
    lb_coordinates, width=input_tb_w-3, textvariable=constellation)
cb_constellation.grid(row=3, column=1, padx=1, pady=1)
cb_constellation['values'] = list_constellations

# Category
categories = ("Galaxy", "Gas/Dust Cloud", "Star", "Planetary Body")
lb_category = LabelFrame(inputMenu, text="Category")
lb_category.grid(row=1, column=0, sticky="nsew")
selected_category = StringVar()

for category in categories:
    r = ttk.Radiobutton(
        lb_category,
        text=category,
        value=category,
        variable=selected_category
    )
    r.pack(side="left", fill="x", padx=5, pady=5)

# Visibility
visibilities = ("Radio", "Milimeter Wave", "Microwave",
                "Infra Red", "Visible", "Ultra Violet", "X-Ray", "Gamma")
lb_visibility = LabelFrame(inputMenu, text="Visibility")
lb_visibility.grid(row=2, column=0, sticky="nsew")

selected_visibilities = dict()
for i, visibility in enumerate(visibilities):
    selected_visibilities[visibility] = BooleanVar()
    c = ttk.Checkbutton(
        lb_visibility,
        text=visibility,
        onvalue=True,
        offvalue=False,
        variable=selected_visibilities[visibility]
    )
    c.grid(row=i//4, column=i % 4, padx=10, pady=5, sticky="nsew")

# Celstial Object image

lb_openImg = LabelFrame(inputMenu, text="Open Image", width=20, height=20)
lb_openImg.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
f_img = Frame(lb_openImg, height=200, width=400)
f_img.pack(side="left", padx=10, pady=10)
f_img.pack_propagate(0)
lb_img = Label(f_img, background="Grey")
lb_img.pack(fill="both", expand="yes")


def getImg():
    # get image filename
    root.filename = filedialog.askopenfilename(initialdir="~",
                                               title="Select a File",
                                               filetypes=(
                                                   ("Images", "*.jpg* *.jpeg* *.png*"), ("all files", "*.*"))
                                               )
    # display image preview
    load = Image.open(root.filename)
    render = ImageTk.PhotoImage(load.resize((400, 200), Image.ANTIALIAS))
    lb_img.configure(image=render)
    lb_img.image = render
    root.image = render
    load.close()


bt_openImg = Button(lb_openImg, text="Browse...", command=getImg)
bt_openImg.pack(side=TOP, padx=10, pady=10)

# submit


def submitObject():
    if((declination.get() == "")
       or (ra.get() == "")
       or (constellation.get() == "")
       or (not bool(selected_visibilities))
       or (selected_category.get() == "")
       or (root.filename == None)
       or (root.filename == "")
       or (root.image == None)
       ):
        messagebox.showwarning(title="Incomplete input",
                               message="Please fill in all required fields")
        pass
    elif not(constellation.get() in list_constellations):
        messagebox.showwarning(title="Invalid Constellation",
                               message="Please choose a valid constellation from the dropdown")
        pass
    else:
        # insert new object to existing list of objects
        celestialObjects.append(CelestialObject(declination.get(), ra.get(), dt.get(), constellation.get(
        ), selected_category.get(), {i: selected_visibilities[i].get() for i in selected_visibilities}, root.filename, root.image))
        # reset the form
        declination.set("")
        ra.set("")
        dt.set("")
        constellation.set("")
        selected_category.set("")
        for i in selected_visibilities:
            selected_visibilities[i].set(False)
        root.filename = None
        root.image = None
        lb_img.configure(image="")


bt_submit = Button(inputMenu, text="Submit", command=submitObject)
bt_submit.grid(row=4, column=0, sticky="ew")

# App Menu
appMenu = Frame(root)
appMenu.pack(side="right", padx=10, pady=10, fill="y")

lb_appName = Label(appMenu, text="Astro\nPhoto\nDB",
                   borderwidth=0, anchor="w", justify=LEFT)
lb_appName.grid(row=0, column=0)
lb_appName.configure(font=("Helvetica", 36, "bold"))


def seeSubmissions():
    top = Toplevel()
    top.title("Submissions")
    top.focus()
    f = Frame(top)
    f.pack(fill="both", expand="yes")
    # Table Header
    lb_hd_declination = Label(f, text="Declination",
                              borderwidth=1, relief="solid")
    lb_hd_declination.grid(row=0, column=0, rowspan=2, sticky="news", ipadx=5)
    lb_hd_ra = Label(f, text="Right Ascension",
                     borderwidth=1, relief="solid")
    lb_hd_ra.grid(row=0, column=1, rowspan=2, sticky="news", ipadx=5)
    lb_hd_dt = Label(f, text="Date Time", borderwidth=1, relief="solid")
    lb_hd_dt.grid(row=0, column=2, rowspan=2, sticky="news", ipadx=5)
    lb_hd_constellation = Label(
        f, text="Constellation", borderwidth=1, relief="solid")
    lb_hd_constellation.grid(
        row=0, column=3, rowspan=2, sticky="news", ipadx=5)
    lb_hd_category = Label(f, text="Category", borderwidth=1, relief="solid")
    lb_hd_category.grid(row=0, column=4, rowspan=2, sticky="news", ipadx=5)
    lb_hd_visibility = Label(f, text="Visibility",
                             borderwidth=1, relief="solid")
    lb_hd_visibility.grid(row=0, column=5, columnspan=len(
        visibilities), sticky="news", ipadx=5)
    for j, visibility in enumerate(visibilities):
        lb_cb_ = Label(f, text=visibility, borderwidth=1, relief="solid")
        lb_cb_.grid(row=1, column=5+j, sticky="news", ipadx=5)

    lb_hd_img = Label(f, text="Image", borderwidth=1,
                      relief="solid", width=40)
    lb_hd_img.grid(row=0, column=5+len(visibilities), rowspan=2, sticky="news")

    # Table Body
    for i, celestialObject in enumerate(celestialObjects):
        lb_cb_declination = Label(
            f, text=celestialObject.declination, borderwidth=1, relief="solid")
        lb_cb_declination.grid(row=i+2, column=0, sticky="nesw", ipadx=5)
        lb_cb_ra = Label(f, text=celestialObject.ra,
                         borderwidth=1, relief="solid")
        lb_cb_ra.grid(row=i+2, column=1, sticky="nesw", ipadx=5)
        lb_cb_dt = Label(f, text=celestialObject.dt,
                         borderwidth=1, relief="solid")
        lb_cb_dt.grid(row=i+2, column=2, sticky="nesw", ipadx=5)
        lb_cb_constelation = Label(
            f, text=celestialObject.constellation, borderwidth=1, relief="solid")
        lb_cb_constelation.grid(row=i+2, column=3, sticky="nesw", ipadx=5)
        lb_cb_cateogry = Label(
            f, text=celestialObject.category, borderwidth=1, relief="solid")
        lb_cb_cateogry.grid(row=i+2, column=4, sticky="nesw", ipadx=5)
        for j, visibility in enumerate(celestialObject.visibilities):
            lb_cb_ = Label(f, text=str(
                celestialObject.visibilities[visibility]), borderwidth=1, relief="solid")
            lb_cb_.grid(row=i+2, column=5+j, sticky="nesw", ipadx=5)
        lb_cb_img = Label(f, image=celestialObject.image,
                          borderwidth=1, relief="solid")
        lb_cb_img.grid(row=i+2, column=5+len(visibilities), sticky="nesw")

    def exit_btn():
        top.destroy()
        top.update()
    bt_exit = Button(f, text="Exit", width=10, command=exit_btn)
    bt_exit.grid(row=3+len(celestialObjects), column=0,
                 columnspan=6+len(visibilities), pady=20, ipadx=5)
    pass


bt_see = Button(appMenu, text="SEE ALL SUBMISSIONS", command=seeSubmissions)
bt_see.grid(row=1, column=0, sticky="new", padx=1, pady=5)


def clearSubmissions():
    confirm = messagebox.askokcancel(
        title="Confirm Clear Submissions", message="Do you want to clear all submissions?")
    if confirm == True:
        celestialObjects.clear()
        messagebox.showinfo(title="Submissions Cleared",
                            message="All submissions have been cleared")


bt_clear = Button(appMenu, text="CLEAR ALL SUBMISSIONS",
                  command=clearSubmissions)
bt_clear.grid(row=2, column=0, sticky="new", padx=1, pady=5)


def about():
    top = Toplevel()
    top.title("About")
    f = Frame(top)
    f.pack(fill="both", expand="yes", ipadx=5, ipady=5)
    lb_title = Label(f, text="AstroPhotoDB", anchor="w")
    lb_title.grid(row=0, column=0, sticky="w")
    lb_desc = Label(f, text="Aplikasi ini merekam data observasi astronomi\nyang memiliki gambar. Data termasuk koordinat,\nkategori, daerah tampak spektrum, dan gambar.", anchor="w")
    lb_desc.grid(row=1, column=0, sticky="w")
    lb_nama = Label(f, text="Nama: Ahmad Izzuddin\nNIM: 1908919", anchor="w")
    lb_nama.grid(row=2, column=0, sticky="w")

    def exit_btn():
        top.destroy()
        top.update()
    bt_exit = Button(f, text="Exit", width=10, command=exit_btn)
    bt_exit.grid(row=3, column=0, pady=5)
    pass


bt_about = Button(appMenu, text="ABOUT", command=about)
bt_about.grid(row=3, column=0, sticky="new", padx=1, pady=5)


def exit():
    confirm = messagebox.askyesno("Confirm exit", "Do you want to exit?")
    if confirm == True:
        root.quit()


bt_exit = Button(appMenu, text="EXIT", command=exit)
bt_exit.grid(row=10, column=0, sticky="sew", padx=1, pady=5)
root.configure(bg=s.lookup('TFrame', 'background'))
root.mainloop()
