import os

from flask import Flask, render_template
from flask_socketio import SocketIO
socketio = SocketIO()
import flaskr.sync_data

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    # from . import auth
    from . import blog
    from . import auth
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    # app.register_blueprint(aut h.bp)
    # app.add_url_rule('/', endpoint='index')
    db.init_app(app)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("auth/404.html")

    return app

if __name__ == "__main__":
    # To allow aptana to receive errors, set use_debugger=False
    app = create_app(config="config.yaml")

    if app.debug: use_debugger = True
    try:
        # Disable Flask's debugger if external debugger is requested
        use_debugger = not(app.config.get('DEBUG_WITH_APTANA'))
    except:
        pass
    socketio = SocketIO(app)
    socketio.run()
    # socketio.run(use_debugger=use_debugger, debug=app.debug,
    #         use_reloader=use_debugger, host='0.0.0.0')
