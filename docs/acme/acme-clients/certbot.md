# Certbot Command Examples

All values that appear in ALL CAPS in the examples below must be customized with values specific to you.

## Register an Account Only
```certbot register --server https://acme-v02-api.pkiaas.io/directory --email YOUREMAIL@YOURDOMAIN.COM --agree-tos --eab-kid YOUREABKID --eab-hmac-key YOUREABHMACKEY```

## Register an Account and Order a Certificate for Apache
```certbot --apache --server https://acme-v02-api.pkiaas.io/directory --email YOUREMAIL@YOURDOMAIN.COM --agree-tos -d MYDOMAIN.COM -d WWW.MYDOMAIN.COM --eab-kid YOUREABKID --eab-hmac-key YOUREABHMACKEY```