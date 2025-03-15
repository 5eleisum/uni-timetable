# University Timetable
This is a project that I made for my Bachelor's Degree in Informatics.

## How to run
After downloading the files, open the terminal or command prompt and type `py manage.py createsuperuser` to create a superuser that allows you to log into the administrative site.
Once you create the superuser by inserting the desired credentials, run the command `py manage.py runserver [port]` (the port can be anything you want. By default it uses port 8000), at which point you can access the site at 127.0.0.1:[port].
When you access the URL, you'll be met with the main page and two links, one going for the timetable itself and the other going for the admin login page.

## Admin page
Here, you can log in using the credentials you inserted when you created the superuser. From here, you can change the database (which uses SQLite3) however you want. Although, I recommend not deleting the records in "hours" as the code behind the Timetable template requires the records to remain as they are. To add a registry to a table, you can click the `Add` button next to said table or, if you want to change/edit a registry, click the `Change` button next to the `Add` button.
