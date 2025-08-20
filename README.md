Login and Registering Users with Authentication.
In order to have users who can contribute to the website and
Associate data to user account,
We need a way to register them and allow them to sign back into their accounts at a later date.
Figure out how to register, login and logout users.
1-Backgtound-color
linear-gradient(to right, rgba(75, 0, 130, 0), rgba(75, 0, 130, 1))
2-Secure the user's password by hashing it before storing it,
So I used the Werkzeug helper function generate_password_hash().
3-To make sure that only registered users can see the secret page:
We'll need to secure certain routes in our server,
and make them accessible if a user is authenticated.
Let's use Flask-login package.
4-from Flask import flash ,send_from_directory,
*Flask Flash messages. They are messages that are sent to the template to be rendered just once
*send_from_directory. Send a file from within a directory
send_from_directory(directory, path, **kwargs)
