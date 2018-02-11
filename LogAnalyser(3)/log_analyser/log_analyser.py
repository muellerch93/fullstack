#!/bin/env python2.7
import psycopg2

try:
    conn = psycopg2.connect("dbname=news")
except:
    print "I am unable to connect to the database"


cur = conn.cursor()
# most popular (viewed) articles, join articles and log table on slug/path
cur.execute("""
        SELECT articles.title, count(*) as num
        FROM articles
        JOIN log ON '/article/' || articles.slug = log.path
        GROUP BY articles.author,articles.title, log.path
        ORDER BY num desc LIMIT 3
""")
print "\n------------------------------------------------------\n"
print "What are the most popular three articles of all time?\n"
rows = cur.fetchall()
for row in rows:
    print "\"%s\" - %s views" % (row[0], row[1])
print "\n------------------------------------------------------\n"

# most popular (viewed), get most viewed articles and join with autors table
print "Who are the most popular article authors of all time?\n"
cur.execute("""
        SELECT authors.name, sum(view_count) as sum_views
        FROM(
            SELECT articles.author, count(*) as view_count,log.path
            FROM articles
            JOIN log ON '/article/' || articles.slug = log.path
            GROUP BY log.path,articles.author
        ) AS most_read_articles
        JOIN authors ON most_read_articles.author = authors.id
        GROUP BY author, authors.name
        ORDER BY sum_views desc
""")
rows = cur.fetchall()
for row in rows:
    print "%s - %s views" % (row[0], row[1])
print "\n------------------------------------------------------\n"

# days with more than 1% of requests led to a HTTP 404 response
# truncate date to achieve day precision, group by day, self join on logs
cur.execute("""
        SELECT to_char(all_logs.all_day,'Month DD,YYYY'),
                error_logs.error_count::float/all_logs.all_count
        FROM(
            SELECT count(*) AS all_count,date_trunc('day',log.time) as all_day
            FROM log
            GROUP BY  all_day
        ) AS all_logs
        JOIN(
            SELECT count(*) AS error_count,
                    date_trunc('day',log.time) as error_day
            FROM log
            WHERE log.status = '404 NOT FOUND'
            GROUP BY error_day
        ) AS error_logs ON all_logs.all_day = error_logs.error_day
        WHERE error_logs.error_count::float/all_logs.all_count > 0.01
""")
print "On which days did more than 1% of requests lead to errors?\n"
rows = cur.fetchall()
for row in rows:
    print "%s - %.2f%% errors" % (row[0], row[1]*100)
print "\n------------------------------------------------------\n"
