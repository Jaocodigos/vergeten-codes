# Description

Both scripts are made to work together. The objective is get an service ip that changes everytime and update your hosts to hold connection.

The **send_ip** needs to be used on service. The script file sends your actual host ip every single minute.

The **get_ip_and_update_hosts** will listen an specific file(that you specify) changes. This file will contains the ip of service, sent by send_ip script. After a file change, he gets the alteration and update your /etc/hosts file.

### Requirements

 - Both machines must be authorized to communicate with each other.



