# Job Analyzer with Grafana Dashboards
###Repository to display statistics of Jenkins jobs visualized.
 - Delivered by composed service with Grafana reading from an Postgresql DB Source.
 - Runs NGINX for referring the Grafana default port to a DNS name as well.


#Services:
 - NGINX:
    - Change Value for those environment Variables:
        - NGINX_HOST - Your full DNS Name.
        - NGINX_PROXY_PASS - Your machine IP:3000 (Default Grafana port)
 - Grafana
    - Editable environment variables:
        - GF_AUTH_ANONYMOUS_ENABLED=true Used for catching the dashboard elements as **iframe** html elements (Great for showing statistics in other Web sources)
        - GF_INSTALL_PLUGINS - Add the Dashboard plugins you want to include as comma separated, they will be installed with docker-compose up
 - Postgres
    - Editable environment variables:
        - POSTGRES_USER=admin
        - POSTGRES_PASS=admin
        - POSTGRES_DB=name
        - POSTGRES_PORT=5432 **(DON'T CHANGE Default port of Postgres)**
        - POSTGRES_HOST_AUTH_METHOD=trust
    - **NOTE: Postgresql volume will mount locally to keep your data maintained**
 - pgAdmin
    - Allows you to connect to your Postgres Engine and run queries over your tables
    - Editable environment variables:
        - **Auth to pass the login page of pgAdmin:**
        - PGADMIN_DEFAULT_EMAIL
        - PGADMIN_DEFAULT_PASSWORD

#Execution Options:
  - After cloning the Repo, Edition of **configuration.json** is required:
      - jobName : The job's name as it is in the config.
      - hostName : Machine Public IP
      - jenkinsUrl : Jenkins full url, including port if there is.
      - jenkinsUser: The jenkins credential in order to collect the parameters of the job
      - jenkinsPass: The jenkins credential in order to collect the parameters of the job
      - databaseName : Database Name  - this is required to connect to it with pgAdmin Interface
      - databaseUser : Username you chose in the compose file in Postgres service
      - databasePass : Password you chose in the compose file in Postgres service
      - port - leave it 5432
  
  - Within the directory of the configuration, build the docker image with:
      - _docker build . -t ${your_tag}_
        - Command Options after building:
        - Create the Table - docker run ${your_tag} -c
        - Insert key=value - docker run ${your_tag} --insert
            - One word parameters should be passed as --{param_name}
            - More than one word: --first-second-third
            - Examples:
              - docker run ${your_tag} --insert --name=jim
              - docker run ${your_tag} --insert --param1=4.5 --number=4 --building=true
              
        - Update key=value - docker run ${your_tag} --update --filter-by ${filter_condition} 
          - Examples:
            - docker run ${your_tag} --update --filter-by number=4 --name=jim2
            - docker run ${your_tag} --update --filter-by name=jim2 --param1=value



           
        
        
    
    