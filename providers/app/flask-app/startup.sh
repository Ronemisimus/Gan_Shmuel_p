#!/bin/sh

python3 -m flask run --host=0.0.0.0
python3 -m flask db init
# if [ $MIGRATE_DB ]
# then
#     flask db migrate -m "chat_rooms" "posts"
#     flask db upgrade
# fi