### Contributing and Feedback:
We welcome any input, feedback, bug reports, and contributions via the DSCI_522_Crime_Prediction_Vancouver Repository
This outlines how to propose a change to DSCI_522_Crime_Prediction_Vancouver

### How To Contribute Code to DSCI_522_Crime_Prediction_Vancouver
Kaggle requires authentications before downloading the file. Refer to the README.md to download data via Kaggle API. 

### Setting Up Your Environment

Fork the repository on GitHub and clone the fork to you local
machine. For more details on forking see the [GitHub
Documentation](https://help.github.com/en/articles/fork-a-repo).
```
$ git clone https://github.com/YOUR-USERNAME/DSCI_522_Crime_Prediction_Vancouver.git
```
You can have a single clone of the repository that points to both your fork and
the main package repository. These pointers to GitHub are called "remotes" .
On your local clone you should run:
```
$ git remote add upstream hhttps://github.com/UBC-MDS/DSCI_522_Crime_Prediction_Vancouver
$ git checkout master
$ git pull upstream master
```
And then you'll have all the updates in the master branch of your local fork.
Note that git will complain if you've committed changes to your local master
branch that are not on upstream (this is one reason it's good practice to **never**
work directly on your master branch).

### Creating a Branch

Once your local environment is up-to-date, you can create a new git branch which will
contain your contribution:
```
$ git checkout -b <branch-name>
```
With this branch checked-out, make the desired changes to the package.

When you are happy with your changes, you can commit them to your branch by running
```
$ git add <modified-file>
$ git commit -m "Some descriptive message about your change"
$ git push origin <branch-name>
```
Finally you will need to submit a pull request (PR) on GitHub asking to merge
your example branch into DSCI_522_Crime_Prediction_Vancouver master branch. For details on creating a PR see GitHub
documentation [Creating a pull
request](https://help.github.com/en/articles/creating-a-pull-request). You can
add more details about your example in the PR such as motivation for the
example or why you thought it would be a good addition.  You will get feed back
in the PR discussion if anything needs to be changed. To make changes continue
to push commits made in your local example branch to origin and they will be
automatically shown in the PR. 

Hopefully your PR will be answered in a timely manner and your contribution will
help others in the future.

### Code of Conduct
Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.
