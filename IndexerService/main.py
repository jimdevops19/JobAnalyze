import json
from argument import Argument
from jenkinsutils import Job
from database import DBSession, ColumnNotFoundException
from converters import Converter
from retry import retry

configuration = dict(json.loads(open('configuration.json').read()))

arguments_dict = dict(json.loads(open('arguments.json').read()))

argument_objects = []
for argument_name, argument_information in arguments_dict.items():
    argument_objects.append(
        Argument(name=argument_name, **argument_information))

parsed_args, unparsed_remainder_args = Argument.ARGUMENTS.parse_known_args()
remainder_args = Argument.parse_unknown_args(remainder_list=unparsed_remainder_args)


db = DBSession(
    user=configuration['databaseUser'],
    password=configuration['databasePass'],
    host=configuration['hostName'],
    port=configuration['port'],
    database=configuration['databaseName']
)

if parsed_args.create_table_only:
    job = Job(configuration['jobName'])
    db.execute_query(query = job.create_table_query())


####
#Checks that some key values specified to insert
#Attempts to insert new row with the unknown arguments
#Collects the conversion to an executable database query from dict_to_insert_query function
#Breaks if no extra key values specified because there is nothing to insert in the new row
#EXAMPLE:
# python main.py --insert --number=1 --version=4.0 --product-name=ocs4
####
def insert():
    table_name = Converter.dash_to_underscore(given_string = configuration['jobName'])
    if len(remainder_args) != 0:
        db.execute_query(query = Converter.dict_to_insert_query(
        table_name = table_name,
        given_dict = remainder_args
        ))
    else:
        raise Exception(f'''
                !!!!!
                You did not specify any extra key values to insert to the job's table!
                Please Specify key values in the convention: --arg=value
                !!!!!
                ''')

if parsed_args.insert:
    insert()

####
#Checks that some key values specified to update
#Expects for the argument --filter-by and the expression right after it in convention: "key=value" (WITHOUT DOUBLE DASHES!)
#Breaks if no extra key values specified because there is nothing to update in the existing row
#In case of failure for Column Not found Exception it is going to retry while it will triggers a query for the creation of the column
#EXAMPLE:
#python main.py --update --filter-by number=10021 --pause-before-upgrade=false --run-teardown=true
####
@retry(ColumnNotFoundException, tries=6, delay=10)
def update():
    table_name = Converter.dash_to_underscore(given_string=configuration['jobName'])
    if len(remainder_args) != 0:
        query = db.execute_query(query=Converter.dict_to_update_query(
                table_name=table_name,
                given_dict=remainder_args,
                filter_string=parsed_args.filter_by
            ))
        if query['result'] == 'COLUMN_NOT_FOUND_ERROR':
            raise ColumnNotFoundException(
                column=query['information'],
                db_connection = db,
                table_name=table_name
            )
    else:
        raise Exception(f'''
                !!!!!
                You did not specify any extra key values to update the job's table in filtered condition!
                Please Specify key values in the convention: --arg=value
                !!!!!
                ''')

if parsed_args.update:
    update()