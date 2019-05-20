from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
import json
#from django.http import HttpResponse
from . import models
from . import forms

EMAIL_HOST_USER = 'constprogrammer@gmail.com'


# This global variable stores the last page visited (not including the register,
# login, or logout pages). When you login or logout from a page, it should
# automatically redirect you to the previous page that you were on, in this
# case it is last_page_visited.
last_page_visited = '/'

# This global variable records the presense or absense of an error
# when filling in the comment_form
comment_form_error = False
# If comment_form_error is True, then this global variable stores the erroneous
# comment_form itself with all the wrong data.
bad_comment_form = None
# Similarly, if we have an error, then we also want to know the id and type
# of the response onto which the user tried to post an erroneous comment.
bad_response_id = None
bad_response_type = None


def home_page(request):
    global last_page_visited
    last_page_visited = '/'
    # Like a redirect, but no reloading upon redirect takes place.
    return articles_listing(request, 0)


def page_not_found(request):
    global last_page_visited
    # An exception: if you previously were on the "Page Not Found" page, and
    # you logged in, you would be automatically redirected to the home page.
    last_page_visited = '/'
    context = {
        "title": "Page Not Found"
    }
    return render(request, "not-found.html", context=context)


def not_found(request):
    global last_page_visited
    # An exception: if you previously were on an errors page, and
    # you logged in, you would be automatically redirected to the home page.
    last_page_visited = '/'
    context = {
        "title": "Page Not Found",
        "error_code": 404,
        "error_description": "Page Not Found"
    }
    return render(request, "errors.html", context=context)


def server_error(request):
    global last_page_visited
    # An exception: if you previously were on an errors page, and
    # you logged in, you would be automatically redirected to the home page.
    last_page_visited = '/'
    context = {
        "title": "Server Error",
        "error_code": 500,
        "error_description": "Server Error"
    }
    return render(request, "errors.html", context=context)


def permission_denied(request):
    global last_page_visited
    # An exception: if you previously were on an errors page, and
    # you logged in, you would be automatically redirected to the home page.
    last_page_visited = '/'
    context = {
        "title": "Permission Denied",
        "error_code": 403,
        "error_description": "Permission Denied"
    }
    return render(request, "errors.html", context=context)


def bad_request(request):
    global last_page_visited
    # An exception: if you previously were on an errors page, and
    # you logged in, you would be automatically redirected to the home page.
    last_page_visited = '/'
    context = {
        "title": "Bad Request",
        "error_code": 400,
        "error_description": "Bad Request"
    }
    return render(request, "errors.html", context=context)


# This view is intended to be used by the superuser only.
# It populates the database with dummy Article objects.
def bacon_ipsum(request):
    if request.user.is_authenticated and request.user.is_superuser:
        new_article = models.Article()
        new_article.article_title = "Garbage Text"
        new_article.article_link = 'whatever'
        new_article.preview_text = "Cheddar hard cheese the big cheese. Swiss fromage fondue cheesy feet queso when the cheese comes out everybody's happy rubber cheese cheese and wine. Cheddar chalk and cheese feta camembert de normandie goat airedale the big cheese brie. Smelly cheese roquefort cheese and biscuits fromage goat."
        new_article.save()

        new_article2 = models.Article()
        new_article2.article_title = "Garbage Text"
        new_article2.article_link = 'whatever'
        new_article2.preview_text = "Cheddar hard cheese the big cheese. Swiss fromage fondue cheesy feet queso when the cheese comes out everybody's happy rubber cheese cheese and wine. Cheddar chalk and cheese feta camembert de normandie goat airedale the big cheese brie. Smelly cheese roquefort cheese and biscuits fromage goat."
        new_article2.save()

        new_article3 = models.Article()
        new_article3.article_title = "Garbage Text"
        new_article3.article_link = 'whatever'
        new_article3.preview_text = "Cheddar hard cheese the big cheese. Swiss fromage fondue cheesy feet queso when the cheese comes out everybody's happy rubber cheese cheese and wine. Cheddar chalk and cheese feta camembert de normandie goat airedale the big cheese brie. Smelly cheese roquefort cheese and biscuits fromage goat."
        new_article3.save()

        new_article4 = models.Article()
        new_article4.article_title = "Garbage Text"
        new_article4.article_link = 'whatever'
        new_article4.preview_text = "Cheddar hard cheese the big cheese. Swiss fromage fondue cheesy feet queso when the cheese comes out everybody's happy rubber cheese cheese and wine. Cheddar chalk and cheese feta camembert de normandie goat airedale the big cheese brie. Smelly cheese roquefort cheese and biscuits fromage goat."
        new_article4.save()

        new_article5 = models.Article()
        new_article5.article_title = "Garbage Text"
        new_article5.article_link = 'whatever'
        new_article5.preview_text = "Cheddar hard cheese the big cheese. Swiss fromage fondue cheesy feet queso when the cheese comes out everybody's happy rubber cheese cheese and wine. Cheddar chalk and cheese feta camembert de normandie goat airedale the big cheese brie. Smelly cheese roquefort cheese and biscuits fromage goat."
        new_article5.save()

    return redirect('/not-found/')


