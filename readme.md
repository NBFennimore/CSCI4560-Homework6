
## Dependencies
- Flask
- SQLAlchemy
- Flask-wtf
- wtforms

## Starting The App
1.  Open main.py and change the values of the following variables to match your local sql database
	- username
	- password
	- server
	- dbname
2. open a terminal at the same location as main.py and enter the following command
	-  ` flask --app main run --debug
3. Type "http://127.0.0.1:5000/" into the address bar of your web browser to begin using the app

## Using The App

### Insert Tuple Into Shipment Table
On the home page, fill out the four fields and the press the submit button. A success/fail message will then be displayed below after the data has been submitted


### Updating Supplier Status
Click the "Update Supplier Status" link at the top of any page. This will direct you to a page that queries and displays all the data currently stored in the Supplier table. Clicking on the button will query for all the values in the "Status" column, increase them by 10%, and then update all the rows with this new value. The page will be reloaded and you should see the change reflected in the table.

### Part Lookup
Click the "Part Lookup" link at the top of any page. On this page, enter the part number you wish to lookup and press submit. If the part number exists in the database, all the information about the suppliers of that part will be displayed in the table below. If it does not exist, the table with be empty