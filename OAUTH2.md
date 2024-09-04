# Create super user if it already does not exist
```sh
python manage.py createsuperuser
```  
# Create credentials for external client
```sh
python manage.py createapplication --name "MyExternalApp" "confidential" "client-credentials"
```
# example client_id and client_secret
cliend_id=lkjtWreU92fMlQ0Etd2HDE1nPeBiQMBJn37Tt2Xy
client_secret=3ccXPnf0W23gES8mKOMt5CBkRPyxsyStVgdoAhEHmLopkEJlMZztrb4mWQyzsK2Ba6ddw72eD5YXvIbbc4LUNVNiJT49ah1tYIkd7su9PD4uTZSbWGHHbc6DRxXW2J5p

# generate token with client_id and client_scret
curl --location '{{domain}}/o/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id={{client_id}}' \
--data-urlencode 'client_secret={{client_secret}}'

# get programas
curl --location '{{domain}}/o/programas/' \
--header 'Authorization: Bearer {{access_token}}'

# get proyectos
curl --location '{{domain}}/o/proyectos/' \
--header 'Authorization: Bearer {{access_token}}'