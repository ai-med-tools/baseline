from cfg_support import get_message_value
import os

main_dir = os.path.dirname(os.path.abspath(__file__))
system_logs_path = os.path.join(main_dir, "logs/system_state_notice.log")
push_logs_path = os.path.join(main_dir, "logs/system_push_notice.log")
session_files_path = os.path.join(main_dir, "files/sessions/")

main_process_start_success_const = dict(op='connect', status='success', message=get_message_value("main_process_start_success"))
main_process_abort_success_const = dict(op='connect', status='success', message=get_message_value("main_process_abort_success"))
connect_success_const = dict(op='connect', status='success', message=get_message_value("connect_success"))
reconnect_success_const = dict(op='reconnect', status='success', message=get_message_value("reconnect_success"))
reconnect_error_const = dict(op='connect', status='error', message=get_message_value("reconnect_error"))
disconnect_success_const = dict(op='disconnect', status='success', message=get_message_value("disconnect_success"))
session_start_success_const = dict(op='start', status='success', message=get_message_value("start_success"))
session_start_error_const = dict(op='start', status='error', message=get_message_value("start_error"))
session_start_blank_const = dict(op='start-blank', status='error', message=get_message_value("start_blank"))

connection_auth_error_const = dict(op='connection', status='error', message=get_message_value("connection_auth_error"))
solution_file_doesnt_exist_const = dict(op='send', status='error', message=get_message_value("solution_file_doesnt_exist"))
data_not_resolved_const = dict(op='send', status='error', message=get_message_value("data_not_resolved"))

abort_success_const = dict(op='abort', status='success', message=get_message_value("abort_success"))
abort_error_const = dict(op='abort', status='error', message=get_message_value("abort_error"))
