/**
 * Created by yiyin on 23/10/2016.
 */
$(document).ready(function () {

    if ($("#all-posts").length) {

        getUpdates();
        //refresh every 5 seconds
        window.setInterval(getUpdates, 5000);
    } else if ($("#profile-posts").length) {
        getProfilePosts();
    } else if ($("#follower-posts").length) {
        getFollowerPosts();
    }
    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});


function getUpdates() {
    $.get("/grumblr/get_post")
        .done(function (data) {
            var list = $("#all-posts");
            for (var i = 0; i < data.posts.length; i++) {
                var post = data.posts[i];
                // if this is a new post
                if (!$("#post-" + post.id).length) {
                    list.prepend(createPostHtml(post));
                    // Add event-handlers
                    $("#commentForm-" + post.id).click(createComment);
                }
            }
        });
}


function getProfilePosts() {
    $.get("/grumblr/get_profile_post/" + $("#profile-id").val().trim())
        .done(function (data) {
            var list = $("#profile-posts");
            for (var i = 0; i < data.posts.length; i++) {
                var post = data.posts[i];
                // if this is a new post
                if (!$("#post-" + post.id).length) {
                    list.prepend(createPostHtml(post));
                    // Add event-handlers
                    $("#commentForm-" + post.id).click(createComment);
                }
            }
        });
}


function getFollowerPosts() {
    $.get("/grumblr/get_follower_post/" + $("#user-id").val().trim())
        .done(function (data) {
            var list = $("#follower-posts");
            for (var i = 0; i < data.posts.length; i++) {
                var post = data.posts[i];
                // if this is a new post
                if (!$("#post-" + post.id).length) {
                    list.prepend(createPostHtml(post));
                    // Add event-handlers
                    $("#commentForm-" + post.id).click(createComment);
                }
            }
        });
}


function createComment() {
    var button = $(this);
    var post_id = button.attr("id").split("-")[1];
    var content = button.parent().find('input:first').val();
    $.post("/grumblr/add-comment/" + post_id, {post: content})
        .done(function (data) {
                if ($("#all-posts").length) {
                    $("#all-posts").html("");
                    getUpdates();
                } else if ($("#profile-posts").length) {
                    $("#profile-posts").html("");
                    getProfilePosts();
                } else if ($("#follower-posts").length) {
                    $("#follower-posts").html("");
                    getFollowerPosts();
                }

            }
        );
}


function createPostHtml(post) {
    var htmlres = '<div class="panel panel-success">' +
        '<div class="panel-heading"><h5>Post by <a href="' + post.profile + '">' + post.username + '</a>, ' + post.time + '</h5></div>' +
        '<div class="panel-body"><div id="post-' + post.id + '" class="col-lg-2">' +
        '<img src="' + post.photo + '" alt="' + post.username + '" width="70"></div><p>' + post.text + '</p></div>';
    // for comment in comments:
    // +=createCommentHTML
    for (var i = 0; i < post.comments.length; i++) {
        var comment = post.comments[i];
        htmlres += createCommentHtml(comment);
    }
    htmlres += createForm(post);
    htmlres += '</div>';
    return htmlres;
}


function createCommentHtml(comment) {
    var commentResult = '<div class="well"><div id="comment-' + comment.id + '" class="col-lg-2">' +
        '<img src="' + comment.photo + '" alt="' + comment.username + '" width="70"></div>' +
        '<h5>Comment by <a href="' + comment.profile + '">' + comment.username + '</a>, ' + comment.time + '</h5>' +
        '<p>' + comment.text + '</p></div>';
    return commentResult;
}

function createForm(post) {
    var formResult = commentForm;
    formResult = '<hr><div class="well-sm text-center">' + formResult + '<input id="commentForm-' + post.id +
        '" class="btn btn-sm btn-primary" type="submit" value="Comment"></input></div><hr>';
    return formResult;
}

