Be sure to have the EAB KID and HMAC Key ready for the steps below. See [Generate EAB Credentials](../generate-eab-credentials.md) for more information.

All values that appear in ALL CAPS in the examples below must be customized with values specific to you.

1. Create a docker-compose.yml on your server with the following content:
``` yaml linenums="1" hl_lines="17-20 35"
version: "3.3"

services:

  traefik:
    image: "traefik:v3.2"
    container_name: "traefik"
    command:
      #- "--log.level=DEBUG"
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entryPoints.web.address=:80"
      - "--entryPoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.httpchallenge=true"
      - "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.myresolver.acme.caserver=https://acme-v02-api.pkiaas.io/directory"
      - "--certificatesresolvers.myresolver.acme.eab.kid=YOUREABKID"
      - "--certificatesresolvers.myresolver.acme.eab.hmacencoded=YOUREABHMACKEY"
      - "--certificatesresolvers.myresolver.acme.email=YOUREMAIL@YOURDOMAIN.COM"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - "./letsencrypt:/letsencrypt"
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  whoami:
    image: "traefik/whoami"
    container_name: "simple-service"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.whoami.rule=Host(`whoami.example.com`)"
      - "traefik.http.routers.whoami.entrypoints=websecure"
      - "traefik.http.routers.whoami.tls.certresolver=myresolver"
```
2. Create a "letsencrypt" directory in the same directory you created the docker-compose.yml file.
3. Replace the values for **certificatesresolvers.myresolver.acme.eab.kid**, **certificatesresolvers.myresolver.acme.eab.hmacencoded**, and **certificatesresolvers.myresolver.acme.email** with your own correct values.
4. Replace whoami.example.com by your own domain within the traefik.http.routers.whoami.rule label of the whoami service.
5. Optionally uncomment the following line if you want to test/debug:
```
#- "--log.level=DEBUG"
```
6. Run `docker-compose up -d` within the folder where you created the previous file.
7. Wait a a few moments for the certificate request to complete, and visit https://your_own_domain to confirm everything worked as expected.

See the [Traefik website](https://doc.traefik.io/traefik/user-guides/docker-compose/acme-http/) for more information about Traefik. 