# This is a simple "C-style struct" containing information about a page:
# - the page number
# - the link to that page,
# - a boolean, if this page is the current page we're on
class PageInfo:
    def __init__(self, number, link, this_page):
        self.number = number
        self.link = link
        self.this_page = this_page


def articles_listing(request, page):
    global last_page_visited
    last_page_visited = "/articles/" + str(page) + "/"
    # This is a list of all Articles in the database.
    articles_list = models.Article.objects.all()
    num_articles = len(articles_list)
    #num_articles = 32
    #page = 1
    # integer division - truncate remainder
    max_num_pages = num_articles // 10
    leftover_articles = num_articles % 10
    # Create a separate page for the leftover_articles
    if leftover_articles != 0:
        max_num_pages += 1
    last_page = max_num_pages - 1
    print("page: " + str(page));
    print("num_articles: " + str(num_articles));
    print("leftover_articles: " + str(leftover_articles));
    print("max_num_pages: " + str(max_num_pages));
    print("last_page: " + str(last_page));
    # If the user requested a page that is out of bounds.
    if page < 0 or page >= max_num_pages:
        return redirect('/not-found/')
    context = {
        "title": "Articles Page " + str(page),
        "page": page,
        "last_page": last_page,
        "articles_list": None,  # Empty until created in the code below.
        "pages_list": None      # Empty until created in the code below.
    }
    p_range = page * 10
    # If the current page is the last page.
    if page == last_page and leftover_articles > 0:
        context["articles_list"] = articles_list[p_range: p_range + leftover_articles]
    else:
        context["articles_list"] = articles_list[p_range: p_range + 10]

    starting_page = 0
    # If we have more than 5 total pages worth of articles.
    if max_num_pages >= 5:
        # Loop for only 5 pages.
        max_num_pages = 5
        # Calculate the starting page offset.
        if page <= 2:
            starting_page = 0
        elif page >= last_page - 2:
            starting_page = last_page - 4
        else:
            starting_page = page - 2

    pages_list = []
    i = 0
    while i < max_num_pages:
        i_page = starting_page + i
        if i_page == page:
            pages_list.append( PageInfo(str(i_page), "/articles/" + str(i_page),
            True) )
        else:
            pages_list.append( PageInfo(str(i_page), "/articles/" + str(i_page),
            False) )
        i += 1
    context["pages_list"] = pages_list

    #return redirect('/not-found/', context=context)
    return render(request, "articles.html", context=context)


