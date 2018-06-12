import pdb

import flask

from elthranonline import app
from models.forum import Board, Thread, Post
import services.decorators
import controller.forum
import models


@app.route('/forum/<int:board_id>/<int:thread_id>', methods=['GET', 'POST'])
@services.decorators.uses_hero
def forum(hero=None, board_id=0, thread_id=0):
    page_title = "Forum"
    # Checking current forum. Currently it's always on this forum as we only have 1
    current_forum = models.Forum.get(1)
    # Letting python/html know which board/thread you are reading. Will be simpler with database and get_thread_by_id ;)
    current_board = models.Board.get(board_id)
    current_thread = controller.forum.view_thread(thread_id)

    if flask.request.method == 'POST':
        form_type = flask.request.form["form_type"]
        if form_type == "new_board":  # If starting new board
            controller.forum.create_board(current_forum, flask.request.form["board_name"])
        elif form_type == "new_thread":  # If starting new thread
            thread_board = models.Board.filter_by(name=flask.request.form["thread_board"]).one()
            thread_name = flask.request.form["thread_name"]
            thread_description = flask.request.form["thread_description"]
            creator = hero.account.username
            new_thread = controller.forum.create_thread(thread_board, thread_name, thread_description, creator)
            if len(flask.request.form["thread_post"]) > 0:  # If they typed a new post, add it to the new thread
                controller.forum.create_post(new_thread, flask.request.form["thread_post"], hero.account)
        else:  # If replying
            post_content = flask.request.form["post_content"]
            controller.forum.create_post(current_thread, post_content, hero.account)

    return flask.render_template('forum.html', hero=hero, current_forum=current_forum, current_board=current_board, current_thread=current_thread, page_title=page_title)  # return a string
