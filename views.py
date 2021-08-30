import hashlib
from urllib.parse import parse_qs
import sqlite3


def check_for_student_token(func):
    def wrapper(*args, **kwargs):
        temp_store = open("temp.txt", "r")
        count = 1
        hashes = temp_store.readlines()
        for i in hashes:
            hash = i.split()
            if f"{hashlib.sha256(view_code(*args)).hexdigest()}student" in hash:
                # print("found",count,":",i)
                return func(*args, **kwargs)
            count += 1
        else:
            with open("assets/Student_redirect.html", "rb") as f:
                data = f.read()
            return data
    return wrapper
def check_for_lecturer_token(func):
    def wrapper(*args, **kwargs):
        temp_store = open("temp.txt", "r")
        count = 1
        hashes = temp_store.readlines()
        for i in hashes:
            hash = i.split()
            if f"{hashlib.sha256(view_code(*args)).hexdigest()}lecturer" in hash:
                # print("found",count,":",i)
                return func(*args, **kwargs)
            count += 1
        else:
            with open("assets/Lecturer_redirect.html", "rb") as f:
                data = f.read()
            return data
    return wrapper
def check_for_admin_token(func):
    def wrapper(*args, **kwargs):
        temp_store = open("temp.txt", "r")
        count = 1
        hashes = temp_store.readlines()
        for i in hashes:
            hash = i.split()
            if f"{hashlib.sha256(view_code(*args)).hexdigest()}admin" in hash:
                # print("found",count,":",i)
                return func(*args, **kwargs)
            count += 1
        else:
            with open("assets/Admin_redirect.html", "rb") as f:
                data = f.read()
            return data
    return wrapper
def view_code(environ):
    useragt = environ.get("HTTP_USER_AGENT")
    # useragt2 = environ.get("HTTP_COOKIE")
    return useragt.encode('utf-8')

def home(environ):
    with open("assets/home.html", "rb") as f:
        data = f.read()
    return data

