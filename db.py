from sqlalchemy import create_engine, select, MetaData, Table, Column

# A basic wrapper to access data from the China Biographical Database
# https://projects.iq.harvard.edu/cbdb/download-cbdb-standalone-database
class CBDB:
    def __init__(self, db_path="D:/databases/chinabiographicaldatabase/cbdb_20201110.db"):
        self.path = "sqlite:///" + db_path
        self.engine = create_engine(self.path)
        self.conn = self.engine.connect()
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        
    # generate a list of the table names
    def list_tables(self): 
        return list(self.meta.tables.keys())

    # generate a list of columns from a given table
    def list_table_columns(self, table):
        if table in self.meta.tables:
            return self.meta.tables[table].columns.keys()
        else:
            return None

    # query the main table, looking for people by name
    # optionally specify a list of columns to return, otherwise return all
    def query_name(self, name, exact=False, select_columns=[]):
        active_table = Table('BIOG_MAIN', self.meta)

        # establish which columns to return
        if len(select_columns) == 0:
            select_columns = [active_table]
        else:
            select_columns = [Column(c) for c in select_columns]

        # if the name does not need to be exact, allow for incomplete namnes
        # so 王安 would return names like 王安石 (in addition to 王安)
        if not exact:
            name_search = active_table.columns.c_name_chn.contains(name)
        else:
            name_search = active_table.columns.c_name_chn == name

        query = select(select_columns).where(name_search)

        return list(self.conn.execute(query))

    # query the database based on year range. you can search index year,
    # birth year, death year, or a combo of birth and death years. Note that
    # index year will return the most results, as index years are used for the 
    # vast majority of entries, but many are missing birth/death years
    def query_year_range(self, start_year, end_year, search="index", 
                        select_columns=[]):
        active_table = Table('BIOG_MAIN', self.meta)

        if len(select_columns) == 0:
            select_columns = [active_table]
        else:
            select_columns = [Column(c) for c in select_columns]

        if search == "index":
            term_1 = active_table.columns.c_index_year >= start_year
            term_2 = active_table.columns.c_index_year <= end_year 
        elif search == "birth":
            term_1 = active_table.columns.c_birthyear >= start_year
            term_2 = active_table.columns.c_birthyear <= end_year
        elif search == "death":
            term_1 = active_table.columns.c_deathyear >= start_year
            term_2 = active_table.columns.c_deathyear <= end_year
        elif search == "combo":
            term_1 = active_table.columns.c_birthyear <= start_year
            term_2 = active_table.columns.c_deathyear >= end_year

        query = select(select_columns).where(term_1).where(term_2)
        return list(self.conn.execute(query))

    # Queries names and dates at the sametime. Useful to differentate people
    # with the same name living at different times.
    def query_name_date(self, name, start_year, end_year, exact=False, 
                        search="index", select_columns=[]):
        active_table = Table('BIOG_MAIN', self.meta)


        if len(select_columns) == 0:
            select_columns = [active_table]
        else:
            select_columns = [Column(c) for c in select_columns]

        if not exact:
            name_search = active_table.columns.c_name_chn.contains(name)
        else:
            name_search = active_table.columns.c_name_chn == name

        if search == "index":
            term_1 = active_table.columns.c_index_year >= start_year
            term_2 = active_table.columns.c_index_year <= end_year 
        elif search == "birth":
            term_1 = active_table.columns.c_birthyear >= start_year
            term_2 = active_table.columns.c_birthyear <= end_year
        elif search == "death":
            term_1 = active_table.columns.c_deathyear >= start_year
            term_2 = active_table.columns.c_deathyear <= end_year
        elif search == "combo":
            term_1 = active_table.columns.c_birthyear <= start_year
            term_2 = active_table.columns.c_deathyear >= end_year

        query = select(select_columns).where(name_search).where(term_1) \
                        .where(term_2)

        return list(self.conn.execute(query))                


    def close(self):
        self.conn.close()

# Demoing some of the functions
if __name__ == "__main__":
    # create the CBDB object (you'll need to specify where you put the db)
    cbdb = CBDB(db_path="D:/databases/chinabiographicaldatabase/cbdb_20201110.db")

    # Search for Wei Zhongxian
    print(cbdb.query_name("魏忠賢"))

    # Find people alive between 1640 and 1645:
    print(cbdb.query_year_range(1640,1645,search="combo",
                                select_columns=["c_name_chn","c_index_year",
                                "c_birthyear", "c_deathyear"]))

    # Find people named Lu Jingzheng with an index year between 1600 and 1700
    print(cbdb.query_name_date("陸經正", 1600,1700,search="index",
                                select_columns=["c_name_chn","c_index_year"]))
    cbdb.close()
