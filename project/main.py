from git_control import GIT_CONTROL


if __name__ == '__main__':

    gc = GIT_CONTROL()
    gc.clone_all_user_repos(dest_path='C:\\Project\\DESTINO', username='DevAlexFR')
