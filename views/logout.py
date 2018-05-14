import flask

from elthranonline import app
import services.decorators


@app.route('/logout')
@services.decorators.login_required
def logout():
    flask.session.clear()
    flask.flash("Thank you for playing! Your have successfully logged out.")
    return flask.redirect(flask.url_for('login'))
