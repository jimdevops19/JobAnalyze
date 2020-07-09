from jenkins import Jenkins
import json
import pprint as pp

configuration = dict(json.loads(open('configuration.json').read()))

#########
#Divided into returning three topics of meta
#1) Job Parameters:
#2) Job Builds History interesting information
#3) Job Cause (username) ['actions'][1]['causes'][0]['userName']
#########

class Job(Jenkins):
    def __init__(self,job_name):
        jenkins = Jenkins.__init__(self, url=configuration['jenkinsUrl'], username=configuration['jenkinsUser'], password=configuration['jenkinsPass'])
        jenkins._session.verify = False
        self.job_name = job_name


    @property
    def extra_columns(self):
        return ['userId','userName','currentStage','teardownStatus']


    @property
    def valid_job_name(self):
        if '-' in self.job_name:
            return self.job_name.replace('-','_')
        else:
            return self.job_name

    @property
    def parameters_collection(self):
        return self.get_parameters_names()+ self.get_meta_parameters()+self.get_test_parameters() + self.extra_columns


    def get_parameters(self):
        try:
            job_info = self.get_job_info(name=self.job_name)
            to_return = dict(job_info['property'][0])['parameterDefinitions']
            return to_return
        except:
            raise Exception("Could not find parameters, are you sure this is the name of the job and it is Parameterized?")

    def get_parameters_names(self):
        names = []
        for param in self.get_parameters():
            names.append(param['name'])

        return names

    def get_parameters_query(self):
        try:
            parameters = self.get_parameters()
            return {parameter['name']:"TEXT" for parameter in parameters}
        except:
            raise Exception(f"Something went wrong with receiving parameters from the job {self.job_name}. Are you sure this job exists?")

    def get_meta_parameters(self):
        return ['number','building','buildDuration','result','url']

    def get_meta_query(self):
        # number going to be in the column as INT type and not text
        meta = {}
        meta['number'] = 'INT'
        meta['building'] = 'BOOLEAN'
        meta['buildDuration'] = 'TEXT'
        meta['result'] = 'TEXT'
        meta['url'] = 'TEXT'

        return meta

    def get_test_parameters(self):
        return ['testDuration','failCount','passCount','skipCount',"successRate"]

    def get_test_query(self):
        meta = {}
        keys  = self.get_test_parameters()
        for key in keys:
            if 'Count' in key or "successRate" in key:
                meta[key] = 'INT'
            else:
                meta[key] = 'TEXT'

        return meta


    def get_extra_columns_query(self):
        meta = {}
        keys = self.extra_columns
        for key in keys:
            meta[key] = 'TEXT'

        return meta


    def parameters_query_column(self):
        columns_query = '\n('

        collection = self.get_parameters_query()
        collection.update(self.get_meta_query())
        collection.update(self.get_test_query())
        collection.update(self.get_extra_columns_query())

        for column,type in collection.items():
            columns_query += f"{column}         {type}   NULL"

            if not list(collection.items())[-1] == (column,type):
                columns_query +=',\n'

        columns_query += ');'

        print(columns_query)
        return columns_query

    def create_table_query(self):
        ########
        #Looking for creating a valid job name because sql query is not ok with dashes
        ########
        query = f'''CREATE TABLE {self.valid_job_name}{self.parameters_query_column()}'''
        return query

