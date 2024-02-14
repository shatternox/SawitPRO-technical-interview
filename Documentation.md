```
ARDIAN DANNY - SAWITPRO, TECHNICAL INTERVIEW
```
## Activate Environment

1. `source .env/bin/activate`
2. 


## Deployment

1. `docker-compose up -d --build`

## Image Storing Mechanism

1. When user register, each user will get a random 16 bytes hex secrets (image_key).
2. When user upload an image, it will be converted to base64 and then encrypted with the user's image_key. Note that each user have a different image_key.
3. When the image is going to be viewed by the user, it will be decrypted with the corresponding user's image key.













