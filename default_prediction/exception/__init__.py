import os
import sys

class ExceptionHandler(Exception):
    
    def __init__(self,error_message:Exception,error_detail:sys):
        
        super().__init__(error_message) ## super() is nothing but parent class initializer

        self.error_message = ExceptionHandler.get_detailed_error_message(error_message=error_message,error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        

        """
        error message = Exception Object
        error_details = Object of sys module
        """

        _,_ ,exec_tb = error_detail.exc_info()

        exception_block_line_number = exec_tb.tb_frame.f_lineno
        try_block_line_number = exec_tb.tb_lineno
            
        #line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename

        #error_message = f"Error occured in script : [{file_name}] at line number : [{line_number}] error message is:[{error_message}]"

        error_message = f"""Error occured in script: 
        [ {file_name} ] at 
        try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}] 
        error message: [{error_message}]
        """

        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self)->str:
        return ExceptionHandler.__name__.str()