image=my
contain=builds


docker build -t  $image . && docker history $image
docker rm $contain -f

