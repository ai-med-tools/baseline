import os, configparser


def get_current_epicrisis_id():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentepicrisisid.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get("currentepicrisisid")


def set_current_epicrisis_id(new_value: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentepicrisisid.cfg")
    config = configparser.ConfigParser()
    config.read(abs_file_path)
    config.set('DEFAULT', "currentepicrisisid", new_value)

    print(config['DEFAULT']["currentepicrisisid"])

    with open(abs_file_path, 'w') as configfile:
        config.write(configfile)

    return new_value


def get_current_epicrisis_path():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentepicrisispath.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get("currentepicrisispath")


def set_current_epicrisis_path(new_value: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentepicrisispath.cfg")
    config = configparser.ConfigParser()
    config.read(abs_file_path)
    config.set('DEFAULT', "currentepicrisispath", new_value)

    print(config['DEFAULT']["currentepicrisispath"])

    with open(abs_file_path, 'w') as configfile:
        config.write(configfile)

    return new_value


def get_current_input_path():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentinputpath.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get("currentinputpath")


def set_current_input_path(new_value: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentinputpath.cfg")
    config = configparser.ConfigParser()
    config.read(abs_file_path)
    config.set('DEFAULT', "currentinputpath", new_value)

    print(config['DEFAULT']["currentinputpath"])

    with open(abs_file_path, 'w') as configfile:
        config.write(configfile)

    return new_value


def get_current_test_path():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currenttestpath.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get("currenttestpath")


def set_current_test_path(new_value: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currenttestpath.cfg")
    config = configparser.ConfigParser()
    config.read(abs_file_path)
    config.set('DEFAULT', "currenttestpath", new_value)

    print(config['DEFAULT']["currenttestpath"])

    with open(abs_file_path, 'w') as configfile:
        config.write(configfile)

    return new_value


def get_current_session_id():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentsessionid.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get("currentsessionid")


def set_current_session_id(new_value: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currentsessionid.cfg")
    config = configparser.ConfigParser()
    config.read(abs_file_path)
    config.set('DEFAULT', "currentsessionid", new_value)

    print(config['DEFAULT']["currentsessionid"])

    with open(abs_file_path, 'w') as configfile:
        config.write(configfile)

    return new_value


def get_current_task_id():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currenttasksid.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get("currenttasksid")


def set_current_task_id(new_value: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/currenttasksid.cfg")
    config = configparser.ConfigParser()
    config.read(abs_file_path)
    config.set('DEFAULT', "currenttasksid", new_value)

    print(config['DEFAULT']["currenttasksid"])

    with open(abs_file_path, 'w') as configfile:
        config.write(configfile)

    return new_value


def get_config_value(config_key: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/state.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['DEFAULT']
    return state.get(config_key)


def get_message_value(config_key: str):
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/lang.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['MESSAGEDICTIONARY']
    return state.get(config_key)

def get_perfomance():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(main_dir, "tmp/creds.cfg")

    config = configparser.ConfigParser()

    config.read(abs_file_path)

    state = config['PERFOMANCE']
    return state








