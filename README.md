**************************
   Welcome to Grumblr!
**************************


The website has been deployed to:

    https://vast-refuge-25388.herokuapp.com/


Summary:

    This site is a featureful, interactive web application based on Django Framework and Twitter Bootstrap 
    CSS framework. Including user registration and authentication, email integration for user verification, 
    photo upload, quasi-real-time updates, the ability to edit and enrich your profile, follow other users, 
    upload images, and comment on posts.


Functions:

    ● Non-logged-in users may register for the site. Registering users must provide user name, first name, 
    last name, and password. Registering for the site leaves the user logged in as the newly registered user.
    ● Registered users may log in using their username and password.
    ● Logged-in users are able to post a short (42 characters or less) message. Posts, when displayed, show 
    the following information:
          ○ the contents of the post,
          ○ the user who posted it (linking to the user’s profile), and
          ○ the date and time the post was written.
    ● Logged-in users may view a 'global stream', displaying all posts that have been posted in reverse-chronological 
    order (most recent first).
    ● Logged-in users may view profiles of other users (or their own profiles) when clicking on links provided with 
    posted messages in the global stream. Profile pages contain information about a user (e.g. first name and last name) 
    as well as all of the posts that user has made, in reverse-chronological order.
    ● Logged-in users are able to log out.
    ● Profiles for logged-in users should include at least the following information:
          ○ first name
          ○ last name
          ○ age
          ○ short bio (420 characters or less)
    ● Logged-in users can edit their profile information and change their password.
    ● Logged-in users can upload a profile image, which is displayed on their profile page and next to their posts as a 
    small image. The image upload form should be located on the profile-editing page.
    ● Logged-in users may choose to ‘follow’ and ‘unfollow’ another user.
    ● Logged-in users may view a ‘follower stream’, displaying all posts from the users that the current user is following 
    (in reverse-chronological order).
    ● New users must register with, and confirm, their e-mail address.
    ● Users can reset their password by a link sent to their registered e-mail address.
    ● The global stream page should be updated with any new posts every five seconds, without refreshing the HTML page.
    ● A logged-in user should be able to add comments to posts anywhere posts are shown to the logged-in user.
          ○ Comments show the author, the profile image, and the time the comment was made.
          ○ Comments should be displayed in chronological order on each post, with the bottom comment being 
    the newest comment on that post.
          ○ It should be clear in your grumblr design which comments belong to which posts.
          ○ Adding a new comment should not require refreshing the entire HTML page.
    ● Deployed to Heroku with data stored on AWS S3


Website map:

1. A login page; displays a form to the user requesting username and password, linking to the registration page if the user wants to register instead.

2. A registration page; displays a form requesting a username, first name, last name, and password (with a password confirmation field).

3. A global stream page; lists posts from all users.

4. A profile page for a user; shows information about a user as well as all posts from that user.

