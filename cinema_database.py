#from _tkinter import create
import psycopg2
import sys

con = None

try:
    con = psycopg2.connect(database='movie_database',
                           user='postgres',
                           password='agfreckles')
    cur = con.cursor()

    st = 'what do want to do ? \ncreate(c), delete(d) or view(v) an item?: '
    cr = "What do u want to create? \na movie(m), rating(r), theater(t) or showing(s): "
    delt = "What do u want to delete? \n a movie(m), rating(r), theater(t) or showing(s): "
    view = "\nView show by a particular movie(m), date(d), all(a) or theater(t): "

    movieid = "Enter movie ID: "
    ratingid = "Enter new rating ID: "
    roomid = "Enter room ID: "
    showingid = "Enter showing ID: "

    movietitle = "Enter new title of your new movie: "

    releasedate = "Enter release date (YEAR-MM-DD): "
    enddate = "Enter end date (YEAR-MM-DD): "
    showdate = "Enter date to show movie\nIt should be in the format YEAR-MM-DD: "

    ratingcode = "Enter new rating code: "
    description = "Enter description of the new rating: "
    name = "Enter name of the new theater: "

    showtime = "Enter time to show movie\nMovies can be shown" +\
               "between 10am-8pm of two hours difference except 4pm\nIt should be in the format HH:MM: "

    dur = "Enter duration of movie in minutes: \n"
    capacity = "Enter the total capacity of the new theater *\n50, 60 or 100: "
   
    def insert(sql):
            try:
                cur.execute(*sql)
                con.commit()
                print 'You have succesfully added a movie'
            except psycopg2.DatabaseError, e:
                if con:
                    con.rollback()
                print 'Error %s' % e
                sys.exit(1)
                print "error inserting into database"
            finally:
                if con:
                    con.close()
            return

    def delete(table, rowid, itemid):
        dsql = "DELETE FROM " + table + " CASCADE WHERE " + rowid + " = "+str(itemid)+ ";"
        try:
            cur.execute(dsql)
            con.commit()
            print 'You have succesfully deleted movie with id: ' + str(itemid)
        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
                print 'Error %s' % e
                sys.exit(1)
                print "error deleting from database"
        finally:
                if con:
                    con.close()
        return

    def ask_for_data(message):
        msg = raw_input(message)
        if msg == 'c' or msg == 'd' or msg == 'v' or msg == 'm' or msg == 'r' or msg == 't' or msg == 's' or msg == 'a':
            return msg
        elif type(msg) == int:
            return msg
        
        while msg != 'c' or msg != 'd' or msg != 'v' or msg != 'm' or msg != 'r' or msg != 't' or msg != 's' or msg != 'a' and type(msg) != int:
            if msg == '0':
                exit(0)
            return msg
        return msg

    def ask_for_int(integer):
        int_msg = int(raw_input(integer))
        while type(int_msg) != int:
            print "enter an integer"
            if int_msg == 0:
                exit()
            return int_msg
        return int_msg

    def show(specify, recid):
        sql = ("select TO_CHAR(showing.show_date, 'YY Mon DD ') as on, movie_table.movie_title as title, rating.description, "
               "movie_table.duration, showing.show_time as time from showing "
               "join movie_table on showing.movie_id = movie_table.movie_id "
               "join rating on rating.rating_id = movie_table.rating_id where " + specify + " =   \' " + str(recid) + "\' ;")
        try:
            cur.execute(sql)
            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()
            print "\n"
            print "|| %-10s | %-20s| %-40s | %-10s | %-10s |" %(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4])
            print "---------------------------------------------------------------------------------------------------------+"
            for row in rows:
                print "|| %-10s| %-20s | %-40s | %-10s | %-10s |" % row
                print "---------------------------------------------------------------------------------------------------------+"
                
        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            print 'Error %s' % e
            sys.exit(1)
            print "error reading from database"
        finally:
            if con:
                con.close()
   
    start = ask_for_data(st)
    if start == 'c':
        cr = ask_for_data(cr)
        if cr == 'm':
            movieid = ask_for_data(movieid)
            ratingid = ask_for_data(ratingid)
            movietitle = ask_for_data(movietitle)
            releasedate = ask_for_data(releasedate)
            enddate = ask_for_data(enddate)
            dur = ask_for_int(dur)
            movie_data = movieid, ratingid, movietitle, releasedate, enddate, str(dur)

            sql = "insert into movie_table values (%s, %s, %s, %s, %s, %s)", movie_data
            insert(sql)

        elif cr == 'r':
            ratingid = ask_for_data(ratingid)
            ratingcode = ask_for_data(ratingcode)
            description = ask_for_data(description)
            
            rating_data = ratingid, ratingcode, description
            sqlr = "insert into rating values (%s, %s, %s)", rating_data

            insert(sqlr)
            print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
            
        elif cr == 't':
            roomid = ask_for_data(roomid)
            capacity = ask_for_int(capacity)
            name = ask_for_data(name)
            
            theater_data = roomid, str(capacity), name
            sq = "insert into room values (%s, %s, %s)", theater_data
            insert(sq)
            
        elif cr == 's':
            showingid = ask_for_data(showingid)
            movieID = ask_for_data(movieid)
            roomid = ask_for_data(roomid)
            showdate = ask_for_data(showdate)
            showtime = ask_for_data(showtime)
            
            showing_data = showingid, movieID, roomid, str(showdate), showtime
            sqls = "insert into showing values (%s, %s, %s, %s, %s)", showing_data
            insert(sqls)
        else:
            print "Enter m, r, t, or s"
            print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'

    elif start == 'd':
        delt = ask_for_data(delt)
        if delt == 'm':
            cur.execute("select movie_id, movie_title from movie_table;")
            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()
            print "||%-10s | %-25s |" %(col_names[0], col_names[1])
            print "-----------------------------------------"
            for row in rows:
                print "||%-10s | %-25s |" % row
                print "-----------------------------------------"

            movieid = ask_for_int(movieid)
            delete('movie_table', 'movie_id', movieid)
            
        elif delt == 'r':
            cur.execute("select rating_id, description from rating;")
            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()
            print "||  %-10s   | %-40s |" %(col_names[0], col_names[1])
            print "-------------------------------------------------------------"
            for row in rows:
                print "||    %-10s | %-40s |" % row
                print "-------------------------------------------------------------"
            ratingid = ask_for_int(ratingid)

            delete('rating', 'rating_id', ratingid)

            print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'

        elif delt == 't':
            cur.execute("select room_id, name from room;")
            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()
            print "||  %-10s   | %-40s |" %(col_names[0], col_names[1])
            print "-------------------------------------------------------------"
            for row in rows:
                print "||    %-10s | %-40s |" % row
                print "-------------------------------------------------------------\n"
            roomid = ask_for_int(roomid)
            delete('room', 'room_id', roomid)
            
            print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'

        elif delt == 's':
            cur.execute("select distinct(movie_title) as title, showing_id, show_date as show_date, "
            "show_time from showing inner join movie_table  on showing.showing_id = showing.showing_id "
            "order by title;")

            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()
            print "||%-5s | %-25s | %-20s | %-10s|" %(col_names[0], col_names[1], col_names[2], col_names[3])
            print "------------------------------------------------------------------"
            for row in rows:
                print "||%-5s | %-25s | %-20s | %-10s" % row
                print "------------------------------------------------------------------\n"
            showingid = ask_for_int(showingid)
            delete('showing', 'showing_id', showingid)
            
        else:
            print "Enter m, r, t, or s"

        print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'

    elif start == 'v':
        view = ask_for_data(view)
        if view == 'm':
            cur.execute("select movie_id, movie_title from movie_table;")
            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()
            print "||  %-10s   | %-40s |" %(col_names[0], col_names[1])
            print "|------------------------------------------------------------|"
            for row in rows:
                print "||%-10s | %-40s |" % row
                print "-------------------------------------------------------------"
            movieid = ask_for_int(movieid)
            specs = "movie_table.movie_id"
            show(specs, movieid)
            print 'All showings of the movie with id: ' + str(movieid)
            print '|*|*|*|*|*|*|*|*|*||*|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||*|*|*|*|*|*|*|*||*'

        elif view == 'd':

            cur.execute("select distinct(TO_CHAR(showing.show_date, 'YY Mon DD ')) as show_date_formatted," +\
                       " movie_table.movie_title from showing inner join movie_table on showing.movie_id=movie_table.movie_id;")

            col_names = [cn[0] for cn in cur.description]

            rows = cur.fetchall()
            print "||%-10s | %-40s|" %(col_names[0], col_names[1])
            print "|---------------------------------------------------------|"
            for row in rows:
                print "||%-10s | %-40s |" % row
                print "---------------------------------------------------------"

            showdate = str(raw_input("Select movie by entering the show-date in the format 'MM-DD-YYYY': \n"))
            specs = "showing.show_date"
            show(specs, showdate)
           
            print 'All showings of the movie on the date: ' + str(showdate)
            print '|*|*|*|*|*|#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#|*|*|*|*|*|'

        elif view == 't':
            cur.execute("select room_id, name from room;")
            col_names = [cn[0] for cn in cur.description]
            rows = cur.fetchall()

            print "||%-10s | %-15s |" % (col_names[0], col_names[1])
            print "-------------------------------"

            for row in rows:
                print "||%-10s | %-15s |" % row
                print "-------------------------------"

            showroom = ask_for_data(roomid)
            specs = "showing.room_id"
            show(specs, showroom)
            
        elif view == 'a':
            print "                 \n"
            print "movie list:\n"

            sql = ("select TO_CHAR(showing.show_date, 'YY Mon DD ') as on, movie_table.movie_title as title, rating.description, "
                  "movie_table.duration, showing.show_time as time from showing "
                  "join movie_table on showing.movie_id = movie_table.movie_id "
                  "join rating on rating.rating_id = movie_table.rating_id ")
            try:
                cur.execute(sql)
                col_names = [cn[0] for cn in cur.description]
                rows = cur.fetchall()
                print "\n"
                print "|| %-10s | %-20s| %-40s | %-10s | %-10s |" %(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4])
                print "---------------------------------------------------------------------------------------------------------+"
                for row in rows:
                    print "|| %-10s| %-20s | %-40s | %-10s | %-10s |" % row
                    print "---------------------------------------------------------------------------------------------------------+"
                
                print 'All shows'
            except psycopg2.DatabaseError, e:
                if con:
                    con.rollback()
                print 'Error %s' % e
                sys.exit(1)
                print "error reading from database"
            finally:
                if con:
                    con.close()

        else:
            print "Enter m, r, t, or s"
    else:
        print "Please enter a valid input. Eg enter c for create etc"
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
        print 'Error %s' % e
        sys.exit(1)
        print "error creating the connection"
finally:
    if con:
        con.close()