@check_for_student_token
def student_home(environ):
    import csv
    if environ.get("REQUEST_METHOD") == "POST":
        import datetime
        now=datetime.datetime.now().strftime('%d/%m/%y %X')
        IP_Address = get_IP(environ)
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)
        try:
            admission_number = data.get(b"admission_number")[0].decode("utf8")
            name = data.get(b"student_name")[0].decode("utf8")
            email = data.get(b"email")[0].decode("utf8")
        except:
            return b'<h1>Please check the credentials you have given, If error persists please contact your lecturer</h1>'
        
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Students WHERE email ='{email}'"
        cur.execute(SQL)

        if cur.fetchone():
            with open("Attendance.csv", "a") as attendance:
                attendance_writer = csv.writer(attendance, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
                attendance_writer.writerow([f"{IP_Address}", name, email, admission_number, now, "currently in exam"])
            f = open("assets/Student_redirect_exam.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            print("OK456")
            return b"You are not allowed to enter exam room, please contact your lecturer..."
    else:
        with open("assets/student_home.html", "rb") as f:
            data = f.read()
    return data

@check_for_lecturer_token
def lecturer_home(environ):
    with open("assets/lecturer_home.html", "rb") as f:
        data = f.read()
    return data

@check_for_admin_token
def admin_home(environ):
    with open("assets/admin_home.html", "rb") as f:
        data = f.read()
    return data

def admin_logout(environ):
    def deletetoken():
        with open("temp.txt", "r") as f:
            data = f.readlines()
            replacement = ""
            for line in data:
                line.strip()
                changes = line.replace(f"{hashlib.sha256(view_code(environ)).hexdigest()}admin","Admin logged out")
                replacement = replacement + changes
        with open("temp.txt", "w") as replaced_file:
            replaced_file.write(replacement)
        return "logged out"
    deletetoken()
    with open("assets/logout.html", "rb") as f:
        data = f.read()
    return data
def lecturer_logout(environ):
    def deletetoken():
        with open("temp.txt", "r") as f:
            data = f.readlines()
            replacement = ""
            for line in data:
                line.strip()
                changes = line.replace(f"{hashlib.sha256(view_code(environ)).hexdigest()}lecturer","Admin logged out")
                replacement = replacement + changes
        with open("temp.txt", "w") as replaced_file:
            replaced_file.write(replacement)
        return "logged out"
    deletetoken()
    with open("assets/logout.html", "rb") as f:
        data = f.read()
    return data
def student_logout(environ):
    def deletetoken():
        with open("temp.txt", "r") as f:
            data = f.readlines()
            replacement = ""
            for line in data:
                line.strip()
                changes = line.replace(f"{hashlib.sha256(view_code(environ)).hexdigest()}student","Admin logged out")
                replacement = replacement + changes
        with open("temp.txt", "w") as replaced_file:
            replaced_file.write(replacement)
        return "logged out"
    deletetoken()
    with open("assets/logout.html", "rb") as f:
        data = f.read()
    return data
def index(environ):
    with open('assets/basicpage.html', 'rb') as f:
        data = f.read()
    return data



def student_login(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Students WHERE email ='{email}' AND password ='{hashlib.sha256(password).hexdigest()}'"
        cur.execute(SQL)

        if cur.fetchone():
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}student".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Student_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            with open("assets/Loginredirect.html", "rb") as f:
                data = f.read()
            return data
    else:
        f = open("assets/Student_login.html", "rb")
        data = f.read()
        f.close()
        return data
def lecturer_login(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        email = data.get(b"email")[0].decode("utf-8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Lecturers WHERE email ='{email}' AND password ='{hashlib.sha256(password).hexdigest()}'"
        cur.execute(SQL)

        if cur.fetchone():
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}lecturer".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Lecturer_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            with open("assets/Loginredirect.html", "rb") as f:
                data = f.read()
            return data
    else:
        f = open("assets/Lecturer_login.html", "rb")
        data = f.read()
        f.close()
        return data
def admin_login(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Admins WHERE email ='{email}' AND password ='{hashlib.sha256(password).hexdigest()}'"
        cur.execute(SQL)

        if cur.fetchone():
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}admin".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Admin_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            with open("assets/Loginredirect.html", "rb") as f:
                data = f.read()
            return data
    else:
        f = open("assets/Admin_login.html", "rb")
        data = f.read()
        f.close()
        return data

def student_signup(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        first_name = data.get(b"first_name")[0].decode("utf8")
        last_name = data.get(b"last_name")[0].decode("utf8")
        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        sql_query = "INSERT INTO Students (first_name,last_name,email,password) VALUES (?, ?, ?, ?)"
        val = [
                (first_name,last_name,email,hashlib.sha256(password).hexdigest())
            ]
        cur.executemany(sql_query, val)
        conn.commit()
        cur.close()
        conn.close()

        while True:
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}student".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Student_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
    else:
        f = open("assets/Student_signup.html", "rb")
        data = f.read()
        f.close()
        return data
def lecturer_signup(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        first_name = data.get(b"first_name")[0].decode("utf8")
        last_name = data.get(b"last_name")[0].decode("utf8")
        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        sql_query = "INSERT INTO Lecturers (first_name,last_name,email,password) VALUES (?, ?, ?, ?)"
        val = [
                (first_name,last_name,email,hashlib.sha256(password).hexdigest())
            ]
        cur.executemany(sql_query, val)
        conn.commit()
        cur.close()
        conn.close()

        while True:
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}lecturer".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Lecturer_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
    else:
        f = open("assets/Lecturer_signup.html", "rb")
        data = f.read()
        f.close()
        return data
def admin_signup(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        first_name = data.get(b"first_name")[0].decode("utf8")
        last_name = data.get(b"last_name")[0].decode("utf8")
        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        sql_query = "INSERT INTO Admins (first_name,last_name,email,password) VALUES (?, ?, ?, ?)"
        val = [
                (first_name,last_name,email,hashlib.sha256(password).hexdigest())
            ]
        cur.executemany(sql_query, val)
        conn.commit()
        cur.close()
        conn.close()

        while True:
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}admin".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Admin_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
    else:
        f = open("assets/Admin_signup.html", "rb")
        data = f.read()
        f.close()
        return data

def get_IP(environ):
    try:
        return environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
    except KeyError:
        return environ['REMOTE_ADDR']

@check_for_student_token
def exam(environ):
    import pandas as pd
    import datetime
    now=datetime.datetime.now().strftime('%d/%m/%y %X')
    IP_Address = get_IP(environ)
    if environ.get("REQUEST_METHOD") == "POST":
        data_write = pd.read_csv("Attendance.csv")
        data_write.loc[(data_write['IP_Address']) == f"{IP_Address}", 'Time_Out'] = now
        data_write.to_csv("Attendance.csv", index=False)
        with open("assets/Student_loggedin_redirect.html", "rb") as f:
            data = f.read()
        return data
    with open("assets/examroom.html", "rb") as f:
        data = f.read()
    return data


@check_for_lecturer_token
def invigilate_exam(environ):
    import pandas as pd
    a = pd.read_csv("Attendance.csv")
    # a.to_html("assets/Table.htm")
    html_file = a.to_html()
    with open('assets/invigilate.html','r',encoding='utf-8') as f:
        data1=f.read()
    data2=data1.replace('excel_sheet', html_file)
    data2.encode("utf8")
    return data2.encode("utf8")

@check_for_lecturer_token
def check_for_plagiarism(environ):
    if environ['REQUEST_METHOD'] == 'POST':
        import cgi
        import os
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            keep_blank_values=True
        )
        fileitems = post["userfile"], post["userfile2"]
        file_index = 1
        for fileitem in fileitems:
            if fileitem.file:
                filename = f"doc{file_index}.txt"
                file_index += 1
                if not filename:
                    try:
                        return b'No valid filename specified'
                    except Exception:
                        pass
                
                file_path = os.path.join("uploaded files", filename)
                counter = 0
                with open(file_path, 'wb') as output_file:
                    while 1:
                        data = fileitem.file.read(1024)
                        if not data:
                            break
                        output_file.write(data)
                        counter += 1
                        if counter == 100:
                            counter = 0
        ##
        file1=open("uploaded files/doc1.txt","r")
        text1=file1.readlines()
        file2=open("uploaded files/doc2.txt","r")
        text2=file2.readlines()
        # Convert list to string 
        str1=''.join(text1)
        str2=''.join(text2)
        # Split the string
        sent_text1=str1.split('.')
        sent_text2=str2.split('.')
        # Create a for loop that compares two lists
        final_list=[]
        for z in sent_text1:
            for y in sent_text2:
                if z == y:
                    final_list.append(z)

        # print(final_list)
        final_paragraph = ""
        for line in final_list:
            final_paragraph += f"{line}\n"
        count = -1
        for line in final_list:
            count += 1
        lines = -1
        for line in sent_text1:
            lines+=1
        percentage = count/lines*100
        with open("assets/Plagiarism_report.html", "r", encoding='utf-8') as f:
            data = f.read()
        data2 = data.replace('final_paragraph', final_paragraph)
        data2 = data2.replace('percentage', f"{percentage}")#replace cannot accept float so we used f string instead
        data2.encode("utf-8")
        return data2.encode("utf-8")
    else:
        with open("assets/Plagiarism.html", "rb") as f:
            data = f.read()
        return data

@check_for_admin_token
def monitor_exam(environ):
    import pandas as pd
    a = pd.read_csv("Attendance.csv")
    # a.to_html("assets/Table.htm")
    html_file = a.to_html()
    with open('assets/monitor.html','r',encoding='utf-8') as f:
        data1=f.read()
    data2=data1.replace('excel_sheet', html_file)
    data2.encode("utf8")
    return data2.encode("utf8")

@check_for_admin_token
def sample_analysis(environ):
    from matplotlib.figure import Figure
    from matplotlib import pyplot as plt
    from io import BytesIO
    import base64
    import pandas as pd
    import numpy as np
    # Generate the figure **without using pyplot**.
    # fig = plt.Figure()
    # ax = fig.subplots()
    ##
    sample_data = pd.read_csv('sample_dataset.csv')
    # sample_data.to_html("assets/dataframe.htm")
    html_file2 = sample_data.to_html()
    # sample_data.corr().to_html("assets/data_correlation.htm")
    html_file = sample_data.corr().to_html()
    #############################################CAT VS FINAL GRAPHS################################
    def CATvsFinal1():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.CAT_Marks, sample_data.Final_Marks)
        ax.set_title('CAT Marks vs Final Marks')
        ax.set_xlabel('CAT')
        ax.set_ylabel('Final Marks')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def CATvsFinal2():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.CAT_Marks, sample_data.Final_Marks)
        x = np.linspace(8,30,100)
        y = (100/30)*x
        ax.plot(x, y, label='y=mx')
        ax.set_title('CAT Marks vs Final Marks')
        ax.set_xlabel('CAT')
        ax.set_ylabel('Final Marks')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def CATvsFinal3():
        fig = plt.Figure()
        ax = fig.subplots()
        sample_data_male = sample_data[sample_data['Gender'] == 'male']
        sample_data_female = sample_data[sample_data['Gender'] == 'female']
        sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
        ax.scatter(sample_data_male.CAT_Marks, sample_data_male.Final_Marks, label='male')
        ax.scatter(sample_data_female.CAT_Marks, sample_data_female.Final_Marks, label='female')
        ax.scatter(sample_data_nonbinary.CAT_Marks, sample_data_nonbinary.Final_Marks, label='others')
        ax.set_title('CAT Marks vs Final Marks')
        ax.set_xlabel('CAT')
        ax.set_ylabel('Final Marks')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    ########################################################################################################
    ################################CAT VS GPA GRAPHS#######################################################
    def CATvsGPA1():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.CAT_Marks, sample_data.GPA)
        ax.set_title('CAT Marks vs GPA')
        ax.set_xlabel('CAT')
        ax.set_ylabel('GPA')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def CATvsGPA2():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.CAT_Marks, sample_data.GPA)
        x = np.linspace(8,30,100)
        y = (4/30)*x
        ax.plot(x, y, label='y=mx')
        ax.set_title('CAT Marks vs GPA')
        ax.set_xlabel('CAT')
        ax.set_ylabel('GPA')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def CATvsGPA3():
        fig = plt.Figure()
        ax = fig.subplots()
        sample_data_male = sample_data[sample_data['Gender'] == 'male']
        sample_data_female = sample_data[sample_data['Gender'] == 'female']
        sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
        ax.scatter(sample_data_male.CAT_Marks, sample_data_male.GPA, label='male')
        ax.scatter(sample_data_female.CAT_Marks, sample_data_female.GPA, label='female')
        ax.scatter(sample_data_nonbinary.CAT_Marks, sample_data_nonbinary.GPA, label='others')
        ax.set_title('CAT Marks vs GPA')
        ax.set_xlabel('CAT')
        ax.set_ylabel('GPA')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    ##########################################################################################
    ###################ATTENDANCE VS FINAL GRAPHS#############################################
    def AttendancevsFinal1():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.Attendance, sample_data.Final_Marks)
        ax.set_title('Attendance vs Final_Marks')
        ax.set_xlabel('Attendance 1:100%')
        ax.set_ylabel('Final Marks')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def AttendancevsFinal2():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.Attendance, sample_data.Final_Marks)
        x = np.linspace(0.2,1,100)
        y = (100/1)*x
        ax.plot(x, y, label='y=mx')
        ax.set_title('Attendance vs Final Marks')
        ax.set_xlabel('Attendance 1:100%')
        ax.set_ylabel('Final Marks')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def AttendancevsFinal3():
        fig = plt.Figure()
        ax = fig.subplots()
        sample_data_male = sample_data[sample_data['Gender'] == 'male']
        sample_data_female = sample_data[sample_data['Gender'] == 'female']
        sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
        ax.scatter(sample_data_male.Attendance, sample_data_male.Final_Marks, label='male')
        ax.scatter(sample_data_female.Attendance, sample_data_female.Final_Marks, label='female')
        ax.scatter(sample_data_nonbinary.Attendance, sample_data_nonbinary.Final_Marks, label='others')
        ax.set_title('Attendance vs Final Marks')
        ax.set_xlabel('Attendance 1:100%')
        ax.set_ylabel('Final Marks')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    #####################################################################################
    ##########################FINAL VS GPA GRAPHS########################################
    def FinalvsGPA1():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.Final_Marks, sample_data.GPA)
        ax.set_title('Final Marks vs GPA')
        ax.set_xlabel('Final Marks')
        ax.set_ylabel('GPA')
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def FinalvsGPA2():
        fig = plt.Figure()
        ax = fig.subplots()
        ax.scatter(sample_data.Final_Marks, sample_data.GPA)
        x = np.linspace(25,100,100)
        y = (4/100)*x
        ax.plot(x, y, label='y=mx')
        ax.set_title('Final Marks vs GPA')
        ax.set_xlabel('Final Marks')
        ax.set_ylabel('GPA')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    
    def FinalvsGPA3():
        fig = plt.Figure()
        ax = fig.subplots()
        sample_data_male = sample_data[sample_data['Gender'] == 'male']
        sample_data_female = sample_data[sample_data['Gender'] == 'female']
        sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
        ax.scatter(sample_data_male.Final_Marks, sample_data_male.GPA, label='male')
        ax.scatter(sample_data_female.Final_Marks, sample_data_female.GPA, label='female')
        ax.scatter(sample_data_nonbinary.Final_Marks, sample_data_nonbinary.GPA, label='others')
        ax.set_title('Final Marks vs GPA')
        ax.set_xlabel('Final Marks')
        ax.set_ylabel('GPA')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    ###########################################################################################################
    ##########################FINAL COMPARISON##################################
    def OnlinevsPhysical():
        fig = plt.Figure()
        ax = fig.subplots()
        sample_data_online = sample_data[sample_data['Mode_of_Study'] == 'Online']
        sample_data_physical = sample_data[sample_data['Mode_of_Study'] == 'Physical']
        ax.scatter(sample_data_online.Final_Marks, sample_data_online.Final_Marks, label='online')
        ax.scatter(sample_data_physical.Final_Marks, sample_data_physical.Final_Marks, label='physical')
        ax.set_title('Online exam vs Physical exam')
        ax.set_xlabel('Online')
        ax.set_ylabel('Physical')
        ax.legend()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        image =  f"<img src='data:image/png;base64,{data}'/>"
        return image
    #################################################################################    

    with open('assets/Analysis_report.html','r',encoding='utf-8') as f:
        data1=f.read()
    data2=data1.replace('correlation_table', html_file)
    data3 = data2.replace('CATvsFinalPLAIN', CATvsFinal1())
    data4 = data3.replace('CATvsFINALMX', CATvsFinal2())
    data5 = data4.replace('CATvsFinalGENDERS', CATvsFinal3())
    data6 = data5.replace('CATvsGPAPLAIN', CATvsGPA1())
    data7 = data6.replace('CATvsGPAMX', CATvsGPA2())
    data8 = data7.replace('CATvsGPAGENDERS', CATvsGPA3())
    data9 = data8.replace('AttendancevsFinalPLAIN', AttendancevsFinal1())
    data10 = data9.replace('AttendancevsFINALMX', AttendancevsFinal2())
    data11 = data10.replace('AttendancevsFinalGENDERS', AttendancevsFinal3())
    data12 = data11.replace('FinalvsGPAPLAIN', FinalvsGPA1())
    data13 = data12.replace('FINALvsGPAMX', FinalvsGPA2())
    data14 = data13.replace('FinalvsGPAGENDERS', FinalvsGPA3())
    data15 = data14.replace('dataframe_table', html_file2)
    data16 = data15.replace('FinalComparison', OnlinevsPhysical())
    data16.encode("utf8")
    return data16.encode("utf8")


