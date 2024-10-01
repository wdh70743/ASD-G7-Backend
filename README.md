<p align="center">
  <img src="https://img.icons8.com/?size=512&id=55494&format=png" width="20%" alt="ASD-G7-BACKEND-logo">
</p>
<p align="center">
    <h1 align="center">ASD-G7-BACKEND</h1>
</p>
<p align="center">
    <em>Streamlining Tasks, Driving Developments. Simplifying Backend Management, One Code at a time!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/wdh70743/ASD-G7-Backend?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/wdh70743/ASD-G7-Backend?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/wdh70743/ASD-G7-Backend?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/wdh70743/ASD-G7-Backend?style=flat&color=0080ff" alt="repo-language-count">
</p>
<p align="center">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
</p>

<br>

#####  Table of Contents

- [ Overview](#-overview)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
    - [ Prerequisites](#-prerequisites)
    - [ Installation](#-installation)
    - [ Usage](#-usage)
    - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)

---

##  Overview

Same environment across various platforms, thereby, enabling consistency and reliability in the execution of the projects functionalities. This is a comprehensive Django-based project designed to serve as the backend environment for an efficient TaskManager application. Leveraging containerization, the Dockerfile accentuates project setup by organizing the Python environment, executing dependencies installation, database migrations, and initiating the Django application. The integration of automated testing and deployment is expertly brought to life by azure-pipelines.yml, allowing for the seamless execution of Python tests across multiple versions, Docker image building, and pushing to DockerHub. It supports the continuous integration and delivery (CI/CD) process, playing a pivotal role in the project's efficiency and delivery speed.The project bolsters user management with create_superuser.py, automating the creation of superusers and enhancing the usability and maintainability of the application. manage.py serves as an effective command-line utility, streamlining administrative tasks and debugging, fostering easy project management. The requirements.txt file encapsulates all the project dependencies, ensuring the application's reliable execution across various platforms by maintaining the testing and deployment environment's consistency.In essence, ASD-G7-Backend is a robust, open-source tool that enhances task management through swift setup, streamlined user management, consistent testing and deployment, and reliable project execution. The value of this project lies in its efficiency, reliability, and maintainability, making it an invaluable resource in the realm of task management applications.

---

##  Repository Structure

```sh
└── ASD-G7-Backend/
    ├── Dockerfile
    ├── azure-pipelines.yml
    ├── create_superuser.py
    ├── manage.py
    ├── project
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── requirements.txt
    ├── task
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── taskmanager
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── users
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations
        ├── models.py
        ├── serializers.py
        ├── tests.py
        ├── urls.py
        └── views.py
```

---

##  Modules

<details closed><summary>utils</summary>

| File | Summary |
| --- | --- |
| [Dockerfile](https://github.com/wdh70743/ASD-G7-Backend/blob/main/Dockerfile) | Dockerfile sets up the Python environment and launches the Django application for the ASD-G7-Backend repository. It installs dependencies, executes database migrations, creates the superuser, and runs the server, preparing the environment for the TaskManager and associated apps. |
| [azure-pipelines.yml](https://github.com/wdh70743/ASD-G7-Backend/blob/main/azure-pipelines.yml) | Azure-pipelines.yml manages the automated testing and deployment of the ASD-G7-Backend repository. It conducts tests on multiple Python versions and reports the results, syncs with the DockerHub registry for image building and pushing, and supports the overall projects continuous integration and delivery (CI/CD) process. |
| [create_superuser.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/create_superuser.py) | Creates a superuser for the Django-based ASD-G7-Backend project, which facilitates easy management of the system. It employs Djangos authentication model, automating the process if the specified superuser doesnt exist, and provides relevant feedback, enhancing maintainability and usability of the backend application. |
| [requirements.txt](https://github.com/wdh70743/ASD-G7-Backend/blob/main/requirements.txt) | Requirements.txt declares all dependencies necessary for the ASD-G7-Backend repository. It assists in reproducing the environment consistently across multiple setups, ensuring the smooth functioning of modules like task, taskmanager, project, and user. |

</details>

<details closed><summary>project_main_folder</summary>

| File | Summary |
| --- | --- |
| [asgi.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/taskmanager/asgi.py) | Taskmanagers ASGI script sets up the Asynchronous Server Gateway Interface configuration and designates the taskmanager.settings' as the default Django settings module. It exposes the ASGI application through a module-level variable, enabling asynchronous communication between the server and the application. |
| [wsgi.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/taskmanager/wsgi.py) | Taskmanagers wsgi.py configures the Web Server Gateway Interface (WSGI) for the project, setting up the environment for the applications settings and exposing the WSGI application callable at the module level. This augments the project's deployment capabilities. |
| [urls.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/taskmanager/urls.py) | TaskManagers urls.py' connects various functions in the system to specific URLs, enabling user interaction with the user, project, and task elements. In debug mode, it also provides Swagger and Redoc interfaces for API documentation, further improving usability. |
| [manage.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/manage.py) | Manage.py serves as a command-line utility for performing administrative tasks in the Django-based ASD-G7-Backend repository. It sets the default Django settings module and executes tasks directly from the command line, facilitating convenient project management and debugging. |
| [settings.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/taskmanager/settings.py) | The `taskmanager/settings.py` file is a pivotal piece of the `ASD-G7-Backend` repository. It defines crucial configurations for the Task Manager project, which is primarily developed using Django-a high-level Python web framework. This settings file contains all the necessary parameters to shape the behaviour of the application, including database connections, middleware configurations, installed apps, template settings and more.The settings file is auto-generated by the Django-admin start project command. Although it's mostly a boilerplate, it often requires careful adjustment to align with the project's specifics. It's a central hub that ties together the different components within the task, project, and users directories, facilitating smooth and coordinated functioning of the overall backend mechanism.This task manager backend repository appears to maintain an MVC-like (Model, View, Controller) structure, with the `settings.py` arguably serving a role akin to that of a controller, directing the architectures overall functionality. |

</details>

<details closed><summary>project</summary>

| File | Summary |
| --- | --- |
| [serializers.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/serializers.py) | Project/serializers.py establishes data interaction for the Project model and User model, providing serialization for efficient data conversion. It defines UserSerializer and ProjectSerializer, supporting multiple users per project and delivering full-field access to project data. |
| [admin.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/admin.py) | Project/admin.py pairs Django's administrative interface with the Project's model, providing customization options for display, search, and filtering. It facilitates smooth managerial actions, comprising a key component in the ASD-G7-Backend's architecture. |
| [apps.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/apps.py) | ProjectConfig, located in project/apps.py, serves as a configuration center for the project module in the ASD-G7-Backend repository. It leverages Django's AppConfig to set the default auto field and specify the app's name. |
| [tests.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/tests.py) | Tests within the project module are written and managed in tests.py. It leverages Django's built-in TestCase for creating comprehensive tests that verify the functionality and reliability of the project's features. |
| [views.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/views.py) | The `views.py` file under the `project` directory in the `ASD-G7-Backend` repository is integral to the applications interface layer. It holds the logic for processing the incoming HTTP requests and mapping them to appropriate models, subsequently returning the appropriate HTTP responses.Its primary function is to handle interactions between the system and its users, mainly through the REST framework provided by Django. The code leverages generic views and mixins to create endpoints for the application, and it manages permissions to secure those endpoints. It uses decorators to enhance or modify its functions. This file is a critical component in managing interactions with the User model in the system and effectively contributes to shaping the overall behavior of the web application. |
| [urls.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/urls.py) | Maps URL routes to specific project functions in the ASD-G7-Backends Django application, enabling project creation, retrieval, update, deletion, and user-specific project listing. These routes integrate with the corresponding views for managing data flow and rendering responses. |
| [models.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/project/models.py) | Project/models.py defines the structure and data attributes for each project in ASD-G7-Backend, including fields such as project name, description, start date, end date, priority level, status, creation and updated timestamps, and associated users. |

</details>

<details closed><summary>users</summary>

| File | Summary |
| --- | --- |
| [serializers.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/serializers.py) | UserSerializer, threaded into the users module, translates User model data for API interactions. It employs Django's REST Framework serializer for model conversion to JSON, exposing all user attributes and conforming to the UsersAppUserSerializer reference name. |
| [admin.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/admin.py) | Administers user data by registering the user model in Djangos admin interface, displaying their id, email, password, and creation time. This functionality forms a crucial part of the users module within the overall ASD-G7-Backend repository structure. |
| [apps.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/apps.py) | UsersConfig in users/apps.py sets configuration for the users application, defining the default auto field type and the application name within the ASD-G7-Backend project repository. |
| [tests.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/tests.py) | The `users/tests.py` file is part of the `ASD-G7-Backend` repository, specifically within the `users` module. It is crucial for maintaining the robustness and reliability of our application as it holds all the tests related to user functionalities. This file contains unit tests that ensure the correct behavior of the user-related views and models. Through these tests, we validate the application's ability to create users, authenticate users, handle user data, and interact correctly with the database. The tests leverage Djangos testing framework and the REST framework's APITestCase to facilitate HTTP request-response cycle testing. These tools help us to simulate and validate the behavior of the RESTful APIs in our application. This is a necessary component of our continuous integration and continuous deployment (CI/CD) strategy, allowing us to catch and fix bugs early in the development process. |
| [views.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/views.py) | The `users/views.py` file is a key component of the `ASD-G7-Backend` repository. Acting as a crucial point within the Django backend structure, it handles the application logic for user-related actions and provides API endpoints with which the client interacts.In broad terms, this file is responsible for processing HTTP requests that are related to the management of user actions. With the imports of modules such as Django's JsonResponse and csrf_exempt, Rest Framework's generics, mixins, status, and response, as well as Django's make_password and check_password, it suggests the file deals with utilities for HTTP responses, cross-site request forgery protection, standard interface for list and object views, HTTP status codes, and password hashing. In essence, the code in `users/views.py` manages user-based functionality such as creating, reading, updating, and deleting user data, as well as securing user data with hashed passwords. |
| [urls.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/urls.py) | Users/urls.py contributes to the routing framework of the ASD-G7-Backend repository, guiding the endpoint traffic to the appropriate User operations. It distinctly handles user creation, individual user retrieval, update or deletion, and user login processes, helping shape the user management flow. |
| [models.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/users/models.py) | Models the User entity within the users module of the ASD-G7-Backend project. It defines essential attributes such as username, email, password, and timestamps for creation and update. Returns the email of a user as a string representation. Unique email addresses enforce user uniqueness in the system. |

</details>

<details closed><summary>task</summary>

| File | Summary |
| --- | --- |
| [serializers.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/serializers.py) | TaskSerializer in task/serializers.py leverages Django's REST Framework to convert Task model data into a format that is easily renderable into JSON or other content types, decked with all attributes of the model, fitting into the larger backend architecture. |
| [admin.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/admin.py) | Task/admin.py manages the administrative interface for the Task model within the ASD-G7-Backend repository. It configures the display of tasks in the admin panel, including fields such as id, owner, project, title, priority, and status. |
| [apps.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/apps.py) | TaskConfig in task/apps.py configures the task application by setting the default auto-field behavior and specifying the app name within the ASD-G7-Backend repository's Django framework. |
| [tests.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/tests.py) | This `tests.py` file is part of the task' module in the parent repository, ASD-G7-Backend. Its primary purpose is to host unit tests for the functionality of the task module. These tests ensure that the crucial components and functionality of the task module, such as task creation, task management, and other task-related operations, are working as expected, providing a necessary layer of quality assurance.The tests are implemented using Django's TestCase and REST framework's status and test classes, which facilitate HTTP request simulation, assertion formation, and response evaluation in the context of RESTful architecture. This includes testing the task-related endpoints defined in the urls.py file of the same module.In essence, this file aims to validate that the task-related functions of the ASD-G7-Backend repository correctly and efficiently deliver their intended functionalities, contributing to the integrity and robustness of the entire project. |
| [views.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/views.py) | The `task/views.py` file in the ‘ASD-G7-Backend’ repository is mainly responsible for managing the applications interface with the user. In essence, it deals with the presentation logic of the task module, specifying how requests to the app are handled and responses are structured.This file employs the Django web framework and its REST framework to facilitate the creation of web APIs. It handles the rendering of user tasks, implements view mixes for common behavior, and interacts with task-related models and serializers to process data for HTTP responses.Being an integral part of the larger task application, this file contributes to the overall functionality of the ASD-G7-Backend repository, which includes numerous other components such as a project app, a users app, and the core taskmanager app. Overall, this file ensures the task' app's interactions are performed in line with the standards set by Django and the REST framework. It fuels the efficient management of tasks in the project, providing end-users with seamless navigability and use. |
| [urls.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/urls.py) | Task/urls.py registers URL paths for the task-related functions. It provides endpoints for task creation, retrieving tasks based on specific projects or users, handling task archival, accessing user-specific archived tasks, and managing tasks (retrieve, update, destroy) via their primary key. |
| [models.py](https://github.com/wdh70743/ASD-G7-Backend/blob/main/task/models.py) | The `task/models.py` file is part of the `ASD-G7-Backend` repository, specifically residing within the task' subdirectory. This file is dedicated to defining the models associated with tasks in the project, particularly those concerned with priority and status. In the context of the overall repository's structure, `task/models.py` contributes to building an object-relational map for task-related data, facilitating how the application interacts with its backend database. The code contained in this file primarily focuses on declaring priority and status choices that a task can have, making the task categorization more structured and consistent. These defined models can then be used in other parts of the application such as in view handling or during serialization. In essence, the `task/models.py` forms the data structure backbone for the task management aspect of the entire project. It helps to ensure that the application effectively handles and categorizes task data according to the defined priorities and statuses. |

</details>

---

##  Getting Started

###  Prerequisites

**Python**: `version 3.10`

###  Installation

Build the project from source:

1. Clone the ASD-G7-Backend repository:
```sh
❯ git clone https://github.com/wdh70743/ASD-G7-Backend
```

2. Navigate to the project directory:
```sh
❯ cd ASD-G7-Backend
```

3. Install the required dependencies:
```sh
❯ pip install -r requirements.txt
```

###  Usage

To run the project, execute the following command:

```sh
❯ python manage.py runserver
```

###  Tests

Execute the test suite using the following command:

```sh
❯ python manage.py test
```

---

##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement R0.</strike>
- [ ] **`Task 2`**: <strike>Implement R1.</strike>
- [ ] **`Task 3`**: Implement feature three.

---
