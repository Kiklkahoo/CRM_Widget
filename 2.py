from tkinter import *
from CustomTkinterUIObjects.CustomWidgets import *

from PIL import Image, ImageTk
import os
from SimpleDialogs.find_client_dialog import FindClientScript
from tkcalendar import Calendar, DateEntry
import copy




class PerDayAccountingWidgetsBox(Frame):
    def __init__(self, parent, input_client_vacancy_list = None, input_clients_info_list = None):
        Frame.__init__(self, parent)
        self.config(bg="light green")
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
        self.in_widget_clients_example = [
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                          ["client_id", "Имя сотрудника"],
                                         ]
        for gg in range(len(self.in_widget_clients_example)):

            client_shift_widget = self.clients_box.create_widget_inside("Shift")
            client_shift_widget.name_frame.create_label(self.in_widget_clients_example[gg], self.bg_color_light, 13, self.fg_color)
            self.label_1.assign_another_widget(client_shift_widget.name_frame)
            self.label_2.assign_another_widget(client_shift_widget.shift_type_frame)
            self.label_3.assign_another_widget(client_shift_widget.shift_duration_frame)
            self.label_4.assign_another_widget(client_shift_widget.food_cost_frame)
            self.label_5.assign_another_widget(client_shift_widget.residence_frame)
            self.label_6.assign_another_widget(client_shift_widget.penalty_frame)
            self.label_7.assign_another_widget(client_shift_widget.prepayment_frame)

            client_shift_widget.pack(side=TOP, fill=BOTH, expand=YES)
            self.in_box_widgets.append([client_shift_widget, self.in_widget_clients_example[gg][0]])

        self.client_shift_widget_additional = ShiftWidget(self.bottom_frame, font=("Ubuntu", 13), state="additional")
        self.client_shift_widget_additional.name_frame.create_button("Добавить", self.bg_color_light, 13,
                                                    self.fg_color, self.add_another_client)
        self.client_shift_widget_additional.pack(side=TOP, fill=BOTH, expand=YES)

    def add_another_client(self):
        self.find_client_window()

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

        self.in_box_widgets.append([client_shift_widget, self.in_widget_clients_example[0]])


    def find_client_window(self):

        find_client_window = FindClientScript.FindWindowUI(self.bg_color_light,
                                                                      self.border_color,
                                                                      self.border_color,
                                                                      self.border_color,
                                                                      14,
                                                                      self.current_dir,
                                                                      5,
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
                            "client_id":            self.in_box_widgets[wp][1],
                            "name":                 info_list[wp][0],
                            "type":                 info_list[wp][1],
                            "time":                 info_list[wp][2],
                            "food":                 info_list[wp][3],
                            "residence":            info_list[wp][4],
                            "penalty":              info_list[wp][5],
                            "prepayments":          info_list[wp][6],
                          }
            all_client_dicts.append(client_dict)

        data = {
                "client_shifts_report":
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




root = Tk()
app = PerDayAccountingWidgetsBox(root)
app.pack(fill=BOTH, expand = YES)
root.geometry("1000x500")
root.mainloop()