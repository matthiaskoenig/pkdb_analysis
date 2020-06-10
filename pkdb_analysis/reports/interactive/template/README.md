
## Local development
### Run development server
```
docker-compose -f docker-compose-serve.yml up
```
Change the web content in the `./app/` folder.


### Update dependencies
```
docker run --rm --volume="$PWD:/srv/jekyll" --volume="$PWD/vendor/bundle:/usr/local/bundle" -it jekyll/jekyll:latest bundle update
```

