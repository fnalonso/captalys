import requests


class Consumer(object):
    """
    Classe responsável por consumir os endpoints da API do github para
    recuperação dos dados de perfil de usuário e repositórios
    Esta classe não faz nenhum tratamento dos dados retornados pela
    API do github, apenas separa a lógica de chamada.
    """

    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_user_account(self, username):
        url = f"{self.api_url}/users/{username}"
        return self._get_from_api(url)

    def get_user_repositories(self, username):
        url = f"{self.api_url}/users/{username}/repos"
        return self._get_from_api(url)

    def get_repository_details(self, username, repository_name):
        url = f"{self.api_url}/repos/{username}/{repository_name}"
        return self._get_from_api(url)

    def _get_from_api(self, url, headers=None, timeout=3):
        """
        Método genérico para efetuar o get em uma dada URL
        A implementação aqui supõe que estamos considerando
        apenas cenários onde a api do github retorna 2XX
        :param url: Url para a chamada
        :param timeout: tempo máximo de espera da resposta
        :return: dict
        """
        try:
            result = requests.get(url, timeout=timeout, headers=headers)
            result.raise_for_status()
            return result.json()
        except requests.exceptions.RequestException as error:
            return dict()