@check_for_admin_token
def analysis(environ):
    import cgi
    import os
    if environ.get("REQUEST_METHOD") == "POST":
        post = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                keep_blank_values=True
        )
        fileitem = post["userfile"]
        if fileitem.file:
            filename = fileitem.filename
            if not filename:
                return b'No valid filename specified'
            file_path = os.path.join("uploaded files", filename)
            counter = 0
            with open(file_path, 'wb') as output_file:
                while 1:
                    data = fileitem.file.read(1024)
                    # End of file
                    if not data:
                        break
                    output_file.write(data)
                    counter += 1
                    if counter == 100:
                        counter = 0
        from matplotlib.figure import Figure
        from matplotlib import pyplot as plt
        from io import BytesIO
        import base64
        import pandas as pd
        import numpy as np
        sample_data = pd.read_csv(os.path.join("uploaded files", filename))
        html_file2 = sample_data.to_html()
        html_file = sample_data.corr().to_html()
        #############################################CAT VS FINAL GRAPHS################################
        def CATvsFinal1():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.CAT_Marks, sample_data.Final_Marks)
                ax.set_title('CAT Marks vs Final Marks')
                ax.set_xlabel('CAT')
                ax.set_ylabel('Final Marks')
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def CATvsFinal2():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.CAT_Marks, sample_data.Final_Marks)
                x = np.linspace(8,30,100)
                y = (100/30)*x
                ax.plot(x, y, label='y=mx')
                ax.set_title('CAT Marks vs Final Marks')
                ax.set_xlabel('CAT')
                ax.set_ylabel('Final Marks')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def CATvsFinal3():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                sample_data_male = sample_data[sample_data['Gender'] == 'male']
                sample_data_female = sample_data[sample_data['Gender'] == 'female']
                sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
                ax.scatter(sample_data_male.CAT_Marks, sample_data_male.Final_Marks, label='male')
                ax.scatter(sample_data_female.CAT_Marks, sample_data_female.Final_Marks, label='female')
                ax.scatter(sample_data_nonbinary.CAT_Marks, sample_data_nonbinary.Final_Marks, label='others')
                ax.set_title('CAT Marks vs Final Marks')
                ax.set_xlabel('CAT')
                ax.set_ylabel('Final Marks')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        ########################################################################################################
        ################################CAT VS GPA GRAPHS#######################################################
        def CATvsGPA1():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.CAT_Marks, sample_data.GPA)
                ax.set_title('CAT Marks vs GPA')
                ax.set_xlabel('CAT')
                ax.set_ylabel('GPA')
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def CATvsGPA2():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.CAT_Marks, sample_data.GPA)
                x = np.linspace(8,30,100)
                y = (4/30)*x
                ax.plot(x, y, label='y=mx')
                ax.set_title('CAT Marks vs GPA')
                ax.set_xlabel('CAT')
                ax.set_ylabel('GPA')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def CATvsGPA3():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                sample_data_male = sample_data[sample_data['Gender'] == 'male']
                sample_data_female = sample_data[sample_data['Gender'] == 'female']
                sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
                ax.scatter(sample_data_male.CAT_Marks, sample_data_male.GPA, label='male')
                ax.scatter(sample_data_female.CAT_Marks, sample_data_female.GPA, label='female')
                ax.scatter(sample_data_nonbinary.CAT_Marks, sample_data_nonbinary.GPA, label='others')
                ax.set_title('CAT Marks vs GPA')
                ax.set_xlabel('CAT')
                ax.set_ylabel('GPA')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        ##########################################################################################
        ###################ATTENDANCE VS FINAL GRAPHS#############################################
        def AttendancevsFinal1():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.Attendance, sample_data.Final_Marks)
                ax.set_title('Attendance vs Final_Marks')
                ax.set_xlabel('Attendance 1:100%')
                ax.set_ylabel('Final Marks')
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def AttendancevsFinal2():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.Attendance, sample_data.Final_Marks)
                x = np.linspace(0.2,1,100)
                y = (100/1)*x
                ax.plot(x, y, label='y=mx')
                ax.set_title('Attendance vs Final Marks')
                ax.set_xlabel('Attendance 1:100%')
                ax.set_ylabel('Final Marks')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def AttendancevsFinal3():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                sample_data_male = sample_data[sample_data['Gender'] == 'male']
                sample_data_female = sample_data[sample_data['Gender'] == 'female']
                sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
                ax.scatter(sample_data_male.Attendance, sample_data_male.Final_Marks, label='male')
                ax.scatter(sample_data_female.Attendance, sample_data_female.Final_Marks, label='female')
                ax.scatter(sample_data_nonbinary.Attendance, sample_data_nonbinary.Final_Marks, label='others')
                ax.set_title('Attendance vs Final Marks')
                ax.set_xlabel('Attendance 1:100%')
                ax.set_ylabel('Final Marks')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        #####################################################################################
        ##########################FINAL VS GPA GRAPHS########################################
        def FinalvsGPA1():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.Final_Marks, sample_data.GPA)
                ax.set_title('Final Marks vs GPA')
                ax.set_xlabel('Final Marks')
                ax.set_ylabel('GPA')
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def FinalvsGPA2():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                ax.scatter(sample_data.Final_Marks, sample_data.GPA)
                x = np.linspace(25,100,100)
                y = (4/100)*x
                ax.plot(x, y, label='y=mx')
                ax.set_title('Final Marks vs GPA')
                ax.set_xlabel('Final Marks')
                ax.set_ylabel('GPA')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        
        def FinalvsGPA3():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                sample_data_male = sample_data[sample_data['Gender'] == 'male']
                sample_data_female = sample_data[sample_data['Gender'] == 'female']
                sample_data_nonbinary = sample_data[sample_data['Gender'] == 'non-binary']
                ax.scatter(sample_data_male.Final_Marks, sample_data_male.GPA, label='male')
                ax.scatter(sample_data_female.Final_Marks, sample_data_female.GPA, label='female')
                ax.scatter(sample_data_nonbinary.Final_Marks, sample_data_nonbinary.GPA, label='others')
                ax.set_title('Final Marks vs GPA')
                ax.set_xlabel('Final Marks')
                ax.set_ylabel('GPA')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        ###########################################################################################################
        ##########################FINAL COMPARISON##################################
        def OnlinevsPhysical():
            fig = plt.Figure()
            ax = fig.subplots()
            try:
                sample_data_online = sample_data[sample_data['Mode_of_Study'] == 'Online']
                sample_data_physical = sample_data[sample_data['Mode_of_Study'] == 'Physical']
                ax.scatter(sample_data_online.Final_Marks, sample_data_online.Final_Marks, label='online')
                ax.scatter(sample_data_physical.Final_Marks, sample_data_physical.Final_Marks, label='physical')
                ax.set_title('Online exam vs Physical exam')
                ax.set_xlabel('Online')
                ax.set_ylabel('Physical')
                ax.legend()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                data = base64.b64encode(buf.getbuffer()).decode("ascii")
                image =  f"<img src='data:image/png;base64,{data}'/>"
                return image
            except:
                return 'you have an invalid attribute in your dataframe'
        #################################################################################

        with open('assets/Analysis_report.html','r',encoding='utf-8') as f:
            data1=f.read()
        data2=data1.replace('correlation_table', html_file)
        data3 = data2.replace('CATvsFinalPLAIN', CATvsFinal1())
        data4 = data3.replace('CATvsFINALMX', CATvsFinal2())
        data5 = data4.replace('CATvsFinalGENDERS', CATvsFinal3())
        data6 = data5.replace('CATvsGPAPLAIN', CATvsGPA1())
        data7 = data6.replace('CATvsGPAMX', CATvsGPA2())
        data8 = data7.replace('CATvsGPAGENDERS', CATvsGPA3())
        data9 = data8.replace('AttendancevsFinalPLAIN', AttendancevsFinal1())
        data10 = data9.replace('AttendancevsFINALMX', AttendancevsFinal2())
        data11 = data10.replace('AttendancevsFinalGENDERS', AttendancevsFinal3())
        data12 = data11.replace('FinalvsGPAPLAIN', FinalvsGPA1())
        data13 = data12.replace('FINALvsGPAMX', FinalvsGPA2())
        data14 = data13.replace('FinalvsGPAGENDERS', FinalvsGPA3())
        data15 = data14.replace('dataframe_table', html_file2)
        data16 = data15.replace('FinalComparison', OnlinevsPhysical())
        data16.encode("utf8")
        return data16.encode("utf8")
    else:
        with open("assets/analysis.html", "rb") as f:
            data = f.read()
        return data