# This function is called whenever the user posts a comment.
def add_comment(request):
    # "Extern" the global variables into this function.
    global comment_form_error
    global bad_comment_form
    global bad_response_id
    global bad_response_type
    # This function will only be called when a user submits the form to post a comment.
    # It is the action of the form submission.
    # This function should not be called explicitly, via a GET.
    #
    # This function was called by the form submission.
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.UserCommentForm(request.POST)
            if form_instance.is_valid():
                form_data = form_instance.cleaned_data
                # Add the form contents to the database.
                new_comment = models.UserComment()
                # Set the author of this new UserComment to the user
                # currently logged in.
                new_comment.comment_author = request.user
                # new_comment.comment_date is automatically set
                new_comment.comment_content = form_data["comment_content"]
                new_comment.comment_type = "user"

                parent_response_id = form_data["parent_response_id"]
                parent_response_type = form_data["parent_response_type"]
                if parent_response_type == "anon":
                    new_comment.anon_parent = True
                    # Get the parent response with the matching id.
                    parent_response = models.Response.objects.get(id=parent_response_id)
                    new_comment.anon_response = parent_response
                    new_comment.user_response = None  # None is NULL in Python
                elif parent_response_type == "user":
                    new_comment.anon_parent = False
                    # Get the parent response with the matching id.
                    parent_response = models.UserResponse.objects.get(id=parent_response_id)
                    new_comment.anon_response = None  # None is NULL in Python
                    new_comment.user_response = parent_response
                new_comment.save()

                comment_form_error = False
                bad_comment_form = None
                bad_response_id = None
                bad_response_type = None
            else:  # form_instance is not valid
                comment_form_error = True
                # I save the form_instance into the global variable, which I can
                # then give to the article() view function, to render out as
                # a template variable to the html page, displaying all the errors
                # and incorrect fields.
                bad_comment_form = form_instance
                form_data = form_instance.cleaned_data
                bad_response_id = form_data["parent_response_id"]
                bad_response_type = form_data["parent_response_type"]
        else:
            form_instance = forms.AnonCommentForm(request.POST)
            if form_instance.is_valid():
                form_data = form_instance.cleaned_data
                # Add the form contents to the database.
                new_comment = models.AnonComment()
                new_comment.author_name = form_data["author_name"]
                new_comment.author_email = form_data["author_email"]
                # new_comment.comment_date is automatically set
                new_comment.comment_content = form_data["comment_content"]
                new_comment.comment_type = "anon"

                parent_response_id = form_data["parent_response_id"]
                parent_response_type = form_data["parent_response_type"]
                if parent_response_type == "anon":
                    new_comment.anon_parent = True
                    # Get the parent response with the matching id.
                    parent_response = models.Response.objects.get(id=parent_response_id)
                    new_comment.anon_response = parent_response
                    new_comment.user_response = None  # None is NULL in Python
                elif parent_response_type == "user":
                    new_comment.anon_parent = False
                    # Get the parent response with the matching id.
                    parent_response = models.UserResponse.objects.get(id=parent_response_id)
                    new_comment.anon_response = None  # None is NULL in Python
                    new_comment.user_response = parent_response
                new_comment.save()

                comment_form_error = False
                bad_comment_form = None
                bad_response_id = None
                bad_response_type = None
            else:  # form_instance is not valid
                comment_form_error = True
                # I save the form_instance into the global variable, which I can
                # then give to the article() view function, to render out as
                # a template variable to the html page, displaying all the errors
                # and incorrect fields.
                bad_comment_form = form_instance
                form_data = form_instance.cleaned_data
                bad_response_id = form_data["parent_response_id"]
                bad_response_type = form_data["parent_response_type"]

        return redirect(last_page_visited)
    # This function was called explicitly by typing in the url.
    else:
        return redirect('/not-found/')


# This function returns a list of comments associated with a response.
# The response parameter can be either a Response or a UserResponse model object.
def get_comments(response):
    # Put the declarations of the list in the outermost scope.
    all_comments_list = []
    anon_comments_list = []
    user_comments_list = []
    if response.response_type == "user":
        anon_comments_list = models.AnonComment.objects.filter(user_response=response)
        user_comments_list = models.UserComment.objects.filter(user_response=response)
    elif response.response_type == "anon":
        anon_comments_list = models.AnonComment.objects.filter(anon_response=response)
        user_comments_list = models.UserComment.objects.filter(anon_response=response)

    num_anon_comments = len(anon_comments_list)
    num_user_comments = len(user_comments_list)
    i = 0
    j = 0

    while i < num_anon_comments and j < num_user_comments:
        if anon_comments_list[i].comment_date < user_comments_list[j].comment_date:
            all_comments_list.append(anon_comments_list[i])
            i += 1
        else:
            all_comments_list.append(user_comments_list[j])
            j += 1

    while i < num_anon_comments:
        all_comments_list.append(anon_comments_list[i])
        i += 1

    while j < num_user_comments:
        all_comments_list.append(user_comments_list[j])
        j += 1

    return all_comments_list


# This is a simple "C-style struct" containing a response, and the comments
# associated with it.
class ResponseWithComments:
    def __init__(self, response, my_comments):
        self.response = response
        self.my_comments = my_comments


