# TODO must fix imports to get models

import random
import string
import hashlib

from nimble.models import *

def make_pw_hash(name, pw):
    salt = ''.join(random.choice(string.letters) for x in xrange(15))
    print salt
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def add_fake_data():        
    '''add user examples king arthur and sir lancelot'''
    lance = User(username='Sir Lancelot',
                email='HolyHandGrenade15@camelot.org',
                password_hash=make_pw_hash('Sir Lancelot', 'camelot'))
    lance.put()

    arthr = User(username='King Arthur', 
                email='KingA@camelot.org',
                password_hash=make_pw_hash('King Arthur', 'camelot') )
    arthr.put()


    '''add tags'''
    pwnd=Tag(name="pwnd")
    hist=Tag(name="history")
    pwnd.put()
    hist.put()

    '''add posts'''
    blackknight = Post(url="/black_knight", 
                        content = "I pwned the black knight"+\
                        " like a bau5, thats all you need to know.", 
                        author = arthr)
    blackknight.put()

    blackknight._liked.append(lance.key())
    pwnd._posts.append(blackknight.key())
    blackknight.put()

    mystory=Post(url="/mystory",
                    content = "Lancelot was super baller"+\
                    "all his life thats my whole history yay", 
                    author = lance, 
                    _tags = [hist])
    mystory.put()

    comment1 = Post(url = mystory.url + "/comment_1",
                    content = "damm straight bro!!",
                    author = arthr,
                    _is_comment = True)
    comment1.put()

    mystory._comments.append(comment1.key())
    mystory.put()

    print 'Database Initialized'

    print 'user ex'
    print lance
    print lance.email

    print 'tag ex'
    print pwnd.name
    print 'post ex and get liked'
    print blackknight
    # print blackknight.get_tags()
    print blackknight.get_likers()
    print mystory
    print mystory.get_likers()

    print 'lance get liked'
    print lance.get_liked()

    # lance.delete()
    # arthr.delete()
    
    # pwnd.delete()
    # hist.delete()

    # blackknight.delete()
    # mystory.delete()



# if __name__ == '__main__':
add_fake_data() 