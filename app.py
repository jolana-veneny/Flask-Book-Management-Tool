import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session, g

import sqlite3 
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps


import re
import collections

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()

    
def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("UserID") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/overview")
@login_required
def overview():

        try:
            UserID = session["UserID"]
            sqliteConnection = sqlite3.connect('BookLog.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sql_select_query = """SELECT * FROM BookList WHERE UserID = (?) ORDER BY Title ASC """
            data = (UserID,)
            cursor.execute(sql_select_query, data)
            rows = cursor.fetchall()

            sqliteConnection.commit()
            cursor.close()
            return render_template("overview.html", rows=rows, UserID=UserID)
         
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
                return render_template("overview.html", rows=rows, UserID=UserID)
        return render_template("index.html")
 
@app.route("/detail/<bookId>", methods=['GET', 'POST'])
@login_required
def detail(bookId):
    session['bookId'] = bookId
    UserID = session["UserID"]
    try:
        
        print(bookId)
        sqliteConnection = sqlite3.connect('BookLog.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select * from BookList where BookId = ? AND UserID = ?"""
        cursor.execute(sql_select_query, (bookId, UserID,))
        row = cursor.fetchone()
        
        sqliteConnection.commit()
        cursor.close()
        return render_template("detail.html", row=row)

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
            #return render_template("detail.html", row=row)
    return render_template("index.html")

@app.route("/edit/<bookId>" , methods=['GET', 'POST'])
@login_required
def edit(bookId):
    UserID = session["UserID"]
    if request.method == "GET":
        session['bookId'] = bookId
        try:
            sqliteConnection = sqlite3.connect('BookLog.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLiteGET")

            query = """SELECT * FROM BookList WHERE BookId = ? AND UserID = ?"""
            cursor.execute(query, (bookId, UserID, ))
            row = cursor.fetchone()
            sqliteConnection.commit()
            print("Python Variables selected successfully from your table")
            cursor.close()

            bookId = row[0]
            title = row[1]
            authorFirstName = row[2]
            authorLastName = row[3]
            year  = row[4]
            language = row[5]
            type = row[6]
            pages = row[7]
            status = row[9]
            review = row[10]
            session['text'] = row[8]
            recommend = row[13]
            # Topics
            action = row[15]
            children = row[16]
            fantasy = row[17]
            mystery = row[18]
            political_thriller = row[19]
            romance = row[20]
            science_fiction = row[21]
            art = row[22]
            autobiography = row[23]
            guide = row[24]
            history = row[25]
            languages = row[26]
            media = row[27]
            politics = row[28]
            national_security = row[29]

            print("Status is:", status)
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
                return render_template("edit.html", languages=languages, media=media, politics=politics, national_security=national_security, romance=romance, science_fiction=science_fiction, art=art, autobiography=autobiography, guide=guide,  history=history, action=action, children=children,  fantasy=fantasy, mystery=mystery, political_thriller=political_thriller,  bookId=bookId, title=title, authorFirstName=authorFirstName, authorLastName=authorLastName, language=language, year=year, pages=pages, type=type, status=status, review=review, recommend=recommend)
    if request.method == "POST":
        try:
            title = request.form.get("Title")
            authorFirstName = request.form.get("AuthorFirstName")
            authorLastName = request.form.get("AuthorLastName")
            year = request.form.get("Year")
            language = request.form.get("Language")
            type = request.form.get("Type")
            pages = request.form.get("Pages")
            status = request.form.get("Status")
            review = request.form.getlist("review")[0]
            recommend = request.form.get("checkbox")

            # Topics
            action = request.form.get("Action")
            children = request.form.get("Children")
            fantasy = request.form.get("Fantasy")
            mystery = request.form.get("Mystery")
            political_thriller = request.form.get("Political_thriller")
            romance = request.form.get("Romance")
            science_fiction = request.form.get("Science_fiction")
            art = request.form.get("Art")
            autobiography = request.form.get("Autobiography")
            guide = request.form.get("Guide")
            history = request.form.get("History")
            languages = request.form.get("Languages")
            media = request.form.get("Media")
            politics = request.form.get("Politics")
            national_security = request.form.get("Security")

            # Reading level
            text = request.form.get("ReadingLevel")

            words = text.count(" ") + 1
            sentences = text.count(".") + text.count("!") + text.count("?")
            punctuation = text.count("'") + text.count(",") + text.count(":") + text.count(";")
            letters = (len(text) - words - sentences - punctuation) + 1

            L = 100 / words * letters
            S = 100 / words * sentences
            level = 0.0588 * L - 0.296 * S - 15.8

            if (level == -15.8):
                result = session.get('text', None)
            elif (level < 1) and (level > 0):
                result = "Before Grade 1"
            elif (level > 16):
                result = "Grade 16+"
            else:
                result = "Grade " + str(round(level))

            # gET BOOKiD out of a session
            bookId = session.get('bookId', None)

            # Update sequence (main data)
            Connection = sqlite3.connect('BookLog.db')
            cursor = Connection.cursor()
            print("Connected to SQLitefor POST")
            query2 = """UPDATE BookList SET Title = ?, AuthorFirstName= ?, AuthorLastName = ?, Year = ?, Language = ?, Type = ?, Pages = ?, Status = ?, review = ?, ReadingLevel =?, Recommend =?, 
            Action =?, Children = ?, Fantasy = ?, Mystery = ?, Political_thriller = ?, Romance = ?, Science_fiction =?, Art = ?, Autobiography = ?, Guide = ?, History = ?, Languages =?, Media = ?,
            politics = ?, National_Security = ?  WHERE BookId = ? AND UserID = ?"""
            data_tuple2 = (title, authorFirstName, authorLastName, year, language, type, pages, status, review, result, recommend, 
            action, children, fantasy, mystery, political_thriller, romance, science_fiction, art, autobiography, guide, history, languages, media, 
            politics, national_security, bookId, UserID,)
            cursor.execute(query2, (data_tuple2))

            Connection.commit()
            cursor.close()
            print("UPDATED")  
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (Connection):
                Connection.close()
                print("The SQLite connection is closed FINALLY")
                return redirect("/overview")

@app.route("/form", methods=["GET", "POST"])
@login_required
def form():
    """Submits form to database"""
    UserID = session["UserID"]
    if request.method == "POST":     
        
        try:
            title = request.form.get("Title")
            authorFirstName = request.form.get("AuthorFirstName")
            authorLastName = request.form.get("AuthorLastName")
            year = request.form.get("Year")
            language = request.form.get("Language")
            type = request.form.get("Type")
            pages = request.form.get("Pages")
            status = request.form.get("Status")
            review = request.form.get("review")
            recommend = request.form.get("checkbox")

            # Topics
            action = request.form.get("Action")
            children = request.form.get("Children")
            fantasy = request.form.get("Fantasy")
            mystery = request.form.get("Mystery")
            political_thriller = request.form.get("Political_thriller")
            romance = request.form.get("Romance")
            science_fiction = request.form.get("Science_fiction")
            art = request.form.get("Art")
            autobiography = request.form.get("Autobiography")
            guide = request.form.get("Guide")
            history = request.form.get("History")
            languages = request.form.get("Languages")
            media = request.form.get("Media")
            politics = request.form.get("Politics")
            national_security = request.form.get("Security")


            # Reading level program

            text = request.form.get("ReadingLevel")

            words = text.count(" ") + 1
            sentences = text.count(".") + text.count("!") + text.count("?")
            punctuation = text.count("'") + text.count(",") + text.count(":") + text.count(";")
            letters = (len(text) - words - sentences - punctuation) + 1

            L = 100 / words * letters
            S = 100 / words * sentences
            level = 0.0588 * L - 0.296 * S - 15.8

            if (level == -15.8):
                result = "Not Available"
            elif (level < 1) and (level > 0):
                result = "Before Grade 1"
            elif (level > 16):
                result = "Grade 16+"
            else:
                result = "Grade " + str(round(level))

            # Establish a SQLite connection from Python.
            sqliteConnection = sqlite3.connect('BookLog.db')
            #Second, create a cursor object using the connection object.
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            query = """SELECT * FROM Users WHERE UserID = ?"""
            data_tuple0 = (UserID,)
            cursor.execute(query, data_tuple0)
            username = cursor.fetchone()
            print(username)


            #Then, Define the SQLite INSERT Query. Here you need to know the table, and it’s column details.
            sqlite_insert_with_param = """INSERT INTO BookList (title, authorFirstName, authorLastName, year, language, type, pages, ReadingLevel, Status, review, recommend, UserID, Username, Action, Children, Fantasy, Mystery, Political_thriller, Romance, Science_fiction, Art, Autobiography, Guide, History, Languages, Media, Politics, National_Security) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?);"""
            data_tuple = (title, authorFirstName, authorLastName, year, language, type, pages, result, status, review, recommend, UserID, username[1], action, children, fantasy, mystery, political_thriller, romance, science_fiction, art, autobiography, guide, history, languages, media, politics, national_security,)
            #Execute the INSERT query using the cursor.execute()
            cursor.execute(sqlite_insert_with_param, data_tuple)

            #After the successful execution of a SQLite query, Don’t forget to commit your changes to the database.
            sqliteConnection.commit()
            print("Python Variables inserted successfully into your table")
            #Close the SQLite database connection.
            cursor.close()
        #Also, don’t forget to catch SQLite exceptions if any.
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        return redirect("/overview")

    if request.method == "GET":
        return render_template("form.html")

@app.route("/delete/<bookId>", methods=["POST"])
@login_required
def delete(bookId):
    UserID = session["UserID"]
    try:
        
        sqliteConnection = sqlite3.connect('BookLog.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        delete = """DELETE FROM BookList where BookId = (?) AND UserID = (?)"""
        delete_data =  (bookId, UserID,)
        cursor.execute(delete, delete_data)
        delete2 = """DELETE FROM BookGenres where BookId = (?) AND UserID = (?)"""
        delete_data2 =  (bookId, UserID,)
        cursor.execute(delete2, delete_data2)

        sqliteConnection.commit()
        print("Deleted")
        flash('Entry deleted')

    except sqlite3.Error as error:
        print("Failed to delete", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return redirect("/overview")

@app.route("/top")
@login_required
def top(): 
    UserID = session["UserID"]
    try:
        
        sqliteConnection = sqlite3.connect('BookLog.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """SELECT * FROM BookList WHERE UserID = ? ORDER BY Review DESC LIMIT 3"""
        data_tuple = (UserID,)
        cursor.execute(sql_select_query, (data_tuple))
        rows = cursor.fetchall()

        sqliteConnection.commit()
        cursor.close()
        return render_template("top.html", rows=rows)
        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return render_template("top.html", rows=rows)


@app.route("/recommend")
@login_required
def recommend(): 
    UserID = session["UserID"]
    try:
        sqliteConnection = sqlite3.connect('BookLog.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        query = """SELECT * FROM BookList WHERE NOT UserID = ? AND Recommend = ? ORDER BY RANDOM()"""
        data_tuple = (UserID, 1, )
        cursor.execute(query, (data_tuple))
        rows = cursor.fetchall()

        sqliteConnection.commit()
        cursor.close()
        return render_template("recommend.html", rows=rows)

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return render_template("recommend.html", rows=rows)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    UserID = session["UserID"]
    if request.method == "POST": 
        try:
            first_name = request.form.get("AuthorFirstName")
            last_name = request.form.get("AuthorLastName")
            title = request.form.get("Title")
            language = request.form.get("Language")

            action = request.form.get("Action")
            children = request.form.get("Children")
            fantasy = request.form.get("Fantasy")
            mystery = request.form.get("Mystery")
            political_thriller = request.form.get("Political_thriller")
            romance = request.form.get("Romance")
            science_fiction = request.form.get("Science_fiction")
            art = request.form.get("Art")
            autobiography = request.form.get("Autobiography")
            guide = request.form.get("Guide")
            history = request.form.get("History")
            languages = request.form.get("Languages")
            media = request.form.get("Media")
            politics = request.form.get("Politics")
            national_security = request.form.get("Security")

            length_200 = request.form.get("200")
            length_400 = request.form.get("400")
            length_600 = request.form.get("600")
            length_800 = request.form.get("800")
            length_1000 = request.form.get("1000")

            review_20 = request.form.get("20")
            review_40 = request.form.get("40")
            review_60 = request.form.get("60")
            review_80 = request.form.get("80")
            review_100 = request.form.get("100")

            name_results, topic_results, length_results, review_results = [],[],[],[]

            print(type(length_800), length_600, length_1000)
            sqliteConnection = sqlite3.connect('BookLog.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            
            # Name, title, langauge search
            if ((len(title) or len(first_name) or len(last_name) or len(language)) != 0):
                if len(title) != 0 and len(first_name) != 0 and len(last_name) != 0 and len(language) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorFirstName = (?) AND AuthorLastName = (?) AND Title = (?) AND Language = (?)"""
                    data = (UserID, first_name, last_name, title, language,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("title, first, last, language")

                elif len(title) != 0 and len(first_name) != 0 and len(last_name) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorFirstName = (?) AND AuthorLastName = (?) AND Title = (?)"""
                    data = (UserID, first_name, last_name, title,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("title, first, last")

                elif len(title) != 0 and len(last_name) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorLastName = (?) AND Title = (?)"""
                    data = (UserID, last_name, title,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("title, last")

                elif len(title) != 0 and len(first_name) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorFirstName = (?) AND Title = (?)"""
                    data = (UserID, first_name, title,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("title, first")

                elif len(title) != 0 and len(language) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Language = (?) AND Title = (?)"""
                    data = (UserID, language, title,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("title, language")

                elif (len(first_name) and len(last_name) != 0):
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorLastName = (?) AND AuthorFirstName = (?)"""
                    data = (UserID, last_name, first_name,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("first, last")

                elif len(language) != 0 and len(last_name) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?)  AND AuthorLastName = (?) AND Language = (?)"""
                    data = (UserID, last_name, language,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("language, last") 

                elif len(last_name) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorLastName = (?)"""
                    data = (UserID, last_name, )
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("last")

                elif len(first_name) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND AuthorFirstName = (?)"""
                    data = (UserID, first_name,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("first")

                elif len(title) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Title = (?)"""
                    data = (UserID, title,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("title")

                elif len(language) != 0:
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Language = (?)"""
                    data = (UserID, language,)
                    cursor.execute(query, data)
                    name_results = cursor.fetchall()
                    print("language")       

                print(name_results)
            if ((action or children or fantasy or mystery or romance or political_thriller or science_fiction or art or autobiography or guide or history or languages or media or politics or national_security) == "1"):
                counter = 0
                rows = []
                # Topic search
                if action == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Action = (?)"""
                    data = (UserID, action,)
                    cursor.execute(query, data)
                    print("action")
                    rows = rows + cursor.fetchall()
                    counter += 1  
                    
                if children == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Children = (?)"""
                    data = (UserID, children,)
                    cursor.execute(query, data)
                    rows = rows + cursor.fetchall()
                    counter += 1 
                    print("children")
                    
                if fantasy == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Fantasy = (?)"""
                    data = (UserID, fantasy,)
                    cursor.execute(query, data)
                    rows = rows + cursor.fetchall()
                    counter += 1 
                    print("fantasy")

                if mystery == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Mystery = (?)"""
                    data = (UserID, mystery,)
                    cursor.execute(query, data)
                    rows = rows + cursor.fetchall()
                    counter += 1 
                    print("mystery")

                if political_thriller == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Political_thriller = (?)"""
                    data = (UserID, political_thriller,)
                    print("political_thriller")
                    cursor.execute(query, data)
                    rows = rows + cursor.fetchall()
                    counter += 1 

                if romance == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Romance = (?)"""
                    data = (UserID, romance,)
                    cursor.execute(query, data)
                    print("romance")
                    rows = rows + cursor.fetchall()
                    counter += 1 

                if science_fiction == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Science_fiction = (?)"""
                    data = (UserID, science_fiction,)
                    cursor.execute(query, data)
                    print("science_fiction")
                    rows = rows + cursor.fetchall()
                    counter += 1 

                if art == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Art = (?)"""
                    data = (UserID, art,)
                    cursor.execute(query, data)
                    print("art")
                    rows = rows + cursor.fetchall()
                    counter += 1 

                if autobiography == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Autobiography = (?)"""
                    data = (UserID, autobiography,)
                    cursor.execute(query, data)
                    print("autobiography")
                    rows = rows + cursor.fetchall()
                    counter += 1 
                
                if guide == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Guide = (?)"""
                    data = (UserID, guide,)
                    cursor.execute(query, data)
                    print("guide")
                    rows = rows + cursor.fetchall()
                    counter += 1 
                
                if history == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND History = (?)"""
                    data = (UserID, history,)
                    cursor.execute(query, data)
                    print("history")
                    rows = rows + cursor.fetchall()
                    counter += 1 
                
                if languages == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Languages = (?)"""
                    data = (UserID, languages,)
                    cursor.execute(query, data)
                    print("languages")
                    rows = rows + cursor.fetchall()
                    counter += 1 

                if media == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Media = (?)"""
                    data = (UserID, media,)
                    cursor.execute(query, data)
                    print("media")
                    rows = rows + cursor.fetchall()
                    counter += 1 
                
                if politics == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Politics = (?)"""
                    data = (UserID, politics,)
                    cursor.execute(query, data)
                    print("politics")
                    rows = rows + cursor.fetchall()
                    counter += 1 

                if national_security == "1":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND National_Security = (?)"""
                    data = (UserID, national_security,)
                    cursor.execute(query, data)
                    print("national_security")
                    rows = rows + cursor.fetchall()
                    counter += 1 

                topic_results = set([x for x in rows if rows.count(x) == counter])
                print(topic_results)

            # Length search
            if ((length_200 or length_400 or length_600 or length_800 or length_1000) != 0):
                rows2 = []
            
                if length_200 == "200":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Pages <= 200 """
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows2 = cursor.fetchall()
                    print("200")

                if length_400 == "400":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Pages BETWEEN 200 AND 400  """
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows2 = rows2 + cursor.fetchall()
                    print("400")

                if length_600 == "600":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Pages BETWEEN 400 AND 600  """
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows2 = rows2 + cursor.fetchall()
                    print("600")

                if length_800 == "800":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Pages BETWEEN 600 AND 800  """
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows2 = rows2 + cursor.fetchall()
                    print("800")

                if length_1000 == "1000":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Pages > 800 """
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows2 = rows2 + cursor.fetchall()
                    print("1000")

                length_results = rows2
                print(length_results)
                
            # Review search
            if ((review_20 or review_40 or review_60 or review_80 or review_100) != 0):
                rows3 = []
                if review_20 == "20":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Review <= 20  """
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows3 = rows3 + cursor.fetchall()
                    print("20")

                if review_40 == "40":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Review > 20  AND Review <= 40"""
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows3 = rows3 + cursor.fetchall()
                    print("40")

                if review_60 == "60":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Review > 40  AND Review <= 60"""
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows3 = rows3 + cursor.fetchall()
                    print("60")

                if review_80 == "80":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Review > 60  AND Review <= 80"""
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows3 = rows3 + cursor.fetchall()
                    print("80")

                if review_100 == "100":
                    query = """SELECT * FROM BookList WHERE UserID = (?) AND Review > 80  AND Review <= 100"""
                    data = (UserID, )
                    cursor.execute(query, data)
                    rows3 = rows3 + cursor.fetchall()
                    print("100")
                
                review_results = rows3
                print(review_results)

            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
                return render_template("search.html", name_results=name_results, topic_results=topic_results, length_results=length_results, review_results=review_results)
        return render_template("search.html", name_results=name_results, topic_results=topic_results, length_results=length_results, review_results=review_results)

    if request.method == "GET":
        return render_template("search.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Display register form if method get
    if request.method == "GET":
        return render_template("register.html")
    
    # Create variables (outside of loops)
    username = request.form.get("UserName")
    password = request.form.get("Password")
    confirmation = request.form.get("ConfirmPassword")
    hashed = generate_password_hash(password)

    if request.method == "POST":
        # Check if no username type
        if not username:
            error = "Enter a username"
            return render_template("apology.html", error=error)

        # Ensure password was submitted
        elif not password:
            error = "Enter a password"
            return render_template("apology.html", error=error)

        # Ensure confirmation password was submitted
        elif not confirmation:
            error = "Confirm pasword"
            return render_template("apology.html", error=error)

        # Check password confirmation field checks original password
        if not (password) == (confirmation):
            error = "Passwords do not match"
            return render_template("apology.html", error=error)

        if len(password) < 8:
            error = "Password has to be longer than 8 characters."
            return render_template("apology.html", error=error)
        elif re.search('[0-9]', password) is None:
            error = "Password needs to contain a number."
            return render_template("apology.html", error=error)
        elif re.search('[A-Z]', password) is None:
            error = "Password needs to contain acapital letter."
            return render_template("apology.html", error=error)
        elif re.search('[^A-Za-z\s0-9]', password) is None:
            error = "Password needs to contain a special character"
            return render_template("apology.html", error=error)
        
        # Start the insert function
        try:
            sqliteConnection = sqlite3.connect('BookLog.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            query = """SELECT * FROM Users WHERE Username= (?)"""
            cursor.execute(query, (username,))
            rows = cursor.fetchall()
            sqliteConnection.commit()
            print("Python Variables selected successfully from your table")
            

            if len(rows) == 1:
                error = "Username alread exists"
                return render_template("apology.html", error=error)

            query2 = """INSERT INTO Users (Username, Hash) VALUES (?, ?) """
            data_tuple = (username, hashed,)
            cursor.execute(query2, (data_tuple))
            sqliteConnection.commit()
            print("Python Variables inserted successfully into your table")

            query3 = """SELECT * FROM Users WHERE Username=?"""
            data_tuple3 = (username,)
            cursor.execute(query3, (data_tuple3))
            user = cursor.fetchone()
            sqliteConnection.commit()
            print("Python Variables selected successfully from your table")
            cursor.close()

            # Remember which user has logged in
            session["UserID"] = user[0]

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        return redirect("/overview")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("UserName")
        # Ensure username was submitted
        if not request.form.get("UserName"):
            error = "Enter a username"
            return render_template("apology.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("Password"):
            error = "Enter a password"
            return render_template("apology.html", error=error)

        # Query database for username
        try:
            sqliteConnection = sqlite3.connect('BookLog.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            query = """SELECT * FROM Users WHERE Username= (?)"""
            data_tuple3 = username,
            cursor.execute(query, (data_tuple3))
            user = cursor.fetchone()
            sqliteConnection.commit()
            print("Python Variables selected successfully from your table")

            if len(user) != 3 :
                error = "invalid username"
                return render_template("apology.html", error=error)
            elif not check_password_hash(user[2], request.form.get("Password")):
                error = "invalid password"
                return render_template("apology.html", error=error)

            # Remember which user has logged in
            session["UserID"] = user[0]

        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        return redirect("/overview")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")





if __name__ == '__main__':
   app.run(debug = True)