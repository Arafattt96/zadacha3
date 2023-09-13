import random
import requests
import string


def generate_random_word(length: int = 10) -> str:
    """
    Генерирует рандомное слово из до 10 букв.

    Args:
        length: Длина слова.

    Returns:
        Рандомное слово.
    """

    letters = string.ascii_lowercase
    word = ''
    for _ in range(length):
        word += letters[random.randint(0, len(letters) - 1)]

    return word


uuid = ''
token = ''
user_name = generate_random_word(10)

# буквы в конце нужны чтобы пароль подходил под валидацию
user_password = generate_random_word(5) + '0!A'


class TestSwagger():

    # проверяем что можем создать пользователя
    def test_create_user(self):
        # Запрос
        url = "https://demoqa.com/Account/v1/User"
        json = {"userName": user_name, "password": user_password}
        print(user_name)
        print(user_password)
        response = requests.post(url, json=json)
        data = response.json()

        global uuid
        uuid = data['userID']

        # Проверка ответа
        assert response.status_code == 201
        assert data['userID'] != ""
        assert data["username"] == user_name

    # проверяем что не можем создать повторно этого же пользователя
    def test_create_existing_user(self):
        url = "https://demoqa.com/Account/v1/User"
        json = {"userName": user_name, "password": user_password}
        response = requests.post(url, json=json)
        data = response.json()

        # Проверка ответа
        assert response.status_code == 406
        assert data['message'] == "User exists!"

    # генерируем токен
    def test_generate_token(self):

        url = "https://demoqa.com/Account/v1/GenerateToken"
        json = {"userName": user_name, "password": user_password}
        response = requests.post(url, json=json)
        data = response.json()

        global token
        token = data["token"]

        # Проверка ответа
        assert response.status_code == 200
        assert data['expires'] != ""
        assert data['status'] == "Success"
        assert token != ""

    # тест на некорректный токен (неправильные авторизационные данные)
    def test_generate_incorrect_token_with_invalid_data(self):

        url = "https://demoqa.com/Account/v1/GenerateToken"
        json = {"userName": user_password, "password": user_name}
        response = requests.post(url, json=json)
        data = response.json()

        # Проверка ответа
        assert response.status_code == 200
        assert data['status'] == "Failed"

    # тест на авторизацию существующего юзера
    def test_authorize_user(self):

        url = "https://demoqa.com/Account/v1/Authorized"
        json = {"userName": user_name, "password": user_password}

        response = requests.post(url, json=json)
        print(response.json())

        # Проверка ответа
        assert response.status_code == 200

    # тест на авторизацию несуществующего юзера
    def test_invalid_authorize_user(self):

        url = "https://demoqa.com/Account/v1/Authorized"
        json = {"userName": user_password, "password": user_name}
        response = requests.post(url, json=json)

        # Проверка ответа
        assert response.status_code == 404

    def test_delete_user(self):

        global uuid
        url = f"https://demoqa.com/Account/v1/User/{uuid}"


        auth = requests.auth.HTTPBasicAuth(user_name, user_password)

        response = requests.delete(url, auth = auth)

        # Проверка ответа
        assert response.status_code == 204