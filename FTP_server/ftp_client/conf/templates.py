#/usr/bin/env python

class r_temp(object):

    def logininfo(self):
        login_info="""\033[32m
        ------------ welcome to the combat system ------------
            1 login the system
            2 register a account
            3 Exit
        ------------------------------------------------------
        \033[0m
            please input  serials number
        """
        return login_info

    def ruleinfo(self):
        Rule_info="""\033[34m
        \tYour should chose one Rule Now

        \t1 令狐冲(English's name：Lhc)
        \t2 孙悟空(English's name: Swk)
        \t3 Exit
        \033[0m
            please input  serials number
        """
        return Rule_info

    def weaponinfo(self):
        msg="""\033[34m
        \tYour should chose one Rule Now

        \t1 倚天剑(ytj)
        \t2 屠龙刀(tld)
        \t3 Exit
        \033[0m
            please input  serials number

        """
        return  msg

    def chose_game(self):
        msg="""\033[34m
        \t1 开启新的征程
        \t2 返回旧的征程
        \t3 Exit
        \033[0m
            please input  serials number
        """
        return msg

    #settings.weapon_harm_value.get(settings.weapon_list.get(str(random.randint(1,2))))