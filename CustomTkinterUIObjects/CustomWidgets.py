from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import pyodbc
from tkinter import *
import json

from PIL import Image, ImageTk
import os
from SimpleDialogs.find_client_dialog import FindClientScript
from tkcalendar import Calendar, DateEntry
import copy



def testVal(inStr, acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True


class CreateToolTip(object):
    def __init__(self, widget, tip_font, text='widget info'):
        self.waittime = 500    #ms
        self.wraplength = 400  #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None
        self.tip_font=tip_font

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, font=self.tip_font,justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class CustomButton(Frame):
    def __init__(self, parent, side=None,fill=None,*args, **kwargs):
        Frame.__init__(self, parent)
        self.but = Button(self,*args, **kwargs)
        if side!=None:
            self.but.pack(expand=1,side=side,fill=X)
        else:
            self.but.pack(expand=1, side=LEFT, fill=X)
        if fill == "both":
            self.but.pack(expand=1, side=LEFT, fill=BOTH)

        self.colors=['white','light gray', 'gray']

    def tag(self, getted_tags_list):
        self.tag = getted_tags_list

    def command(self, command):
        self.but.config(command = command)


    def set_border_color(self, color):
        self.configure(background=color,borderwidth = 2, padx=1,pady=1,relief = FLAT)

    def set_border_color_width(self, color, border_width):
        self.configure(background=color,borderwidth = border_width, padx=1,pady=0,relief = FLAT)
    def bind(self,*args):
        self.but.bind(*args)
    def state(self,state):
        self.but.config(state=state)

    def relief(self, relief):
        self.but.config(relief=relief)
    def disabledforeground(self, color):
        self.but.config(disabledforeground = color)
    def create_label(self,*args, **kwargs):
        self.label = Button(self,*args, **kwargs)
        self.label.pack(expand=1, side=LEFT, fill=BOTH)
        self.label['command']=self.but['command']
    def destroy_label(self):
        self.label.destroy()
    def activated(self):
        self.but.config(relief=RAISED)
    def deactivated(self):
        self.but.config(relief=FLAT)
    def set_near_label(self,near_label):
        self.near_label=near_label
    def color_change(self,*args):
        self.cur_color = self.but['bg']
        for gg in range(len(self.colors)):
            if self.colors[gg] != self.cur_color:
                self.but.config(bg=self.colors[gg])

    def mem_client_num_and_date(self, num, date):
        self.client_num = num
        self.client_date = date

class CustomLabel(Frame):
    def __init__(self, parent, side=None,fill=None, border=False, *args, **kwargs):
        Frame.__init__(self, parent)
        self.labl = Label(self,*args, **kwargs)
        if side!=None:
            self.labl.pack(expand=1,side=side,fill=X)
        else:
            self.labl.pack(expand=1, side=LEFT, fill=X)
        if fill=="both":
            self.labl.pack(expand=1, side=LEFT, fill=BOTH)
        self.colors=['white','gray']
        if border:
            border_widget = Button(self, bg="GREEN", relief=FLAT, state=DISABLED, text=" ", font=5)
            border_widget.pack(expand=1, side=TOP, fill=X)



    def set_border_color(self, color, width=2):
        self.configure(background=color,borderwidth = width, padx=1,pady=1,relief = FLAT)

    def set_border_color_width(self, color, border_width):
        self.configure(background=color,borderwidth = border_width, padx=1,pady=0,relief = FLAT)
    def set_bg_color(self, color):
        self.labl.configure( bg = color)
    def set_fg_color(self, color):
        self.labl.configure(fg=color)
    def set_text(self, text, font):
        self.labl.configure(text = text, font = font, width = 5)

class CustomLabelWithBorder(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.labl = Label(self,*args, **kwargs)
        self.labl.pack(expand=1,side=TOP,fill=BOTH)
        self.border_widget = Frame(self, bg="GREEN", height=5)
        self.border_widget.pack(expand=NO, side=BOTTOM, fill=X)
        self.assigned_widgets=[]
        self.labl.bind("<Enter>", self.mouse_over_enter_event)
        self.labl.bind("<Leave>", self.mouse_over_leave_event)

    def disable_border(self):
        self.border_widget.configure(bg="light gray")
        self.labl.unbind("<Enter>")
        self.labl.unbind("<Leave>")

    def assign_another_widget(self, widget):
        self.assigned_widgets.append(widget)


    def mouse_over_enter_event(self, event):
        for gg in range(len(self.assigned_widgets)):
            try:
                self.assigned_widgets[gg].mouse_over_enter_event(event)
            except:
                pass


        self.border_widget.configure(bg="light green")

    def mouse_over_leave_event(self, event):
        for gg in range(len(self.assigned_widgets)):
            try:
                self.assigned_widgets[gg].mouse_over_leave_event(event)
            except:
                pass

        self.border_widget.configure(bg="GREEN")

    def set_border_color(self, color):
        self.configure(background=color,borderwidth = 2, padx=1,pady=1,relief = FLAT)

    def set_border_color_width(self, color, border_width):
        self.configure(background=color,borderwidth = border_width, padx=1,pady=0,relief = FLAT)
    def set_bg_color(self, color):
        self.labl.configure( bg = color)
    def set_fg_color(self, color):
        self.labl.configure(fg=color)
    def set_text(self, text, font, width=5):
        self.labl.configure(text = text, font = font, width = width)
    def set_empty(self, text, font):
        self.labl.configure(font=font, text=text, width=1)



class WidgetsBox(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.inside_widgets_list = []
        pass

    def create_widget_inside(self, widget_type, text="", height = 1, font_size = 10, state = "common"):
        created_widget = ""
        font = 'Ubuntu ' + str(4 + int(font_size)) + ' bold'
        if widget_type == "Label":
            created_widget = CustomLabel(self, fill="both", text = text, height = height, font = font)
        if widget_type == "Button":
            created_widget = CustomButton(self, text = text, height = height, font = font, state=DISABLED, disabledforeground = "black")
        if widget_type == "Entry":
            created_widget = CustomEntry(self, text = text, height = height, font = font)
        if widget_type == "Combobox":
            created_widget = CustomCombobox(self, text = text, height = height, font = font)
        if widget_type == "Frame":
            created_widget = CustomCombobox(self)
        if widget_type == "Shift":
            print(state)
            created_widget = ShiftWidget(self, state=state,font=("Ubuntu", 13))


        self.inside_widgets_list.append(created_widget)
        #print(self.inside_widgets_list)
        return created_widget

    def set_bg_color(self, color):
        self.config(bg=color)

class CustomFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)


        self.font=("Ubuntu", 11)

    def set_border_color(self, color, width=2):
        self.configure(background=color,borderwidth =width, padx=1,pady=1, relief = FLAT)

    def enable_border(self):
        self.border_widget = Frame(self, bg="GREEN", height=2)
        self.border_widget.pack(expand=NO, side=BOTTOM, fill=X)

    def mouse_over_enter_event(self, event):

        self.border_widget.configure(bg="light green")

    def mouse_over_leave_event(self, event):

        self.border_widget.configure(bg="GREEN")

    def set_bg(self, color):
        Frame.config(self, bg = color)
    def set_bg_image(self, image):
        background_label = Label(self, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = image
    def set_font(self, font):
        self.font=font


    def create_label(self,text, color, width, fg_color):

        if width!=None:
            if len(text[1])>int(width)+1:
                a=len(text[1])

                self.label = Label(self, text=text[1][0:width], relief=FLAT, bg=color, width=width, font=self.font, fg=fg_color)
                self.label_2 = Label(self, text=text[1][width:len(text[1])], relief=FLAT, bg=color, width=width, font=self.font, fg=fg_color)
            else:
                self.label = Label(self, text=text[1], relief=FLAT, bg=color, width=width, font = self.font, fg= fg_color)
        else:
            if len(text[1])>=10:

                self.label = Label(self, text=text[1][0:10], relief=FLAT, bg=color, font=self.font, fg=fg_color)
                self.label_2 = Label(self, text=text[1][10:len(text[1])], relief=FLAT, bg=color, width=width,
                                     font=self.font, fg=fg_color)


            else:
                self.label = Label(self, text=text[1], relief=FLAT, bg=color, font=self.font, fg=fg_color)

        self.label.pack(fill="both", expand=2, side=TOP)
        try:
            self.label_2.pack(fill="both", expand=2, side=TOP)
        except:
            pass


    def create_button(self,text, color, width, fg_color, command):

        if width!=None:
            self.button = Button(self, text=text, relief=FLAT, bg=color, width=width, font = self.font, fg= fg_color, command = command)
        else:
            self.button = Button(self, text=text, relief=FLAT, bg=color, font=self.font, fg=fg_color,  command = command)

        self.button.pack(fill="both", expand=2, side=LEFT)


    def get(self):
        return self.label['text']


class CustomFrameWithBorder(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.Frame = Frame(self,*args, **kwargs)
        self.Frame.pack(fill="both", expand=2, side=TOP)

        self.font = ("Ubuntu", 11)

    def set_border_color(self, color):
        self.configure(background=color, borderwidth=2, padx=1, pady=1, relief=FLAT)

    def enable_border(self):
        self.border_widget = Frame(self, bg="GREEN", height=2)
        self.border_widget.pack(expand=NO, side=BOTTOM, fill=X)

    def mouse_over_enter_event(self, event):

        self.border_widget.configure(bg="light green")

    def mouse_over_leave_event(self, event):

        self.border_widget.configure(bg="GREEN")

    def set_bg(self, color):
        Frame.config(self, bg=color)

    def set_bg_image(self, image):
        background_label = Label(self, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = image

    def set_font(self, font):
        self.font = font

    def create_label(self, text, color, width, fg_color):

        if width != None:
            if len(text[1]) > int(width) + 1:
                a = len(text[1])

                self.label = Label(self, text=text[1][0:width], relief=FLAT, bg=color, width=width, font=self.font,
                                   fg=fg_color)
                self.label_2 = Label(self, text=text[1][width:len(text[1])], relief=FLAT, bg=color, width=width,
                                     font=self.font, fg=fg_color)
            else:
                self.label = Label(self, text=text[1], relief=FLAT, bg=color, width=width, font=self.font, fg=fg_color)
        else:
            if len(text[1]) >= 10:

                self.label = Label(self, text=text[1][0:10], relief=FLAT, bg=color, font=self.font, fg=fg_color)
                self.label_2 = Label(self, text=text[1][10:len(text[1])], relief=FLAT, bg=color, width=width,
                                     font=self.font, fg=fg_color)


            else:
                self.label = Label(self, text=text[1], relief=FLAT, bg=color, font=self.font, fg=fg_color)

        self.label.pack(fill="both", expand=2, side=TOP)
        try:
            self.label_2.pack(fill="both", expand=2, side=TOP)
        except:
            pass

    def create_button(self, text, color, width, fg_color, command):

        if width != None:
            self.button = Button(self, text=text, relief=FLAT, bg=color, width=width, font=self.font, fg=fg_color,
                                 command=command)
        else:
            self.button = Button(self, text=text, relief=FLAT, bg=color, font=self.font, fg=fg_color, command=command)

        self.button.pack(fill="both", expand=2, side=LEFT)

    def get(self):
        return self.label['text']


class CustomCombobox(Frame):
    def __init__(self, parent, side=LEFT,*args, **kwargs):
        Frame.__init__(self, parent)
        self.combo = ttk.Combobox(self, *args, **kwargs)
        self.combo.pack(fill="both", expand=2,side=side)
        self.get = self.combo.get
        self.insert = self.combo.insert
        self.values_list=[]

    def enable_border(self):
        self.border_widget = Frame(self, bg="GREEN", height=2)
        self.border_widget.pack(expand=NO, side=BOTTOM, fill=X)

    def mouse_over_enter_event(self, event):

        self.border_widget.configure(bg="light green")

    def mouse_over_leave_event(self, event):

        self.border_widget.configure(bg="GREEN")

    def set_border_color(self, color):
        self.configure(background=color,borderwidth = 2, padx=1,pady=1, relief = FLAT)
    def bind(self, *args):
        self.combo.bind(*args)
    def zdelat_zaebis(self,*args):
        self.combo.configure(width=8)
    def current(self,*args):
        self.combo.current(*args)
    def values(self,list):
        self.combo.config(values=list)
        self.values_list=list
    def create_tooltip(self,font,tooltip_text):
        self.toolip = CreateToolTip(self.combo,font,tooltip_text)
    def get(self):
        return self.combo.get()

class CustomEntry(Frame):
    def __init__(self, parent, placeholder=None,side=None, *args, **kwargs):
        Frame.__init__(self, parent)



        self.entry = Entry(self, relief=FLAT,*args, **kwargs)

        if side!=None:
            self.entry.pack(fill="both", expand=2, side=TOP)
        else:
            self.entry.pack(fill="both", expand=2, side=LEFT)



        self.get = self.entry.get
        self.insert = self.entry.insert
    def enable_border(self):
        self.border_widget = Frame(self, bg="GREEN", height=2)
        self.border_widget.pack(expand=NO, side=BOTTOM, fill=X)

    def mouse_over_enter_event(self, event):

        self.border_widget.configure(bg="light green")

    def mouse_over_leave_event(self, event):

        self.border_widget.configure(bg="GREEN")

    def tag(self, getted_tags_list):
        self.tag = getted_tags_list

    def set_border_color(self, color):
        self.configure(background=color,borderwidth = 2, padx=1,pady=1,relief = FLAT)
    def bind(self,*args):
        self.entry.bind(*args)
    def insert(self,*args):
        self.entry.insert(*args)
    def delete(self,*args):
        self.entry.delete(*args)
    def validate_on(self,*args):
        self.entry.config(validate="key")
        self.entry['validatecommand'] = (self.entry.register(testVal), '%P', '%d')
    def destroy(self):
        Frame.destroy(self)
    def create_tooltip(self,font,tooltip_text):
        self.toolip = CreateToolTip(self.entry,font,tooltip_text)
    def get(self):
        return self.entry.get()

class FindClientMultiWidget(CustomFrame):
    def __init__(self, parent, font, current_dir, button_command, main_color, combo_values, default_state="entry"):
        Frame.__init__(self, parent)
        self.parent_frame = parent

        self.configure(bg="green")
        self.state=default_state
        self.button_command = button_command
        self.current_dir = current_dir
        self.main_color = main_color
        self.font = font
        self.combo_values=combo_values
        self.create_widgets()

    def create_widgets(self):
        self.label_frame = CustomFrame(self)
        self.label_frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.find_frame = CustomFrame(self)
        self.find_frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.label = Label(self.label_frame, text="Поиск работников по ",
                                              background=self.main_color,
                                              font=self.font, )
        self.label.pack(side=LEFT, fill=BOTH, expand=YES)

        self.combo = CustomCombobox(self.label_frame,
                                                             values=self.combo_values, height=len(self.combo_values),
                                                             foreground='black',
                                                             state='readonly',
                                                             font=self.font)
        self.combo.pack(side=LEFT, fill=BOTH, expand=NO)
        self.combo.bind("<<ComboboxSelected>>", self.change_state)



    def change_state(self, event):
        self.state=self.combo.get()
        print(self.state)
        self.clear_widgets()
        if self.state=="ФИО":

            self.find_widget = CustomEntry(self.find_frame,
                                                         font=self.font,
                                                         justify=LEFT)
            self.find_widget.pack(side=LEFT, fill=BOTH, expand=YES)

            image3 = Image.open('%s\\images\\lupa.png' % (self.current_dir))
            render3 = ImageTk.PhotoImage(image3.resize((22, 22), Image.ANTIALIAS))

            self.find_button = CustomButton(self.find_frame,
                                           font=self.font,
                                           image = render3,
                                           relief=FLAT,
                                           overrelief=SOLID,
                                           command=self.button_command,
                                           justify=LEFT)
            self.find_button.pack(side=LEFT, fill=BOTH, expand=NO)
            self.find_button.image = render3

            self.parent_frame.update()


        if self.state=="Вакансия":

            self.find_widget = CustomCombobox(self.find_frame,
                                              values=self.get_all_vacancies(), height=7,
                                              width=20,
                                              foreground='black',
                                              state='readonly',
                                              font=self.font,
                                              justify=LEFT)


            self.find_widget.pack(side=LEFT, fill=BOTH, expand=YES)


            image3 = Image.open('%s\\images\\lupa.png' % (self.current_dir))
            render3 = ImageTk.PhotoImage(image3.resize((22, 22), Image.ANTIALIAS))

            self.find_button = CustomButton(self.find_frame,
                                           font=self.font,
                                           image = render3,
                                           relief=FLAT,
                                           overrelief=SOLID,
                                           command=self.button_command,
                                           justify=LEFT)
            self.find_button.pack(side=LEFT, fill=BOTH, expand=NO)
            self.find_button.image = render3

            self.parent_frame.update()

        if self.state=="Объект":

            print("TODO TODO TODO TODO TODO TODO TODO")

    def clear_widgets(self):
        try:
            self.find_widget.destroy()
            self.find_button.destroy()
        except:
            pass

    def get_all_vacancies(self):
        self.dbq = pyodbc.connect('DSN=KADRY')
        self.cursor = self.dbq.cursor()
        table = []
        sql = "SELECT [Код],[Название должности] FROM [Вакансии] ORDER BY [Код]"
        result = self.cursor.execute(sql)
        for row in result:
            table.append(list(row))
        return table





class PerDayAccountingWidgetsBox(Frame):
    def __init__(self, parent, input_client_vacancy_list = None, input_clients_info_list = None):
        Frame.__init__(self, parent)
        self.config(bg="light green")
        self.input_client_vacancy_list = copy.deepcopy(input_client_vacancy_list)
        self.input_clients_info_list = copy.deepcopy(input_clients_info_list)


        self.border_color = "#dbdbdb"
        self.bg_color_light = "light gray"

        self.another_frame_color = "#bfffa3"
        self.fg_color = "black"

        self.create_widgets()
    def create_widgets(self):
        self.current_dir=os.getcwd()

        self.top_frame = Frame(self, bg="blue")
        self.top_frame.pack(side = TOP, fill=BOTH, expand = NO)

        self.top_frame_top_half_frame = CustomFrame(self.top_frame)
        self.top_frame_top_half_frame.set_bg("light blue")
        self.top_frame_top_half_frame.pack(side = TOP, fill=BOTH, expand = YES)



        self.date_lbl = CustomLabel(self.top_frame_top_half_frame, fill= BOTH)
        self.date_lbl.set_bg_color(self.border_color)
        self.date_lbl.set_fg_color("black")
        self.date_lbl.set_text(text="Дата", font=("Ubuntu", 14))
        self.date_lbl.pack(side=LEFT, fill = BOTH, expand = YES)

        self.calendar_widget = DateEntry(self.top_frame_top_half_frame, width=12, font=("Ubuntu", 12), background='blue', foreground='white', borderwidth=2)
        self.calendar_widget.pack(side=LEFT, fill = BOTH, expand = YES)

        self.save_button = CustomButton(self.top_frame_top_half_frame,
                                                                 background=self.border_color, foreground="green",
                                                                 activebackground=self.another_frame_color, height=1,
                                                                 relief=FLAT, overrelief=SOLID,
                                                                 font=("Ubuntu", 12, "bold"), justify=CENTER,
                                                                 text="Сохранить", command=self.save_data,
                                                                 )
        self.save_button.pack(side=LEFT, fill = BOTH, expand = YES)




        self.top_frame_bottom_half_frame = Frame(self.top_frame, bg="light gray")
        self.top_frame_bottom_half_frame.pack(side=TOP, fill=X, expand=NO)


        self.create_label_frames(self.top_frame_bottom_half_frame, self.fg_color)

        self.middle_frame = VerticalScrollFrame(self)
        self.middle_frame.pack(side = TOP, fill=BOTH, expand=YES)



        self.clients_box = WidgetsBox(self.middle_frame.interior)
        self.clients_box.pack(side=TOP, fill = BOTH, expand = YES)
        self.clients_box.set_bg_color("RED")



        self.bottom_frame = Frame(self, bg="yellow")
        self.bottom_frame.pack(side = TOP, fill=BOTH, expand=NO)

        self.fill_widgets()


    def fill_widgets(self):
        self.in_box_widgets = []
        self.in_widget_clients = self.input_clients_info_list

        for gg in range(len(self.in_widget_clients)):

            client_shift_widget = self.clients_box.create_widget_inside("Shift")
            client_shift_widget.name_frame.create_label(self.in_widget_clients[gg], self.bg_color_light, 13, self.fg_color)
            self.label_1.assign_another_widget(client_shift_widget.name_frame)
            self.label_2.assign_another_widget(client_shift_widget.shift_type_frame)
            self.label_3.assign_another_widget(client_shift_widget.shift_duration_frame)
            self.label_4.assign_another_widget(client_shift_widget.food_cost_frame)
            self.label_5.assign_another_widget(client_shift_widget.residence_frame)
            self.label_6.assign_another_widget(client_shift_widget.penalty_frame)
            self.label_7.assign_another_widget(client_shift_widget.prepayment_frame)

            client_shift_widget.pack(side=TOP, fill=BOTH, expand=YES)
            self.in_box_widgets.append([client_shift_widget, self.in_widget_clients[gg][0],self.input_client_vacancy_list[gg]])

        self.client_shift_widget_additional = ShiftWidget(self.bottom_frame, font=("Ubuntu", 13), state="additional")
        self.client_shift_widget_additional.name_frame.create_button("Добавить", self.bg_color_light, 13,
                                                    self.fg_color, self.add_another_client)
        self.client_shift_widget_additional.pack(side=TOP, fill=BOTH, expand=YES)

    def add_another_client(self):
        self.find_client_window()
        print("waiting for func return ...")
    def create_widget_on_adding(self):

        adding_client_info_list = self.find_client_dialog_returned_value['values']
        print(adding_client_info_list)
        print(adding_client_info_list[1])

        client_shift_widget = self.clients_box.create_widget_inside("Shift")
        client_shift_widget.name_frame.create_label(adding_client_info_list, self.bg_color_light, 13, self.fg_color)
        self.label_1.assign_another_widget(client_shift_widget.name_frame)
        self.label_2.assign_another_widget(client_shift_widget.shift_type_frame)
        self.label_3.assign_another_widget(client_shift_widget.shift_duration_frame)
        self.label_4.assign_another_widget(client_shift_widget.food_cost_frame)
        self.label_5.assign_another_widget(client_shift_widget.residence_frame)
        self.label_6.assign_another_widget(client_shift_widget.penalty_frame)
        self.label_7.assign_another_widget(client_shift_widget.prepayment_frame)

        self.client_shift_widget_additional.pack_forget()
        client_shift_widget.pack(side=TOP, fill=BOTH, expand=YES)
        self.client_shift_widget_additional.pack(side=TOP, fill=BOTH, expand=YES)
        self.middle_frame.force_update()

        self.in_box_widgets.append([client_shift_widget, self.in_widget_clients[0]])


    def find_client_window(self):
        self.finded_client_info = ''
        find_client_window = FindClientScript.FindWindowUI(self.bg_color_light,
                                                                      self.border_color,
                                                                      self.border_color,
                                                                      self.border_color,
                                                                      14,
                                                                      self.current_dir,
                                                                      5,
                                                                      self.finded_client_info,
                                                                      self.return_value_from_find_client_dialog,
                                                                      self)

    def return_value_from_find_client_dialog(self, client_info_list):
        self.find_client_dialog_returned_value = copy.deepcopy(client_info_list)
        self.create_widget_on_adding()


    def save_data(self):
        info_list = []
        for gg in range(len(self.in_box_widgets)):
            info_list.append(self.in_box_widgets[gg][0].give_away_shift_info())
        date = self.calendar_widget.get()
        path = self.current_dir + "\\clients_reports"
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        all_client_dicts=[]

        for wp in range(len(info_list)):
            client_dict = {
                            "client_id":                self.in_box_widgets[wp][1],
                            "client_vacancy_id":        self.in_box_widgets[wp][2],
                            "client_name":              info_list[wp][0],
                            "shift_type":               info_list[wp][1],
                            "shift_hours":              info_list[wp][2],
                            "shift_food_cost":          info_list[wp][3],
                            "shift_residence_cost":     info_list[wp][4],
                            "shift_penalty_cost":       info_list[wp][5],
                            "shift_prepayments_cost":   info_list[wp][6],
                            "shift_paid_state":         [False, [0,0]],
                          }
            all_client_dicts.append(client_dict)

        data = {
                "clients_shifts_reports":
                    all_client_dicts
                    }
        with open(path + '\\date_' + str(date) + '.json', "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, ensure_ascii=False)




    def create_label_frames(self, parent, fg_color):
        self.label_1 = CustomLabelWithBorder(parent, height = 2)
        self.label_1.set_bg_color(self.bg_color_light)
        self.label_1.set_fg_color(fg_color)
        self.label_1.set_text("Имя сотрудника", ("Ubuntu", 14))
        self.label_1.pack(side=LEFT, expand = YES, fill=X)

        self.label_2 = CustomLabelWithBorder(parent,height = 2)
        self.label_2.set_bg_color(self.bg_color_light)
        self.label_2.set_fg_color(fg_color)
        self.label_2.set_text("Тип смены", ("Ubuntu", 14))
        self.label_2.pack(side=LEFT, expand=YES, fill=X)

        self.label_3 = CustomLabelWithBorder(parent, height = 2)
        self.label_3.set_bg_color(self.bg_color_light)
        self.label_3.set_fg_color(fg_color)
        self.label_3.set_text("Часов", ("Ubuntu", 14))
        self.label_3.pack(side=LEFT, expand=YES, fill=X)

        self.label_4 = CustomLabelWithBorder(parent, height = 2)
        self.label_4.set_bg_color(self.bg_color_light)
        self.label_4.set_fg_color(fg_color)
        self.label_4.set_text("Питание", ("Ubuntu", 14))
        self.label_4.pack(side=LEFT, expand=YES, fill=X)

        self.label_5 = CustomLabelWithBorder(parent, height = 2)
        self.label_5.set_bg_color(self.bg_color_light)
        self.label_5.set_fg_color(fg_color)
        self.label_5.set_text("Проживание", ("Ubuntu", 14))
        self.label_5.pack(side=LEFT, expand=YES, fill=X)

        self.label_6 = CustomLabelWithBorder(parent, height = 2)
        self.label_6.set_bg_color(self.bg_color_light)
        self.label_6.set_fg_color(fg_color)
        self.label_6.set_text("Штрафы", ("Ubuntu", 14))
        self.label_6.pack(side=LEFT, expand=YES, fill=X)

        self.label_7 = CustomLabelWithBorder(parent, height = 2)
        self.label_7.set_bg_color(self.bg_color_light)
        self.label_7.set_fg_color(fg_color)
        self.label_7.set_text("Авансы", ("Ubuntu", 14))
        self.label_7.pack(side=LEFT, expand=YES, fill=X)

        self.label_empty = CustomLabelWithBorder(parent, height = 2, font = ("Ubuntu", 14), width=1)
        self.label_empty.set_bg_color(self.bg_color_light)
        self.label_empty.disable_border()
        self.label_empty.pack(side=LEFT, expand=NO, fill=X)




class ShiftWidget(CustomFrame):
    def __init__(self, parent, font, state="common"):
        Frame.__init__(self, parent)
        self.configure(bg="#70878f")
        self.state=state
        self.create_widgets(font)

    def create_widgets(self, font):

        self.name_frame = CustomFrame(self, height=2)
        self.name_frame.set_font(font)
        self.name_frame.enable_border()
        self.name_frame.pack(side=LEFT, expand=YES, fill=BOTH)
        if self.state=="additional":
            return
        else:

            self.shift_type_frame = CustomCombobox(self,side=TOP, width=17)
            self.shift_type_frame.enable_border()
            self.shift_type_frame.pack(side=LEFT, expand=YES, fill=BOTH)

            self.shift_duration_frame = CustomCombobox(self, side=TOP, width=17)
            self.shift_duration_frame.enable_border()
            self.shift_duration_frame.pack(side=LEFT, expand=YES, fill=BOTH)

            self.food_cost_frame = CustomEntry(self, side=TOP)
            self.food_cost_frame.enable_border()
            self.food_cost_frame.pack(side=LEFT, expand=YES, fill=BOTH, padx=1)

            self.residence_frame = CustomEntry(self, side=TOP)
            self.residence_frame.enable_border()
            self.residence_frame.pack(side=LEFT, expand=YES, fill=BOTH)

            self.penalty_frame = CustomEntry(self, side=TOP)
            self.penalty_frame.enable_border()
            self.penalty_frame.pack(side=LEFT, expand=YES, fill=BOTH, padx=1)

            self.prepayment_frame = CustomEntry(self, side=TOP)
            self.prepayment_frame.enable_border()
            self.prepayment_frame.pack(side=LEFT, expand=YES, fill=BOTH)

            self.set_defaults()


    def set_defaults(self):
        self.shift_type_frame.values(["Дневная","Ночная","Обе"])
        self.shift_duration_frame.values(["6", "8", "10", "12"])


    def give_away_shift_info(self):
        returned_info_list = []
        returned_info_list.append(self.name_frame.get())
        returned_info_list.append(self.shift_type_frame.get())
        returned_info_list.append(self.shift_duration_frame.get())
        returned_info_list.append(self.food_cost_frame.get())
        returned_info_list.append(self.residence_frame.get())
        returned_info_list.append(self.penalty_frame.get())
        returned_info_list.append(self.prepayment_frame.get())
        return returned_info_list



class VerticalScrollFrame(ttk.Frame):

    def __init__(self, parent, *args, **options):
        style = options.pop('style', ttk.Style())
        pri_background = options.pop('pri_background', 'light grey')
        sec_background = options.pop('sec_background', 'grey70')
        arrowcolor = options.pop('arrowcolor', 'black')
        mainborderwidth = options.pop('mainborderwidth', 0)
        interiorborderwidth = options.pop('interiorborderwidth', 0)
        mainrelief = options.pop('mainrelief', 'flat')
        interiorrelief = options.pop('interiorrelief', 'flat')

        ttk.Frame.__init__(self, parent, style='main.TFrame',
                           borderwidth=mainborderwidth, relief=mainrelief)

        self.__setStyle(style, pri_background, sec_background, arrowcolor)

        self.__createWidgets(mainborderwidth, interiorborderwidth,
                             mainrelief, interiorrelief,
                             pri_background)
        self.__setBindings()

    def __setStyle(self, style, pri_background, sec_background, arrowcolor):
        style.configure('main.TFrame', background=pri_background)
        style.configure('interior.TFrame', background=pri_background)
        style.configure('canvas.Vertical.TScrollbar', background=pri_background,
                        troughcolor=sec_background, arrowcolor=arrowcolor)

        style.map('canvas.Vertical.TScrollbar',
                  background=[('active', pri_background), ('!active', pri_background)],
                  arrowcolor=[('active', arrowcolor), ('!active', arrowcolor)])

    def __createWidgets(self, mainborderwidth, interiorborderwidth,
                        mainrelief, interiorrelief, pri_background):

        self.vscrollbar = ttk.Scrollbar(self, orient='vertical',
                                        style='canvas.Vertical.TScrollbar')
        self.vscrollbar.pack(side='right', fill='y', expand='false')
        self.canvas = Canvas(self,
                                bd=0,
                                highlightthickness=0,
                                yscrollcommand=self.vscrollbar.set,
                                background=pri_background
                                )
        self.canvas.pack(side='left', fill='both', expand='true')
        self.vscrollbar.config(command=self.canvas.yview)


        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)


        self.interior = ttk.Frame(self.canvas,
                                  style='interior.TFrame',
                                  borderwidth=interiorborderwidth,
                                  relief=interiorrelief)
        self.interior_id = self.canvas.create_window(0, 0,
                                                     window=self.interior,
                                                     anchor='nw')

    def __setBindings(self):

        self.canvas.bind('<Configure>', self.__configure_canvas_interiorframe)

    def __configure_canvas_interiorframe(self, event):

        self.canvas.update_idletasks()


        interiorReqHeight = self.interior.winfo_reqheight()
        canvasWidth = self.canvas.winfo_width()
        canvasHeight = self.canvas.winfo_height()


        self.canvas.itemconfigure(self.interior_id, width=canvasWidth)


        if canvasHeight > interiorReqHeight:

            self.canvas.itemconfigure(self.interior_id, height=canvasHeight)
            self.canvas.config(scrollregion="0 0 {0} {1}".
                               format(canvasWidth, canvasHeight))
        else:

            self.canvas.itemconfigure(self.interior_id, height=interiorReqHeight)
            self.canvas.config(scrollregion="0 0 {0} {1}".
                               format(canvasWidth, interiorReqHeight))
    def force_update(self):
        #override?
        self.canvas.update_idletasks()


        interiorReqHeight = self.interior.winfo_reqheight()
        canvasWidth = self.canvas.winfo_width()
        canvasHeight = self.canvas.winfo_height()


        self.canvas.itemconfigure(self.interior_id, width=canvasWidth)


        if canvasHeight > interiorReqHeight:

            self.canvas.itemconfigure(self.interior_id, height=canvasHeight)
            self.canvas.config(scrollregion="0 0 {0} {1}".
                               format(canvasWidth, canvasHeight))
        else:

            self.canvas.itemconfigure(self.interior_id, height=interiorReqHeight)
            self.canvas.config(scrollregion="0 0 {0} {1}".
                               format(canvasWidth, interiorReqHeight))