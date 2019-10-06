

################################
# Build The Nodes of the Graph #
################################

build_graph_nodes <- function(myData, host, active_flag = TRUE)
{
  ######################
  ## Defining Nodes   ##
  ######################
  db=host
  users <- aggregate(account ~ display_name , data = myData, FUN = length)
  names(users) <- c('id', 'frequency')
  
  users$label <- users$id
  
  ######################
  ## IPs selection    ##
  ######################
  usersIP <-
    aggregate(account ~ display_name + peer_address ,
              data = myData,
              FUN = length)
  names(usersIP) <- c('id', 'IPs', 'frequency')
  usersIP <- usersIP[, c('id', 'IPs')]
  
  usersIP <- aggregate(IPs ~ ., usersIP, toString)
  
  users = merge(users, usersIP, by = 'id')
  ######################
  ## SUBs selection   ##
  ######################
  usersSUB <-
    aggregate(account ~ display_name + subnet ,
              data = myData,
              FUN = length)
  names(usersSUB) <- c('id', 'sub', 'frequency')
  usersSUB <- usersSUB[, c('id', 'sub')]
  
  usersSUB <- aggregate(sub ~ ., usersSUB, toString)
  
  users = merge(users, usersSUB, by = 'id')
  
  #########################
  ## Templates selection ##
  #########################
  usersTempl <-
    aggregate(account ~ display_name + dispalynametemp ,
              data = myData,
              FUN = length)
  names(usersTempl) <- c('id', 'templ', 'frequency')
  usersTempl <- usersTempl[, c('id', 'templ')]
  
  usersTempl <- aggregate(templ ~ ., usersTempl, toString)
  
  users = merge(users, usersTempl, by = 'id')
  
  #########################
  ## Protocol selection  ##
  #########################
  usersProt <-
    aggregate(account ~ display_name + protocol ,
              data = myData,
              FUN = length)
  names(usersProt) <- c('id', 'protocol', 'frequency')
  usersProt <- usersProt[, c('id', 'protocol')]
  
  usersProt <- aggregate(protocol ~ ., usersProt, toString)
  
  users = merge(users, usersProt, by = 'id')
  
  #########################
  ## accounts selection  ##
  #########################
  usersACT <-
    aggregate(protocol ~ display_name + account ,
              data = myData,
              FUN = length)
  names(usersACT) <- c('id', 'account', 'frequency')
  usersACT <- usersACT[, c('id', 'account')]
  
  usersACT <- aggregate(account ~ ., usersACT, toString)
  
  users = merge(users, usersACT, by = 'id')
  
  #########################
  ##   Vendor selection  ##
  #########################
  usersVendor <-
    aggregate(protocol ~ display_name + vendor ,
              data = myData,
              FUN = length)
  names(usersVendor) <- c('id', 'vendor', 'frequency')
  usersVendor <- usersVendor[, c('id', 'vendor')]
  usersVendor <- aggregate(vendor ~ ., usersVendor, toString)
  
  users = merge(users, usersVendor, by = 'id')
  users$group <- 'User'
  
  ############################
  #Checking for active Users #
  ############################
  if (active_flag == TRUE) {
    #print("Here Active")
    #print(host)
    active <- active_items(host=host)
    # Definitions for the session
    active$label_active <-
      paste0(
        "<br><h4>The User has an Active Session in Progress:</h4> Ticket associated: <b>",
        active$ticket,
        "</b><br>from the IP: <b>",
        active$peer_address,
        "</b><br>Active Chanells: <b>",
        active$channel_count,
        "</b>"
      )
    
    # Definitions for the device to be aggregate
    active$label2 <-
      paste0(
        "<br>Connected to the Hostname:<b>",
        active$hostname,
        "</b><br>Account Used: <b>",
        active$account,
        "</b><br>Protocol: <b>",
        active$protocol,
        "<br></b>Template: <b>",
        active$dispalynametemp,
        "</b><br>"
      )
    
    temp <- active[c("display_name", "label2")]
    temp <- aggregate(label2 ~ ., temp, toString)
    
    
    active <- active[c('display_name', 'label_active')]
    active <- unique(active)
    active <- merge(active, temp, by = "display_name")
    active$label_active <- paste(active$label_active, active$label2)
    active$label2 <- NULL
    
    users["display_name"] <- users$id
    
    users <- merge(users, active, by = 'display_name', all.x = TRUE)
    users$label_active[is.na(users$label_active)] <- ""
    users$group[users$id %in% active$display_name] <- "User-Active"
  }
  
  
  ###############################
  # Generating the HTML         #
  # for the Hover               #
  ###############################
  
  users$title <-
    paste0(
      "<p>User Name: <B>",
      users$id,
      "</B><br>",
      users$label_active,
      "<br><h4>Historic Information (for the Selected Date Range):</h4>IP(s): <B>{",
      users$IPs,
      "}</B><br>Subnets(s): <B>{",
      users$sub,
      "}</B><br>Templates(s): <B>{",
      users$templ,
      "}</B><br>Vendor(s) Interacting: <B>{",
      users$vendor,
      "}</B><br>Protocol(s): {<B>",
      users$protocol,
      "}</B><br>Account(s): <B>{",
      users$account,
      "}</B><br> Connections: <B>",
      users$frequency,
      "</B></p>"
    )
  
  ##################################
  # Cleaning no relevant variables #
  ##################################
  users$display_name <- NULL
  users$devId <- 0
  users$sub <- NULL
  users$templ <- NULL
  users$protocol <- NULL
  users$account <- NULL
  users$vendor <- NULL
  users$IPs <- NULL
  users$activeSide <- NULL
  users$label_active <- NULL
  
  
  ###########################################################################################
  ####                        Device ID + Frequency                                      ####
  ###########################################################################################
  
  device <-
    aggregate(account ~ typeslname + hostname ,
              data = myData,
              FUN = length)
  names(device) <- c('devId', 'id', 'frequency')
  device$label <- device$id
  device$devId[!(
    device$devId  %in% c(
      'firewall',
      'hypervisor',
      'linuxserver',
      'switchrouter',
      'windows'
    )
  )] = 'other'
  device$group <- device$devId
  
  ###########################
  ##   Select Account      ##
  ###########################
  
  devAccount <-
    aggregate(typeslname ~ hostname + account ,
              data = myData,
              FUN = length)
  names(devAccount) <- c('id', 'account', 'frequency')
  devAccount <- devAccount[, c('id', 'account')]
  
  devAccount <- aggregate(account ~ ., devAccount, toString)
  
  device = merge(device, devAccount, by = 'id')
  ###########################
  ##   Select Protocol     ##
  ###########################
  
  devProtocol <-
    aggregate(typeslname ~ hostname + protocol ,
              data = myData,
              FUN = length)
  names(devProtocol) <- c('id', 'protocol', 'frequency')
  devProtocol <- devProtocol[, c('id', 'protocol')]
  
  devProtocol <- aggregate(protocol ~ ., devProtocol, toString)
  
  device = merge(device, devProtocol, by = 'id')
  
  ###########################
  ##   Select Template     ##
  ###########################
  
  devdispalynametemp <-
    aggregate(typeslname ~ hostname + dispalynametemp ,
              data = myData,
              FUN = length)
  names(devdispalynametemp) <- c('id', 'dispalynametemp', 'frequency')
  devdispalynametemp <- devdispalynametemp[, c('id', 'dispalynametemp')]
  
  devdispalynametemp <-
    aggregate(dispalynametemp ~ ., devdispalynametemp, toString)
  
  device = merge(device, devdispalynametemp, by = 'id')
  
  ###############################
  # Checking for active Devices #
  ###############################
  #device$label_active<-""
  if (active_flag == TRUE) {
    active <-
      active_items(host=host) #refreshing the dataframe for the active devices
    w <- which(device$id %in% unique(active$hostname))
    device$group[w] <- paste0(device$group, "-Active")
    ##########################################################################
    label0 <-
      "<br><h4>The Device has Active Session(s) in Progress:</h4>"
    active$label_active <-
      paste0(
        "<br>Ticket associated: <b>",
        active$ticket,
        "</b><br>With The Account: <b>",
        active$account,
        "</b><br>Protocol: <b>",
        active$protocol,
        "</b><br>template: <b>",
        active$dispalynametemp,
        "</b><br>"
      )
    temp <- active[c("hostname", "label_active")]
    colnames(temp) <- c("id", "label_active")
    temp <- aggregate(label_active ~ ., temp, toString)
    temp$label_active <- paste0(label0, temp$label_active)
    device <- merge(device, temp, by = 'id', all.x = TRUE)
    
    ##########################################################################
  }
  
  ###############################
  # Generating the HTML         #
  # for the Hover               #
  ###############################
  #device$label_active[is.na(device$label_active)] <- "" # bit of cleaning....
  
  device$title <-
    paste0(
      "<p>HostName: <B>",
      device$id,
      "</B>",
      device$label_active,
      "<h4>Historic Information (for the Selected Date Range):</h4><br>Device Type: <B>",
      device$devId,
      "</b><br>Account(s): <B>{",
      device$account,
      "}</b><br>Protocol(s): <B>{",
      device$protocol,
      "}</b><br>Templates(s): <B>{",
      device$dispalynametemp,
      "}</b><br>Connections: <B>",
      device$frequency,
      "</B</p>"
    )
  
  ########################
  # Removing unused data #
  ########################
  
  device$account <- NULL
  device$protocol <- NULL
  device$dispalynametemp <- NULL
  device$label_active <- NULL
  
  ########################
  # Final Merge:         #
  # Users +Devices       #
  #######################
  
  nodes <- rbind(users, device)
  nodes$shape = "icon"
  return (nodes)
}

################################
# Build The edges of the Graph #
################################

build_graph_edges <- function(myData, host, active_flag = TRUE) {
  db=host
  links = aggregate(account ~ display_name + hostname ,
                    data = myData,
                    FUN = length)
  
  names(links) <- c('from', 'to', 'width')
  links$title <-
    paste('connections in the Selected Date Range: ', links$width, sep = ' ')
  maxWith = 8
  max <- max(links$width)
  links$width <- ceiling(maxWith * links$width / max)
  links$arrows <- 'middle'
  links$color <- 'lightblue'
  
  ###############################
  # Checking for active Devices #
  ###############################
  if (active_flag == TRUE) {
    active <- active_items(host=host)
    active$temp <- paste0(active$display_name, active$hostname)
    links$temp <- paste0(links$from, links$to)
  }
  
  if (exists("active")) {
    links$width[links$temp %in% active$temp] <- 20
    links$arrows[links$temp %in% active$temp] <- "to"
  }
  
  return(links)
}