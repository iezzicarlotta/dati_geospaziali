"""Bootstrap Flask application with blueprint and MongoDB integration."""

from flask import Flask


def create_app() -> Flask:
    """
    Create and configure Flask application.
    
    Returns:
        Flask: Configured Flask app instance
    """
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static"
    )
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    from backend.flask_app.blueprints.web import web_bp
    app.register_blueprint(web_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        return {"error": "Internal server error"}, 500
    
    return app


app = create_app()