# This function is called under two scenarios:
# 1. When the webpage is loaded initially with a GET request.
# 2. When data from the form is sent to the server with a POST request.
def article(request, article_url):
    # "Extern" the global variables into this function.
    global comment_form_error
    global bad_comment_form
    global bad_response_id
    global bad_response_type
    global last_page_visited
    last_page_visited = "/article/" + article_url + "/"
    # Get the target article
    target_article = models.Article.objects.get(article_link__exact=article_url)
    # Get the anonymous responses of that article.
    # Look at each response's parent_article, the id field has to be an exact match.
    responses_list = models.Response.objects.filter(parent_article__id=target_article.id)
    # Get the user responses of that article.
    # Look at each response's parent_article, the id field has to be an exact match.
    user_responses_list = models.UserResponse.objects.filter(parent_article__id=target_article.id)
    # The all_responses_list will be a list of ResponseWithComments objects.
    all_responses_list = []
    num_anon_responses = len(responses_list)
    num_user_responses = len(user_responses_list)
    i = 0
    j = 0

    # When I append a response to the responses_list, I also append it together
    # with it's comments, since they are considered as a single unit.
    # I bundle them together in a ResponseWithComments object.
    while i < num_anon_responses and j < num_user_responses:
        if responses_list[i].response_date < user_responses_list[j].response_date:
            all_responses_list.append( ResponseWithComments(responses_list[i],
            get_comments(responses_list[i])) )
            i += 1
        else:
            all_responses_list.append( ResponseWithComments(user_responses_list[j],
            get_comments(user_responses_list[j])) )
            j += 1

    while i < num_anon_responses:
        all_responses_list.append( ResponseWithComments(responses_list[i],
        get_comments(responses_list[i])) )
        i += 1

    while j < num_user_responses:
        all_responses_list.append( ResponseWithComments(user_responses_list[j],
        get_comments(user_responses_list[j])) )
        j += 1

    context = {
        "title": target_article.article_title,
        "target_article": target_article,
        "item_list": all_responses_list,
        "response_form": "",  # empty until created automatically in the code below
        "comment_form": "",  # empty until created automatically in the code below
        "bad_comment_form": None,  # None unless there a bad comment form exits.
        "comment_form_errors": False,
        "bad_response_id": None,
        "bad_response_type": None,
        "show_form": True,
        "user_prompt": "Add your response to my article"
    }

    # This code decides whether to send a UserCommentForm or an AnonCommentForm
    # to the template html page depending if the user is logged in or not.
    if request.user.is_authenticated:
        comment_form = forms.UserCommentForm()
        context["comment_form"] = comment_form
    else:
        comment_form = forms.AnonCommentForm()
        context["comment_form"] = comment_form

    # If this function was called upon a redirect from add_comment(),
    # and there were errors, then replace the new instance of the comment_form
    # with the bad_comment_form containing all the errors.
    # if comment_form_error is True, then bad_comment_form will necessarily
    # not be None, it will contain the bad data and errors.
    # if comment_form_errors is True, then the html template page will not hide
    # the comment_form on that response.
    if comment_form_error:
        context["comment_form_errors"] = True
        context["bad_comment_form"] = bad_comment_form
        context["bad_response_id"] = bad_response_id
        context["bad_response_type"] = bad_response_type
        # I don't want to get rid of the comment_form, since it could be useful
        # for adding comments to other responses as well.

    # This code is related to the user filling out the response forms.
    if request.user.is_authenticated:
        # When data from the form is sent to the server.
        if request.method == "POST":
            # This is the form_instance that is returned from the client to the
            # server, with the data already filled in.
            form_instance = forms.UserResponseForm(request.POST)
            context["response_form"] = form_instance
            if form_instance.is_valid():
                # This is a dictionary containing the names of the fields as keys
                # and the input data for that field as values.
                form_data = form_instance.cleaned_data

                # Add the form contents to the dataase.
                new_response = models.UserResponse()
                # Set the author of this new UserResponse to the user
                # currently logged in.
                new_response.response_author = request.user
                # new_response.response_date is automatically set
                new_response.response_content = form_data["response_content"]
                new_response.parent_article = target_article
                new_response.response_type = "user"
                new_response.save()
                all_responses_list.append( ResponseWithComments(new_response,
                get_comments(new_response)) )

                # If the user entered data into the form successfully, then the
                # form disappears; it is no longer needed.
                context["show_form"] = False
                context["user_prompt"] = "Your response was saved successfully."
            else:
                # if the user entered data into the form unsuccessfully (it failed
                # to be validated), then we still see the form with the user's
                # erroneous data so that they can fix it.
                context["show_form"] = True
                context["user_prompt"] = "Error: form input not valid"
        # When the webpage is loaded initially with a GET request.
        elif request.method == "GET":
            # This is the form instance which is sent from the server to the client
            # to be filled in by the user; a fresh unfilled form.
            form_instance = forms.UserResponseForm()
            context["response_form"] = form_instance
            context["show_form"] = True
            context["user_prompt"] = "Add your response to my article"
    else:
        # When data from the form is sent to the server.
        if request.method == "POST":
            # This is the form_instance that is returned from the client to the
            # server, with the data already filled in.
            form_instance = forms.ResponseForm(request.POST)
            context["response_form"] = form_instance
            if form_instance.is_valid():
                # This is a dictionary containing the names of the fields as keys
                # and the input data for that field as values.
                form_data = form_instance.cleaned_data

                # Add the form contents to the dataase.
                new_response = models.Response()
                new_response.author_name = form_data["author_name"]
                new_response.author_email = form_data["author_email"]
                # new_response.response_date is automatically set
                new_response.response_content = form_data["response_content"]
                new_response.parent_article = target_article
                new_response.response_type = "anon"
                new_response.save()
                all_responses_list.append( ResponseWithComments(new_response,
                get_comments(new_response)) )

                # If the user entered data into the form successfully, then the
                # form disappears; it is no longer needed.
                context["show_form"] = False
                context["user_prompt"] = "Your response was saved successfully."
            else:
                # if the user entered data into the form unsuccessfully (it failed
                # to be validated), then we still see the form with the user's
                # erroneous data so that they can fix it.
                context["show_form"] = True
                context["user_prompt"] = "Error: form input not valid"
        # When the webpage is loaded initially with a GET request.
        elif request.method == "GET":
            # This is the form instance which is sent from the server to the client
            # to be filled in by the user; a fresh unfilled form.
            form_instance = forms.ResponseForm()
            context["response_form"] = form_instance
            context["show_form"] = True
            context["user_prompt"] = "Add your response to my article"

    article_page = article_url + ".html"
    return render(request, article_page, context=context)


