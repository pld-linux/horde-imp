#!/bin/sh
NEWUSER=www-data
SYSID=33
CANCREATE=t
CANADDUSER=t
PSQL=/usr/bin/psql

QUERY="insert into pg_shadow \
        (usename, usesysid, usecreatedb, usetrace, usesuper, usecatupd) \
       values \
         ('$NEWUSER', $SYSID, '$CANCREATE', 't', '$CANADDUSER','t')"

RES=`$PSQL -c "$QUERY" template1`
if [ -n "$RES" ]
then
    echo "$CMDNAME: user "\"$NEWUSER\"" already exists" 1>&2
    exit 1
fi


