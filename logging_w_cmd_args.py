'''

Basic example of python logging
module, with user cmd args
related to those logs.

=================================

Default behavior (no cmd args):

    1. print all messages from INFO
        up to stdout
    2. print all messages from DEBUG
        up to logfile 'out.log', in
        same dir as this python file.
        NOTE: EVERY TIME YOU RUN THIS
        FILE, IT WILL APPEND TO WHICHEVER
        LOG ITS WRITING TO. So, if you run
        this 3 times in a row with no args,
        it's not that the print statements
        are duplicating, it's that each
        run is appending to the same logfile.

=================================

Usage:

    python logging_w_cmd_args.py [-h] [--logfile LOGFILE]
                  [--stderr] [--noconsole]
                  [--nologfile] [--loglevel LOGLEVEL]
                  [--loglevelfile LOGLEVELFILE]


    -h / --help:
        Displays help message then quits.

    --logfile
        * A file to log to.
        * If relative path, will be relative
          to script dir.
        * If file doesn't exist, will create it.
        * If file does exist, will append to it.
        * If not supplied, defaults to 'out.log'
          (However, can disable logging to file
          via --nologfile arg)
        * --logfile None has same effect as
          --nolongfile (won't log to any file)

    --stderr
        If printing to console, print to
        stderr rather than stdout.

    --nologfile
        Do not print to a logfile.
        (same affect as --logfile None)

    --noconsole
        Don't print any logs to the console.
        (same affect as --loglevel None)

    --loglevel:
        level for console logging.
        "debug", "info", "warning",
        "error", "critical".

        Whichever chosen, it will log
        that and what's beneath. (e.g.
        --loglevel info will print
        all message of info and debug;
        --loglevel critical will print
        all messages.

        if None, will log NOTHING to console.

    --loglevel-logfile
        level for logfile.
        see --loglevel for valid log levels
        and what they mean.

'''

import sys
import os
import argparse
import logging
''' get a logger for this module '''
logger = logging.getLogger(__name__)
''' formatting to use for my logs '''
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


''' dir containing this .py file
(if --logfile is a rel path,
it will be rel this dir)
'''
FILEPATH = os.path.dirname(os.path.abspath(__file__))


'''Validate cmdarms related
to logging; set up program logging'''


def setup_logging(args):

    logfile = None
    loglevel_console = None
    loglevel_logfile = None

    '''check if a loglevel given
    to a cmd arg is valid
    (i.e. --loglevel debug)
    if so, return corresponding
    value for initializing logger
    to that level'''
    def check_loglevel(loglevel, argname):
        valid_loglevel_map = {
                "debug": logging.DEBUG,
                "info": logging.INFO,
                "warning": logging.WARNING,
                "error": logging.ERROR,
                "critical": logging.CRITICAL}
        valid_loglevels = valid_loglevel_map.keys()
        if loglevel not in valid_loglevels:
            raise Exception("""Invalid value for cmdarg {}.
                            Valid values: {}"""
                            .format(argname, str(valid_loglevels)))
        return valid_loglevel_map[loglevel]

    '''
    simple booleans indicating
    if console and/or log output
    will display, based on user
    args
    '''
    will_have_console_output = True
    if args.noconsole or not args.loglevel:
        will_have_console_output = False

    will_have_logfile = True
    if args.nologfile or args.logfile == "None":
        will_have_logfile = False

    '''
    Validate user args
    '''
    if args.stderr and not will_have_console_output:
        raise Exception("""Incompatable args: --stderr and
                        --noconsole. (Can't suppress console logs and
                        also print to stderr)""")

    '''
    Set up path for log file
    (if any is to be set up)
    '''

    if will_have_logfile:
        if not os.path.isabs(args.logfile):
            ''' --logfile was a relative path.
            make logfile rel dir of python script.
            P.S. os.path.normpath() will fix path
            in case a combination of UNIX and
            Windows notation. i.e. FILEPATH in UNIX
            notation, but --logfile ".\\myfolder\\log.txt"
            '''
            logfile = os.path.normpath(os.path.abspath(
                os.path.join(FILEPATH, args.logfile)))

    '''
    Determine log levels
    for console and/or logfile
    '''

    loglevel_logfile = check_loglevel(
                args.loglevelfile, "--loglevelfile")
    loglevel_console = check_loglevel(args.loglevel, "--loglevel")

    '''
    set up logging for application run

    You must call logging.basicConfig to
    configure things, and then you can
    add additional handlers after.
    '''

    if will_have_console_output:
        '''
        Set up basicConfig on stream
        (stdout or stderr)
        '''
        mystream = sys.stdout
        if args.stderr:
            mystream = sys.stderr
        logging.basicConfig(stream=mystream, level=loglevel_console)

        '''
        add additional file handler
        if also logging to file
        '''
        if logfile:
            fh = logging.FileHandler(logfile)
            fh.setLevel(loglevel_logfile)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    elif logfile:
        logging.basicConfig(filename=logfile, level=loglevel_logfile)
        '''
        if logging to console won't be
        in this else, so no need to
        check and add a StreamHandle
        '''
    else:
        '''
        dont want to log to console
        OR file; create dummy config
        and then disable everything
        '''
        logging.basicConfig()
        logging.disable(logging.CRITICAL)  # disables anything from critical down; hence everything


def main(args):
    parser = argparse.ArgumentParser(
        description="""An example use of python's logging module.
                    This script sets up logging and then
                    makes 5 print statements (one for each
                    of the loglevels in the logging module:
                    DEBUG, INFO, WARNING, ERROR, and CRITICAL.)

                    If you provide no cmd ags to the script,
                    if will:

                    (1) Print all messages from INFO up to stdout
                    (2) Print all messages from DEBUG up to a file
                        'out.log', which will be written in
                        this script's directory if it doesn't exist.
                        (Note: subsequent runs of the script will
                        append to this file, not overwrite it.)

                    Optionally, you can supply command line argument
                    to change the behavior of the logger. See below.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--logfile', default="out.log",
                        help="""Logfile to use.
                        Can be relative or absolute path.
                        If relative, will be rel script's dir.
                        If None, there will be no logfile.""")
    parser.add_argument('--stderr', action="store_true",
                        help="""If supplied, console logs will
                        print to stderr, not stdout.""")
    parser.add_argument('--noconsole', action="store_true",
                        help="""If supplied, console logs will
                        be suppressed.""")
    parser.add_argument('--nologfile', action="store_true",
                        help="""If supplied, no logfile will be
                        generated.""")
    parser.add_argument('--loglevel', default="info",
                        help="""Loglevel to use on the console. valid
                        values: debug, info, warning, error, critical""")
    parser.add_argument('--loglevelfile', default="debug",
                        help="""Loglevel to use in
                        the logfile. valid values: debug, info, warning,
                        error, critical""")

    # parse cmd args
    args = parser.parse_args(args)

    # validate logging args and set up the logger
    setup_logging(args)
    logger.debug("Debug logging test...")
    logger.info("Program is working as expected")
    logger.warning("Warning, the program may not function properly")
    logger.error("The program encountered an error")
    logger.critical("The program crashed")


if __name__ == "__main__":
    main(sys.argv[1:])
