# Flask-Book-Management-Tool

BookLog is a Flask application which uses Python, SQL, HTML, CSS, and JavaScript. BookLog is an online library tool which allows users to keep track of their physical books, add books to their library, edit, and recommend them to other users. 
BookLog allows the users to:
-	Register with a username and a password. The password is stored as a hashed value.
-	Log in and log out 
-	See an overview of all the books and their details
-	Add books to BookLog through a simple form
-	Edit their books through a form with pre-loaded values
-	Rate the books and assign topics to each book
-	Get an assessment of each book's reading level
-	Delete books from their library
-	Run an advanced search by book title, author's name, language, book length, book review, and topics
-	Recommend books to other users and see other users' recommendations.


The application was built in Visual Studio Code and it took the author nearly a month to complete.

On the technical side of things, the BookLog's python application "app.py" consists of 12 app routes and approximately 900 lines. Each app route has a corresponding html template. Altogether 7 of the routes make use of both the get and the post method. To enable the login function and limit access to user-specific content, each app carries a User ID session. Some routes also make a use of a Book ID session to get access to a specific line in the SQL database. 
The SQL database consists of two tables, one called Users which stores users' login data and their unique ID number; the second table called BookList contains all the book-related data organized by unique book IDs. 

The html templates are all based on the main "layout.html" template which stores the CSS links as well as the navbar code and other basic page layout. A number of the html templates especially those producing tables and data results make use of "if/else" and "for" statements to achieve a flexible layout. 
The CSS was designed to achieve a clean yet visually interesting layout. To this end the :hover feature and the transform: translate3d function were used frequently. Some of the CSS code was based on the PaperCSS framework (https://www.getpapercss.com/) and on an adaptation of a public navbar code (https://codepen.io/pirrera/pen/zapbh).  

JavaScript was used only marginally to enable an as-you-type quick search and as such was incorporated directly into the layout.html template within a script tag.

BookLog was originally created in August 2020 as my [CS50](https://cs50.harvard.edu/x/2022/) final project.


You can view a  short demo at: https://youtu.be/mI0ESddbIiA

