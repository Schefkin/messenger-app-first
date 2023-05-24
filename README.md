# messenger-app-first

## App.py
app.py contains main part of the code,
at start I import all the libraries that I used for this project.
Then I start a flask session and import tables.db database.

### index page ("/")
First route I made is the index page "/"
It requires to be logged in to acces this page
The purpose of the page is just to show you a simple form that asks you to add friends when opened.
What index does is check if the request method is POST or GET.
If the method turned out to be POST it checks what the user has typed into the form then it checks if the name that the user typed is already in the database.
If the name doesnt exist it reloads the page. If the name exists in the database
the program proceeds to get the list of all friends that the current user has. If the name
that was typed in the form already is in his friend list it just reloads the page.
If the name doesnt exist in his friend list it adds the name to the persons friendlist.
And the user adds himself in the friendlist of the person he juist added so they both
can see eachother. Then it just returns the index page.

If the moethod turned out to be get it just gives user the index.html page.

### friends page ("/friends")
What friends function does is at first get the list of all the friends current user has.
If the method is POST it selects the friend on which name the user pressed and redirects user to the messages page while storing the friends name in the session variable for convenience, because then the messages page gets all the messages based on that session variable.

If the request method is GET then just display the friends page.

### messages page ("/messages")
First thing the function does is get the friend name from the session variable that aI stored when I clicked on the friend name on the friends page. Then it proceeds to get the message that was submitted via the form on the page. After that it selects all the previous messages that I had with the person I chose to speak with.

If the request method is POST then it submits the form (only if something was typed in the form) and then inserts the message into the messages table alongside with current time, recipient and sender and then returns all the messages that are in the messages table.

If the request method is GET then it just loads all the messages on the messages page (if there are even any).

### register page ("/register")

If the request method is POST then it checks if the username already exists or not and
if the check password is the same as the first password that was typed in. If all the checks are passed it iserts a new account into the users table with their id, name and hashed password.

If request method is GET then it just loads the register page.

### login page ("/login")

at first it clears the session from any cookies
 If method is post it checks if everything was typed in correctly, if was the program continues.
 If username didnt match any name in the database it reloads the page. And if the password is incorrect it also relaods the page. If all checks are passed it creates a new session variable to remember who was loggen in and then redirects the user to the index page.

 If method is get it shows user the login form.

 ### logout button
 If the log out button is pressed on the navigation bar it forgets all the session cookies and redirects user to the login page.

 ## table.db
 This is a database.
 I used it to store the users, friends and messages tables.
 When deciding on the messages table I had a choice between different implementation methods. First was to create one table where all messages are stored that are connected to the reciever
 and sender by their ids and then the message itself but then I realized it wouldnt be the best way to implement the table because it would be too big of a mess to start selecting users by their id's instead of their names. And also I thought that I would insert time manually iontop this table which also was a bad design choice.

 Second design was that I create two different tables one for recieved messages and the othe one for sent messages. But I realized that it would be too hard to run python commands on two different tables and thed order them by time.

 My third and final table looked something like this. It had reciever, sender, message and time columns where I could insert info. The id and time column would not have to be inserted into manually but they would do everything by themselves which was the best design choice so for in my opinion because it saves time and it's easier to manage all the messages when they are stored inside only one table and also time increases automaically which is really convenient because then I could sort by time column to select my messages which is again very convenient.
 And thats why I went with this design choice.

 ## scroll_down.js
 I actually wrote very little java script and the only code I wrote is to scroll to bottom of the container in the messages page. Because it wouldnt be logical if every time you open your messages you start from the first message that you ever sent.

 ## styles.css
 It's just a css file containing all the styling choices I made so I could design my site to be more beautiful.

 It also contains some conditions for people who are using phones so the site would be formatted according to their screen. I added it because I thought it wouldnt be convenient for users with different or smaller screens than mine.

 Also styles.css includes syle for the brand on the navbar which is set to xx-large so it would look like legitimate logo.

 ## friends.html
 It extends the layout page. The page shows you a list of your friends as clickable buttons so these buttons can redirect you to the messages page. Login is requiered.

 ## index.html
 This is the main page, login is requiered to access this page.
 This page shows user a form where they can search for people that are registered in the database.
 After the from is submitted it returns a message to the back end.

 ## layout.html
 This is the layout for all the pages that I created.
 It includes meta tags for people with phones so the site will be resized according to that.
 It includes bopotstrap tags so I can use the navbar on my website.
 It has a jinja syntax expanding in the title sectrion so I could choose different titles for my pages. As the body part it includes the navbar if the user is logged in the navbar will show user menu with logo, friends, messages and log out buttons. And if the user is not logged in it shows him navbar with logo, register and log in buttons.
 Logo button just redirects user to the main page. Friends button redirects him to his friend list page. Messages redirects user to messages page. Log out buttonb logs out the user.
 Register button redirects user to register page and login redirects user to log in page.
 Then as the main part of the page it extends jinja syntax so I could write code inside other pages.

 ## login.html
 shows the user the login form with input box and a button.

 ## messages.html
 checks if a friend button was pressed on the friends page using jinja.
 If it returns true then it prints out all the messages the two users have between them.
 If it returns fale it shows some text indicating the user to click on a friend to select a conversation to open. It has a text field abouve that sais with whom is the person talking right now. It has a box where all the messages are displayed. And it has the input form that submits the typed in message to the back-end.
 Also it imports the javasrcipt that I meantioned so the box would feel more "natural" on the page.

 # register .html
 It loads the register page that has a form on it.
 It has three fields username, password and password(again).
 The form submits all the answers to thje backend so it can choose what to do next with the user.
