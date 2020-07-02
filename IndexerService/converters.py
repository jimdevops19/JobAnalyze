def valid_sql_value(given_value):
    if type(given_value) is str:
        return f"""'{given_value}'"""
    else:
        return given_value

def valid_filter_string(given_filter):
        return f'''{given_filter.split('=')[0]}={valid_sql_value(given_filter.split('=')[1])} '''
##########
#
##########
class Converter():
    @staticmethod
    def dict_to_insert_query(table_name,given_dict):
        keys = list(given_dict.keys())
        values = list(given_dict.values())
        query = ''

        query += f'INSERT INTO {table_name}\n'


        query += '('
        for key in keys:
            if keys[-1] == key:
                query += key
            else:
                query += f'{key}, '
        query += ')'


        query += 'VALUES ('
        for value in values:
            if values[-1] == value:
                query += valid_sql_value(value)
            else:
                query += f'{valid_sql_value(value)}, '

        query += ');'

        return query


    @staticmethod
    def dict_to_update_query(table_name,filter_string,given_dict):
        query = ''
        query += f'UPDATE {table_name} \n'
        query += 'SET '

        for key_value in given_dict.items():
            key,value = key_value
            if list(given_dict.items())[-1] == key_value:
                query += f'{key}={valid_sql_value(value)}\n'
            else:
                query += f'{key}={valid_sql_value(value)}, '


        query += f'WHERE {valid_filter_string(filter_string)};'

        return query

    @staticmethod
    def dash_to_underscore(given_string,lower = True):
        if lower:
            fixed_string = str(given_string.replace('-','_')).lower()
            return fixed_string
