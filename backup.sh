# Input Variables
DATABASE=$1
HOST=$2
USERNAME=$3
PASSWORD=$4

cp ./mysqldump /tmp/mysqldump
chmod 755 /tmp/mysqldump

# Use an environment variable for the MySQL password so that mysqldump doesn't have to prompt for one.
export MYSQL_PWD="${PASSWORD}"

# Dump the saintsxctf database into a sql file
/tmp/mysqldump -v --host ${HOST} --user ${USERNAME} --max_allowed_packet=1G --single-transaction --quick --lock-tables=false --routines --column-statistics=0 --ssl-mode=DISABLED ${DATABASE} > /tmp/backup.sql
