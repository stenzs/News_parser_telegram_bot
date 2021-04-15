import sqlite3
conn = sqlite3.connect('base.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE "users" ( "id" INTEGER, "user_id" TEXT NOT NULL, "status" BOOLEAN NOT NULL DEFAULT 'TRUE', PRIMARY KEY("id" AUTOINCREMENT) )""")
cur.execute("""CREATE TABLE "keywords" ( "key" TEXT NOT NULL, "user_id" TEXT NOT NULL )""")
cur.execute("""CREATE TABLE "categories" ( "name" TEXT NOT NULL, "user_id" TEXT NOT NULL )""")
conn.commit()