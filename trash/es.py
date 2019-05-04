from datetime import tzinfo, timedelta, datetime, timezone
from pytz import timezone
import pytz
import tzlocal
import tzlocal  # $ pip install tzlocal
import dateutil.parser
import time
from dateutil.tz import gettz

now = datetime.now().timestamp()

<preConditions onFail="MARK_RAN">
            <not>
                <tableExists schemaName="public" tableName="contragent" />
            </not>
        </preConditions>




    <preConditions onFail="HALT">
         <sqlCheck expectedResult="NULL">select id from contragent id=2</sqlCheck>
    </preConditions>


< changeSet
id = "1"
author = "dbobro" >
< preConditions
onFail = "MARK_RAN" >
< not >
< tableExists
schemaName = "public"
tableName = "contragent" / >
< / not >
< / preConditions >
< createTable
tableName = "contragent" >

< column
name = "id"
type = "serial" >
< constraints
primaryKey = "true"
nullable = "false" / >
< / column >
< column
name = "name"
type = "varchar(50)" >
< constraints
nullable = "false" / >
< / column >
< column
name = "account"
type = "integer" >
< constraints
nullable = "false" / >
< / column >
< / createTable >

< rollback >
< dropTable
tableName = "contragent" / >
< / rollback >

< / changeSet >

< / databaseChangeLog >
