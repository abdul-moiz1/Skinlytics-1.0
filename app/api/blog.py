import os
import uuid
from flask import request, jsonify, current_app
from flask_login import current_user
from app.api import api_bp, api_admin_required
from app.models import BlogPost
from app import db


# --- Public Routes ---

@api_bp.route('/blog/posts', methods=['GET'])
def api_blog_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return jsonify({'posts': [p.to_dict() for p in posts]}), 200


@api_bp.route('/blog/posts/<int:post_id>', methods=['GET'])
def api_blog_post_detail(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    return jsonify({'post': post.to_dict()}), 200


# --- Admin: Blog Posts ---

@api_bp.route('/admin/blog/posts', methods=['POST'])
@api_admin_required
def api_admin_blog_create():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and content are required.'}), 400

    filename = None
    if 'featured_image' in request.files and request.files['featured_image'].filename:
        file = request.files['featured_image']
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            return jsonify({'error': 'Only JPG and PNG images are allowed.'}), 400
        filename = f"blog_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(filepath)

    post = BlogPost(
        title=title,
        content=content,
        featured_image=filename,
        author_id=current_user.id,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({'post': post.to_dict()}), 201


@api_bp.route('/admin/blog/posts/<int:post_id>', methods=['PUT'])
@api_admin_required
def api_admin_blog_update(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found.'}), 404

    post.title = request.form.get('title', post.title).strip()
    post.content = request.form.get('content', post.content).strip()

    if 'featured_image' in request.files and request.files['featured_image'].filename:
        file = request.files['featured_image']
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in ('jpg', 'jpeg', 'png'):
            return jsonify({'error': 'Only JPG and PNG images are allowed.'}), 400
        filename = f"blog_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(filepath)
        post.featured_image = filename

    db.session.commit()
    return jsonify({'post': post.to_dict()}), 200


@api_bp.route('/admin/blog/posts/<int:post_id>', methods=['DELETE'])
@api_admin_required
def api_admin_blog_delete(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found.'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted.'}), 200
