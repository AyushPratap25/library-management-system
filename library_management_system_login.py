# NOTE: Default Login ID: Admin (UI)
#       Default Password: 123   (UI)

import mysql.connector as mc
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.widgets import DateEntry
import customtkinter as ctk
from random import choice 
import random
from datetime import datetime


# App login credentials — change these if needed
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '123'


# DB config — change these if your setup is different
HOST = 'localhost' # change to your host name 
USER = 'root' # change to your user name
PASSWORD = 'mysql' # change to your own password
DATABASE = 'library_management_system'


# DATABASE CONNECTION

# Create DB if it doesn't exist
mycon_temp = mc.connect(
    host=HOST, 
    user=USER, 
    password=PASSWORD)
cursor_temp = mycon_temp.cursor()
cursor_temp.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
mycon_temp.close()

# Establish a connection to the MySQL database
mycon = mc.connect(
    host=HOST, 
    user=USER, 
    password=PASSWORD,
    database=DATABASE)
cursor = mycon.cursor()

# Check if the database connection is successful
if mycon.is_connected:
    print('Connection Successfull')


# TABLE CREATION
# Mysql table creation 
# Creates the main book inventory table (if it doesn't already exist)
def create_books_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_list (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_name VARCHAR(255),
            author VARCHAR(255),
            date DATE            
        )
    """)

# Creates the rented books table to track which books are currently rented
def create_rented_books_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rented_books_1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_name VARCHAR(255),
            author VARCHAR(255),
            date DATE,
            No_of_days INT
        )
    """)


