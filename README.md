# ARDIAN DANNY - SAWITPRO, TECHNICAL INTERVIEW

## Activate Environment (for development)

1. `source .env/bin/activate`

## Deployment

1. `docker-compose up -d --build`

## Image Storing Mechanism

1. When user register, each user will get a random 16 bytes hex secrets (image_key).
2. When user upload an image, it will be converted to base64 and then encrypted with the user's image_key. Note that each user have a different image_key.
3. When the image is going to be viewed by the user, it will be decrypted with the corresponding user's image key.

## What to improve

1. Of course the UI/UX (I'm not even a developer, but quite a fun challenge for a cybersecurity engineer)
2. I think the code could be cleaner but the time given is not sufficient.


## Note to self

1. Mysql issue: https://copyprogramming.com/howto/mysql-scripts-in-docker-entrypoint-initdb-are-not-executed










