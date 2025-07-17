#Name: Ahmed Ebrahim Elmohamdy  ID: 320220109 Sec(6)

import DataBase as DataBase
from tkinter import *
from tkinter import ttk
#pip install ttkthemes
from ttkthemes import themed_tk 


server_connection = DataBase.create_server_connection('127.0.0.1','3306','root',DataBase.db_pw) 
connection =  DataBase.create_db_connection('127.0.0.1','root',DataBase.db_pw,'pasword')

spec_menu_values = ['Optics','Neurology','Dermatology','Pathology','Pediatrics']
running = True


class patient:
   name = ""
   spec = 0
   stat = ""
   num = 0
   def __init__(self, name, spec, stat):
      self.name = name
      self.spec = spec
      self.stat = stat


class manager:
   def add(self,spec:str,name:str,status:int,root):
      server_connection = DataBase.create_server_connection('127.0.0.1','3306','root',DataBase.db_pw)
      connection =  DataBase.create_db_connection('127.0.0.1','root',DataBase.db_pw,'HospitalSystem')
      result = DataBase.execute_query(connection,f"SELECT COUNT(*) FROM spec1 WHERE Specialization = '{spec}'")
      num_rows = result.fetchone()
      num_rows = num_rows[0]
      container = Text(root, height=2, width=40)
      container.place(x=180,y=230)
      result = DataBase.execute_query(connection,f"SELECT * FROM spec1 WHERE Specialization = '{spec}'")
      for patient in result:
         if patient[0] == name:
            container.insert(END,f"This name already exists in this specialization.")
            return
      if spec not in spec_menu_values:
         container.insert(END,"No such specialization.")
         return
      if num_rows >= 10:
         container.insert(END, "can't add to this specialization.")
         return
      if all(lett.isalpha() or lett.isspace() for lett in name) != True:
         container.insert(END,"Please enter a name")
         return
      if status == 'Normal':
         DataBase.execute_query(connection,f"""
      insert into spec1 (Name,Specialization,Status,Date) values ("{name}","{spec}","{status}",CURRENT_DATE());
      """)
      elif status == 'Urgent':   
         DataBase.execute_query(connection,f"""
      insert into spec1 (Name,Specialization,Status,Date) values ("{name}","{spec}","{status}",CURRENT_DATE());
      """)
      elif status == 'Super Urgent': 
         DataBase.execute_query(connection,f"""
      insert into spec1 (Name,Specialization,Status,Date) values ("{name}","{spec}","{status}",CURRENT_DATE());
      """)
      else:
         container.insert(END, f'Please Enter A Valid Status')
         return
      #text indicate successful add
      for index,lett in enumerate(name):
         if name[index].isspace() == True and index != len(name)-1:
            container.insert(END, f'Successfully added {name} to the "{spec}" specialization')
            return   
      container.insert(END, f'Successfully added {name} to the "{spec}" specialization')
      #insert into spec table
      server_connection.close()
      connection.close()   
      return 
   


   def print(self,spec,root): 
      server_connection = DataBase.create_server_connection('127.0.0.1','3306','root',DataBase.db_pw)
      connection =  DataBase.create_db_connection('127.0.0.1','root',DataBase.db_pw,'HospitalSystem')

      tree = ttk.Treeview(root, show="headings")
      tree.place(x=20,y=80)
      if len(tree.get_children()) != 0:
         for item in tree.get_children():
            tree.delete(item)
      result = DataBase.execute_query(connection,f"SELECT COUNT(*) FROM spec1 WHERE Specialization = '{spec}';").fetchone()
      num_rows = result[0]
      if spec not in spec_menu_values:
         tree.destroy()
         return
      if num_rows == 0:
         tree.destroy()
         return
      connection.commit()
      column_names = ["Name", "Specialization", "Status", "Date"]
      rows = DataBase.execute_query(connection,f"""SELECT * FROM Spec1 WHERE Specialization = '{spec}' ORDER BY CASE
         WHEN Status = 'Super Urgent' then 1
         WHEN Status = 'Urgent' then 2 
         WHEN Status = 'Normal' then 3
         END ASC  """) 
      rows = rows.fetchall() 
      tree["columns"] = tuple(range(len(rows[0])))  # Assuming each row has the same number of columns

      # Add headings to the treeview
      for i, name in enumerate(column_names):
         tree.column(i, anchor="center")
         tree.heading(i, text=name)

      # Add data to the treeview
      for row in rows:
         tree.insert("", END, values=row)
      scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
      tree.configure(yscrollcommand=scrollbar.set)
      scrollbar.place(x=810,y=109,height=201)  

      server_connection.close()
      connection.close()         
      return 
   
   def get_next(self,spec,root):
      server_connection = DataBase.create_server_connection('127.0.0.1','3306','root',DataBase.db_pw)
      connection =  DataBase.create_db_connection('127.0.0.1','root',DataBase.db_pw,'HospitalSystem')

      container = Text(root, height=2, width=40)
      container.place(x=200,y=140)  
      result = DataBase.execute_query(connection,f"SELECT COUNT(*) FROM spec1 WHERE Specialization = '{spec}';").fetchone()
      num_rows = result[0]
      connection.commit()
      if spec not in spec_menu_values:
         container.insert(END,"No such specialization.")
         return
      if num_rows == 0:
         container.insert(END,"No patients in this specialization.")
         return
      result = DataBase.execute_query(connection, f"""SELECT * FROM hospitalsystem.spec1 
        WHERE Specialization = '{spec}' ORDER BY CASE
        WHEN Status = 'Super Urgent' then 1
        WHEN Status = 'Urgent' then 2 
        WHEN Status = 'Normal' then 3
        END ASC LIMIT 1""")
      for patient in result:
         container.insert(END,f"patient: {patient[0]} pls go with the doctor\n")
         DataBase.execute_query(connection,f"DELETE FROM spec1 WHERE Name = '{patient[0]}' AND Specialization = '{patient[1]}' LIMIT 1")
      server_connection.close()
      connection.close()   
      return 
      
   def change_pass_word(self, old_pass, new_pass, root):
      server_connection._open_connection()
      connection._open_connection()
      container = Text(root, height=2, width=40)
      container.place(x=180,y=200)
      result = DataBase.execute_query(connection, "SELECT pasword FROM pasword_table  LIMIT 1;").fetchone()
      if old_pass == result[0]:
         DataBase.execute_query(connection,f"UPDATE pasword_table SET pasword = '{new_pass}' LIMIT 1")
         container.insert(END, "Pass Word Changed Successfully")
      else:
         container.insert(END, "Old Password Doesn't Match")
      server_connection.close()
      connection.close()


   def delete(self,spec,root,name):
      server_connection = DataBase.create_server_connection('127.0.0.1','3306','root',DataBase.db_pw)
      connection =  DataBase.create_db_connection('127.0.0.1','root',DataBase.db_pw,'HospitalSystem')

      container = Text(root, height=2, width=40)
      container.place(x=180,y=130)
      result = DataBase.execute_query(connection,f"SELECT * FROM spec1 WHERE Specialization = '{spec}';")
      if spec not in spec_menu_values:
         container.insert(END,"No such specialization.")
         return
      if all(lett.isalpha() or lett.isspace() for lett in name) != True:
         text = ttk.Label(root,text="Please enter a name")
         text.place(x=110,y=70)
         return
      else:
         for patient in result:
            if patient[0] == name and patient[1] == spec:
               DataBase.execute_query(connection,f"DELETE FROM spec1 WHERE Name = '{name}' AND Specialization = '{spec}';")
               container.insert(END,"Deletion Succesful")
               return 
         container.insert(END,"No such name in the specialization")  
         server_connection.close()
         connection.close()      
      return  








