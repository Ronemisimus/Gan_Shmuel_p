FROM mysql:5.7
COPY init /init
ADD init/init.sql  /docker-entrypoint-initdb.d
RUN chmod -R +x /init
EXPOSE "3306"