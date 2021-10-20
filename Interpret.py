
class Interpret:
    space = ' '
    def __init__(self):
        self.__interpret = ''
        

    def add_header(self,  text ,level = 1):
        self.line_break()
        self.__interpret  = self.__interpret + '#' * level + self.space + text 
        self.line_break()
        self.line_break()


    def add_paragraph(self,text):
        self.__interpret = self.__interpret + text 
        self.line_break()
        self.line_break()


    def add_paragraphs(self,paragraphs_list):
        for paragraph in paragraphs_list:
            self.add_paragraph(paragraph)


    def add_text_and_break(self,text):
       self.add_text(text)
       self.line_break()
    
    
    def add_text (self,text ):
       self.__interpret = self.__interpret +  text + self.space
    

    def add_italic_text(self , text):
        self.__interpret = self.__interpret + '*' + text + '*' + self.space
        
    
    def add_bold_text (self,text ):
       self.__interpret = self.__interpret + '**' + text + '**' + self.space
       
    
    def add_italic_and_bold_text (self,text ):
       self.__interpret = self.__interpret + '***' + text + '***' + self.space      

    
    def add_block_quotes(self,text,level=1):
        self.__interpret = self.__interpret + '>' * level +  self.space + text 
        self.line_break()

    
    def draw_horizontal_line(self):
        self.__interpret = self.__interpret + '---'
        self.line_break()
    
    def add_bullet_text (self , text):
        self.__interpret = self.__interpret + '*' + self.space + text 
        self.line_break()

    def line_break(self):
        """
        after each self.line_break, other things start from the next line
        """
        self.__interpret = self.__interpret +"\n" 
        # self.__interpret = self.__interpret +
        #     "   \..."
        #     "sd"


    def get_text(self ):
        return self.__interpret






 
