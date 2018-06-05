import models


def create_board(forum, board_name):
    """Create a new board attached to this forum."""
    board = models.Board(board_name)
    forum.boards.append(board)
    return board


def create_thread(board, name, description, creator):
    """Create a new thread attached to this board."""

    thread = models.Thread(name, creator, description)
    board.threads.append(thread)
    return thread


def create_post(thread, content, account):
    """Create a new post attached to passed thread."""
    post = models.Post(content, account)
    thread.posts.append(post)
    account.prestige += 1  # Give the user prestige. It's used to track meta activities and is unrelated to gameplay
    return post


def view_thread(thread_id):
    """Return and increase the view count of a thread."""
    thread = models.Thread.get(thread_id)
    if thread:
        thread.views += 1
    return thread
