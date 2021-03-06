#!/usr/bin/env python

import os
import warnings
from webob.dec import wsgify
from webob import Response
from graphsdb import db

# These table-exists warnings are boring:
warnings.filterwarnings('ignore', message=r'Table.*already exists')

here = os.path.dirname(os.path.abspath(__file__))
sql_file = os.path.join(here, '../sql/schema.sql')


@wsgify
def application(req):
    cursor = db.cursor()
    sql = open(sql_file).read()
    sql = [
        s.strip()
        for s in sql.split(';')
        if s.strip()]
    resp = Response(content_type='text/plain')
    for chunk in sql:
        try:
            cursor.execute(chunk)
        except:
            import sys
            print >> resp, "Bad SQL: %s" % chunk
            raise
    cursor.close()
    print >> resp, 'Setup ok'
    return resp
