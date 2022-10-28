## phonebook
#
from PyQt5 import QtWidgets, uic, QtGui
import sys
import sqlite3
from winsound import Beep

connection = sqlite3.connect('phonebook.db')
cursor = connection.cursor()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() 
        uic.loadUi('main_window.ui', self) 
        self.show()
        self.loaddata()
        self.search = search_screen()
        self.help = help_screen()
        

        self.add_btn.clicked.connect(self.add_data)
        self.del_btn.clicked.connect(self.delete_data)
        self.edit_btn.clicked.connect(self.edit_data)
        self.ok_btn.clicked.connect(self.edit)
        self.search_btn.clicked.connect(self.search.show)
        self.help_btn.clicked.connect(self.help.show)
        

        # sets the width for the headers
        self.phone_table.setColumnWidth(0, 190)
        self.phone_table.setColumnWidth(1, 190)
        self.phone_table.setColumnWidth(2, 55)
        self.phone_table.setColumnWidth(3, 174)



    def loaddata(self):
        self.phone_table.setRowCount(0)
        sqlquery = 'SELECT * FROM phonebook ORDER BY name' 
        
        # drawes the exact number of rows
        result = cursor.execute('SELECT COUNT(*) FROM phonebook').fetchone()
        for _ in result:
            self.phone_table.setRowCount(_)

        #displays the number of records on database    
        self.records_numbers.setText(str(_))

        # prints database to table widget        
        data = cursor.execute(sqlquery)
        tablerow = 0
        for _ in data:
            self.phone_table.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(_[0]).title()))
            self.phone_table.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(_[1]).title()))
            self.phone_table.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(_[2])))
            self.phone_table.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(_[3])))
            tablerow+=1

        connection.commit()



    def delete_data(self):
        selected_row = -1

        while True:
            selected_row = self.phone_table.currentRow()
            if selected_row == -1:
                self.output.setText('Select a register to delete')
                break
            else:
                phone = self.phone_table.item(selected_row,3).text()
                delete_query = f"DELETE FROM phonebook WHERE phone = '{phone}'"
                cursor.execute(delete_query)
                self.output.setText('Record deleted successfully')
                Beep(200,150)             
                Beep(180,150)
                break
        
        connection.commit()

        self.phone_table.removeRow(selected_row)
        self.loaddata()
        

    def add_data(self):
        name = self.campo_name.text()
        lastname = self.campo_lastname.text()
        ddd = self.campo_ddd.text()
        phone = self.campo_phone.text()        

        try:
            sql_add = "INSERT INTO phonebook (name,lastname, ddd, phone)  VALUES(?,?,?,?)"
            cursor.execute(sql_add, (name, lastname, ddd, phone, ))

            self.output.setText('Phone added succesfully')
            Beep(300,150)             
            Beep(320,150)
            
        except:
            self.output.setText('Phone already in PhoneBook')
            Beep(600,150)             
            Beep(650,150)

        self.campo_name.clear()
        self.campo_lastname.clear()
        self.campo_ddd.clear()
        self.campo_phone.clear()
        
        self.loaddata()
        
        connection.commit()



    # shows data on edit fields
    def edit_data(self):        
        selected_row = self.phone_table.currentRow()

        # prints data on edit fields
        name = self.phone_table.item(selected_row,0).text()
        lastname = self.phone_table.item(selected_row,1).text()
        ddd = self.phone_table.item(selected_row,2).text()
        phone = self.phone_table.item(selected_row,3).text()
        self.campo_name.setText(name)
        self.campo_lastname.setText(lastname)
        self.campo_ddd.setText(ddd)
        self.campo_phone.setText(phone)


        
    def edit(self):
        # new variables
        newname = self.campo_name.text().title()
        newlastname = self.campo_lastname.text().title()
        newddd = self.campo_ddd.text()
        newphone = self.campo_phone.text()

        selected_row = self.phone_table.currentRow()
        xphone = self.phone_table.item(selected_row,3).text()
                    
        sql_edit = f"UPDATE phonebook SET name='{newname}', lastname='{newlastname}', ddd='{newddd}', phone='{newphone}' WHERE phone = '{xphone}'"
        cursor.execute(sql_edit)

        self.output.setText('Phone edited succesfully')

        Beep(290,150)             
        Beep(310,150)

        self.campo_name.clear()
        self.campo_lastname.clear()
        self.campo_ddd.clear()
        self.campo_phone.clear()

        self.loaddata()
        
        connection.commit()



class search_screen(QtWidgets.QMainWindow):
    def __init__(self):
        super(search_screen, self).__init__()        
        uic.loadUi('search_window.ui', self)

        self.search_btn.clicked.connect(self.search_fc)
        
        # sets the width for the headers
        self.search_table.setColumnWidth(0, 190)
        self.search_table.setColumnWidth(1, 190)
        self.search_table.setColumnWidth(2, 55)
        self.search_table.setColumnWidth(3, 174)


    def search_fc(self):
        Beep(400,200)
        Beep(430,200)

        name_search = self.campo_search.text().strip().title()
        sql_search = f"SELECT * FROM  phonebook WHERE name LIKE '{name_search}%' ORDER BY name"
        
        try:    
            # drawes the exact number of rows
            sql_rows = f"SELECT COUNT (*) FROM  phonebook WHERE name LIKE '{name_search}%'"
            result = cursor.execute(sql_rows).fetchone()
            for _ in result:
                self.search_table.setRowCount(_)

            data = cursor.execute(sql_search)
            tablerow = 0
            for _ in data:
                self.search_table.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(_[0])))
                self.search_table.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(_[1])))
                self.search_table.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(_[2])))
                self.search_table.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(_[3])))
                tablerow+=1

        except:
            self.search_output.setText('ERROR')
      
        connection.commit()
        

class help_screen(QtWidgets.QMainWindow):
    def __init__(self):
        super(help_screen, self).__init__()        
        uic.loadUi('help_window.ui', self)

  
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()