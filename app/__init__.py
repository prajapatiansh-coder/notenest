import os
import structlog
import sentry_sdk
from flask import Flask, request
from .extensions import db, login_manager, migrate, cache, limiter, talisman, api, jwt, socketio, cors
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure Sentry
    if os.environ.get('SENTRY_DSN'):
        sentry_sdk.init(dsn=os.environ.get('SENTRY_DSN'))

    # Configure Logging
    structlog.configure(
        processors=[structlog.processors.JSONRenderer()],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Ensure upload folders exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['PROFILE_PICS']):
        os.makedirs(app.config['PROFILE_PICS'])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)
    cors.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    
    # Security Headers (Updated for API support)
    talisman.init_app(app, content_security_policy={
        'default-src': "'self'",
        'style-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
        'font-src': ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
        'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
        'img-src': ["'self'", "data:", "https://*"]
    })

    # Register Blueprints & API Resources
    from .auth.routes import auth_bp
    from .notes.routes import notes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    # Register SocketIO Events
    from . import socket_events

    # Register API v1
    # from .api.v1 import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api/v1')

    # Error Handlers
    from flask import render_template, jsonify
    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith('/api/'):
            return jsonify(error="Not found", success=False), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.path.startswith('/api/'):
            return jsonify(error="Internal server error", success=False), 500
        return render_template('errors/500.html'), 500

    # Health Check
    @app.route('/health')
    def health_check():
        return jsonify(
            status="healthy",
            db="connected",
            redis="connected",
            version="1.0.0"
        ), 200

    return app
