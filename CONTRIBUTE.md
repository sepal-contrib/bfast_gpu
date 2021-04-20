# SEPAL_UI_TEMPLATE

First off, thank you for considering contributing to the development of this module. It's people like you that make Sepal a living platform. If it's your first time contributing on a github project take a look at this [link](http://makeapullrequest.com/) to better understand what a PR is. 

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

This module is an open source project and we love to receive contributions from our community — you! There are many ways to contribute, from writing tutorials in google Classroom, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into the module itself.

## set up your environment 

SEPAL modules are of course meant to work on the sepal plateform so you should use the same [requirements](https://github.com/openforis/sepal/blob/master/modules/geospatial-toolkit/docker/config/requirements.txt) as we use on the prod platform if you work locally. But of course the easyest way is to work directly from [SEPAL](https://sepal.io) ! 

> don't forget to use the `earthengine authenticate` command to connect to your GEE account.

To develop in this project first fork the module in your own github repositories and clone the repository with a terminal:

```
$ git clone https://github.com/[github_account]/sepal_ui_template.git
```

## how to work with the issue tracker 

If you find yourself wishing for a feature that doesn't exist in this module, you are probably not alone. There should be others out there with similar needs. Many of the features that the module provide today have been added because our users saw the need. Open an issue on our issues list on GitHub which describes the feature you would like to see, why you need it, and how it should work.

As a contributor you can also send PR (pull request) to solve issues tagged as "help wanted" or small correction (typo, documentation improvement, examples). For bigger contributions or new fonctionnalities please open an issue and discuss with our team before sending PR. 

## code guidelines

We try our best to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) rules for python coding. 
This module is develop within the framework of the `sepal-ui` lib, check out its [documentation](https://sepal-ui.readthedocs.io/en/latest/) to better understand the design guidelines. 
