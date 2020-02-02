FROM flask
WORKDIR /flask-app
COPY  ./flask-app /flask-app
ENV FLASK_APP=/flask-app/app.py
RUN chmod +x startup.sh
EXPOSE "5000"
ENTRYPOINT [ "/bin/bash", "startup.sh" ]

# add ENV for port and stuff