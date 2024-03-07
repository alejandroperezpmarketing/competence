#import psycopg2
import json

class Conn():
    conn=None
    cursor=None
    
    def __init__(self) -> None:
                
        self._user = None
        
    def __repr__(self) -> str:
        
        report = {
            
            "user":self._user      
            
        }
        
        report = json.dumps(report,indent=4)
        
        return report
    
    def _get_user(self):
       
        return self._user

    def _set_user(self, code):
        
         self._user = code
        
        
    user = property(fget=_get_user,fset=_set_user)