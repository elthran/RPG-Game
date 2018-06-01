from elthranonline import app

import controller


# This runs after every @app.route before returning a response.
# It even runs if there is an error.
# I am unsure of this approach. Myabe '@app.after_request' would be a better
# fit as this wouldn't write data that caused an error.
@app.after_request
def update_after_request(response):
    controller.update()
    # print("Database updated.")
    # print(response.data)
    return response


# @app.before_request
# def handle_redirect_session_bug():
#     print("Before Request session status")
#     print(database.session.new)
#     print(database.session.dirty)
