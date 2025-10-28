from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGridLayout,
    QLineEdit, QPushButton, QMainWindow, QTableWidget,QTableWidgetItem,QDialog,QVBoxLayout,
    QComboBox,QToolBar,QStatusBar,QMessageBox
)
from PyQt6.QtGui import QAction,QIcon
import sys
import sqlite3
import mysql.connector

class DatabaseConnection:
    def __init__(self,host="localhost",user='root',password='ahraz@2009@123',database='ahrazdb'):
        self.host=host
        self.user=user
        self.password=password
        self.database=database

    def connect(self):
        connection=mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database) 
        return connection  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)

        # Create Menus
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        Edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add actions
        add_student_action = QAction(QIcon("add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)# here we amade a about method

        #fir serch of student
        Search_student_action = QAction(QIcon("search.png"),"Search Student", self)
        Search_student_action.triggered.connect(self.search)
        Edit_menu_item.addAction(Search_student_action)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #create toolbar
        toolbar=QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # add the add student icon call
        toolbar.addAction(add_student_action)

        toolbar.addAction(Search_student_action)


        #create a status bar

        self.status=QStatusBar()
        self.setStatusBar(self.status)

        #detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)#whenever i cell on the databse table gto clicked  rwo options will apppear edit record and the delete record
    def cell_clicked(self):
        edit_button=QPushButton("Edit Record")#creating a push button for the edit and the delete record
        edit_button.clicked.connect(self.edit)

        delete_button=QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        childeren=self.findChildren(QPushButton)#whenver i click edit and delete were created so in order to avoid this we created this method
        if childeren:
            for child in childeren:
                self.status.removeWidget(child)

        self.status.addWidget(edit_button)# this line adds the lement to status bar
        self.status.addWidget(delete_button)# this line adds the lement to status bar

    def load_data(self):
        connection=DatabaseConnection().connect()# connect to that classs
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM students")
        result=cursor.fetchall()
        self.table.setRowCount(0)
        for rownumber,rowdata in enumerate(result):# adding the e;emts in tha table shown to front end
            self.table.insertRow(rownumber)
            for column_number , data in enumerate(rowdata):#the add the lemts to specific columns with the help of the row number
                self.table.setItem(rownumber,column_number,QTableWidgetItem(str(data)))

        connection.close()
    def insert(self):
        dialog=InsertDialog()
        dialog.exec()    

    def search(self):
        S_dialog=SearchDialog()
        S_dialog.exec()    

    def edit(self):#moves to the edit window from the main window
        dialog=EditDialog()
        dialog.exec()   

    def delete(self):#moves to the delte windwo from the main windoe
        dialog=DeleteDialog()
        dialog.exec()        

    def about(self):
        dialog=AboutDialog()
        dialog.exec()       

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content="The app was created to learn about how student database management system works"
        self.setText(content)

# class EditDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Insert Student Data")
#         self.setFixedHeight(300)
#         self.setFixedWidth(300)

#         layout= QVBoxLayout()
#         index=window.table.currentRow()
#         student_name=window.table.item(index,1).text()
#         self.student_name=QLineEdit(student_name)
#         self.student_name.setPlaceholderText("Name")
#         layout.addWidget(self.student_name)

#         # get id from selected row
#         self.student_id=window.table.item(index,0).text()

#         #add the coursees
#         course_name=window.table.item(index,2).text()
#         self.course_name=QComboBox() # is is selcyt boc
#         courses=["Biology","Astronomy","Math","Physics"]
#         self.course_name.addItems(courses)
#         self.course_name.setCurrentText(course_name)
#         layout.addWidget(self.course_name)

#         #add the phone number
#         mobile=window.table.item(index,3).text()
#         self.mobile=QLineEdit(mobile)
#         self.mobile.setPlaceholderText("Mobile")
#         layout.addWidget(self.mobile)

#         # add the submit button
#         button=QPushButton("Update")
#         button.clicked.connect(self.update_student)#goes to the student function
#         layout.addWidget(button)   # ✅ You missed this line!

#         self.setLayout(layout)
#     def update_student(self):
#         connection=DatabaseConnection().connect()
#         cursor=connection.cursor()
#         cursor.execute("UPDATE students SET name=%s, course=%s,mobile=%s WHERE id=%s",(self.student_name.text(),self.course_name.itemText(self.course_name.currentIndex()),
#                         self.mobile.text(),self.student_id))# make changes to the databse
#         connection.commit()
#         cursor.close()
#         connection.close()
#         #referesh the table
#         window.load_data()
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        index = window.table.currentRow()
        if index < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to edit.")
            self.close()
            return

        item_name = window.table.item(index, 1)
        item_id = window.table.item(index, 0)
        item_course = window.table.item(index, 2)
        item_mobile = window.table.item(index, 3)

        if item_name is None or item_id is None or item_course is None or item_mobile is None:
            QMessageBox.warning(self, "Invalid selection", "Selected row does not contain full data.")
            self.close()
            return

        student_name = item_name.text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.student_id = item_id.text()

        course_name = item_course.text()
        self.course_name = QComboBox()
        courses = ["Biology", "Astronomy", "Math", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        mobile = item_mobile.text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        button.clicked.connect(self.update_student)  # ✅ method exists below
        layout.addWidget(button)

        self.setLayout(layout)

    # ✅ Make sure this method is indented inside the class
    def update_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name=%s, course=%s, mobile=%s WHERE id=%s",
            (
                self.student_name.text(),
                self.course_name.itemText(self.course_name.currentIndex()),
                self.mobile.text(),
                self.student_id,
            ),
        )
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        self.close()



    
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("delete Student Data")
              

        layout=QGridLayout()# it is compulsiry to write to generATE  the window
        confirmation=QLabel("Are you Sure you want to delete")# it is label which i want to be shown
        yes=QPushButton("yes")# made a button
        no=QPushButton("No")# made a button

        layout.addWidget(confirmation,0,0,1,2)# where the question is to be present in the window
        layout.addWidget(yes,1,0)# in delete window where yes is present
        layout.addWidget(no,1,1)# in delete window where no is present
        self.setLayout(layout)# how thw delete window looks to the user
        yes.clicked.connect(self.delete_student)# goes to the function where we made changes in the data base
    def delete_student(self):
        # get index 
        index=window.table.currentRow()# to get the index of the row on which the user clicked 
        
        # get id from selected row
        student_id=window.table.item(index,0).text()# now take out the elemnt from the table

        connection=DatabaseConnection().connect()
        cursor=connection.cursor() # amde a connection 
        cursor.execute("DELETE from students WHERE id=%s",(student_id, ))# what user ask the program to do
        connection.commit()# commit the changes made by the user in the data base 
        cursor.close()# close down the cursor 
        connection.close()# clise down the connection
        window.load_data()# to refresh the main window by changes

        self.close()# weneed to wroite this because it tell we need to close the window od delete 

        confirmation_widget=QMessageBox()# it shows the success message
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("the record was deleted Succesfully")
        confirmation_widget.exec()
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout1= QVBoxLayout()
        #create layout and input widget
        self.student_name_search=QLineEdit()
        self.student_name_search.setPlaceholderText("Name")
        layout1.addWidget(self.student_name_search)

        # add the submit button
        button=QPushButton("Search")
        #button.clicked.connect(self.add_student)#goes to the student function
        button.clicked.connect(self.Seach_Student)
        layout1.addWidget(button)   

        self.setLayout(layout1)

    def Seach_Student(self):
        name=self.student_name_search.text()
        connection=DatabaseConnection().connect()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name= %s",(name,))
        result=cursor.fetchall()
        rows=list(result)
        # print(rows)
        items=window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout= QVBoxLayout()

        self.student_name=QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        #add the coursees
        self.course_name=QComboBox()
        courses=["Biology","Astronomy","Math","Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        #add the phone number

        self.mobile=QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # add the submit button
        button=QPushButton("Register")
        button.clicked.connect(self.add_student)#goes to the student function
        layout.addWidget(button)   # ✅ You missed this line!

        self.setLayout(layout)
    def add_student(self):
        name=self.student_name.text()
        course=self.course_name.itemText(self.course_name.currentIndex())

        mobile=self.mobile.text()
        connection=DatabaseConnection().connect()    
        cursor=connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES (%s,%s,%s)",
                       (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())

