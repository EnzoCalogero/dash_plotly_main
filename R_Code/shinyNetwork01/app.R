require(shiny)
library(visNetwork)

source('External_Functions.R')
source('PostgressQueries.R')
source('GraphBuilders.R')

#######################################
# Shiny Server side                   #
#######################################

server <- function(input, output, session) {
  #####################################
  #   Time Counter in Milliseconds    #
  #####################################
  autoInvalidate <- reactiveTimer(30 * 1000)
  
  #####################################
  #   DB Dispaly for Debug           #
  #####################################
  # to be used only for debug!!!!!
  
  #output$value <- renderPrint({input$select})
  
  #####################################
  # Created the Baseline Chart Graph  #
  #  The static definitions           #
  #####################################
  output$network <- renderVisNetwork({
    if (input$dates[2] >= input$dates[1]) {
     # print(input$select)
      #Collect the relevant data...
      myData <-
        collect_data(
          db = input$select,
          min = input$dates[1],
          max = input$dates[2]
        )
      
      if (dim(myData)[1] > 0) {
        output$messangermio <-
          renderText({
            ""
          }) # Clean the Messanger Display
        
        # activity flag in case Graph Show Active Data
        
        status_ <- active_status(data_in_max = input$dates[2])
        
        nodes <-
          build_graph_nodes(myData = myData, host=input$select, active_flag = status_)
        links <-
          build_graph_edges(myData = myData, host=input$select, active_flag = status_)
        
        #network Graph
        visNetwork(nodes, links, height = "1500px", width = "100%") %>%
          visPhysics(stabilization = TRUE) %>%
          visEdges(smooth = TRUE) %>%
          visIgraphLayout() %>%
          visOptions(
            highlightNearest = list(
              enabled = T,
              degree = 1,
              hover = T
            ) ,
            nodesIdSelection = list(enabled = T),
            selectedBy = "group"
          ) %>%
          visGroups(groupname = "User",
                    icon = list(code = "f007", color = "red")) %>%
          visGroups(groupname = "User-Active",
                    icon = list(
                      code = "f007",
                      color = "cyan",
                      size = 85
                    )) %>%
          visGroups(groupname = "firewall",
                    icon = list(
                      code = "f233",
                      color = 'blue',
                      size = 35
                    )) %>%
          visGroups(groupname = "firewall-Active",
                    icon = list(
                      code = "f233",
                      color = 'cyan',
                      size = 95
                    )) %>%
          visGroups(groupname = "linuxserver",
                    icon = list(
                      code = "f17c",
                      color = 'blue',
                      size = 35
                    )) %>%
          visGroups(groupname = "linuxserver-Active",
                    icon = list(
                      code = "f17c",
                      color = 'cyan',
                      size = 95
                    )) %>%
          visGroups(groupname = "windows",
                    icon = list(
                      code = "f17a",
                      color = 'blue',
                      size = 35
                    )) %>%
          visGroups(groupname = "windows-Active",
                    icon = list(
                      code = "f17a",
                      color = 'cyan',
                      size = 95
                    )) %>%
          visGroups(groupname = "other",
                    icon = list(
                      code = "f233",
                      color = 'blue',
                      size = 35
                    )) %>%
          visGroups(groupname = "other-Active",
                    icon = list(
                      code = "f233",
                      color = 'cyan',
                      size = 95
                    )) %>%
          visGroups(groupname = "switchrouter",
                    icon = list(
                      code = "f233",
                      color = 'blue',
                      size = 35
                    )) %>%
          visGroups(groupname = "switchrouter-Active",
                    icon = list(
                      code = "f233",
                      color = 'cyan',
                      size = 95
                    )) %>%
          visGroups(groupname = "hypervisor",
                    icon = list(
                      code = "f233",
                      color = 'blue',
                      size = 35
                    )) %>%
          visGroups(groupname = "hypervisor-Active",
                    icon = list(
                      code = "f233",
                      color = 'cyan',
                      size = 95
                    )) %>%
          addFontAwesome()
      } else {
        output$messangermio <- renderText({
          "NO DATA Available! for this  Date range Selection"
        })
      }
    } else {
      output$messangermio <- renderText({
        "Please Check the Date Range Selection"
      })
    }
  })
  
  ####################
  #   Updating Graph #
  ####################
  observe({
    autoInvalidate()
    if (input$dates[2] >= input$dates[1]) {
      myData <-
        collect_data(
          db = input$select,
          min = input$dates[1],
          max = input$dates[2]
        )
      if (dim(myData)[1] > 0) {
        # activity flag in case Graph Show Active Data
        status_ <- active_status(data_in_max = input$dates[2])
        
        nodes <-
          build_graph_nodes(myData = myData, host=input$select, active_flag = status_)
        edges <-
          build_graph_edges(myData = myData, host=input$select, active_flag = status_)
        
        visNetworkProxy("network") %>%
          visUpdateNodes(nodes = nodes) %>%
          visUpdateEdges(edges = edges)
      }
    }
  })
  
  
  ####################
  #   Updating date  #
  ####################
  
  observe({
    x <-input$select
    updateDateRangeInput(
      session, "dates",
      label = paste("Last entry from ", as.character(max_on_db(db=x))),
      start = max_on_db(db=x) -30
      )
   })

}

##################
# User Interface #
##################

ui <- fluidPage(
  fluidRow(
    column(
      3,
      dateRangeInput(
        "dates",
        label = Sys.Date(),
        start = Sys.Date() -90, 
        format = "yyyy/mm/dd",
        separator = " - "
      )
    ),
    column(
      3,
      selectInput(
        "select",
        label = NULL,
        choices = listdb(),
        selected = 1
      )
    ),
    column(3,
           h3(textOutput("value"))),
    column(3,
           h3(textOutput("messangermio")))
  ),
  
  ###############
  # Graph Chart #
  ###############
  
  visNetworkOutput("network", height = "1500px", width = "100%")
)


shinyApp(
  ui = ui,
  server = server,
  options = list(host = '0.0.0.0', port = 3838)
)