############################################################################################################
#################################################### IMAGES ###############################################
def comp(environ):
    with open('assets/images/404(comp).png','rb') as f:
        data = f.read()
    return data
def phone(environ):
    with open('assets/images/404(phone).png','rb') as f:
        data = f.read()
    return data
def favicon(environ):
    with open('assets/images/favicon.png','rb') as f:
        data = f.read()
    return data
def nav_icon(environ):
    with open('assets/images/nav.png','rb') as f:
        data = f.read()
    return data
def green_logo(environ):
    with open('assets/images/Logo-final(green).png','rb') as f:
        data = f.read()
    return data
def white_logo(environ):
    with open('assets/images/Logo-final(white).png','rb') as f:
        data = f.read()
    return data
def github(environ):
    with open('assets/images/github.png','rb') as f:
        data = f.read()
    return data
def instagram(environ):
    with open('assets/images/instagram.png','rb') as f:
        data = f.read()
    return data
def linkedin(environ):
    with open('assets/images/linkedin.png','rb') as f:
        data = f.read()
    return data
def twitter(environ):
    with open('assets/images/twitter.png','rb') as f:
        data = f.read()
    return data
def dataframe(environ):
    with open('assets/images/dataframe.png','rb') as f:
        data = f.read()
    return data
def logincss(environ):
    data = b''
    with open('assets/static/login.css', 'rb') as f:
        data = f.read()
    return data
