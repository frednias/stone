import psycopg2

class PostgreSql:

    def __init__(self):
        # Connect to an existing database
        self.conn = psycopg2.connect("dbname=brewsim user=brewsim")
        self.openCursor()

    def openCursor(self):
        # Open a cursor to perform database operations
        self.cur = self.conn.cursor()

    def exec(self, sql, values):
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        self.cur.execute(sql, values)
        return self.cur.rowcount

    def query(self, sql):
        # Query the database and obtain data as Python objects
        self.cur.execute(sql)
        self.cur.fetchone()
        # (1, 100, "abc'def")

    def commit(self):
        # Make the changes to the database persistent
        self.conn.commit()

    def closeCursor(self):
        # Close communication with the database
        self.cur.close()
        self.conn.close()

    def get(self):
        return self.cur.fetchone()


class Vdb:

    def query(self, table):
        self.table = table
        return self

    def set(self, set):
        self.set = set
        return self

    def values(self, values):
        self.values = values
        return self

    def where(self, where):
        self.where = where
        return self

    def equals(self, equals):
        self.equals = equals
        return self

    def update(self):
        sql = "update " + self.table + " set "
        for k,v in self.set.items():
            sql += "{}=%({})s, ".format(k, k)
        sql += "upd_date=now() where "
        for k,v in self.where.items():
            sql += "{}=%({})s and ".format(k, k)
        sql += "del_date is null"
        print(sql)

        pg = PostgreSql()
        pg.exec(sql, dict(list(self.set.items())+list(self.where.items())))
        pg.commit()

    def insert(self):
        s1 = '';
        s2 = '';
        for k, v in self.values.items():
            s1 += k + ","
            s2 += "%({})s,".format(k)
        sql = "insert into "+self.table+" ("+s1+"ins_date) values ("+s2+"now())"
        print(sql)

        pg = PostgreSql()
        n = pg.exec(sql, self.values)
        pg.commit()
        return n

    def count(self):
        sql = "select count(*) from "+self.table+" where "
        for k,v in self.where.items():
            sql += "{}=%({})s and ".format(k, k)
        sql += "del_date is null"
        print(sql)

        pg = PostgreSql()
        pg.exec(sql, self.where)
        row = pg.get()
        return row[0]
        

