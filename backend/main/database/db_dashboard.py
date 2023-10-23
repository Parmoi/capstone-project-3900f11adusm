import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import auth
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |     Functions for dashboard        |
    |------------------------------------| """

def get_dashboard(user):
    return jsonify({
        "msg": '''
______________________________________ 
/ This does not exist yet! WE HAVE NOT \
\\ BUIlT THIS YET! Coming soonn!        /
 -------------------------------------- 
                       \\                    ^    /^
                        \\                  / \\  // \
                         \\   |\\___/|      /   \\//  .\
                          \\  /O  O  \\__  /    //  | \\ \\           *----*
                            /     /  \\/_/    //   |  \\  \\          \\   |
                            @___@`    \\/_   //    |   \\   \\         \\/\\ \
                           0/0/|       \\/_ //     |    \\    \\         \\  \
                       0/0/0/0/|        \\///      |     \\     \\       |  |
                    0/0/0/0/0/_|_ /   (  //       |      \\     _\\     |  /
                 0/0/0/0/0/0/`/,_ _ _/  ) ; -.    |    _ _\\.-~       /   /
                             ,-}        _      *-.|.-~-.           .~    ~
            \\     \\__/        `/\\      /                 ~-. _ .-~      /
             \\____(oo)           *.   }            {                   /
             (    (--)          .----~-.\\        \\-`                 .~
             //__\\\\  \\__ Ack!   ///.----..<        \\             _ -~
            //    \\\\               ///-._ _ _ _ _ _ _{^ - - - - ~'''})