def basicpagecss(environ):
    data = b''
    with open('assets/static/basicpage.css', 'rb') as f:
        data = f.read()
    return data
def notfoundcss(environ):
    data = b''
    with open('assets/static/404.css', 'rb') as f:
        data = f.read()
    return data
def indexjs(environ):
    data = b''
    with open('assets/static/index.js', 'rb') as f:
        data = f.read()
    return data
def loading(environ):
    with open('assets/loading.html','r',encoding='utf-8') as f:
        data=f.read()
    data.encode("utf8")
    return data.encode("utf8")
def gif(environ):
    with open('assets/images/among-us-7.gif', 'rb') as f:
        data = f.read()
    return data
def documentation(environ):
    with open('documents/LOAS USER MANUAL.pdf') as f:
        return f



def admin_forgot_password(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Admins WHERE email ='{email}'"
        cur.execute(SQL)

        if cur.fetchone():
            cur.execute(f"UPDATE Admins SET password = '{hashlib.sha256(password).hexdigest()}' WHERE email = '{email}'")
            conn.commit()
            cur.close()
            conn.close()
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}admin".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Admin_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            with open("assets/Loginredirect.html", "rb") as f:
                data = f.read()
            return data
    else:
        f = open("assets/Admin_forgotPass.html", "rb")
        data = f.read()
        f.close()
        return data
