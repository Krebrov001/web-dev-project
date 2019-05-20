# starter_repo
Konstantin Rebrov Assignment 3 Django Getting Started
Repo to initialize class repositories from, setups initial CI/CD for gitlab as well

# description of my Javascript code and what it does
On many programming blogs, it is common to add code snippets into suggestions because the people using these blogs are engineers, not just the general public. They have a different set of requirements for how their suggestions look. Each code snippet needs to be formatted as code, preserving whitespace, in a separate code box, and easily copy/pasteable.

So for one of the fields in my form I have a textarea, where the user can write their response. I had the idea of letting the user also type in code into the response form, and then the code should be displayed on the page inside the "suggestion".
Any code should be surrounded by the ``` above and below. So for example, if the user enters:
```
fprintf(stderr, "your number is %ld\n", number);
```
Any text inside the ``` should be neatly formatted with whitespace preserved inside a "code box".

For the Assignment 5, I created my own custom Javascript which looks for text inside the ``` in the suggestion, and automatically formats it and puts it into a "code box" so that the code is displayed as code, and would be easily copy/pasteable. This is done after the HTML files have already arrived from the server side. Only the code delimiters ``` are actually stored in the model. The Javascript makes sure that the code within them gets shown on the webpage as actual code, with all the desired properties described above.

The source code of this Javascript is inside the article1.html file, at the very bottom in the scripts template tag.

## regular files

* **Dockerfile** - Initial dockerfile to help us setup our environment
* **docker-compose.yml** - Initial starter docker-compose file
* **requirements.txt** - Blank requirements.txt file for us to add python package requirements into

## hidden files

* **.gitignore** - ignores python code & macOS generated files that don't need to be in the repo
* **.gitlab-ci.yml** - initial CI/CD pipeline file that will be used in CINS465 during class, should be modified to fit your project/code
* **.coveragerc** - provides initial settings for the coverage.py package to test our CI testing coverage and omit specific files/folders/lines that are problematic. This will need to be moved and modified to be useful, and will be introduced in class. 
