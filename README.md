# ARDIAN DANNY - SAWITPRO, TECHNICAL INTERVIEW

## Activate Environment (for development)

1. `source .env/bin/activate`

## Deployment

1. `rm -rf mysql_data`
2. `docker-compose up -d --build --force-recreate`

*I like using docker, so I guess that's a plus point*

## Image Storing Mechanism

*Instead of storing the image file locally on the web server, I decided to take a different approach (considering encryption as well)*
*Encrypting and decrypting the file directly using an encryption software will be server heavy and ineffective*

1. When user register, each user will get a random 16 bytes hex secrets (image_key). Each user have unique key.
2. When user upload an image, it will be converted to base64 and then encrypted with the user's image_key. Note that each user have a different image_key.
3. When the image is going to be viewed by the user, it will be decrypted with the corresponding user's image key.
4. Filesize is protected and limited by NGINX.
5. I've also put a super secure response header on the NGINX configuration.
6. File type has been filtered by the File Signature + Extensions making upload of malicious file impossible. Even if the attacker edit the file signature hex and the extensions, the file would be unusable because of improper formatting.
7. The web is 100% not vulnerable to the OWASP Top 10 checklists (Injection attack such as SQLI, XXE, etc is not possible).
7. To delete the image, just click the image, then there's a delete button below.


## What to improve

1. Of course the UI/UX (I'm not even a developer, but quite a fun challenge for a cybersecurity engineer. Thank god I used to participate in CTF a lot and also manage web exploitation challenges for competitions)
2. I think the code could be cleaner.
3. And of course HTTPS and stuff, but I feel it's not necessary for a demo site.
4. I purposedly didn't add any strong password policy because it will just hinder the testing and it's annoying. Later if you want to make this production, surely we can implement that.


## Note to self

1. Mysql issue: https://copyprogramming.com/howto/mysql-scripts-in-docker-entrypoint-initdb-are-not-executed










