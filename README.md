# MSc Group Project Guide

1. [Using our Web App](#web-app)
2. [Getting the Source](#getting-the-source)
3. [Workflow](#workflow)
4. [Merge Requests](#merge-requests)
5. [Virtual Environment](#venv)
6. [Visualisation App (local)](#visualisation-app)
7. [Trouble](#trouble)

<a name="web-app"></a>

## Using our website application

https://visualise-news.herokuapp.com/

<a name="getting-the-source"></a>

## Getting the Source

```
git clone https://gitlab.doc.ic.ac.uk/g21mscprj08/project.git
```

<a name="workflow"></a>

## Workflow

Before creating a new branch, pull the changes from upstream. </br>
Your master needs to be up to date.

```
git pull
```

Create the branch on your local machine and switch into this branch:

```
git checkout -b <name_of_new_branch>
```

**Immediately** push the branch on github:

```
git push -u origin <name_of_new_branch>
```

After doing some work:

```
git add .
```

or

```
git add <file>
```

Commit with an appropriate message in _present-tense_,
using a verb followed by short description:
</br> **Verbs**: add, create, delete, edit, fix
</br> e.g. commit message: fix bug that hides visualisation

```
git commit -m "<commit message>"
```

Push the file:

```
git push
```

Test the code before merging into master branch:

```
cd project
pytest
```

When you are satisfied with your code and want to merge your changes, see Merge Requests!

<a name="venv"></a>

## Virtual Environment

Get in the **VIRTUAL ENVIRONMENT**

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements-dev.txt
```

<a name="visualisation-app"></a>

## Visualisation App

To launch the visualisation app on local:

```
cd project/visualisation_app/frontend
npm install
npm run build
npm start
```

<a name="merge-requests"></a>

## Merge Requests

Go to project URL: https://gitlab.doc.ic.ac.uk/g21mscprj08/project
</br>
Click on "Merge Requests" and create a new one.
</br>
Merge your local branch onto the master branch and ask for approval on the group.

<a name="trouble"></a>

## Trouble

Do not `reset --hard` or `push -f` anything, just ask for help :)

</br></br>
