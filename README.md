===
Weebly Mini
===

[API Documentation](https://github.com/shivamthapar/weebly-mini/blob/master/app/api/README.md)

### About the Project
Front-end Options: 1,2

Back-end Options: 1,2,3

### Instructions
1. Clone this repo and navigate to it.
2. Create a [virtualenv](http://virtualenv.readthedocs.org/en/latest/) by running the following command: `virtualenv venv`
3. Activate the virtualenv by running `. venv/bin/activate`
4. Install dependencies through pip by running `pip install -r requirements.txt`
5. Follow the instructions [here](https://developers.google.com/+/quickstart/python) to create a Google API Project.  Make sure to include `http://localhost:5000` in the Authorized Javascript Origins. Note your Client ID and Secret.
6. Rename `client_secrets_template.json` to `client_secrets.json` and input your Client ID and Secret.
7. Run the sever by calling `python run.py`
8. Point your browser to [http://localhost:5000](http://localhost:5000).

### Capabilities
#### Web Interface:
- New users can be created, using authentication through Google+.
- New pages can be created through the sidebar.
- Pages can be renamed or deleted.
- Contents of text elements can be changed. It is saved upon clicking outside the text box.

#### API:
- Pages can be created, retrieved, updated, and deleted. Check [API Documentation](https://github.com/shivamthapar/weebly-mini/blob/master/app/api/README.md).

