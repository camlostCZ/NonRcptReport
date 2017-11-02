##
# NonRcptReport.py
#
# Usage:   NonRcptReport.py <file_mask> <CSV_output_file>
# Example: NonRcptReport.py "201710*" nonrcpt-report.csv

import argparse
import dns.resolver
import glob
import gzip
import os.path
import re
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

#LOG_MASK = "/var/log/mail/mail.log-"
LOG_MASK = "C:/Users/sol60527/Downloads/!/log/m01/"


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


def is_email_domain(domain_name):
	'''
    Verify if specified domain is able to receive e-mail messages.
	domain_name is a string argument containing name of a domain,
	ex. "google.com".

    Args:
        domain_name (str): Domain name string.

    Returns:
        True if domain exists, otherwise False.
	'''
	res = dns.resolver.Resolver()
	res.nameservers = ["8.8.8.8", "8.8.4.4"]
	rec_types = ("MX", "A")
	answer_count = 0
	for item in rec_types:
		try:
			answer = res.query(domain_name, item)
			answer_count += len(answer)
			if answer_count > 0:
				break
		except (dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.NXDOMAIN):
			pass
		except dns.exception.Timeout:
			answer_count += 1
	return answer_count > 0


def process_line(line):

    def check_dsn_patterns(m):
        result = None
        is_nonexisting = False
        rcpt = m.group(2)
        relay = m.group(3)
        dsn = m.group(6)
        status = m.group(7)
        for pat in DSN_PATTERNS:
            is_nonexisting = is_nonexisting or re.search(pat, status)
            if is_nonexisting and re.search(PATTERN_DNS_ERROR, status):
                domain = re.sub(r"^[^@]+@", "", rcpt).strip()
                is_nonexisting = (len(domain) > 0 and not is_email_domain(domain))
            if is_nonexisting:
                result = (rcpt, dsn, pat, relay, status)
                break  # No need to check for other pattern matches
        return result

    regex_pat = "^[^\]]+\]:\s([^:]+):\sto=<([^>]*)>,\srelay=([^,]+),\sdelay=([^,]+),\sdelays=([^,]+),\sdsn=(5[^,]+),\sstatus=(.*)$"
    match = re.match(regex_pat,line)
    return check_dsn_patterns(match) if match else None


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


def process_file(filename, file_out):
    '''
    Process single file.

    Args:
        filename (str): Name of the file
        file_out (file object): Output file
    '''
    fp = gzip.open(filename, "rt") if re.search("\.gz$", filename) else open(filename, "r")
    for line in fp:
        data = process_line(line)
        if data:
            rcpt, dsn, pattern, relay, status = data
            print('"{0}","{1}"'.format(rcpt, pattern), file=file_out)
    fp.close()


def main(args):
    '''
    Main function.

    Args:
        args: Object containing cmdline arguments as properties

    Returns:
        none
    '''

    #print(args)
    search_filter = LOG_MASK + args.filter
    lst_files = glob.iglob(search_filter)
    f_out = open(args.output, "w") if args.output != None else sys.stdout
    for file in lst_files:
        print("Processing file ", os.path.basename(file))
        process_file(file, f_out)
    f_out.close()
    print("Done.")


if __name__ == "__main__":
    try:
        main(parse_args())
    except SystemExit:
        pass
    except BaseException:
        handle_exception(sys.exc_info(), msg="UNHANDLED EXCEPTION")
