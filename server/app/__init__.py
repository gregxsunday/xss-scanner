from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object('app.config')

# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
  return render_template('404.html', path=request.path, title='404 page'), 404

from app.core.views import mod as core
app.register_blueprint(core)


# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)