def register(request):
    # Neither register() not login() modify the last_page_visited,
    # which allows me to wormhole back to the page I was previously.
    if request.method == "POST":
        # Populate the RegistrationForm with data gotten from the user.
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        # Create a brand-new form.
        form_instance = forms.RegistrationForm()
    context = {
        "title": "Register",
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)


# This is an intermediate step to login, unsets global flags, then redirects
# you to the real login page.
def log_in(request):
    # "Extern" the global variables into this function.
    global comment_form_error
    global bad_comment_form
    global bad_response_id
    global bad_response_type
    # If the previous anonymous user set the error flags because they were
    # unable to fill out a comment_form correctly, these flags should be unset
    # upon login so that the next authenticated user does not see what
    # the previous anonymous user entered as invalid input for the form.
    comment_form_error = False
    bad_comment_form = None
    bad_response_id = None
    bad_response_type = None
    return redirect("/login/")


def logout_view(request):
    # "Extern" the global variables into this function.
    global comment_form_error
    global bad_comment_form
    global bad_response_id
    global bad_response_type
    # last_page_visited is not modified by this function, and therefore
    # it does not need to be "externed."
    logout(request)
    # If the previously logged in user set the error flags because they were
    # unable to fill out a comment_form correctly, these flags should be unset
    # upon logout so that the next user (or an anonymous user) does not see
    # what the previous user entered as invalid input for the form.
    comment_form_error = False
    bad_comment_form = None
    bad_response_id = None
    bad_response_type = None
    return redirect(last_page_visited)


# Whenever a user logs in, they will be redirected to the last_page_visited.
@login_required
def next_page(request):
    return redirect(last_page_visited)


def about_me(request):
    global last_page_visited
    last_page_visited = '/about-me/'
    context = {
        "title": "About this website"
    }
    return render(request, "about-me.html", context=context)


