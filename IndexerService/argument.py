from argparse import ArgumentParser,REMAINDER


class Argument():
    ARGUMENTS = ArgumentParser()

    def __init__(self,name,help,required_argument,requires_value,is_boolean = False):
        self.name = name
        self.help = help
        self.required_argument = required_argument
        self.requires_value = requires_value
        self.is_boolean = is_boolean

        self.set_script_arguments()


    @property
    def argument_action(self):
        if self.is_boolean:
            return 'store_true'
        else:
            return 'store'

    @property
    def first_letter(self):  # Returns the first letter of an argument name
        return str(self.name[0]).lower()

    @property
    def short_option(self):  # Returns the short option for user to put argument
        return '-{}'.format(self.first_letter)

    @property
    def long_option(self):  # Returns the long option for user to put argument
        return '--{}'.format(str(self.name).lower())

    def set_script_arguments(self):
        Argument.ARGUMENTS.add_argument(self.short_option, self.long_option,
                                        help=self.help, required=self.required_argument,
                                        action=self.argument_action)

    ########
    #This will check up if the given arguments is in the given convention --word-otherword
    #This will also return the given arguments as a dictionary
    #IMPORTANT: Since the arguments word separators are with dashes, this will end up storing by underscore
    #EXAMPLE: --cluster-name will end up with cluster_name
    ########
    @staticmethod
    def parse_unknown_args(remainder_list):
        remainder_collection = {}
        for argument in remainder_list:
            try:
                key,value = tuple(str(argument).split('='))
                if key[0:2] == '--':
                    fixed_key = key.replace('--','')
                    fixed_key = fixed_key.replace('-','_')
                    remainder_collection[fixed_key] = value
                else:
                    raise
            except:
                print(f'''
                !!!!!
                Something went wrong with,{argument}.
                Make sure to use the convention --firstword-secondword
                !!!!!
                ''')

        return remainder_collection



