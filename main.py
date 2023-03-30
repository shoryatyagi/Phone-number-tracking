from tkinter import *
import mysql.connector
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from tkintermapview import TkinterMapView


class Phone:
    timeZone = str('')
    Carrier = str('')
    Region = str('')

    def __init__(self):
        self.home_screen()

    def check_no(self) -> 'True or False':

        entry_widget['highlightcolor'] = "blue"
        entry_widget['highlightthickness'] = 0

        try:
            phone_number = phonenumbers.parse(number.get())
            a = type(phone_number.national_number)
            valid = phonenumbers.is_valid_number(phone_number)
            possible = phonenumbers.is_possible_number(phone_number)
        except:
            valid_label.config(text='The number you have entered is not valid !!', fg='red')
            print('the number is not vaid')
            return False
        finally:
            if valid == True and a == int:
                valid_label.config(text='The number you have entered is valid', fg='#3d9e1c')
                self.get_details(phone_number)
                return True
            elif a != int:
                valid_label.config(text='The number you have entered is not valid !!', fg='#cf3a3a')
                print('the number is not vaid')
                return False
            else:
                valid_label.config(text='The number you have entered is not valid !!', fg='red')
                print('the number is not vaid')
                return False

    """ def find_location(self):
        place_entity = locationtagger.find_locations(text=Phone.Region)
        get_country = str(place_entity.countries)
        print(get_country)"""

    def update_values(self):
        time_zone_label.config(text=f'Time Zone                 -- -- -- -- --    {Phone.timeZone} ')
        company_label.config(text=f'Comapny                   -- -- -- -- --    {Phone.Carrier}')
        region_label.config(text=f'Region                       -- -- -- -- --     {Phone.Region}')

    def set_address(self, event):
        map_widget.set_address(Phone.Region, marker=True)

    def connection(self):
        a = "127.0.0.1"
        user = "root"
        key = "1234"

        try:
            self.mydatabase = mysql.connector.connect(
                host=a,
                user=user,
                password=key,
                database="history"
            )
            self.cursor = self.mydatabase.cursor()
            print('Connection Established')
        except Exception:
            print("Connection Failed")

    def insertion(self):
        
        self.connection()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_details (Timezone varchar(60), Region varchar(20),Number int(20));")
        sql = "INSERT INTO User_Details (Timezone,Region,Number) VALUES ({},{},{})".format(Phone.timeZone, Phone.Region,
                                                                                           number.get())

        self.cursor.execute(sql)
        self.mydatabase.commit()

    def get_details(self, no):

        Phone.timeZone = str(timezone.time_zones_for_number(no))
        Phone.Carrier = str(carrier.name_for_number(no, 'en'))
        Phone.Region = str(geocoder.description_for_number(no, 'en'))
        Phone.timeZone = Phone.timeZone.replace('(', '').replace(',', '').replace(')', '')

        print(Phone.timeZone)
        print(Phone.Carrier)
        print(Phone.Region)
        self.update_values()

    def reset_values(self, event):
        Phone.timeZone = str()
        Phone.Carrier = str()
        Phone.Region = str()
        valid_label.config(text='', fg='#2B2B2B')
        self.update_values()

    def update_entry(self, event):
        entry_widget['highlightcolor'] = "#960e32"
        entry_widget['highlightthickness'] = 3

    def home_screen(self):
        global window
        window = Tk()
        window.geometry('1190x600')
        window.title('Phone Track')
        window.config(bg='#050e1c')
        icon = PhotoImage(file='tracking.png')
        window.wm_iconphoto(False, icon)

        title = Label(window, text='Phone Tracker', fg='#DDDDDD', bg='#050e1c',
                      font=('Arial Rounded MT Bold', 25)).place(x=729, y=12)

        a = Frame(window, height=521, width=562, bg='#0a1221').place(x=589, y=67)

        Entry_text = Label(a, text='Enter your phone no. with + _ _', fg='#DDDDDD', bg='#0a1221',
                           font=('Roboto Regular', 14))
        Entry_text.place(x=729, y=85)

        global number, entry_widget
        number = StringVar()
        entry_widget = Entry(textvariable=number, bg='#050e1c', width=32, font=('Berlin Sans FB', 18), fg='White',
                             borderwidth=0)
        entry_widget.place(x=666, y=135)
        entry_widget.bind('<Button>', self.update_entry)
        entry_widget.bind('<Button>', self.reset_values, add='+')

        global valid_label
        valid_label = Label(text='', font=('Berlin Sans FB', 13), bg='#0a1221', fg='#2B2B2B')
        valid_label.place(x=730, y=170)
        enter_btn = Button(a, width=6, height=1, bg='#145d82', borderwidth=0, text='Enter', fg='white',
                           font=('Berlin Sans FB', 15), command=self.check_no)
        enter_btn.place(x=828, y=210)

        global time_zone_label, company_label, region_label, map_widget

        time_zone_label = Label(a, text='Time Zone                 -- -- -- -- --   ', fg='#DDDDDD', bg='#0a1221',
                                font=('Bahnschrift SemiBold', 14))
        time_zone_label.place(x=610, y=275)
        company_label = Label(a, text='Comapny                   -- -- -- -- --', fg='#DDDDDD', bg='#0a1221',
                              font=('Bahnschrift SemiBold', 14))
        company_label.place(x=610, y=345)
        region_label = Label(a, text='Region                       -- -- -- -- --', fg='#DDDDDD', bg='#0a1221',
                             font=('Bahnschrift SemiBold', 14))
        region_label.place(x=610, y=415)
        get_location_btn = Button(a, width=11, height=1, bg='#145d82', borderwidth=0, text='Get Location',
                                  fg='white', font=('Berlin Sans FB', 18))
        get_location_btn.place(x=788, y=485)
        get_location_btn.bind('<Button>', self.set_address)

        map_widget = TkinterMapView(window, width=550, height=50, corner_radius=5)
        map_widget.pack(fill=Y, side=LEFT, )
        # google_url
        map_widget.set_tile_server('https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=20')

        window.resizable(False, False)
        window.mainloop()


a = Phone()
