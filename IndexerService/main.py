import json
import traceback
from argument import Argument
from jenkinsutils import Job
from database import DBSession
from converters import Converter
import time

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

if parsed_args.insert:
    if len(remainder_args) != 0:
        db.execute_query(query = Converter.dict_to_insert_query(
        table_name = Converter.dash_to_underscore(given_string = configuration['jobName']),
        given_dict = remainder_args
        ))
    else:
        raise Exception(f'''
                !!!!!
                You did not specify any extra key values to insert to the job's table!
                Please Specify key values in the convention: --arg=value
                !!!!!
                ''')

if parsed_args.update:
    if len(remainder_args) != 0:
        db.execute_query(query = Converter.dict_to_update_query(
            table_name= Converter.dash_to_underscore(given_string = configuration['jobName']),
            given_dict = remainder_args,
            filter_string = parsed_args.filter_by
        ))
    else:
        raise Exception(f'''
                !!!!!
                You did not specify any extra key values to update the job's table in filtered condition!
                Please Specify key values in the convention: --arg=value
                !!!!!
                ''')