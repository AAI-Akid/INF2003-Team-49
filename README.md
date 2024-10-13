# INF2003-Team-49
Database Systems Project

## Downloading MySQL Server and Workbench
Download MySQL installer here: https://dev.mysql.com/downloads/installer/.

1. Run MySQL installer

2. Choose Full Setup type

   
![Full Setup Type](mysql_installation/setuptype.png)

3. Click 'execute' to install all products.


![Execute Installation](mysql_installation/installation.png)

4. Configure MySQL Server (if you have MariaDB installed, its most likely running on port 3306. Change the port for your MySQL Server to another available port, e.g. 3307).


![MySQL Server Configuration](mysql_installation/mysqlserver.png)

5. Use strong password authentication


![Authentication Method](mysql_installation/auth.png)

6.  Set root user password (your own password)

7. Start MySQL Server at System Startup. Use Standard System Account. Apply configuration.

8. Use default configuration for other MySQL products.

9.  Check to see if can connect to server. If not check if password and username (default root) is correct.


![alt text](mysql_installation/connection.png)

10. Start MySQL workbench after setup.

## Setting up database

1. Click on `Local instance MySQL80` and enter password (take note which port your MySQL Server is running on).
![MySQL Server Instance](mysql_installation/server.png)

2. In top left, under `File` tab, select `Open SQL script`. Open `bookstore.sql` (from github repo).

![Running SQL script](mysql_installation/openscript.jpg)

![Running SQL script2](mysql_installation/sqlscript.png)


3. Highlight text show in photo below, and click the lightning button (circled in red).
![Run SQL script](mysql_installation/firststep.png)

4. Refresh the SCHEMAS on the left.

![Schema Refresh](mysql_installation/refresh.png)

5. In the navigation pane, click `Schemas`. Make sure that `bookstore` has been created.

![Bookstore DB added](mysql_installation/schemas.png)

6. Import table found in Github Repo named: trimmed_books_data50rows.csv. Steps:

![Import Table Data Wizard](mysql_installation/tableimportdatawizard.png)

![Browse](mysql_installation/browse.png)

![Dataset](mysql_installation/dataset.png)

![next](mysql_installation/next.png)

![existingtable](mysql_installation/existingtable.png)

7. Remember to untick book_id!

![Untick book id](mysql_installation/untickbookid.png)

![Final](mysql_installation/final.png)

![Finish 1](mysql_installation/finish1.png)

![Finish 2](mysql_installation/finish2.png)

8. Checking if data has been imported correctly

![check1](mysql_installation/check1.png)

9. Running rest of the scripts

![runrest](mysql_installation/runrest.png)

10. Refresh Schema to check if everything is in

![runrest](mysql_installation/refreshfinal.png)

11. Your final schema page should look like this

![schemafinal](mysql_installation/finalschema.png)

## Running app.py

1. Make sure requirements are installed. If not, run `pip install -r requirements.txt`.

2. Run `python app.py`. Open web browser and go to `http://127.0.0.1:5000`.


![Website](mysql_installation/website.png)
