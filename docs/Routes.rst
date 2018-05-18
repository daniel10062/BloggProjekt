Routes
======

.. autoflask:: app:create_app('default')

Default route
-------------
**Highlighted lines show methods and imports of forms
that are very specific for this type of route**

.. literalinclude:: ../app/main/views.py
   :language: python
   :lines: 21-39
   :emphasize-lines: 1, 5-6
   :linenos:

Explore route
-------------
**On this route users can find other
registered users to then go on there page**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 43-54
  :emphasize-lines: 1
  :linenos:

*The line highlighted shows a decorater called*
**@login_required** *and forces the user to be logged in
to access this route*

Update route
-------------
**This route is not accessable from a users perspective because all it does
is to check wheather the checkbox field has been checked and then filter the returning True
away from the list**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 56-67
  :emphasize-lines: 7-10
  :linenos:

*Highlighted lines show the process to delete a post with valid checkbox value*

User route
-------------
**This route transfers a user to its own unic user site**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 70-81
  :emphasize-lines: 1
  :linenos:

*Keep in mind that username is used in the location specifier to create the "unique" site*

Follow route
-------------
**The following route is a hidden route for the user and makes a follow function possible**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 83-96
  :emphasize-lines: 11,12
  :linenos:

*The highlighted lines is showing how we access the* **User** *model and how the to commit the result.*

Unfollow route
--------------
**This route is doing the same as the route shown above except it unfollows a user instead of follows it**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 98-111
  :linenos:

Login route
-------------
**The login route is a important route because it checks wheather a user is valid or not and actually lets the user access the main site**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 113-129
  :emphasize-lines: 11, 12, 17
  :linenos:

*The highlighted lines shows how the checking process for both username and password goes. First the user object tries to get the user with the given username from the database.*
*If the username was a valid and registered username in the database we then check if the given password matches the users* **hash_password.**

**After the user is valid we then redirect the user to main.index which in this case is the main site (line 17)**

Profile edit route
------------------
**This route allows the user to make small adjustments on the users username, email and bio.**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 131-145
  :linenos:

Logout route
-------------
**The logout route is very simple and just calls the logout_user() function from flask-login**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 147-150
  :emphasize-lines: 3
  :linenos:

Register route
--------------
**The register route just commits the data from the from to the database**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 152-164
  :emphasize-lines: 7-9
  :linenos:

Space_invaders route
--------------------
**On the Space invaders route a clever trick to make a website window inside a website window is used called iFrame.**

.. literalinclude:: ../app/main/views.py
  :language: python
  :lines: 166-174
  :emphasize-lines: 3,4
  :linenos:
