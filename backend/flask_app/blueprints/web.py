"""Flask web blueprint for serving pages and static content."""

from flask import Blueprint, render_template

web_bp = Blueprint(
    'web',
    __name__,
    url_prefix='/',
    template_folder='../templates',
    static_folder='../static',
)


@web_bp.route('/', methods=['GET'])
def home():
    """Home page route."""
    return render_template('home.html')


@web_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Flask Web Server"
    }
