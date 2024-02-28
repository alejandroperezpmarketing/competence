'''
Created on 27 feb. 2024

@author: vagrant
'''
import psycopg2
import settings

class Conn():
    conn=None
    cursor=None
    def __init__(self):
        self.conn=psycopg2.connect(database=settings.DATABASE, 
                      user=settings.USER, 
                      password=settings.PASSWORD, host=settings.HOST, 
                      port=settings.PORT)
        
        self.cursor=self.conn.cursor()
        
    def close(self):
        self.conn.close()
