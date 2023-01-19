# WIUT's Key Registration App
#### Video Demo:  <URL HERE>
#### Description:
    A simplistic key registration app created to minimize the time spent by students to register keys.
    Previously students would write when they took or returned keys in a paper notebook.
    However, with this app students can scan a QR-code and fill in the registration form to register 
    a key via their smartphones.
    The information about the keys and students is then stored in a database and can be retrieved 
    and displayed on a web page. A web page makes it easier to track the status of the keys and provides
    more detailed information on the history, which helps to track them and makes them easier to find.
    
    The first page is the keys.html, where the status of the keys and additional information such as who
    and when took or returned the keys can be seen. The data is represented in a table, where a green circle under the "Status" section indicates that the key is available and the time shown is the time the key was returned, whereas a red circle indicates that the key is unavailable and the time taken is shown under the "Time" section.

    The second page is the register.html, where students need to fill in a form to register. After successfully registering the user is then redirected to the keys.html page, where the user will be able to observe the data they have entered. SQL queries are used to log the data into the key.db database.
    Regarding the style of the html pages, the Bootstrap framework has been used to style them.
    