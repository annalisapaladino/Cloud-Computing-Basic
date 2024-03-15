#!/bin/bash 

for user in $(seq 0 39); do
    docker exec -e OC_PASS=test_password1234! --user www-data nextcloud /var/www/html/occ user:add --password-from-env "user${user}"
done
