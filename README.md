# Running the Application:
1. Run <code>python3 create_db.py</code> in the root directory
2. Run <code>python3 manage.py migrate</code>
3. Now you can start the app with <code>python3 manage.py runserver</code>

The python script will create the database with 2 premade users:
- **Username**: bob  - **Password**: passwd  _(Not admin)_
- **Username**: admin  - **Password**: coffee  _(Admin)_


# The Flaws In the Application
The flaws are based on the OWASP 2017 top 10 flaws list:
https://owasp.org/www-project-top-ten/2017/

## FLAW 1: Broken Authentication

https://github.com/kuroniil/titupe-projekti/blob/61dea7425136c5f2f814228436e376b45555af4a/src/pages/views.py#L33

The first flaw is broken authentication. Applications that allow users to register with weak, well-known and overused passwords are vulnerable to this flaw. This application allows registration with any password (and no password at all), which makes it vulnerable. Weak passwords make the users account vulnerable to brute force attacks. Also overused passwords are very weak since an attacker can automate login attempts with a list of known passwords.

The solution to fix this flaw in the application is commented out in the same ```registerView``` function linked above. In the variable ```overused_passwords``` is a list of overused and default passwords. This would be one criterion the users password would have to fulfill to register successfully. The if-clause also involves checking the users desired password is long enough, and that it doesn't consist of just characters a-z. More requirements could be added easily, such as that the password must contain numbers to require a stronger password. The application would not add the user and password to the database otherwise and would redirect the user to a page explaining what went wrong.

## FLAW 2: Injection

https://github.com/kuroniil/titupe-projekti/blob/61dea7425136c5f2f814228436e376b45555af4a/src/pages/views.py#L97

The second flaw is SQL-injection vulnerability. The application has a feature that allows the user to look for a specific note they have added in the past. The application queries the database to look for notes based on the users input. The user input is not handled properly, which allows the user to query the database for much more than just their own notes, if they know what they are doing. For example, this can be used as input to get default user bob's password as search results: ```öö"%' UNION SELECT password FROM Users WHERE username = 'bob' OR username LIKE '%"```

The solution to fix the flaw in the application is to handle the user input properly. When done correctly, the same functionality can be provided for the user without the vulnerability. The fix is commented out on line 100 of the same document. The fix concatenates the %-signs on each side of the user-inputted search term. This makes it so that the query will always look for a note that includes the user-inputted string. With the fix enabled the user is not able to inject any SQL since the input is handled as a string that is looked for within the notes table.

## FLAW 3: Cross-Site Scripting (XSS)

https://github.com/kuroniil/titupe-projekti/blob/61dea7425136c5f2f814228436e376b45555af4a/src/pages/templates/pages/notes.html#L19

The third flaw is Cross-Site Scripting. The application has a feature that allows users to add a note/message that is displayed to all users. The note displayed in the template has the safe template filter which allows the users to, for example make better notes with headers. It also allows the user to execute javascript on other users browsers with the HTML script tag. A user in the application is allowed to post a script that, for example, steals the sessionid cookie of another user and sends it to their own server. The code is executed when another user opens the notes pages of the application, which has the public notes/messages.

The fix to this flaw is commented out on line 20. The fix is removing the 'safe' template filter from the template. Django templates escape HTML automatically. Thus, after removing the safe-filter, user-inputted HTML read within the template is escaped. This fix makes it so that when public note/message with a script is posted, the script message is displayed as a string on the page, rather than executing in the browser of the user opening their notes page.

## FLAW 4: Broken Access Control

https://github.com/kuroniil/titupe-projekti/blob/61dea7425136c5f2f814228436e376b45555af4a/src/pages/views.py#L108

The fourth flaw is Broken access control. The application has a page for admins in which the admins can view users notes and delete them. The flaw is that anyone can access the admin page just by typing in the url '/adminpage'. This makes it so that users with no admin rights can do what only admins are supposed to be able to do. This flaw induces a security risk since everyone's notes can be viewed by anyone who knows to type in the adminpage url, even though the notes are supposed to be private.

The fix for this flaw start at where the link points to. It includes a function that checks if a given user is an admin by querying the database with the given username. This function is then implemented to ```adminView``` and ```deleteView``` functions to check if the user making the request is an admin and acting accordingly. If a user is an admin they are let on the page and allowed to make deletions. If they are not an admin, they are directed to a page with a message of access denied. Because the application does not allow users to make admin accounts, the only way to make one is by manually inputting into the database.

## FLAW 5: Cross-site Request Forgery (CSRF)

https://github.com/kuroniil/titupe-projekti/blob/61dea7425136c5f2f814228436e376b45555af4a/src/config/settings.py#L47

The fifth flaw is Cross-site Request Forgery. The Django's CSRF-middleware is disabled in the application by commenting out in ```settings.py``` as seen in the link. This flaw in the application would allow an attacker to make requests on behalf of the victim. For example if the victim was an admin, the attacker could make requests to delete users very important notes.

This flaw can be fixed by enabling Django's CSRF-middleware (behind the link) and adding the CSRF-tokens to all forms (commented out on each form). When the middleware is enabled, each request must include a CSRF-token, which is then validated. If the request does not contain a correct CSRF-token, the user will receive an error from Django. This fix, which is enabled by default on Django fixes the vulnerability.
