# Timechange

#### Description

The purpose of the Timechange project is to design an open source software tool that simplifies as much as possible the task of sophisticated ML analysis of time series data. Moreover, Timechange will be unique in that it will serve as a one stop shop solution for data input, pre-processing, and transformation, as well as training and evaluation of state-of-the-art deep learning methods. 


The focus with regards to the design of this system during the Spring 2017 Software Engineering course, will be on the implementation of features that will allow the system to generate images from transformed time series data, and then to use these images to train a deep learning model such as a convolutional neural network.


The focus with regards to the design of this system during the Fall 2017 Software Engineering course, will be: 
1. Converting Timechange into a web app through use of Flask
2. Addition of the ability to train RNNs 

#### Installation
1. Clone this project using git

2. install virtualenv
```
pip install virtualenv
```

#### Usage Instructions

1. Create and run a virtual environment
```
#creates project
virtualenv my_project             

#activates projects
source my_project/bin/activate    
```

2. Change to web directory

```cd web```

3. Install requirements to run app

```pip install -r requirements.txt```

4. start server 

```python manage.py runserver```

5. Enter the following address in your favorite browser

```localhost:5000```

#### Error: Too Many Open Files

You'll see this error if you try to upload more files than your system settings currently permit. This is not as big of an issue as it may seem at first.

[Linux users should look here](http://posidev.com/blog/2009/06/04/set-ulimit-parameters-on-ubuntu/)

[Unix users should look here](https://blog.dekstroza.io/ulimit-shenanigans-on-osx-el-capitan/)