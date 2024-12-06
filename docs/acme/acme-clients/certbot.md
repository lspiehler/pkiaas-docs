Be sure to have the EAB KID and HMAC Key ready for the steps below. See [Generate EAB Credentials](../generate-eab-credentials.md) for more information.

All values that appear in ALL CAPS in the examples below must be customized with values specific to you.

## Register an Account Only
```certbot register --server https://acme-v02-api.pkiaas.io/directory --email YOUREMAIL@YOURDOMAIN.COM --agree-tos --eab-kid YOUREABKID --eab-hmac-key YOUREABHMACKEY```

## Register an Account and Order a Certificate for Apache
```certbot --apache --server https://acme-v02-api.pkiaas.io/directory --email YOUREMAIL@YOURDOMAIN.COM --agree-tos -d MYDOMAIN.COM -d WWW.MYDOMAIN.COM --eab-kid YOUREABKID --eab-hmac-key YOUREABHMACKEY```

See the [EFF certbot website](https://certbot.eff.org/instructions) for more information about certbot. 