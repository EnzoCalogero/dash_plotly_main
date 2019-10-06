#PATH = "/home/enzo/PycharmProjects/local_dash/data/multi_db_VM"  # running from the RStudio multi db
PATH = "/home/enzo/R_Project/shinyNetwork01/current.ini"

##########################################
# Function to discreminat if the current #
# graph data is actually today           #
##########################################

active_status <- function(data_in_max = "2018-06-20") {
  # Comparing the given date with the today date
  
  if (format(Sys.Date(), format = "%Y-%m-%d") == data_in_max)
  {
    return(TRUE)
  }
  else
  {
    return (FALSE)
  }
}


##########################################
# Function to collect data from Multi DB #
# it gives the section name of each db  #
##########################################
listdb <- function(path = PATH) {
  library(ConfigParser)
  dblist <- list()
  config <- ConfigParser$new()
  config$read(path)
  for (ii in seq(2, as.numeric(config$data[1]$dbs) + 2)) {
    #Section Name
    section <- names(config$data[ii][1])
    # Host IP
    if (section != "ElasticSearch"){
        b <- config$get("host", section = section)
        #Append element to the list
        dblist[section] <- section #b
        #dblist<-c(dblist, section)
        }
    
  }
  return(dblist)
}

###########################################
# Function to collect data from Multi DB  #
# it gives the section of the first server#        #
###########################################
listdb_first <- function(path = PATH) {
  library(ConfigParser)
  config <- ConfigParser$new()
  # read all the info from the ini file
  config$read(path)
  
  # Extract the IP from first available server
  First_section <- names(config$data[2][1])
  IP <- config$get("host", section = First_section)
  return(IP)
}

##########################################
# Function to gives all the detail for   #
# the selected DB                        #
##########################################
db_info <- function(path=PATH, host="BAE Applied Inteligence Ltd_-_DET10APP53") {
  #print("IN DB INFO")
  #print(host)
  
  library(ConfigParser)
  dblist <- list()
  config <- ConfigParser$new()
  config$read(path)
  for (ii in seq(2, as.numeric(config$data[1]$dbs) + 2)) {
    #Section Name
    section <- names(config$data[ii][1])
    #print(section)
    # Identify the requested section ....
    if(tolower(section) == tolower(host)) {
      
      #print("matching")
      dblist['host'] <- config$get("host", fallback = NA ,section = section)
      dblist['user'] <- config$get("user",fallback = NA , section = section)
      dblist['database'] <- config$get("database", fallback = NA ,section = section)
      dblist['port'] <- config$get("port",fallback = NA , section = section)
      dblist['password'] <- config$get("password", fallback = NA ,section = section)
    }
    
  }
  return(dblist)
}
