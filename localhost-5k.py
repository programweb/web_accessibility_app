#!/usr/bin/env python
import pymongo
import psycopg2 # for PostgreSQL
from datetime import datetime
from pytz import timezone
from flask import Flask, request, render_template, abort, redirect, url_for
from task_library import getTaskList
import subprocess



# TESTING (may not use)
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}
def html_escape(text):
    return "".join(html_escape_table.get(c,c) for c in text)

# remove startup warning, start with: export FLASK_ENV=development
port = '32768' # use docker ps to make sure you have the correct port
cfg = {
    'server': f"127.0.0.1:{ port }",
    'database': 'pa11y-webservice',
    'result_collection': 'results',
    'task_collection': 'tasks',
    'date_format': '%Y-%m-%d %H:%M:%S — %A',
    'timezone': 'US/Pacific'
}

try:
    out_bytes = subprocess.check_output(['docker', 'ps'])
except subprocess.CalledProcessError as e:
    out_bytes = e.output       # Output generated before error
    errCode      = e.returncode   # Return code
    print('Error code: ', errCode)
    print('Output before error: ', out_bytes.decode('utf-8'))
    exit(0)

portInDockerPS = False
lines = out_bytes.decode('utf-8').split('\n')
for line in lines:
    if port in line:
        portInDockerPS = True

if not portInDockerPS:
    print('Port ', port, 'not found in docker ps output.')
    print('Will exit.  Edit file to fix port or maybe you need to start the container.')
    exit(0)

app = Flask(__name__)
app.config.from_object('config')

def getMongo():
    connector = 'mongodb://{}'.format(cfg['server'])
    client = pymongo.MongoClient(connector)
    return client[ cfg['database'] ]

def getCommon(ttl):
    title = ttl
    db = getMongo()
    dtList = getResultDates(db)
    dtMap = getDateMap(db, dtList)
    error_message, task_count, result_date_count = getNumbers(db)
    tasks = getTaskList() # oh maybe this should not be in common
     
    return {'db': db,
            'title': title,
            'error_message': error_message,
            'task_count': task_count,
            'result_date_count': result_date_count,
            'dtList': dtList,
            'dtMap': dtMap,
            'tasks': tasks}

def getResultDates(db):
    dtList = []
    cursorObj = db[cfg['result_collection']].find()
    for dict in cursorObj:
        unixtm = dict['date']
        dtList.append( unixtm ) 

    dtList.sort(reverse=True)
    return dtList
    

def getNumbers(db):
    
    error_message = ''
    task_count = 0
    result_date_count = 0

    try:
        task_count = db[cfg['task_collection']].count_documents({})
        result_date_count = db[cfg['result_collection']].count_documents({})
    except Exception as e:
        error_message = e
        
    return error_message, task_count, result_date_count


@app.route('/')
def homepage():
    d = getCommon('Homepage')
    return render_template( 'home.html', d=d )

@app.route('/task/<taskPass>')
def showconfig(taskPass):
    d = getCommon('Task Configuration')
    db = getMongo()
    task = db[cfg['task_collection']].find_one({"passnm":taskPass})
    d['passnm'] = task.get('passnm')
    d['name'] = task.get('name')
    d['url'] = task.get('url')
    return render_template( 'task.html', d=d )    

def getPostgres():
    """ POSTGRESQL DATABASE """
    try:
        connection = psycopg2.connect(user="web",
                                    password="YQx25Ry038",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="accessibility")
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        toLog = "Error while connecting to PostgreSQL."
        connection = False
        cursor = False

    return (connection, cursor)

def closePostgres(connection, cursor):
    """ POSTGRESQL DATABASE """
    if(cursor):
        cursor.close()
    if(connection):
        connection.close()
    return True

def getIssue(code): # can get type too from result

    id = ''
    xcode = ''
    notes = ''
    solutions = ''
    odr = ''
    haveRow = False

    (connection, cursor) = getPostgres()
    if not any((connection, cursor)):
        return (id, code, notes, solutions, odr, haveRow)

    try:
        cursor.execute("SELECT id, code, notes, solutions, odr FROM issues WHERE code = %(code)s", {'code': code})
        (id, code, notes, solutions, odr) = cursor.fetchone()
        haveRow = True

    except (Exception, psycopg2.Error) as error:
        toLog = "Error while fetching data from PostgreSQL."
        haveRow = False

    finally:
        closePostgres(connection, cursor)

    return (id, code, notes, solutions, odr, haveRow)


