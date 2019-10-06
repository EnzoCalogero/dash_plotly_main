docker run --rm -p 3838:3838 \
    -v ~/R_Project/shinyNetwork01/:/srv/shiny-server/ \
    -v /srv/shinylog/:/var/log/shiny-server/ \
     shiny:first