def lecturer_forgot_password(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Lecturers WHERE email ='{email}'"
        cur.execute(SQL)

        if cur.fetchone():
            cur.execute(f"UPDATE Lecturers SET password = '{hashlib.sha256(password).hexdigest()}' WHERE email = '{email}'")
            conn.commit()
            cur.close()
            conn.close()
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}admin".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Lecturer_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            with open("assets/Loginredirect.html", "rb") as f:
                data = f.read()
            return data
    else:
        f = open("assets/Lecturer_forgotPass.html", "rb")
        data = f.read()
        f.close()
        return data
def student_forgot_password(request):
    if request.get("REQUEST_METHOD") == "POST":
        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        email = data.get(b"email")[0].decode("utf8")
        password = data.get(b"password")[0]
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        SQL = f"SELECT * FROM Students WHERE email ='{email}'"
        cur.execute(SQL)

        if cur.fetchone():
            cur.execute(f"UPDATE Students SET password = '{hashlib.sha256(password).hexdigest()}' WHERE email = '{email}'")
            conn.commit()
            cur.close()
            conn.close()
            try:
                with open("temp.txt", "ab") as temp_store:
                    temp_store.write(f"\n{hashlib.sha256(view_code(request)).hexdigest()}admin".encode('utf-8'))
            except AssertionError:
                pass
            f = open("assets/Student_loggedin_redirect.html", "rb")
            data = f.read()
            data = data.decode("utf8")
            return data.encode("utf8")
        else:
            with open("assets/Loginredirect.html", "rb") as f:
                data = f.read()
            return data
    else:
        f = open("assets/Student_forgotPass.html", "rb")
        data = f.read()
        f.close()
        return data