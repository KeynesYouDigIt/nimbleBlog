

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

    # the below helps flask login work normally in init and views
    @property
    def id(self):
        self.key().id()

    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

    # end UserMixin attrs

    def check_password(self, password_provided):
        '''h is a preixisting (hash,salt) tuple'''
        pass_salt = self.password_hash.split(',')
        return pass_salt[0] == hashlib.sha256(\
            self.username + password_provided + pass_salt[1]).hexdigest()


    def get_liked(self):
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
        likers = []
        for k in self._liked:
            if User.get_by_id(k.id()):
                likers.append(User.get_by_id(k.id()))
            else:
                self._liked.remove(k)
        return likers

    def get_comments(self):
        list_of_comments = []
        for p in self.comments:
            if Post.get_by_id(p.id()):
                print 'got'
                print Post.get_by_id(p.id())
                list_of_comments.append(Post.get_by_id(p.id()))
            else:
                self.comments.remove(p)
                'removed' + str(p)
        self.put()
        print 'list o comments'
        print list_of_comments
        return list_of_comments


    def get_tags(self, just_names = False):
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

# class Comment(db.Model):
#     """This model allows comment storage
    
#     only stores comment, commenter, and post.
#     """
#     content = db.StringProperty(required = True)
#     commenter = db.ReferenceProperty(User)
#     post = db.ReferenceProperty(Post)

class Tag(db.Model):
    """This model allows tag storage.

    name is the tag as a string
    """
    name = db.StringProperty(required = True)
    _posts = db.ListProperty(db.Key)


    @classmethod
    def get_or_create(cls, name):
        get_tag = Tag.gql("WHERE name = :tag_name", tag_name = name).get()
        if not get_tag:
            get_tag = cls(name = name)
            get_tag.put()
        print  'get tag from classmethod'       
        return get_tag


    def get_posts(self):
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