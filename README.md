# Preparation for upload to DAFNI
docker build . -t pyramid-dl-2-hipims

docker run -v "$(pwd)/data:/data" pyramid-dl-2-hipims

docker save -o pyramid-dl-2-hipims.tar pyramid-dl-2-hipims:latest

gzip pyramid-dl-2-hipims.tar