# LOGIN
def sign_in():
    username = user.get()
    password = code.get()
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        window_login.destroy() # close login window, open main app
        
        def add_book():
            global window_add
            window_add = tk.Toplevel()
            window_add.title('extra window')
            window_add.geometry('450x450')
        
            def add_get_book():
                global Calender
                Book = user.get()
                Author = author.get()
                Calender = calender.entry.get()
                try:
                    date = datetime.strptime(Calender, "%m/%d/%y")
                except ValueError:
                    date = datetime.strptime(Calender, "%d-%m-%Y")
                mysql_date_format = date.strftime("%Y-%m-%d")

                data = (Book, Author, mysql_date_format)
                table.insert(parent = '',index = 0, values = data)
       
                # inserting entry data to database
                insert_query = "INSERT INTO book_list (book_name, author, date) VALUES (%s, %s, %s)"
                values = (Book, Author, mysql_date_format)    
                cursor.execute(insert_query, values)
                mycon.commit()
                messagebox.showinfo("Success", "Book Added Successfully!")
                  

            def on_enter(_):
                user.delete(0,'end')

            def on_leave(_):
                name = user.get()
                if name=='':
                    user.insert(0,'Book Name')

            def on_enter_1(_):
                author.delete(0,'end')

            def on_leave_1(_):
                name = author.get()
                if name=='':
                    author.insert(0,'Author')

            # frame
            frame_add = tk.Frame(window_add)
            frame_add.place(x=0,y=0,relwidth=1,relheight=1)

            # label
            heading = ttk.Label(frame_add,text='Add Book',font = ('Microsoft YaHei UI Light',23,'bold'),anchor='center')
            heading.pack(pady=30)

            # Entry
            user = ttk.Entry(frame_add,width=25,font = ('Microsoft YaHei UI Light',11),justify='center', style='info.TEntry')
            user.pack(pady=20)
            author = ttk.Entry(frame_add,width=25,font = ('Microsoft YaHei UI Light',11),justify='center', style='info.TEntry')
            author.pack()

            # key binding
            user.bind('<FocusIn>',on_enter)
            user.bind('<FocusOut>',on_leave)
            author.bind('<FocusIn>',on_enter_1)
            author.bind('<FocusOut>',on_leave_1)

            # box highlight name
            user.insert(index=0,string='Book Name')
            author.insert(index=0,string='Author')

            # calender
            calender = DateEntry(frame_add,style='success.TCalendar')
            calender.pack(pady=30)

            # add button
            tk.Button(
                frame_add,
                width=39,
                text='Add',
                anchor='center',
                command=lambda:[add_get_book(),Calender]).pack(pady=30)
            
            window_add.mainloop()

        # rent_layout
        def on_enter(_):
            user.delete(0, 'end')

        def on_leave(_):
            name = user.get()
            if name == '':
                user.insert(0, 'Book Name')

        def on_enter_1(_):
            author.delete(0, 'end')

        def on_leave_1(_):
            name = author.get()
            if name == '':
                author.insert(0, 'Author')

        def on_menu_item_select(value):
            menu_button.config(text=str(value))
            print("Selected:", value)

        def rent_book_get():
            global Calender
            Book = user.get()
            Author = author.get()
            Calender = calender.entry.get()

            try:
                date = datetime.strptime(Calender, "%m/%d/%y")
            except ValueError:
                date = datetime.strptime(Calender, "%d-%m-%Y")
            mysql_date_format = date.strftime("%Y-%m-%d")


            # Check if a book with the given title and author exists in the database
            def book_exists(book_title, book_author):
                cursor.execute("SELECT COUNT(*) FROM book_list WHERE book_name = %s AND author = %s", (book_title, book_author))
                count = cursor.fetchone()[0]

                return count > 0

            # Usage
            if book_exists(Book, Author):
                # The book exists in the database
                # inserting entry data to database
                insert_query = "INSERT INTO rented_books_1 (book_name, author, date, No_of_days) VALUES (%s, %s, %s, %s)"
                values = (Book, Author, mysql_date_format, selected_value)    
                cursor.execute(insert_query, values)
                mycon.commit()
                
                # message box
                messagebox.showinfo("Success", "Book Rented Successfully!")
                
                # delete the rented item 
                def delete_rented_book_from_table(book_name, author):
                    # delete from book_list
                    delete_query = "DELETE FROM Book_list WHERE book_name = %s AND author = %s"
                    values = (book_name, author)     
                    cursor.execute(delete_query, values)
                    mycon.commit()
                   
                    # delete from book_list treeview
                    for item in table.get_children():
                        book_name = table.item(item, 'values')[0]  # Assuming the book name is in the first column
                        if book_name == Book:
                            table.delete(item)
                            return # Exit the function and loop
   
                delete_rented_book_from_table(Book,Author)
                         
            else:
                # message box
                messagebox.showerror('Book Not Found', 'Book not found in the database')

        def rent_book_list():
            global window_rent_list, table1
            # window
            window_rent_list = tk.Toplevel()
            window_rent_list.title('Rent Book')
            window_rent_list.geometry('800x450')
            
            # frame
            frame_rent_list = tk.Frame(window_rent_list)
            frame_rent_list.place(x=0, y=0, relwidth=1, relheight=1)

            # title
            heading = ttk.Label(frame_rent_list, text='Rented Book List', font=('Microsoft YaHei UI Light', 23, 'bold'), anchor='center')
            heading.pack(pady=30)

            # treeview_rent_book
            table1 = ttk.Treeview(frame_rent_list, columns=('first', 'last', 'date', 'days'), show='headings', style='info.Treeview')
            table1.heading('first', text='Book Name')
            table1.heading('last', text='Author')
            table1.heading('date', text='Rent Date')
            table1.heading('days', text='No. OF Days')
            table1.pack(fill='both', expand=True)

            # extracting data from rent_book_1 to table1
            def populate_treeview_rent_book():
                cursor.execute("SELECT book_name, author, date, No_of_days FROM rented_books_1")
                records = cursor.fetchall()
                    
                for record in records:
                    table1.insert(parent = '',index = 0, values = record)            
            print('Successfully extracted from rented_book_1')
            populate_treeview_rent_book()  

            # delete the rented item 
            
            def book_return():    
                   
                # delete from book_list treeview
                for i in table1.selection():
                    print(table1.item(i)['values'])
                    data = table1.item(i)['values']

                    # delete from treeview
                    table1.delete(i)


                    # delete from rented_books_1
                    delete_query = "DELETE FROM rented_books_1 WHERE book_name = %s AND author = %s"
                    values = (data[0],data[1])
                    cursor.execute(delete_query,values)
                    mycon.commit()

                    insert_query = "INSERT INTO book_list (book_name, author, date) VALUES (%s, %s, %s)"
                    values = (data[0],data[1],data[2])    
                    cursor.execute(insert_query, values)
                    mycon.commit()

            # return button
            button_return = ctk.CTkButton(
                frame_rent_list,text='return book',
                fg_color='#718BF1',
                text_color='#000',
                hover_color='#0c5eb1',
                command=book_return,
                corner_radius=5,
                )
            button_return.pack(pady=10,padx=10,side='right')

            window_rent_list.mainloop()

        def rent_book():
            global window_rent,user,author,calender,menu_button
            window_rent = tk.Toplevel()
            window_rent.title('Rent Book')
            window_rent.geometry('450x500')

            # layout
            # frame_rent
            frame_rent = tk.Frame(window_rent)
            frame_rent.place(x=0,y=0,relwidth=1,relheight=1)

            # label
            heading = ttk.Label(frame_rent,text='Rent Book',font = ('Microsoft YaHei UI Light',23,'bold'),anchor='center')
            heading.pack(pady=30)

            # Entry
            user = ttk.Entry(frame_rent,width=25,font = ('Microsoft YaHei UI Light',11),justify='center', style='success.TEntry')
            user.pack(pady=20)
            author = ttk.Entry(frame_rent,width=25,font = ('Microsoft YaHei UI Light',11),justify='center', style='success.TEntry')
            author.pack()

            # key binding
            user.bind('<FocusIn>',on_enter)
            user.bind('<FocusOut>',on_leave)
            author.bind('<FocusIn>',on_enter_1)
            author.bind('<FocusOut>',on_leave_1)

            # box highlight name
            user.insert(index=0,string='Book Name')
            author.insert(index=0,string='Author')
            
            # menu
            def on_menu_item_select(value):
                global selected_value
                selected_value = value
                menu_button.config(text=str(value))  # Update the text of the menu_button
                print("Selected:", value)
                
            # menu button
            menu_button = ttk.Menubutton(frame_rent,text ='No. Of Days')
            menu_button.pack(pady=20)

            button_sub_menu = tk.Menu(menu_button,tearoff=False)
            for i in range(1, 31):
                button_sub_menu.add_command(label=str(i), command=lambda i=i: on_menu_item_select(i))

            menu_button['menu'] = button_sub_menu

            # calender
            calender = DateEntry(frame_rent)
            calender.pack(pady=20)

            # add button
            tk.Button(
                frame_rent,
                width=39,
                text='Add',
                anchor='center',
                command=lambda:[rent_book_get(),print(calender.entry.get())]).pack(pady=30)

            # run
            window_rent.mainloop()


        # function to change the theme
        def theme():
            global window_theme
            window_theme = tk.Toplevel()
            window_theme.title('Rent Book')
            window_theme.geometry('400x500')

            # frame
            frame_theme = tk.Frame(window_theme)
            frame_theme.place(x=0,y=0,relwidth=1,relheight=1)

            # label
            heading = ttk.Label(frame_theme,text='Theme',font = ('Microsoft YaHei UI Light',23,'bold'),anchor='center')
            heading.pack(pady=30)
            
            # radio buttons
            def change_theme():
                selected_theme = theme_var.get()
                window.style.theme_use(selected_theme)

            # Create a theme variable to store the selected theme
            theme_var = tk.StringVar()
            themes = ['vapor','cosmo','morph','solar','darkly','cyborg','']
            for theme in themes:
                ttk.Radiobutton(
                    frame_theme,
                    text=theme.title(),
                    value=theme,
                    variable=theme_var,
                    command=change_theme).pack(expand=True)


        # main library management system window
        #window
        window =  ttk.Window(themename='darkly')
        window.title("App")
        window.geometry('1000x550+200+150')
        window.resizable(False,False)

        # title
        title_label = ttk.Label(
            master = window, 
            text = "Library Management System",
            font = 'Calibri 24 bold',)
        title_label.pack()

        # frame
        menu_frame = ttk.Frame(window)
        main_frame = ttk.Frame(window)

        # placing frame
        menu_frame.place(x=0,y=80,relwidth=0.3,relheight=0.9)
        main_frame.place(relx=0.3,y=84,relwidth=0.65,relheight=0.7)

        # menu widget buttons
        menu_button1 = ctk.CTkButton(
            menu_frame,text='Add Book',
            fg_color='#718BF1',
            text_color='#000',
            hover_color='#0c5eb1',
            corner_radius=10,
            command=add_book)
        menu_button2 = ctk.CTkButton(
            menu_frame,text='Rent Book',
            fg_color='#718BF1',
            text_color='#000',
            hover_color='#71F1BB',
            corner_radius=10,
            command=rent_book)
        menu_button3 = ctk.CTkButton(
            menu_frame,text='Rented Book List',
            fg_color='#718BF1',
            text_color='#000',
            hover_color='#F171F1',
            corner_radius=10,
            command=rent_book_list)
        menu_button4 = ctk.CTkButton(
            menu_frame,text='Theme',
            fg_color='#718BF1',
            text_color='#000',
            hover_color='#F19B71',
            corner_radius=10,
            command=theme)
        

        # menu layout
        menu_frame.columnconfigure((0,1,2,4),weight=1,uniform='a')
        menu_frame.rowconfigure((0,1,2,3,4),weight=1,uniform='a')

        menu_button1.grid(row=0,column=0,sticky='nsew',columnspan=2,padx=10,pady=2)
        menu_button2.grid(row=1,column=0,sticky='nsew',columnspan=2,padx=10,pady=2)
        menu_button3.grid(row=2,column=0,sticky='nsew',columnspan=2,padx=10,pady=2)
        menu_button4.grid(row=3,column=0,sticky='nsew',columnspan=2,padx=10,pady=2)
        
       
        # treeview_widget_book_information
        table = ttk.Treeview(main_frame,columns=('first','last','date'),show = 'headings',style='info.Treeview')
        table.heading('first',text='Book Name')
        table.heading('last',text='Author')
        table.heading('date',text='Date')
        table.pack(fill = 'both',expand = True)
       
        # extracting data from book_list to treeview main
        def populate_treeview_main():
            cursor.execute("SELECT book_name, author, date FROM book_list")
            records = cursor.fetchall()
                
            for record in records:
                table.insert(parent = '',index = 0, values = record)            
        print('Successfully extracted from book_list')

        # Function to refresh the Treeview 
        def refresh_treeview():
            # Delete all existing items in the Treeview
            for item in table.get_children():
                table.delete(item)
            
            # data 
            initial_data = populate_treeview_main()

            # Insert the data into the Treeview
            if initial_data is not None:
                for item in initial_data:
                    table.insert('', 'end', values=item)
            else:
                # Handle the case where initial_data is None
                print("Error: populate_treeview_main returned None")

        # refresh button
        refresh_button = ctk.CTkButton(
            window,
            text='Refresh',
            fg_color='#718BF1',
            text_color='#000',
            hover_color='#0c5eb1',
            corner_radius=6, 
            width=90,
            height=5,
            command=refresh_treeview)
        
         # refresh button pack
        refresh_button.pack(padx=38,pady=5,side='bottom',anchor='se')


        # events
        def item_select(_):
            print(table.selection())
            for i in table.selection():
                print(table.item(i)['values'])

        def delete_item(_):
            print('del')
            for i in table.selection():
                table.delete(i)
                

        # Bind events to the Treeview
        table.bind('<<TreeviewSelect>>', item_select)
        table.bind('<Delete>', delete_item)

        # add a scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=table.xview)
        table.configure(xscroll=scrollbar.set)
        scrollbar.pack(after=table,fill='x')

        # mysql table creation
        create_books_table()
        create_rented_books_table()

        #Populate main Treeview with book data
        populate_treeview_main()          

        #run main library management system window
        window.mainloop()

    # password validation
    elif username!=ADMIN_USERNAME or ADMIN_PASSWORD:
        messagebox.showerror('Invalid','Invalid username or password')


