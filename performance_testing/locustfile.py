"""
A locust file that simulates an authenticated MulticastMenu user.
After logging into MulticastMenu, the user randomly loads one of the following MulticastMenu endpoints:
    the main page,
    the main page with a search query,
    the main page with a category,
    the trending section,
    the editors' choice section,
    the liked streams section,
    the detail pages of the streams,
    the open action of the streams,
    the like action of the streams.

In order for the script to work properly, the following files should be present in the ./data directory:
    credentials.csv - A csv file that contains the user credentials in the form (username, password).
                      These credentials should be available in MulticastMenu.
                      In util.py there are two scripts that can create and delete the users specified in the csv file.
    stream_ids.csv - A csv file that contains the stream ids in the form (stream_id)
    category_slugs.csv - A csv file that contains the slugs for the categories available in MulticastMenu in the form (cat_slug)

The locust file can be started with the following command:
    locust -f locustfile_for_v4.0.0.py
After that the number of users to be spawned, the spawn rate and the address of MulticastMenu can be configured in the locust web interface.

See:
    Performance, load and stress testing in Django,
    https://stackoverflow.com/questions/46893226/performance-load-and-stress-testing-in-django
"""
import csv
import random

from bs4 import BeautifulSoup
from locust import HttpUser, TaskSet, task, run_single_user, between, events

USER_CREDENTIALS = None
STREAM_IDS = None
CATEGORY_SLUGS = None

FETCH_STATIC_ASSETS = False


class MulticastMenuTaskSet(TaskSet):
    username = "NOT_FOUND"
    password = "NOT_FOUND"

    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            self.username, self.password = USER_CREDENTIALS.pop()

        response = self.client.get("/login/")
        csrf_token = response.cookies.get("csrftoken")
        response = self.client.post('/login/', {'username': self.username, 'password': self.password},
                                    headers={'X-CSRFToken': csrf_token})
        if "login" in response.url:
            print("Login failed with credentials (" + self.username + ", " + self.password + ")")
        else:
            print("Login successful with credentials (" + self.username + ", " + self.password + ")")

    def on_stop(self):
        if self.username != "NOT_FOUND" and self.password != "NOT_FOUND":
            self.client.get("/logout/")
            print("Logged out from credentials (" + self.username + ", " + self.password + ")")

    def fetch_static_assets(self, response):
        """
        Fetching the static resources from the html document.

        See:
        Simulating real browser behaviour #120,
        https://github.com/locustio/locust/issues/120

        :param response:
        :return:
        """
        if FETCH_STATIC_ASSETS:
            soup = BeautifulSoup(response.text, "html.parser")
            for res in soup.find_all(src=True):
                url = res['src']
                if url.startswith("/static/"):
                    self.client.get(url, name="/static/...")
                elif url.startswith("/media/"):
                    self.client.get(url, name="/media/...")

    @task
    def index(self):
        response = self.client.get("/")
        self.fetch_static_assets(response)

    @task
    def search(self):
        query = random.choice(["research", "presentations", "llamigos", "yellowstone", "spring", "sintel", "bunny"])
        response = self.client.get("/?query=" + query, name="/?query=<query>")
        self.fetch_static_assets(response)

    @task
    def filter_by_category(self):
        slug = random.choice(CATEGORY_SLUGS)[0]
        response = self.client.get("/?category=" + slug, name="/?category=<slug>")
        self.fetch_static_assets(response)

    @task
    def trending(self):
        response = self.client.get("/trending/")
        self.fetch_static_assets(response)

    @task
    def editors_choice(self):
        response = self.client.get("/editors_choice/")
        self.fetch_static_assets(response)

    @task
    def liked(self):
        response = self.client.get("/liked/")
        self.fetch_static_assets(response)

    @task
    def detail(self):
        stream_id = random.choice(STREAM_IDS)[0]
        response = self.client.get("/detail/" + stream_id + "/", name="/detail/<id>")
        self.fetch_static_assets(response)

    @task
    def open(self):
        stream_id = random.choice(STREAM_IDS)[0]
        response = self.client.get("/detail/open/" + stream_id + "/", name="/detail/open/<id>")

    @task
    def like(self):
        stream_id = random.choice(STREAM_IDS)[0]
        response = self.client.get("/detail/like_stream/" + stream_id + "/",
                                   headers={"X-Requested-With": "XMLHttpRequest"}, name="/detail/like_stream/<id>")


class MulticastMenuAuthenticatedUser(HttpUser):
    host = "http://localhost:8000"
    tasks = [MulticastMenuTaskSet]
    wait_time = between(1, 5)


def load_credentials():
    global USER_CREDENTIALS
    with open('data/credentials.csv', 'r') as f:
        reader = csv.reader(f)
        USER_CREDENTIALS = list(reader)


def load_stream_ids():
    global STREAM_IDS
    with open('data/stream_ids.csv', 'r') as f:
        reader = csv.reader(f)
        STREAM_IDS = list(reader)


def load_category_slugs():
    global CATEGORY_SLUGS
    with open('data/category_slugs.csv', 'r') as f:
        reader = csv.reader(f)
        CATEGORY_SLUGS = list(reader)


@events.test_start.add_listener
def on_test_start(**kw):
    print("Test is starting: Load credentials, stream ids, category slugs...")
    load_credentials()
    load_stream_ids()
    load_category_slugs()


@events.test_stop.add_listener
def on_test_start(**kw):
    print("Test is stopping")


# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(MulticastMenuAuthenticatedUser)
