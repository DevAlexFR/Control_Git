import os
import requests


class GIT_CONTROL:

    def __init__(self):
        """ Configuração padrão da classe com token, usuário e nome da organização obtidos do arquivo SU_KEYS.

        O arquivo SU_KEYS deve conter:
        1. Token do GitHub clasico
        2. Nome de usuário do GitHub
        3. Nome da organização do GitHub

        Exemplo do conteúdo do arquivo SU_KEYS:
        ----------
            184572094523890fwqefno
            User123
            OrgName
        """
        with open(os.path.join(os.path.dirname(__file__), 'SU_KEYS'), 'r') as file:
            self.token = file.readline().strip()
            self.user = file.readline().strip()
            self.org = file.readline().strip()


    def clone_all_org_repo(self, dest_path: str) -> None:
        """ Clona todos os repositórios de uma organização para um diretório de destino especificado.

        Parameters
        ----------
        dest_path : str
            Diretório de destino onde os repositórios serão clonados.

        Exemplo de uso:
        ---------
            gc = GIT_CONTROL()
            gc.clone_all_org_repo(dest_path='C:\\Project\\DESTINO')
        """
        page = 1
        while True:
            response = requests.get(
                f"https://api.github.com/orgs/{self.org}/repos?per_page=200&page={page}", 
                auth=(self.user, self.token)
            ) 
            repos = response.json()

            if not repos:
                break

            for repo in repos: 
                repo_dir_dest = os.path.join(dest_path, repo['name'])
                if not os.path.exists(repo_dir_dest):
                    repo_dir_dest = os.path.join(dest_path, repo['name'])
                    command = f"git clone {repo['html_url']}.git {repo_dir_dest}"
                    os.system(command)
            
            page += 1

    def clone_all_user_repos(self, dest_path: str, username: str, owner: bool = False) -> None:
        """Clona todos os repositórios públicos e/ou privados de um usuário para um diretório de destino especificado.

        Parameters
        ----------
        dest_path : str
            Diretório de destino onde os repositórios serão clonados.
        username : str
            Nome do usuário do GitHub cujos repositórios serão clonados. Caso este nome seja igual ao nome em SU_KEYS, também clona os repositórios privados.
        owner : bool
            Se True -> Caso este nome seja igual ao nome em SU_KEYS, para todas organização onde for o owner, também clona os repositórios privados.

        Exemplo de uso:
        ---------
            gc = GIT_CONTROL()
            gc.clone_all_user_repos(dest_path='C:\\Project\\DESTINO', username='User123')
        """
        page = 1
        while True:
            if username == self.user:
                if owner:
                    response = requests.get(
                        f"https://api.github.com/user/repos?per_page=200&page={page}",
                        auth=(self.user, self.token)
                    )
                else:
                    response = requests.get(
                        f"https://api.github.com/user/repos?type=owner&per_page=200&page={page}",
                        auth=(self.user, self.token)
                    )
            else:
                response = requests.get(
                    f"https://api.github.com/users/{username}/repos?per_page=200&page={page}",
                    auth=(self.user, self.token)
                )
            
            repos = response.json()

            if not repos:
                break

            for repo in repos:
                repo_dir_dest = os.path.join(dest_path, repo['name'])
                if not os.path.exists(repo_dir_dest):
                    command = f"git clone {repo['html_url']} {repo_dir_dest}"
                    os.system(command)

            page += 1


    def create_all_repos_org(self, orig_path: str, dest_org: str):
        """ Cria repositorios na organização de destino ja alimentados

        Parameters
        ----------
        orig_path : str
            Caminho com todos os projetos que quer criar um repositorio
        dest_org : str
            Nome da organização de destino destes repositorios

        Exemplo de uso:
        ----------
            gc = GIT_CONTROL()
            gc.create_all_repos_org('C:\\Project', 'minhaORG')
        """
        for path in os.listdir(orig_path):
                full_path = os.path.join(orig_path, path)
                if os.path.isdir(full_path):
                    repo_exists = os.system(f'gh repo view {dest_org}/{path}') == 0
                    if not repo_exists:
                        os.chdir(full_path)

                        git_folder = os.path.join(full_path, '.git')
                        if os.path.exists(git_folder):
                            os.system(f'rmdir /s /q "{git_folder}"')
                        
                        os.system(f'gh repo create {dest_org}/{path} --private')
                        
                        os.system('git init')
                        os.system('git add .')
                        os.system('git commit -m "Initial commit"')

                        remote_check = os.system('git remote show origin')
                        if remote_check != 0:
                            os.system(f'git remote add origin https://github.com/{dest_org}/{path}.git')

                        os.system('git branch -M main')
                        os.system('git push -u origin main')
