## Prerequisite

* Python 2.7
* pip 1.1
* virtualenv 1.6.x
* [Twitter Access Tokens](https://dev.twitter.com/docs/auth/obtaining-access-tokens)

## Install

Provided `.twitter-friends` is cloned to $HOME:

	$ virtualenv --python=/usr/bin/python2.7 ~/.twitter-friends
	$ source ~/.twitter-friends/bin/activate
	$ pip install -r requirements.txt
	$ cp local-add-config.sh.sample local-add-config.sh

Modify `local-add-config.sh` to set Twitter Access Tokens information.

## Run

    $ source local-add-config.sh
	$ python web.py

You can access to the service via http://localhost:5000.

