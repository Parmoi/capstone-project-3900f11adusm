import db_manager as dbm

def login(email, password):

    if dbm.validate_account(email, password):
        return {'response': 'Logging in account!.'}
    else:
        raise ValueError("Invalid login email")


def register(name, email, password):

    dbm.insert_collector(email, name, name, '', password, '')

    return {'response': 'Account successfully registered!.'}