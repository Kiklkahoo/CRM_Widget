from tkinter import *
import functools
import pyodbc
import hashlib
from CustomTkinterUIObjects import CustomWidgets
import configparser
from tkinter import ttk
from tkinter import Tk, Label, BOTH
import math
#import SELFIE
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
import random
import getpass
import os
import time
from tkinter import ttk, messagebox, filedialog
from tkinter.messagebox import showerror
from tkinter import font
from tkinter import filedialog as fd
import datetime
import configparser

class FindWindowUI(Frame):
    def __init__(self,main_color,second_color,button_color,border_color,font_size,current_dir,pad_y, func, root):
        another_frame = Toplevel(root, bg=main_color)
        another_frame.configure(background=main_color)
        another_frame.title("Поиск клиента")
        self.window=another_frame

        super(FindWindowUI, self).__init__(another_frame)
        self.main_color=main_color
        self.border_color=border_color
        self.button_color=button_color
        self.second_color=second_color
        self.font_size=font_size
        self.font_size_entry=str(int(self.font_size)+4)
        self.table_columns = []
        self.columns_values = []
        self.current_dir=current_dir
        self.pad_y=pad_y

        self.func = func

        self.grid()
        self.entry_width = 22
        self.is_ui_already_loaded=False


        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size_norm = (465, 212)
        x = w / 2 - size_norm[0] / 2
        y = h / 2 - size_norm[1] / 2

        self.additional_params=[]
        self.column_count=1

        self.create_widgets()



    def create_widgets(self):

        self.row_counter=0

        self.create_tree_widgets()





        self.under_tree_find_frame = Frame(self, background=self.second_color, padx=0)
        self.under_tree_find_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        self.under_tree_frame=Frame(self,background=self.second_color,padx=-20)
        self.under_tree_frame.pack(fill=BOTH, expand=YES,side=LEFT)

        self.find_label = Label(self.under_tree_find_frame, text="Поиск работника:", font="Ubuntu 12 bold",
                                justify=LEFT,
                                bg=self.second_color)
        self.find_label.grid(row=self.row_counter, column=0, columnspan=10,padx=10, pady=7,sticky=W)
        self.row_counter+=1

        self.find_client_label = Label(self.under_tree_find_frame, text="ФИО: ",
                                      font='Ubuntu ' + str(int(self.font_size)),
                                      justify=LEFT, bg=self.second_color)
        self.find_client_label.grid(row=self.row_counter, column=0, padx=10, pady=7, sticky=W,)

        self.find_client_entry = CustomWidgets.CustomEntry(self.under_tree_find_frame, width=self.entry_width,
                                                          font='Ubuntu ' + str(int(self.font_size_entry)),
                                                          justify=LEFT)
        self.find_client_entry.grid(row=self.row_counter, column=4, columnspan=3, sticky=W, padx=0, pady=self.pad_y)
        self.find_client_entry.set_border_color(self.border_color)

        image3 = Image.open('%s\\images\\magnifier.png' % (self.current_dir))
        render3 = ImageTk.PhotoImage(image3.resize((27, 28), Image.ANTIALIAS))
        self.find_client_button = Button(self.under_tree_find_frame, image=render3, bg=self.button_color,relief=FLAT, overrelief=SOLID,
                                      command=self.find_client)
        self.find_client_button.grid(row=self.row_counter, column=7, columnspan=1,padx=0, pady=self.pad_y)
        self.find_client_button.image = render3


        self.confirm_finding_button = Button(self.under_tree_frame,text='OK', bg=self.main_color, relief=FLAT,font='Ubuntu ' + str(int(self.font_size_entry)),
                                      overrelief=SOLID,
                                      command=self.confirm_finding,height=2,state=DISABLED)
        self.confirm_finding_button.pack(fill=BOTH, expand=YES,)
        self.row_counter += 1



    def confirm_finding(self):
        string_buffer=self.client_info_list['values']
        my_file = open("temp.txt", "w")
        my_file.write(str(string_buffer[0]))
        my_file.close()
        self.window.destroy()


    def find_client(self):

        self.dbq = pyodbc.connect('DSN=KADRY')
        self.cursor = self.dbq.cursor()

        self.tree.delete(*self.tree.get_children())
        self.destroy_list = []

        style = ttk.Style()
        style.configure("Tpole", background="#333")

        table = []
        #request = "SELECT * FROM [Клиенты] where [ФИО] LIKE '%s'" % (str('%'+self.find_client_entry.get()+'%'))
        #print(request)
        example = [
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Отсутствует"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                  ]
        for appended_str in example:
            if appended_str[1] != "None":

                self.tree.insert('', index=END, values=(
                        appended_str[0], appended_str[1], appended_str[2], appended_str[3], appended_str[4], appended_str[5]))

                table.append(appended_str)

        self.treeview_sort_column(self.tree, 'ID', 0)
    def create_tree_widgets(self):

        self.tree = ttk.Treeview(self,height=14, show='headings', columns=(
            'ID', 'Name','SitizenShip', 'Age','Phone','Position'))
        self.tree.column("ID", width=int(30*math.sqrt(int(self.font_size)/12)), anchor=CENTER)
        self.tree.column("Name", width=int(100*math.sqrt(int(self.font_size)/12)), anchor=CENTER)
        self.tree.column("SitizenShip", width=int(170*math.sqrt(int(self.font_size)/12)), anchor=CENTER)
        self.tree.column("Age", width=int(80*math.sqrt(int(self.font_size)/12)), anchor=CENTER)

        self.tree.column("Phone", width=int(120*math.sqrt(int(self.font_size)/12)), anchor=CENTER)

        self.tree.column("Position", width=int(180*math.sqrt(int(self.font_size)/12)), anchor=CENTER)


        self.tree.heading("ID", text='ID')
        self.tree.heading("Name", text='ФИО')
        self.tree.heading("SitizenShip", text='Гражданство')
        self.tree.heading("Age", text='Возраст')

        self.tree.heading("Phone", text='Номер телефона')

        self.tree.heading("Position", text='Должность')

        self.tree.pack(anchor=N, fill=X, expand=NO)
        self.tree.bind('<<TreeviewSelect>>', self.tree_select_event)
        self.update_tree("not_an_event")


    def update_tree(self,event):
        self.dbq = pyodbc.connect('DSN=KADRY')
        self.cursor = self.dbq.cursor()

        self.tree.delete(*self.tree.get_children())
        self.destroy_list = []

        style = ttk.Style()
        style.configure("Tpole", background="#333")
        table=[]
        example = [
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Отсутствует"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 1"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 2"],
                    ["client_id", "Имя сотрудника", "Россия", "37","89998885555", "Должность 3"],
                  ]
        for appended_str in example:
            if appended_str[1]!="None":
                self.tree.insert('',index=END,values=(
                                                        appended_str[0],
                                                        appended_str[1],
                                                        appended_str[2],
                                                        appended_str[3],
                                                        appended_str[4],
                                                        appended_str[5]
                                                     )
                                 )
                table.append(appended_str)


        self.treeview_sort_column(self.tree, 'ID', 0)

    def treeview_sort_column(self,tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)

        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


    def tree_select_event(self, event):
        self.confirm_finding_button.config(state=ACTIVE, fg="green")
        self.update_idletasks()
        self.window.update_idletasks()
        self.window.update()

        self.client_info_list = self.tree.item(self.tree.selection())

        self.func(self.client_info_list)
