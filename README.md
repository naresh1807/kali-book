# Kali Book

An interactive security-learning handbook, with basic-to-advanced concepts, searchable lessons, light/dark themes, guided diagrams and synthetic local labs.

Live site: https://kali-naresh.web.app

## Build the book

Requires Python 3.10+.

```sh
python _source/build_book.py
python firebase-hosting/build.py
```

The first command generates START HERE.html, the Markdown handbook and study plan. The second builds the website and downloadable labs in firebase-hosting/public and runs the public-content privacy audit. Open START HERE.html directly for the offline book.

## Preview the web edition

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory firebase-hosting/public
```

Then open http://127.0.0.1:8000 and stop the server with Ctrl+C when finished.

## Publish to Firebase

Requires Node.js/npm and an authorized Firebase account. The CLI version is pinned in package.json. The existing project alias is kali-naresh; use your own project ID for a separate deployment.

```sh
cd firebase-hosting
npm run firebase -- login
npm run firebase -- deploy --only hosting --project kali-naresh
```

Hosting's predeploy hook rebuilds the public folder. No Firebase credentials are stored in this repository. Deployment replaces the selected site's hosted content.

## Edit and validate

Canonical lesson data and browser code are in _source. commands.json contains the numbered reference lessons; build_book.py combines them with the concept guides and examples. Generated books are ignored by Git and are rebuilt from source. Historical patch scripts, browser profiles, screenshots, local backups and cached hosting output are excluded.

Each examples folder documents its prerequisites and expected results. For example:

```sh
python -m unittest discover -s examples/forensics -p 'test_*.py'
python -m unittest discover -s examples/network-assessment -p 'test_*.py'
python -m unittest discover -s examples/web-deep-dive -p 'test_*.py'
```

Labs use synthetic data and intentionally simplified designs. Read each README before running it and test only owned or explicitly authorized systems. Some examples deliberately demonstrate vulnerable behavior for comparison with a repair. Tool documentation does not imply that every optional tool was installed or executed.
