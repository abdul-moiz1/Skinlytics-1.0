import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from app.blog import bp
from app.blog.forms import BlogPostForm
from app.models import BlogPost
from app import db


@bp.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/post/<int:post_id>')
def detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog/detail.html', post=post)


# --- Admin routes ---

@bp.route('/admin')
@login_required
def admin_list():
    if not current_user.is_admin:
        abort(403)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog/admin/list.html', posts=posts)


@bp.route('/admin/create', methods=['GET', 'POST'])
@login_required
def admin_create():
    if not current_user.is_admin:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        filename = None
        if form.featured_image.data:
            file = form.featured_image.data
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"blog_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(filepath)

        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            featured_image=filename,
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Article published successfully!', 'success')
        return redirect(url_for('blog.admin_list'))

    return render_template('blog/admin/form.html', form=form, title='Create Article')


@bp.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_edit(post_id):
    if not current_user.is_admin:
        abort(403)

    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        if form.featured_image.data:
            file = form.featured_image.data
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"blog_{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            file.save(filepath)
            post.featured_image = filename

        db.session.commit()
        flash('Article updated successfully!', 'success')
        return redirect(url_for('blog.admin_list'))

    return render_template('blog/admin/form.html', form=form, title='Edit Article')


@bp.route('/admin/delete/<int:post_id>', methods=['POST'])
@login_required
def admin_delete(post_id):
    if not current_user.is_admin:
        abort(403)

    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Article deleted.', 'info')
    return redirect(url_for('blog.admin_list'))
