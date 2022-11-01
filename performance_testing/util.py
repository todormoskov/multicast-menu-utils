import csv

from django.contrib.auth.models import User


def create_dummy_users(str_credentials_path):
    """
    Creates dummy users specified in a csv file.

    The first column of the csv file should contain the usernames and the second column the corresponding passwords.

    :param str_credentials_path:
    :return:
    """
    if str_credentials_path is None:
        ValueError("Illegal argument: str_credentials_path is null!")

    with open(str_credentials_path, 'r') as f:
        reader = csv.reader(f)
        user_credentials = list(reader)
        users = []
        for username, password in user_credentials:
            user = User(username=username)
            user.set_password(password)
            users.append(user)
            print("Creating user (" + username + ", " + password + ")")
        User.objects.bulk_create(users)


def delete_dummy_users(str_credentials_path):
    """
    Deletes dummy users specified in a csv file.

    The first column of the csv file should contain the usernames and the second column the corresponding passwords.

    :param str_credentials_path:
    :return:
    """
    if str_credentials_path is None:
        ValueError("Illegal argument: str_credentials_path is null!")

    with open(str_credentials_path, 'r') as f:
        reader = csv.reader(f)
        user_credentials = list(reader)
        for username, password in user_credentials:
            u = User.objects.get(username=username)
            u.delete()
            print("Deleting user " + username)
