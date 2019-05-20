from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    tag_name = models.CharField(max_length = 40, unique = True, blank = True)

    class Meta:
        ordering = ['tag_name']

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # The name of the author.
    author_name = models.CharField(max_length = 32, default = 'Konstantin Rebrov')
    # The title of the article.
    article_title = models.CharField(max_length = 100, default = '')
    # The date when this article was created.
    # auto_now automatically sets the field to now every time the object
    # is saved.
    article_date = models.DateField(auto_now_add=True)
    # A link to the html page of that article.
    # Specifying the article contents as an html page rather than a text field
    # allows me to embed images, links, canvas animations, and other html
    # elements directly into the article
    article_link = models.SlugField()
    # The preview text is the first 400 characters of the article.
    # It appears in the preview of an article, in the list of articles.
    preview_text = models.TextField(max_length=400, default='')
    # The number of views.
    article_views = models.IntegerField(default = '0')
    # The number of likes.
    article_likes = models.IntegerField(default = '0')
    # The tags of the article, which is a many to many foreign key.
    #tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['article_date']

    # This is used for returning a string description of the Article for the
    # admin interface.
    def __str__(self):
        return self.article_title


# This is an "anonymous" Response
class Response(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # Because there is no user associated with an anonymous response, we have
    # to have the name and email address of the author in the model.
    #
    # The name of the author.
    author_name = models.CharField(max_length=32)
    # The author's email address.
    author_email = models.EmailField(max_length=254)
    # The date and time when this response was made.
    response_date = models.DateTimeField(auto_now_add=True)
    # The text content of the response.
    response_content = models.TextField(max_length=4000)
    # This is the article to which the response is attached.
    parent_article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    # This is the type of the response, always equal to "anon" here.
    response_type = models.CharField(max_length=4, default="anon")

    class Meta:
        ordering = ['response_date']

    # This is used for returning a string description of the Response for the
    # admin interface.
    def __str__(self):
        return ("A " + str(self.id) + " " + self.author_name + " | " +
        self.response_content[:50] + "...")


# This is a user's response
class UserResponse(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # The author of this response is a User.
    response_author = models.ForeignKey(User, on_delete=models.CASCADE)
    # The date and time when this response was made.
    response_date = models.DateTimeField(auto_now_add=True)
    # The text content of the response.
    response_content = models.TextField(max_length=4000)
    # This is the article to which the response is attached.
    parent_article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    # This is the type of the response, always equal to "user" here.
    response_type = models.CharField(max_length=4, default="user")

    class Meta:
        ordering = ['response_date']

    # This is used for returning a string description of the UserResponse for
    # the admin interface.
    def __str__(self):
        return ("U " + str(self.id) + " " + self.response_author.first_name +
        " " + self.response_author.last_name + " (" +
         self.response_author.username + ") | " + self.response_content[:50] +
          "...")


# This is an "anonymous" comment
class AnonComment(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # The name of the author.
    author_name = models.CharField(max_length=32)
    # The author's email address.
    author_email = models.EmailField(max_length=254)
    # The date and time when this comment was made.
    comment_date = models.DateTimeField(auto_now_add=True)
    # The text content of the comment.
    comment_content = models.TextField(max_length=4000)
    # Each comment may be attached to either a Response or a UserResponse.
    # The combination of blank=True, null=True is what allows a ForeignKey
    # field to be optional. It is optional because if the current comment
    # "is pointing to" a UserResponse, then it should not point to a Response.
    anon_response = models.ForeignKey(Response, on_delete=models.CASCADE, null=True, blank=True)
    user_response = models.ForeignKey(UserResponse, on_delete=models.CASCADE, null=True, blank=True)
    # True if the parent response is a Response (anonymous response),
    # False if the parent response is a UserResponse.
    anon_parent = models.BooleanField()
    # This is the type of the comment, always equal to "anon" here.
    comment_type = models.CharField(max_length=4, default="anon")

    class Meta:
        ordering = ['comment_date']

    # This is used for returning a string description of the AnonComment for the
    # admin interface.
    def __str__(self):
        return ("A " + str(self.id) + " " + self.author_name + " | " +
        self.comment_content[:50] + "...")


class UserComment(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # The author of this comment is a User.
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    # The date and time when this comment was made.
    comment_date = models.DateTimeField(auto_now_add=True)
    # The text content of the comment.
    comment_content = models.TextField(max_length=4000)
    # Each comment may be attached to either a Response or a UserResponse.
    # The combination of blank=True, null=True is what allows a ForeignKey
    # field to be optional. It is optional because if the current comment
    # "is pointing to" a UserResponse, then it should not point to a Response.
    anon_response = models.ForeignKey(Response, on_delete=models.CASCADE, null=True, blank=True)
    user_response = models.ForeignKey(UserResponse, on_delete=models.CASCADE, null=True, blank=True)
    # True if the parent response is a Response (anonymous response),
    # False if the parent response is a UserResponse.
    anon_parent = models.BooleanField()
    # This is the type of the comment, always equal to "user" here.
    comment_type = models.CharField(max_length=4, default="user")

    class Meta:
        ordering = ['comment_date']

    # This is used for returning a string description of the UserResponse for
    # the admin interface.
    def __str__(self):
        return ("U " + str(self.id) + " " + self.comment_author.first_name +
        " " + self.comment_author.last_name + " (" +
        self.comment_author.username + ") | " + self.comment_content[:50] +
         "...")


class ChatInstance(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # Make chat_name unique, you can't have more than one ChatInstance with the same name.
    chat_name = models.CharField(max_length=32, unique=True)
    # The date and time when this chat instance was made.
    chat_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chat_date']

    # This is used for returning a string description of the ChatInstance for
    # the admin interface.
    def __str__(self):
        return (str(self.id) + " " + self.chat_name + " " + str(self.chat_date))


class ChatPost(models.Model):
    # Default field options: (null=False, blank=False)
    # By default, Django gives each model the following field:
    # id = models.AutoField(primary_key=True)
    #
    # The name of the author.
    author_name = models.CharField(max_length=45)
    # The date and time when this chat post was made.
    chat_date = models.DateTimeField(auto_now_add=True)
    # The text content of the chat.
    chat_content = models.TextField(max_length=4000)
    # This is the ChatInstance, to which this ChatPost belongs.
    chat_instance = models.ForeignKey(ChatInstance, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['chat_date']

    # This is used for returning a string description of the ChatPost for
    # the admin interface.
    def __str__(self):
        return (str(self.id) + " " + self.author_name + " " + str(self.chat_date) +
        '|' + self.comment_content[:50])


#my