# I created a certain feature that no one else has.
# I want my website to have the ability to send email messages automatically.
# Any reader, in the "Contact Me" section of the website, can type in their
# message, and it will automatically send it to my email inbox.
# Also, if a user makes a response onto one of my articles, then it send me
# and email message telling me that.
# And if a user posts a comment onto another user's response, that user will
# get an email delivered to their inbox letting them know that.
#
# I wanted to use google's SMTP server for my purposes.
# But google's stupid AI detected me trying to send email messages
# programatically, so it disabled my email account!
#   It looks like this account was used to send unwanted content.
#   Spamming is a violation of Google’s policies.
def contact_me(request):
    global last_page_visited
    last_page_visited = '/contact-me/'
    context = {
        "title": "Contact Me",
        "show_form": True,
        "form": None,
        "user_prompt": "Send me an email."
    }
    if request.method == "POST":
        email_form = forms.EmailForm(request.POST)
        if email_form.is_valid():
            send_mail(
                str(email_form["sender_name"]) + "Sent you an email",
                str(email_form["sender_name"]) + "Sent you an email. " +
                "Their email address is: " + str(email_form["sender_email"]) +
                "They wrote: " + str(email_form["email_text"]),
                str(email_form["sender_email"]),
                [EMAIL_HOST_USER],
                fail_silently=False
            )
            context["show_form"] = False
            context["form"] = None
            context["user_prompt"] = "Thank you. Your message was sent successfully."
        else:
            # Form was not valid, display the bad input to the user.
            context["show_form"] = True
            context["form"] = email_form
            context["user_prompt"] = "Error: form input not valid"
    else:
        # Clean new email_form.
        email_form = forms.EmailForm()
        context["show_form"] = True
        context["form"] = email_form
        context["user_prompt"] = "Send me an email."
    return render(request, "contact-me.html", context=context)


@login_required(login_url="/login/")
def programmer_chat(request):
    global last_page_visited
    last_page_visited = '/programmer-chat/'
    # This is a list of all ChatInstance objects in the database.
    chat_instances = models.ChatInstance.objects.all()
    context = {
        "title": "Programmer Chat",
        "chat_instances": chat_instances
    }
    return render(request, "chat/programmer_chat.html", context=context)


@login_required(login_url="/login/")
def room_demo(request):
    global last_page_visited
    last_page_visited = '/room-demo/'
    context = {
        "title": "Chat Room Demo"
    }
    return render(request, "chat/room_demo.html", context=context)


@login_required(login_url="/login/")
def room(request, room_name):
    global last_page_visited
    last_page_visited = '/programmer-chat/'

    chat_instance = None
    chat_posts_list = None

    # Get the ChatInstance object corresponding to that room, if it exists.
    # If it already exists, then I'm joining an already existing chat room.
    # If it doesn't exist, then I'm starting a new chat room.
    try:
        chat_instance = models.ChatInstance.objects.get(chat_name=room_name)
        # Return a list of all chat posts attached to that chat_instance.
        # If there are no ChatPosts, then filter will return an empty queryset.
        chat_posts_list = models.ChatPost.objects.filter(chat_instance=chat_instance)
    except models.ChatInstance.DoesNotExist:
        chat_instance = None
        chat_posts_list = None

    context = {
        "title": "Programmer Chat",
        "room_name_json": mark_safe(json.dumps(room_name)),
        "chat_posts_list": chat_posts_list
    }
    return render(request, 'chat/room.html', context=context)


# This view is for looking at all the past chat sessions and their chat posts.
# If user is not authenticated, or you're not the super user (admin),
# you are redirected to page-not-found. Only I can open this view.
def chat_history(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # This is a list of all ChatInstance objects in the database.
        chat_instances = models.ChatInstance.objects.all()
        num_instances = len(chat_instances)
        # This is a list of ChatInstances and ChatPosts attached to them.
        complete_chats_list = []
        i = 0
        while i < num_instances:
            # Resuse the ResponseWithCommentsObject to hold a ChatInstance,
            # and it's respective ChatPosts, why not?
            complete_chats_list.append( ResponseWithComments(chat_instances[i],
            models.ChatPost.objects.filter(chat_instance=chat_instances[i])) )
            i += 1
        context = {
            "title": "View Chat History",
            "complete_chats_list": complete_chats_list
        }
        return render(request, 'chat/view_chat_history.html', context=context)
    else:
        return redirect('/not-found/')