@app.route('/results/<dt>')
def selectresults(dt):
    d = getCommon('Results')

    #dtList = getResultDates(db)
    #dtMap = getDateMap(db, dtList)
    #print(dtMap)

    d['dt'] = dt  # getDateLocal(dt).strftime( cfg['date_format'] ) # dtMap[dt]['dateHR'] # dt
    db = getMongo()
    cursorObj = db[cfg['result_collection']].find()
    taskID = "ObjectId('0')"
    d['count'] = []
    d['results'] = []
    for dict in cursorObj:
        if str(dict['date']) == dt:
            d['count'].append( dict['count'] )
            d['results'].append( dict['results'] )
            taskID = dict['task']
    

    for i,result in enumerate( d['results'][0] ):
        id, code, note, solution, odr, haveRow = getIssue(result['code'])
        d['results'][0][i]['note'] = note
        d['results'][0][i]['solution'] = solution
        d['results'][0][i]['haveRow'] = haveRow

    itm = db[ cfg['task_collection'] ].find_one({"_id":taskID})
    d['passnm'] = itm.get('passnm')
    d['name'] = itm.get('name')
    d['url'] = itm.get('url')
    
    return render_template( 'results.html', d=d )

@app.route('/addnotes/<accessibilityCode>', methods=['GET','POST'])
def addnotes(accessibilityCode):
    d = getCommon('Add Notes')
    d['code'] = accessibilityCode
    if 'notes' in request.form:
        d['usernotes'] = request.form['notes']
    else:
        d['usernotes'] = ''

    if 'solutions' in request.form:
        d['usersolutions'] = request.form['solutions']
    else:
        d['usersolutions'] = ''
    
    if( d['usernotes'] ): #TODO or check for solutions (and ck for code?)
        (connection, cursor) = getPostgres()
        if not any((connection, cursor)):
            pass
        else:
            try:
                sql = "INSERT INTO issues(code, notes, solutions) VALUES('" + d['code'] + "', '" + d['usernotes'] + "', '" + d['usersolutions'] + "')" 
                cursor.execute(sql)
                connection.commit()
            except (Exception, psycopg2.Error) as error:
                toLog = "Error while adding data to PostgreSQL."
            finally:
                closePostgres(connection, cursor)

    return render_template( 'addnotes.html', d=d )

@app.route('/editnotes/<accessibilityCode>', methods=['GET','POST'])
def editnotes(accessibilityCode):
    d = getCommon('Edit Notes')
    d['code'] = accessibilityCode

    (connection, cursor) = getPostgres()
    if not any((connection, cursor)):
        pass

    (id, code, notes, solutions, odr, haveRow) = getIssue(d['code'])
    if 'notes' in request.form and 'solutions' in request.form:
        d['usernotes'] = request.form['notes']
        d['usersolutions'] = request.form['solutions']

        sql = "UPDATE issues SET notes = %s, solutions = %s WHERE id = %s"
        cursor.execute(sql, (d['usernotes'], d['usersolutions'], id,))
        connection.commit()
        return redirect("/showtests?i=" + str(id), code=303)

    else:
        d['usernotes'] = notes
        d['usersolutions'] = solutions
    
    return render_template( 'editnotes.html', d=d )


@app.route('/showtests', methods=['GET','POST'])
def showtest():
    d = getCommon('Show Tests')
    d['ds'] = []
    d['error'] = '' # cdb 

    (connection, cursor) = getPostgres()
    if not any((connection, cursor)):
        d['error'] = "Error while trying to connect to PostgreSQL."
        return render_template( 'showtests.html', d=d )

    try:
        i = request.args.get('i', '0')   # 2nd arg is default
        cursor.execute("SELECT id, code, notes, solutions, odr, CASE WHEN id = %s THEN 1 ELSE 0 END AS wasUpdated FROM issues ORDER BY odr", (i,))
        d['ds'] = cursor.fetchall()
    
    except (Exception, psycopg2.Error) as error:
        d['error'] = "Error while fetching dataset from PostgreSQL." + str(psycopg2.Error) + str(Exception)

    finally:
        closePostgres(connection, cursor)

    return render_template( 'showtests.html', d=d )


