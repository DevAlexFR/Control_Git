from git_control import GIT_CONTROL


if __name__ == '__main__':

    gc = GIT_CONTROL()
    # gc.clone_all_org_repo('C:\\Project\\FIS')
    gc.create_all_repos_org(dest_org='AF-Code-Developer', orig_path='C:\\Project\\FIS')
    # gc.clone_all_user_repos(username='DevAlexFR', dest_path='C:\\Project\\DESTINO')
