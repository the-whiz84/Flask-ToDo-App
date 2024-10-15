# To-Do App using Python and Flask

## Description
A simple to-do app built with Python using the Flask framework. The app allows users to create, edit, and manage their tasks. This project is part of my capstone project portfolio based on [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Angela Wu.It is designed to showcase my skills in web development using Flask and various other technologies.

Current functionality only allows user to edit tasks in a single master to do list. For future improvements, I'd consider creating a functionality to manage different to do lists (like a traditional Reminders app) and viewing completed tasks. 
![Current Version of the App](images/Home_Page.png)

## Table of Contents
- [Usage](#usage)
- [Features](#features)
- [Future Improvements](#future-improvements)
- [Technologies Used](#technologies-used)
- [Challenges Faced](#challenges-faced)
- [Contact Information](#contact-information)
- [Acknowledgments](#acknowledgments)
- [Links](#links)


## Usage
1. Run the app: `python main.py`
2. Open a web browser and go to `http://127.0.0.1:5000`
3. You will be greeted with a `Landing Page`![Landing Page](images/Landing_Page.png)
4. Use `Register` menu to create a user account ![`Register`](images/Register_Page.png) 
5. You will be redirected to the `Home` page to add Tasks
6. Existing users can use the `Login` page to log in to their home page ![`Login`](images/Login_Page.png) 
7. Interact with the app to create, resolve and delete your tasks.

## Features
- Create tasks with descriptions and due dates.
- Mark tasks as completed (which will also apply a strikethorugh and a `Completed` badge).
- Delete tasks that you no longer want and they will be removed from the page and database.

## Future Improvements
After I tackle a few other projects, I'd consider enhancing the app in the future, including:
- Give user ability to sort to-dos by name, due status, or due date.
- Give user ability to create different lists with to do tasks.
- Give user ability to move tasks between lists.
- Implementing task categorization and filtering.

## Technologies Used
- Python
- Flask
- HTML
- SQL-Alchemy
- WTForms
- Bootstrap5 (CSS Framework)

## Challenges Faced
One of the biggest challenges of creating this app was writing html and css code. I'm also not very familiar with bootstrap framework so it took a lot of experimenting and debugging to get the app going. 

For example, I initially used HTML tables to display the list of tasks, but I couldn't get it to display the way I wanted. I found a work-around by using containers and divs. Here's what an earlier draft looked like: 
![Earlier Version of the App](images/first-version-of-my-to-do-app.png)

## Contact Information
I welcome any feedback from the community and you're welcome to fork the repository for your own project. 
You can reach me at [roman.pk@yahoo.com](mailto:roman.pk@yahoo.com).

## Acknowledgments
- [Bootstrap](https://getbootstrap.com) - CSS framework for styling.
- [Pandas](https://pandas.pydata.org) - Used for data manipulation.

## Links
- Live Demo - TBA 
- [GitHub Repository](https://github.com/roman-pk/To-Do-App-Python-Flask)