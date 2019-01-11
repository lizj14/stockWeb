# stockWeb
A web project for predicting the change of stock prices.

Group Member:
    Boying Wang, Zijie Li, YulongBao

The project is an online stock price predicting system. It allows users to:
* login
* select the stock which the user is interested in, and then review the past history of the stock price.
* input the new prices, and then use the models trained offline to see the prediction of the stock price in future.
* as the prediction result generated, a report which compares the prediction result with the existing ones will be exhibited.

In order to achieve functions above, we utilize following tools:
* Cloud 9 as the HTTP server which allows internet accessment.
* Django as the framework of the whole project and the database of the project.
* BootStrap as the framework of the front end.
* virtualenv equiped with neccessary Python packages provides the elastic running enviromnent
* online predict model with Tensorflow
* coveraged test achieved with the combine of Coverage and Django.test

Following are the interfaces:

* The login:
<img src="/pic/login.png" width="700">

* The select of stock:
<img src="/pic/predict.png" width="700">

* The prediction result:
<img src="/pic/judge.png" width="700">

Coverage test result:
[coverage test](https://htmlpreivew.github.com/?https://github.com/lizj14/stockWeb/coverage_test/index.html)
