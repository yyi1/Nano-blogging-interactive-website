from django.conf.urls import include, url

import django.contrib.auth.views
import grumblr.views

urlpatterns = [
    url(r'^$', grumblr.views.home, name='home'),
    url(r'^get_json_post', grumblr.views.get_json_post, name='testpost'),
    url(r'^get_json_comment', grumblr.views.get_json_comment, name='testcomment'),

    url(r'^get_post', grumblr.views.get_post, name='getpost'),

    url(r'^add-post', grumblr.views.add_post, name='addpost'),
    url(r'^add-comment/(?P<id>\d+)$', grumblr.views.add_comment, name='comment'),
    url(r'^photo/(?P<id>\d+)$', grumblr.views.get_photo, name='photo'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', django.contrib.auth.views.login, {'template_name': 'login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^password$', grumblr.views.password, name='password'),
    url(r'^confirm/(?P<username>.*)/(?P<token>.*)$', grumblr.views.confirm_registration, name='confirm'),
    url(r'^profile/(?P<id>\d+)$', grumblr.views.profile, name='profile'),
    url(r'^get_profile_post/(?P<id>\d+)$', grumblr.views.get_profile_post, name='profile_post'),
    url(r'^get_follower_post/(?P<id>\d+)$', grumblr.views.get_follower_post, name='profile_post'),
    url(r'^profile/edit-profile/(?P<id>\d+)$', grumblr.views.edit_profile, name='edit'),
    url(r'^follow/(?P<id>\d+)$', grumblr.views.relationship, name='follow'),
    url(r'^follow/edit-follow/(?P<id>\d+)$', grumblr.views.edit_relationship, name='edit_follow'),

    url(r'^globalStream$', grumblr.views.home),
]
