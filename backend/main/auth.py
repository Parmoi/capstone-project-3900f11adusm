import db_manager as dbm

def login(email, password):



    return None


def register(name, email, password):

    dbm.insert_collector(email, name, name, '', password, '')

    return None