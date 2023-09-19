import os
from ipcqueue import posixmq
from cfg_support import set_current_input_path, set_current_test_path
from baseline_constants import session_files_path


def validate_soultion():
    pass


def create_dirs_for_session(session_id):

    session_global_path = os.path.join(session_files_path, session_id)

    session_global_input_path = os.path.join(session_global_path, "input")
    session_global_output_path = os.path.join(session_global_path, "output")
    session_global_test_path = os.path.join(session_global_path, "test")

    set_current_input_path(session_global_input_path)
    set_current_test_path(session_global_test_path)

    if not os.path.exists(session_global_path):
        os.mkdir(session_global_path)

    if not os.path.exists(session_global_input_path):
        os.mkdir(session_global_input_path)

    if not os.path.exists(session_global_output_path):
        os.mkdir(session_global_output_path)

    if not os.path.exists(session_global_test_path):
        os.mkdir(session_global_test_path)

    return dict(cur_input=session_global_input_path, cur_output=session_global_output_path)


def get_inline_queue():
    return posixmq.Queue('/inline')