# login window
def on_enter(_):
    user.delete(0,'end')

def on_leave(_):
    name = user.get()
    if name=='':
        user.insert(0,'Username')

def on_enter_1(_):
    code.delete(0,'end')

def on_leave_1(_):
    name = code.get()
    if name=='':
        code.insert(0,'Password')

# window
window_login = tk.Tk()
window_login.title('login')
window_login.geometry('925x500+300+200')
window_login.configure(background='#fff')
window_login.resizable(False,False)

# image
img= tk.PhotoImage(file=r"login.png") 
Label = tk.Label(window_login,image=img,background='white').place(x=50,y=50)

# frame
frame = tk.Frame(window_login,width=350,height=350,bg='white')
frame.place(x=480,y=70)

# title
heading = tk.Label(frame,text='Sign in',fg='#57a1f8',background='white',font = ('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

# Entry
user = tk.Entry(frame,width=25,border=0,fg='black',bg='white',font = ('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(index=0,string='Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)
tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

code = tk.Entry(frame,width=25,border=0,fg='black',bg='white',font = ('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(index=0,string='Password')
code.bind('<FocusIn>',on_enter_1)
code.bind('<FocusOut>',on_leave_1)
tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

# button
tk.Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=False,command=sign_in).place(x=35,y=204)

label = tk.Label(frame,text="Don't have an account?",fg='black',background='white',font = ('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

# signup button
sign_up = tk.Button(frame,text='Sign up',width=6,border=0,cursor='hand2',bg='white',fg='#57a1f8')
sign_up.place(x=215,y=270)

# run login window
window_login.mainloop()



