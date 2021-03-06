import psycopg2
from psycopg2.extras import DictCursor ,RealDictCursor ,RealDictRow
from app.database.QueryFactory import QF
from argon2 import PasswordHasher , exceptions

dsn_web = "dbname='d1ufc7dp4m125k' user='kzkoadpajawjfo' host='ec2-54-235-114-242.compute-1.amazonaws.com' password='5bcd5e361babc3229beac6b0e6a2c7c509b7a576360dc7281806ab7744daf98b' port='5432'"
dsn = "dbname='rate_system' user='postgres' host='localhost' password='jojodio' port='5432'"
dsn_web2 = "dbname='d8qqm1tdt7a7p8' user='ehieysywbgqwmy' host='ec2-54-225-242-183.compute-1.amazonaws.com' password='846ad9e7a623935894144cada5935b40fd6e332cd9001ccb1fc19eeb742d12d5' port='5432'"
#dsn_old = "dbname='d8qqm1tdt7a7p8' user='ehieysywbgqwmy' host='ec2-54-225-242-183.compute-1.amazonaws.com' password=''"
psql = psycopg2
dcurs= DictCursor
qf  =   QF()
ph  =   PasswordHasher(hash_len=100)

class DataManager():

    def Connect(self):
        conn = psql.connect(dsn_web)
        curs = conn.cursor(cursor_factory=DictCursor)
        return  curs


    def CheckUser(self , username):
        curs = self.Connect()
        curs.execute("SELECT * FROM manage_persons WHERE manage_persons_login = '%s'" %(username,))
        if curs.fetchall():
            return True
        else:
            return False

    def GetDate(self):
        curs = self.Connect()
        curs.execute("select * from season")
        return curs.fetchall()

    def ShowAll(self):
        curs = self.Connect()
        curs.execute(qf.select_all())
        return curs.fetchall()

    def user_is_exist(self , log):
        is_user = False
        curs = self.Connect()
        curs.execute("SELECT manage_persons_login FROM manage_persons WHERE manage_persons_login = '%s'" % (log,) )
        if curs.fetchall():
            return True
        else:
            return False


    def AddUser(self ,login , password , privileges):
        conn = psql.connect(dsn_web)
        curs = conn.cursor()
        if  self.user_is_exist(login):
            print('user is exist')
            return False
        #     not add user
        else:
            print('user is not exist')
        #     add user
            h_password = ph.hash(password)
            curs.execute(qf.add_user_in_manage_persons(login,h_password,privileges))
            conn.commit()

    def GetIDTeacherByIIN(self , iin):
        curs = self.Connect()
        curs.execute("SELECT id_teacher FROM teachers WHERE iin_teacher = %s " , (iin,))
        return curs.fetchall()[0]

    def GetAllRecordsByTable(self , table ):
        curs = self.Connect()
        curs.execute("SELECT * FROM "+table)
        return curs.fetchall()

    def VerifyPassword(self , login , password):
        curs = self.Connect()
        curs.execute("SELECT manage_persons.manage_persons_password FROM manage_persons WHERE manage_persons.manage_persons_login=%s" , (login,))
        data = curs.fetchone()[0]
        try:
            if ph.verify(data,password):
                return True
        except exceptions.VerifyMismatchError:
            print('wrong password in ajax\n')
            return False

    def EditRecord(self , table , index):
        conn = psql.connect(dsn_web)
        curs = conn.cursor()
        curs.execute("UPDATE ")
        conn.commit()

    def GetTeacherRateByIin(self , IIN):
        curs = self.Connect()
        curs.execute(qf.get_teacher_rate_by_iin(IIN))
        return curs.fetchall()

    def GetManagePersonsPrivileges(self , username):
        curs = self.Connect()
        curs.execute("SELECT manage_persons.manage_persons_priv_value FROM manage_persons WHERE manage_persons_login= %s" , (username,))
        return curs.fetchone()[0]

    def GetSeasonByTeacher(self):
        print()

    def GetRateByTeacher(self , id_teach):
        curs = self.Connect()
        curs.execute("SELECT val_rate , id_indicator FROM rate WHERE id_teacher = %s" ,(id_teach,))
        return curs.fetchall()

    #dev
    def GetIndicators(self , group):
        curs = self.Connect()
        curs.execute("SELECT indicator.indicator_id , indicator.indicator_name FROM indicator INNER JOIN indicator_group ON indicator_group.indicator_group_id ='%i' and indicator.indicator_group_id=indicator_group.indicator_group_id" % group)
        return curs.fetchall()

    #dev
    def GetGroupIndicators(self):
        curs = self.Connect()
        curs.execute("SELECT * FROM indicator_group")
        return curs.fetchall()

    #dev
    def AddGroupInds(self , name):
        conn = psql.connect(dsn_web)
        curs = conn.cursor()
        curs.execute("INSERT INTO indicator_group(indicator_group_name) VALUES('%s')" % name)
        conn.commit()
    #dev
    def DelGroupInds(self , id):
        conn = psql.connect(dsn_web)
        curs = conn.cursor()
        curs.execute("DELETE FROM indicator_group WHERE indicator_group_id = '%i'" % id)
        conn.commit()
    #dev
    def AddInds(self , select , name):
        conn = psql.connect(dsn_web)
        curs = conn.cursor()
        curs.execute("INSERT INTO indicator(indicator_name , indicator_group_id) VALUES('%s' , '%i')" % (name , select,))
        conn.commit()
    #dev
    def DelInds(self , id):
        conn = psql.connect(dsn_web)
        curs = conn.cursor()
        curs.execute("DELETE FROM indicator WHERE indicator_id = '%i'" % id)
        conn.commit()

    def GetTeachersByManagePerson(self , id_mp , id_season):
        curs = self.Connect()
        curs.execute(QF.get_teachers_and_rate_value_by_manager_teachers(self ,id_mp , id_season))
        return curs.fetchall()
    #dev
    def JOIN(self):
        curs = self.Connect()
        curs.execute('''
					SELECT
					  teachers.sname_t , login
					FROM
					  teachers
					INNER JOIN
					  manage_persons
					ON
					  manage_persons.id_user=1
						AND
					  teachers."Id_teacher_group" = manage_persons.id_user;
					''')
        # curs.execute("SELECT * FROM teachers")
        return curs.fetchall()

    #dev
    def GetIINs(self):
        curs = self.Connect()
        curs.execute("SELECT * From teachers")
        return curs.fetchall()
