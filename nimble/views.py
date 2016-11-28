from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from nimble import app
from forms import *
from models import *


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash ('welcome {}! you can now edit posts.'.format(user.username))
            return redirect(request.args.get('next') or url_for('to_start'))
            #note, url_for references the function that returns the tempate, nt the decorator or url
        else:
            flash('nope, pwd or username is wrong.')

    return render_template('login.html', 
        form=form, 
        hfour='welcome back yo.')


@app.route('/logout')
def logout():
    flash ('Thanks for hanging out! You are now in anon mode (view only).')
    logout_user()
    return    redirect(request.args.get('next') or url_for('login'))


@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    form=SignupForm()
    if form.validate_on_submit():
        email=form.Email.data
        username=form.username.data
        noob = User(email=form.Email.data,
            username=form.username.data,
            password=form.password.data)
        db.session.add(noob)
        db.session.commit()
        app.logger.debug('registred: ' + username + ' , ' + email)
        flash('welcome to the site %s' % email)
        login_user(noob)
        return redirect('/start', code=302)  
    top_posts_results = db.session.query(Post, db.func.count(likes.c.user_id)\
            .label('total'))\
            .join(likes)\
            .group_by(Post)\
            .order_by('total DESC').all()
    top_posts = [post_result.Post for post_result in top_posts_results]
    return render_template('register.html',
        top_posts = top_posts,
        form = form, 
        hfour ='sign up and start creating posts.')


@app.route('/register')
@app.route('/')
def to_start ():
    if current_user.is_authenticated:
        return redirect('/start', code=302)
    else:
        return redirect('/sign_up', code=302)


@app.route('/start', methods=['GET','POST'])
@login_required
def starter():
    add_form=DataForm()
    add_form.tags.data = current_user.username
    if add_form.validate_on_submit():
        return redirect(url_for('add', post = add_form.url.data.strip('/')))
    else:
        print 'no form validation'
    return  render_template('user.html',
        form = add_form,
        active_user = current_user, 
        posts = Post.query.filter_by(user = current_user))


@app.route('/edit/<post>', methods=['GET','POST'])
@login_required
def add(post):

    edit_post = Post.query.filter_by(url = '/' + post, user = current_user).first()
    print 'edit post'
    print edit_post
    if edit_post:
        post_edit_form = DataForm(obj=edit_post)
        if post_edit_form.validate_on_submit():
            print "post_edit validated"
            post_edit_form.populate_obj(edit_post)
            db.session.commit()
            flash("The post'{}' has been edited".format(post_edit_form.url.data))
            return redirect(url_for('render_user_post', 
                user = edit_post.user.username,
                post_name = post_edit_form.url.data.strip('/')))
        return render_template ('edit.html', form = post_edit_form, post = edit_post)
    else:
        start_post = Post(url = post)
        post_add_form = DataForm(obj=start_post)
        if post_add_form.validate_on_submit():
            new_post = Post(
                url = post_add_form.url.data,
                content = post_add_form.content.data,
                tags = post_add_form.tags.data,
                user = current_user)
            db.session.add(new_post)
            db.session.commit()
            print new_post
            print db.session
            flash("The post'{}' has been created!".format(post_add_form.url.data))
            return redirect(url_for('render_user_post', 
                user = new_post.user.username,
                post_name = new_post.url.strip('/')))
        return render_template('add.html', form=post_add_form, edit_post_result=edit_post)


@app.route('/<user>/<post_name>')
def render_user_post(user, post_name):
    author = User.query.filter_by(username = user).first()
    post = Post.query.filter_by(url = '/' + post_name, user = author).first_or_404()
    print 'post author'
    print author
    print 'post get'
    print post
    if post:
        return render_template('user_post.html', 
            post = post,
            active_user = current_user)


@app.route('/tags/<tag>')
def catch_tag(tag):
    target_tag=Tag.query.filter_by(name=tag).first_or_404()
    return render_template('tag_post.html', tag=target_tag)

@app.route('/like/<user>/<post_name>')
def like(user, post_name):
    author = User.query.filter_by(username = user).first()
    like_post = Post.query.filter_by(url = '/' + post_name, user = author).first_or_404()
    print 'like_post'
    print like_post
    like_post._liked.append(current_user)
    db.session.commit()
    flash("liked  '{}'".format(post_name))
    return redirect(url_for('render_user_post', 
        user = user,
        post_name = post_name))


@app.errorhandler(404)
def post_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def unauth(e):
    return render_template('401.html'), 401

@app.errorhandler(500)
def unauth(e):
    return render_template('500.html', error = e), 500

@app.context_processor
def inject_tags():
    return dict(all_tags = Tag.all)