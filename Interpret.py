
class Interpret:
    def __init__(self):
        self.__interpret = ''
        pass
    
    def bind_header(self,  text ,level = 1):
        self.__interpret  = self.__interpret + '#'*level + ' ' + text + '  ' +"\n"
    
    def bind(self,text):
        self.__interpret = self.__interpret + text + '  '
    
    def italic_and_bind(self , text):
        self.__interpret = self.__interpret + '*' + text + '*  '
        
    
    def bold_and_bind (self,text ):
       self.__interpret = self.__interpret + '**' + text + '**'
       
    
    def bold_and_italic_and_bind (self,text ):
       self.__interpret = self.__interpret + '***' + text + '***'
      
    
    def line_break(self):
        self.__interpret = self.__interpret + '  '
    
    def add_block_quotes(self,text,level=1):
        self.__interpret = self.__interpret + '>'*level + ' ' + text + '  ' 
    
    def draw_horizontal_line(self):
        self.__interpret = self.__interpret + '---'
    
    def add_bullet_text (self , text):
        self.__interpret = self.__interpret + '* ' + text + '  '

    def get_text(self ):
        return self.__interpret






 
