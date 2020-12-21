# A small Python Class for integrating the Chinese Biographical Database with your Python workflow
This is a very small utility that I use to query CBDB in my Python scripts. Feel free to suggest new queries, analyses, and so on, in the issues!

## Use
### "Installation"
Download db.py and put it in the folder with the rest of your code. You will also need to download the [Standalone CBDB SQLite database, which you can find on the CBDB website.](https://projects.iq.harvard.edu/cbdb/download-cbdb-standalone-database) Uzip the database and you are ready to go.

### demo
```python
from db import CBDB

# create CBDB object
cbdb = CBDB("path/to/database")
```
Once you've created the cbdb object, you can start running queries and gathering info

```python
# print table names
print(cbdb.list_tables())

# print table columns
print(cbdb.list_table_columns("BIOG_MAIN"))
```
By default most queries will run on the BIOG_MAIN table

```python
# basic name search
wang_ans = cbdb.query_name("王安") # cbdb.query_name("王安", exact=True) will match 王安 exactly
print(names)
```
For all queries, you can sepecify selected_columns, which will return only the columns you ask for (otherwise you will get all back)


```python
# basic date search
folks_from_seventeenth_cent = cbdb.query_year_range(1600, 1700, search="index", select_columns=["c_name_chn", "c_index_year"])
```
You can also set "search" to "birth", "death", or "combo" (which will return people who were alive between the two dates. But do note that this information is missing for many people within the database, and this will truncate your results.


You can also query name and dates at the same time
```python
# name and date search
cbdb.query_name_date("陸經正", 1600,1700,search="index", select_columns=["c_name_chn","c_index_year"]))
```
