##
# NonRcptReport.py
#
# Usage:   NonRcptReport.py <file_mask> <CSV_output_file>
# Example: NonRcptReport.py "201710*" nonrcpt-report.csv

import argparse
import traceback

##
# Constants
PATTERN_DNS_ERROR = "Host or domain name not found"
DSN_PATTERNS = [
    PATTERN_DNS_ERROR,
    "address rejected",
    "does not exist",
    "no mailbox here",
    "no such user",
    "recipient rejected",
    "user invalid",
    "user unknown"
]

LOG_MASK = "/var/log/mail/mail.log-"

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filter", default="*", help="Mask used to filter files")
    parser.add_argument("-o", "--output", help="Path to an output file")
    result = parser.parse_args()

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
        #main(sys.argv)
        args = parse_args()
        print(args)
    except BaseException:
        handle_exception(sys.exc_info(), msg="UNHANDLED EXCEPTION")