@app.route('/sorttests', methods=['GET','POST'])
def sorttest():
    d = getCommon('Sort Tests')
    d['ds'] = []

    (connection, cursor) = getPostgres()
    if not any((connection, cursor)):
        return render_template( 'sorttests.html', d=d )

    odr = 1
    if 'seq' in request.form:
        sql = "UPDATE issues SET odr = %s WHERE id = %s"
        for itemID in request.form['seq'].split(','):
            cursor.execute(sql, (odr, itemID,))
            odr = odr + 1

        connection.commit()
        return redirect("showtests", code=303)

    try:
        cursor.execute("SELECT id, code, notes FROM issues ORDER BY odr")
        d['ds'] = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        toLog = "Error while fetching dataset from PostgreSQL."

    finally:
        closePostgres(connection, cursor)

    return render_template( 'sorttests.html', d=d )



@app.route('/addtasks', methods=['GET','POST'])
def addtasks():
    d = getCommon('Add Tasks')
    d['xx'] = 'nothing_yet'
    d['tasks'] = []
    
    """ POSTGRESQL DATABASE """
    conn = psycopg2.connect(dbname="accessibility", user="web", password="YQx25Ry038")
    cur = conn.cursor()
    cur.execute('''
        SELECT passnm, task_name, CONCAT('http://healthdata.org/', url) AS url, standard
        FROM tasks
        ''')
    rows = cur.fetchall()
    for row in rows:
        d['tasks'].append({'passnm':row[0],'name':row[1],'url':row[2],'standard':'WCAG2AA','ignore':[]})                # "name:{}".format(row[0]))
    cur.close()
    conn.close()

    """
     "passnm" : "A8-5Tx05", "name" : "Google", "url" : "http://www.google.com", "standard" : "WCAG2AA", "ignore" : [ ] }
     "name" : "About DCPN", "url" : "dcpn/about", "passnm" : "8f14e45fce", "standard" : "WCAG2AA", "ignore" : [ ] }
    """
     
    if request.method == 'POST':
        db = getMongo()
        tasksDesired = request.form.getlist('tasks[]')
        for task in d['tasks']:
            if task['passnm'] in tasksDesired:
                d['xx'] = task['passnm']
                db.tasks.insert_one( task )
        return redirect('http://localhost:5000')
        d['title'] = 'myHome'
        return render_template( 'home.html', d=d )
    """
    Leaving off:   , 'headers' : null
    """
    return render_template( 'addtasks.html', d=d )

@app.route('/deltasks')
def deltasks():
    # delete tasks and return to homepage
    db = getMongo()
    db[ cfg['task_collection'] ].drop()
    d = getCommon('Delete Tasks')
    return render_template( 'home.html', d=d )
    
@app.route('/delresults')
def delresults():
    # delete results and return to homepage
    db = getMongo()
    db[ cfg['result_collection'] ].drop()
    d = getCommon('Delete Results')
    return render_template( 'home.html', d=d )

@app.route('/findings2021')
def findings21():
    d = getCommon('Findings 2021')
    return render_template( 'findings_2021.html', d=d )

def strtr(text, trans):
    for key in trans.keys():
        text = text.replace(key, str(trans[key]))
    return text

def getSimpleURL(url):
    dict = {'https://www.': '', 'http://www.': '', 'https://': '', 'http://': ''}
    return strtr(url, dict).strip('/')


def getDateLocal(dt):
    # Localize the date
    tz = timezone( cfg['timezone'] )
    return tz.localize( datetime.fromtimestamp(dt / 1000.0) )
    
def getDateHR(dt):
    return dt.strftime( cfg['date_format'] )

def getDateMap(db, dtList):
    dtMap = {}
    
    for dt in dtList:
        result = db[ cfg['result_collection'] ].find_one({"date":dt})
        taskID = result.get('task')
        task = db[ cfg['task_collection'] ].find_one({"_id":taskID})

        dtMap[dt] = {
                    'dateHR': getDateLocal(dt).strftime( cfg['date_format'] ),  # getDateHR( getDateLocal(dt) ),
                    'passnm': task.get('passnm'),
                    'name': task.get('name'),
                    'url': task.get('url'),
                    'urlSimple': getSimpleURL( task.get('url') ),
                    }

    return dtMap
    
if __name__ == '__main__':
    app.run(debug=True)
