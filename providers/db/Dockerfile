FROM mysql:5.7
COPY init /init
COPY init/init.sql  /docker-entrypoint-initdb.d
COPY init/my.cnf /etc/mysql/my.cnf
RUN chmod -R +x /init
EXPOSE "3306"
