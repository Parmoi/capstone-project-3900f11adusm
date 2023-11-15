import sqlalchemy as db
import bcrypt
import smtplib, ssl
from random import randrange
from email.message import EmailMessage
from email.mime.text import MIMEText

from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    create_refresh_token,
    set_refresh_cookies,
)


from database import db_collectors
import database.db_manager as dbm
from privelage import COLLECTOR, MANAGER, ADMIN

from error import InputError, AccessError, OK

""" |------------------------------------|
    |     Functions for Authorization    |
    |------------------------------------| """


def login(password, email=None, username=None):
    """login.

    Logs a user in by setting fresh access and refresh tokens in client cookies
    if credentials are correct.

    Args:
        password: users password
        email: users email
        username: users username

    provide username or email, not both.
    """
    if email:
        collector_id = db_collectors.get_collector_id(email=email)
        if collector_id is None:
            return jsonify({"msg": "Invalid email!"}), InputError
    elif username:
        collector_id = db_collectors.get_collector_id(username=username)
        if collector_id is None:
            return jsonify({"msg": "Invalid username!"}), InputError
    else:
        return jsonify({"msg": "No email or username provided!"}), InputError

    if not validate_password(email, password):
        return jsonify({"msg": "Invalid password!"}), InputError

    user_id = db_collectors.get_collector_id(email=email, username=username)
    response = jsonify(
        {"userId": user_id, "privelage": get_user_privelage(user_id)}
    )
    access_token = create_access_token(identity=user_id, fresh=True)
    refresh_token = create_refresh_token(identity=user_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK


def logout():
    """Removes cookies from client"""
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, OK


def register_collector(email, username, password, privelage=COLLECTOR):
    """register_collector.

    Checks if email or usernames exists, returns <error_code> if they do.
    Hashes password and inserts the collector into the database.
    Generates access and response tokens and attatches them to response object cookies.
    Returns response for successful collector registration.

    Args:
        email:
        username:
        password:
    """

    collector_id = db_collectors.get_collector_id(email=email, username=username)
    if collector_id is not None:
        return jsonify({"msg": "Email or user name already registered!"}), InputError

    password = hash_password(password)

    resp, status = db_collectors.insert_collector(email, username, password, privelage)

    if status != OK:
        return jsonify({"msg": "Account unsuccessfully registered!"}), status

    collector_id = db_collectors.get_collector_id(email=email, username=username)

    response = jsonify({"msg": "Account successfully registered!"})
    access_token = create_access_token(identity=collector_id, fresh=True)
    refresh_token = create_refresh_token(identity=collector_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK


def send_manager_email(admin_id, manager_id):
    manager_info = db_collectors.get_collector_dict(user_id=manager_id)

    if manager_info is None:
        return jsonify({"msg": "Invalid collector id"}), InputError

    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    # smtp_server = "localhost"

    app_email = "woolliescollectiblescorner@gmail.com"
    password = "collectibles1234"
    app_password = "lvyztdilxougllhb"

    invite_email = manager_info.get("email")
    # invite_email = "greg.whitehead21@gmail.com"

    subject = "Email Subject"
    code = randrange(100000, 999999)
    body = f"Manager invitation code: \n\n{code}"

    context = ssl.create_default_context()

    try:
        print("Connecting to smtp server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)
        server.login(app_email, app_password)
        print("connected to server!")
        print(f"Sending manager invitation email to {invite_email}")
        server.sendmail(app_email, invite_email, body)
    except Exception as e:
        return jsonify(print(e))

    finally:
        server.quit()

    engine, conn, metadata = dbm.db_connect()
    privelages = db.Table("privelages", metadata, autoload_with=engine)
    update_stmt = (
        db.update(privelages)
        .where(privelages.c.collector_id == manager_id)
        .values({"code": code})
    )
    conn.execute(update_stmt)
    conn.close()

    return jsonify({"msg": "Manager invitation email sent!"}), OK


def check_manager_email_code(manager_id, code):
    engine, conn, metadata = dbm.db_connect()
    privelages = db.Table("privelages", metadata, autoload_with=engine)
    select_stmt = db.select(privelages).where(privelages.c.collector_id == manager_id)
    result = conn.execute(select_stmt)
    manager_info = result.fetchone()._asdict()
    conn.close()

    if manager_info.get("code") == code:
        engine, conn, metadata = dbm.db_connect()
        privelages = db.Table("privelages", metadata, autoload_with=engine)
        update_stmt = (
            db.update(privelages)
            .where(privelages.c.collector_id == manager_id)
            .values({"privelage": ADMIN})
        )
        result = conn.execute(update_stmt)
        conn.close()

        return (
            jsonify({"msg": "Manager authorization code verified!"}),
            OK,
        )
    else:
        return (
            jsonify({"msg": "Manager authorization code invalid!"}),
            InputError,
        )


# We will create a function to send mail .We will pass above values in funcion parameter.
# def send_email(subject, body, sender, recipients, password):
# msg = MIMEText(body)   # Creating msg object using MIMEText class of email module
# msg['Subject'] = subject  # Assigning the subject
# msg['From'] = app_email# Assigning the sender email address
# msg['To'] = invite_email  # Assigning recepients email address.
# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:   # Creating connection using context manager
#    smtp_server.login(app_email, app_password)
#    smtp_server.sendmail(app_email, invite_email, msg.as_string())
# print("Email sent Successfully!")


# We will call the function and pass the parameter values defined in line no 4 to 8.
# send_email(subject, body, sender, recipients, password)

# # creates SMTP session
# s = smtplib.SMTP('smtp.gmail.com', port)

# # start TLS for security
# s.starttls()

# # Authentication
# s.login(app_email, app_password)

# # message to be sent
# message = "Message_you_need_to_send"

# # sending the mail
# s.sendmail(app_email, invite_email, message)

# # terminating the session
# s.quit()

# # port = 465  # For SSL

# # Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login(email, password)
#     # TODO: Send email here

# with open("manager_email.txt") as fp:
#     msg = EmailMessage()
#     msg.set_content(fp.read())

# msg["Subject"] = "Collectible Corner Manager Authorization"
# msg["From"] = "greg.whitehead21@gmail.com"
# msg["To"] = "greg.whitehead21@gmail.com"
#
# smtp = smtplib.SMTP('localhost')
# smtp.send_message(msg)
# smtp.quit()


def refresh(user_id):
    # TODO: Write docstring clearly explainig what refresh does.
    """refresh.

    Args:
        user_id:
    """
    access_token = create_access_token(identity=user_id)
    response = jsonify({"refresh": True})
    set_access_cookies(response, access_token)
    return response, OK


def get_privelage(user_id):
    user_privelage = get_user_privelage(user_id)
    return jsonify({"privelage": user_privelage}), OK


def update_privelage(user_id, privelage):
    engine, conn, metadata = dbm.db_connect()

    privelages = db.Table("privelages", metadata, autoload_with=engine)

    update_stmt = (
        db.update(privelages)
        .where(privelages.c.collector_id == user_id)
        .values({"privelage": privelage})
    )
    conn.execute(update_stmt)
    conn.close()

    user_privelage = get_user_privelage(user_id)

    return jsonify({"privelage": user_privelage}), OK


def check_privelage(user_id, required_privelage):
    user_privelage = get_user_privelage(user_id)
    has_privelage = user_privelage >= required_privelage

    if not has_privelage:
        return jsonify(
            {
                "msg": "user {} has privelage level {}, requires at least privelage level {}!".format(
                    user_id, user_privelage, required_privelage
                ),
                "privelage": user_privelage,
            },
            AccessError,
        )
    else:
        return jsonify({"privelage": user_privelage})


""" |------------------------------------|
    | Helper functions for Authorization |
    |------------------------------------| """


# TODO: Return proper error on user does not exist
def validate_password(email, password):
    """validate_password.

    Validates users password associated with given email.
    Returns True if password is valid.

    Args:
        email: user email
        password: user password to be validated
    """

    user_hashed_pw = db_collectors.get_collector_pw(email=email)
    # collector = db_collectors.get_collector(email=email)
    if user_hashed_pw is not None:
        user_hashed_pw_bytes = user_hashed_pw.encode("utf-8")
        input_pw_bytes = password.encode("utf-8")
        return bcrypt.checkpw(input_pw_bytes, user_hashed_pw_bytes)
    else:
        return


def hash_password(password):
    pw_bytes = password.encode("utf-8")
    hashed_pw = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed_pw.decode("utf-8")


def get_user_privelage(user_id):
    engine, conn, metadata = dbm.db_connect()
    privelages = db.Table("privelages", metadata, autoload_with=engine)
    select_stmt = db.select(privelages.c.privelage).where(
        privelages.c.collector_id == user_id
    )
    res = conn.execute(select_stmt)
    conn.close()

    user_privelage = res.fetchone()._asdict().get("privelage")
    return user_privelage


def check_user_privelage(user_id, required_privelage):
    user_privelage = get_user_privelage(user_id)
    return user_privelage >= required_privelage
