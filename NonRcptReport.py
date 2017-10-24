##
# NonRcptReport.py
#
# Usage:   NonRcptReport.py <file_mask> <CSV_output_file>
# Example: NonRcptReport.py "201710*" nonrcpt-report.csv

import traceback

def handle_exception(err, msg="ERROR"):
    '''
    Print exception info.

    Args:
        err:      Exception object as returned by sys.exc_info()
        msg(str): Label printed before exception name
    '''
    err_info = traceback.extract_tb(err[2], limit=-1)
    print("{0}: {1}".format(msg, err[0]))
    print("  file:      {0} (line {1})".format(err_info[0].filename, err_info[0].lineno))
    print("  function: ", err_info[0].name)
    print("  code:     ", err_info[0].line)

def main(args):
    '''
    Main function.

    Args:
        args (str[]): List of cmdline arguments

    Returns:
        none
    '''

    raise(Exception('spam', 'eggs'))
    pass

if __name__ == "__main__":
    import sys
    try:
        main(sys.argv)
    except BaseException:
        handle_exception(sys.exc_info(), msg="UNHANDLED EXCEPTION")
