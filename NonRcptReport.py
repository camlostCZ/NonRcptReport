##
# NonRcptReport.py
#
# Usage:   NonRcptReport.py <file_mask> <CSV_output_file>
# Example: NonRcptReport.py "201710*" nonrcpt-report.csv

import argparse
import sys
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

    import traceback

    err_info = traceback.extract_tb(err[2], limit=-1)
    print("{0}: {1}".format(msg, err[0]))
    print("  file:      {0} (line {1})".format(err_info[0].filename, err_info[0].lineno))
    print("  function: ", err_info[0].name)
    print("  code:     ", err_info[0].line)

def parse_args():
    '''
    Parse command line arguments.

    Returns:
        Object as returned by parse_args()
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filter", default="*", help="Mask used to filter files")
    parser.add_argument("-o", "--output", help="Path to an output file")
    return parser.parse_args()

def main(args):
    '''
    Main function.

    Args:
        args: Object containinf cmdline arguments as properties

    Returns:
        none
    '''

    print(args)
    raise Exception('Not implemented yet')


if __name__ == "__main__":
    try:
        main(parse_args())
    except BaseException:
        handle_exception(sys.exc_info(), msg="UNHANDLED EXCEPTION")
