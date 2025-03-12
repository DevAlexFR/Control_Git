from git_control import GIT_CONTROL


if __name__ == '__main__':

    gc = GIT_CONTROL()
    gc.clone_all_org_repo('C:\\Project\\FIS')
    # gc.create_all_repos_org(dest_org='AF-Code-Developer', orig_path=r'C:\\Project\\FIS', True)
    # gc.clone_all_user_repos(username='DevAlexFR', owner=True, dest_path='C:\\Project\\DESTINO')
