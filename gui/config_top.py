import typing
import os
import shutil
from pathlib import Path
from tkinter import messagebox

from web import web
from gui.notification import _give_notification_link

from tkinter import *
from tkinter.ttk import *

from helper.popup import PopUp

if typing.TYPE_CHECKING:
    from gui import GUI


def start_fullfisher_config(gui: 'GUI'):
    def save():
        gui._config.set("tesseract_dir", tesseract_entry.get(), False)
        gui._config.save_config()

    top = PopUp(save, gui._root, background=gui._root["background"])
    controls_frame = Frame(top)
    top.title("Config")

    Label(controls_frame, text="Tesseract Directory:").grid(row=0, column=0)
    tesseract_entry = Entry(controls_frame, justify=CENTER)
    tesseract_entry.insert(0, gui._config.get("tesseract_dir", ""))
    tesseract_entry.grid(row=0, column=1)

    controls_frame.pack(padx=(5, 5), pady=(5, 5))
    top.start()


def start_semifisher_config(gui: 'GUI'):
    def buttonClick():
        save()
        print(os.getcwd())
        currentPATH = os.getcwd()
        addonsPATH = gui._config.get("addons_path")
        try:
            addonsPATH=str(addonsPATH)
            if len(addonsPATH) != 0: #NULL value
                try:
                    os.chdir(addonsPATH)
                    FooAddon = Path('FooAddon')
                    ProvisionsChalutier = Path('ProvisionsChalutier')
                    if FooAddon.exists() and FooAddon.is_dir():
                        shutil.rmtree(FooAddon)
                    if ProvisionsChalutier.exists() and ProvisionsChalutier.is_dir():
                        shutil.rmtree(ProvisionsChalutier)
                except:
                    messagebox.showerror("Eror","No location found Addons PATH!")
            os.chdir(currentPATH)
            shutil.copytree("Addons", addonsPATH + "/FooAddon" )
            shutil.copytree("Addons", addonsPATH + "/ProvisionsChalutier" )
            messagebox.showerror("Successful","Addons are added!")
        except:
            messagebox.showerror("Eror","No location found!")
        
        
        
        
        
    def save():
        gui._config.set("action_key", action_key_entry.get(), False)
        gui._config.set("addons_path", addons_path_entry.get(), False)
        gui._config.set("borderless", borderless.instate(['selected']), False)
        gui._config.save_config()

    top = PopUp(save, gui._root, background=gui._root["background"])
    controls_frame = Frame(top)
    top.title("Config")

    Label(controls_frame, text="Notification:").grid(row=0, column=0)

    gui._notify = IntVar(0)
    gui._notify_check = Checkbutton(controls_frame, command=lambda: _give_notification_link(gui),
                                    variable=gui._notify)
    gui._notify_check.grid(row=0, column=1)
    gui._notify_check['state'] = DISABLED
    is_subbed = web.is_subbed(gui._config.get('uid'))
    if is_subbed[1]:
        gui._notify_check['state'] = NORMAL
        gui._notify.set(is_subbed[0])

    Label(controls_frame, text="Fullscreen: ").grid(row=1, column=0, pady=(5, 5))
    borderless = Checkbutton(controls_frame, var=BooleanVar(value=gui._config.get("borderless")))
    borderless.grid(row=1, column=1)

    Label(controls_frame, text="Action Key:").grid(row=2, column=0)
    Label(controls_frame, text="Addons PATH:").grid(row=3, column=0)
    action_key_entry = Entry(controls_frame, justify=CENTER)
    action_key_entry.grid(row=2, column=1)
    action_key_entry.insert(0, gui._config.get("action_key","e"))
    addons_path_entry = Entry(controls_frame, justify=CENTER)
    addons_path_entry.grid(row=3, column=1)
    addons_path_entry.insert(0, gui._config.get("addons_path",""))
    Label(controls_frame, text="Addons PATH:").grid(row=3, column=0)
    Label(controls_frame, text="Please enter the road as in the example. \nThis process takes time. Please wait!").grid(row=4, columnspan=2)
    Label(controls_frame, text="C:\\Users\\***\\Documents\\Elder Scrolls Online\\live\\AddOns").grid(row=5, columnspan=2)
    Apply=Button(controls_frame, text="APPLY JUST ADDONS ", command=buttonClick).grid(row=6, columnspan=2)
    
    
    controls_frame.pack(padx=(5, 5), pady=(5, 5))
    
    top.start()
    
    