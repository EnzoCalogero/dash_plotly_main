
#################################
# initialise the server option  #
#  in case the UI is not ready  #
#################################
host <- listdb_first()

#########################################
# return info on the current connect    #
#  Users /Devices                       #
#########################################


active_items <- function(host) {
  require("RPostgreSQL")
  conn <- NULL
  db <-host
  # loads the PostgreSQL driver
  drv <- dbDriver("PostgreSQL")
  query = "
  select us.display_name,dev.hostname hostname, account, protocol,peer_address,channel_count, templ.display_name  as dispalynameTemp, ch.active_change_ticket_id as ticket
  from channels ch, sessions ses,users us,devices dev,devicetemplates templ,devicetypes types
  where ses.id= ch.session_id
  and ses.user_id=us.id
  and ch.device_id=dev.id
  and dev.devicetemplate_id=templ.id
  and types.id = templ.devicetype_id
  and ses.token NOTNULL;
  "
  db_info<-db_info(host = db)
  conn <- dbConnect(
    drv,
    dbname = db_info$database, #"enzo",
    host = db_info$host ,#Host,
    port = db_info$port,#5432,
    # for run locally localhost and "database" to work in a Docker linked system....
    user =  db_info$user,#"postgres"
    #if(!is.na(db_info$password) )
             password = db_info$password 
  )
  
  
  result <- dbSendQuery(conn, query)
  result <- fetch(result, n = -1)
  dbDisconnect(conn)
  
  return(result)
}

#######################################
# Retrieve the last entry on the db   #
#######################################
max_on_db <-function(db="BAE Applied Inteligence Ltd_-_DET10APP53") {
  query='select date(created_at) from channels order by created_at desc limit 1;'
  conn <- NULL
  
  # loads the PostgreSQL driver
  drv <- dbDriver("PostgreSQL")
  db_info<-db_info(host = db)
  conn <- dbConnect(
    drv,
    dbname = db_info$database, #"enzo",
    host = db_info$host ,#Host,
    port = db_info$port,#5432,
    # for run locally localhost and "database" to work in a Docker linked system....
    user =  db_info$user,#"postgres"
    #if(!is.na(db_info$password) )
    password = db_info$password 
  )
  
  result <- dbSendQuery(conn, query)
  result <- fetch(result, n = -1)
  dbDisconnect(conn)
   
  # Return only the value not the data.frame
  return(as.Date(result[1,1]))
}


    ###################################
    # Function for collecting data    #
    # to create the Graphs            #
    ###################################
collect_data <-
  function(db = db,
           min = "2018-01-01",
           max = "2018-05-01") {

    #####################################
    # fix when data is browsed in a     #
    # not online context                #
    #####################################
    maxvalue=max_on_db(db=db)
    if ((maxvalue + 1) < max){
      max <-maxvalue
      min <-max-15
    }
    #################
    # end Amend     #
    #################
    require("RPostgreSQL")
    conn <- NULL
    
    # loads the PostgreSQL driver
    drv <- dbDriver("PostgreSQL")
    query_base = "
    select templ.devicetype_id,us.display_name,dev.hostname, account, protocol,(ses.deleted_at - ses.created_at) as durSession, (ch.deleted_at - ch.created_at) as durChanel,peer_address,substring(peer_address from '^[0-9]*.[0-9]*.[0-9]*' ) as subnet,channel_count,
    templ.name as templateName,templ.display_name  as dispalynameTemp,types.name as typeslName,
    types.display_name as typesDisplayName,vendor.name as vendor
    from channels ch, sessions ses,users us,devices dev,devicetemplates templ,devicetypes types,devicevendors vendor
    where ses.id= ch.session_id
    and ses.user_id=us.id
    and ch.device_id=dev.id
    and dev.devicetemplate_id=templ.id
    and vendor.id= templ.devicevendor_id
    and types.id = templ.devicetype_id
    and ses.deleted_at >= '"
    
    query <-
      paste0(
        query_base,
        min,
        " 00:00:00.000000' and ses.deleted_at <= '",
        max,
        " 23:59:59.999999' ;"
      )
    
    db_info<-db_info(host = db)
    conn <- dbConnect(
      drv,
      dbname = db_info$database, #"enzo",
      host = db_info$host ,#Host,
      port = db_info$port,#5432,
      # for run locally localhost and "database" to work in a Docker linked system....
      user =  db_info$user,#"postgres"
 #     if(!is.na(db_info$password) )
       password = db_info$password 
    )
    
    result <- dbSendQuery(conn, query)
    result <- fetch(result, n = -1)
    dbDisconnect(conn)
    
    return(result)
  }
