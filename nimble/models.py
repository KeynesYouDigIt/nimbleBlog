'''models.py represents the fairly standard blogging database schema, 
upon which Nimble blg is built.

Originaly written in SQL Alchemy, 
and rebuilt for the Google app engine datastore.

All functionality is derived from User, Post, and Tag objects.

Likes are a list of Users on Posts, Tags contain a list of Posts, etc.

One quirk to note is that comments are Posts listed in Posts. A field in each
Post instance stores whether or not a post is considered a comment. 

The advantage is a simplified database model and the inherent possibilty to 
expand features to both comments and posts, with the caveat being that posts and
comments are not in different tables and must be distinguished in the code only
by the _is_comment field.

'''

from google.appengine.ext import db

import hashlib

class User(db.Model):
    """This model allows user storage.

    username is a username, must be provided and unique

    email is email, does not have to be unique

    posts stores posts by the user

    password_hash is the encrypted storage of the user password
    """
    username = db.StringProperty(required = True)
    email = db.StringProperty()
    password_hash = db.StringProperty(required = True)

    @property
    def id(self):
        # set id for direct retrieval
        self.key().id()

    def to_dict(self):
        # create a dictionary with instance properties
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

    def check_password(self, password_provided):
        '''Returns a boolean of whether a provided password can be hashed and 
        match the stored password hash, thus checking if passwords match without
        any plain text password storage.
        '''
        pass_salt = self.password_hash.split(',')
        # pasword hash containst the salt and the hash, hence to return true we
        # must use both the password at [0] and the salt at [1] from the object
        # generated above.
        return pass_salt[0] == hashlib.sha256(\
            self.username + password_provided + pass_salt[1]).hexdigest()

    def get_liked(self):
        # returns a list of posts the user has liked.
        return [post for post in Post.all().fetch(limit=None) if self in post.get_likers()]
    
    def __repr__(self):
        return "< username : email '{}' : '{}' >".format(self.username, self.email)

class Post(db.Model):
    """This model allows post storage.

    url will be like the name of the post with a '/' added for easy routing
    and a web aesthetic when displayed.

    content is an open text field containing the content of the post 
    with no restrictions.

    author links Users to posts

    _tags links tags to posts

    _liked stores a list of Users that have liked a post
    """
    url = db.StringProperty(required = True)
    content = db.StringProperty(multiline = True)
    author = db.ReferenceProperty(User)
    comments = db.ListProperty(db.Key)
    _liked = db.ListProperty(db.Key)
    _is_comment = db.BooleanProperty()

    def get_likers(self):
        '''Returns a list of of users listed as liking this post, removing any
        user accounts that cannot be retrieved (were deleted).
        '''
        likers = []
        for k in self._liked:
            if User.get_by_id(k.id()):
                likers.append(User.get_by_id(k.id()))
            else:
                self._liked.remove(k)
        return likers

    def get_comments(self):
        '''Returns a list of Post objects that were created as comments on 
        this post.

        Removes any posts accounts that cannot be retrieved (were deleted).
        '''
        list_of_comments = []
        for p in self.comments:
            if Post.get_by_id(p.id()):
                list_of_comments.append(Post.get_by_id(p.id()))
            else:
                self.comments.remove(p)
        self.put()
        return list_of_comments


    def get_tags(self, just_names = False):
        '''Returns a set of tags affiliated with the post.

        A set is used instead of a list since accidental double tagging isn't
        explicitly prohibited.

        The just_names boolean arg allows this method to be used to get a set 
        of tag names rather than the full object.
        '''
        tags_on_post = set()
        for tg in Tag.all():
            if self.key() in tg._posts:
                tags_on_post.add(tg)
        if just_names:
            return [str(t.name) for t in tags_on_post]
        return tags_on_post

    def __repr__(self):
        return "content and url of post:"+\
        "'{1}': '{0}' -- by {2}'".format(self.content, self.url, self.author)


class Tag(db.Model):
    """This model allows tag storage.

    name is the tag as a string.
    _posts tracks posts affiliated with the tag.
    """
    name = db.StringProperty(required = True)
    _posts = db.ListProperty(db.Key)


    @classmethod
    def get_or_create(cls, name):
        '''This function returns an existing tag if the tag exists,
        and creates a new tag if it does not. '''
        get_tag = Tag.gql("WHERE name = :tag_name", tag_name = name).get()
        if not get_tag:
            get_tag = cls(name = name)
            get_tag.put()
        print  'get tag from classmethod'       
        return get_tag


    def get_posts(self):
        '''Returns a list of posts affiliated with the tag.
        Removes any posts accounts that cannot be retrieved (were deleted).
        '''
        list_of_posts = []
        for p in self._posts:
            if Post.get_by_id(p.id()):
                list_of_posts.append(Post.get_by_id(p.id()))
            else:
                self._posts.remove(p)
        print list_of_posts
        return list_of_posts


    def __repr__(self):
        return "< tag string {0} >".format(self.name)