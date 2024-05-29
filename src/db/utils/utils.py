import os


def get_env_file_path():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.abspath(os.path.join(current_file_dir, '..', '..', '..',))
    env_file_path = os.path.join(project_root_dir, '.env')

    return env_file_path
