#!/usr/bin/python3

from systemd import journal
import logging, uuid, sys, getopt
import serial
import signal

def signal_handler(sig, frame):
    print("Exiting program")
    sys.exit(0)

def main(argv):
    port = ' '
    baud = ' '
    logger_name = ' '

    try:
        opts, args = getopt.getopt(argv, "p:b:n:")
    except getopt.GetoptError:
        print('log.py -p "TTY port" -b "baudrate" -n "logger name"\n')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-p':
            port = arg
        elif opt == '-b':
            baud = arg
        elif opt == '-n':
            logger_name = arg

    if port == ' ' or baud == ' ' or logger_name == ' ':
        print('log.py -p "TTY port" -b "baudrate" -n "logger name"\n')
        sys.exit(2)


    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(logger_name)
    logger.addHandler(journal.JournaldLogHandler())

    ser = serial.Serial()
    ser.baudrate = baud
    ser.port = port
    ser.timeout = 1
    ser.open()

    lastLine = ''
    except_lines_left = 0
    while True:
        try:
            line = ser.readline().decode()
            if line != '' and line != lastLine:
                lastLine = line

                if "reset" in line:
                    except_lines_left = 25

                if except_lines_left > 0:
                    logger.error(line.rstrip())
                    except_lines_left -= 1
                else:
                    logger.info(line.rstrip())
        except UnicodeDecodeError:
            logger.info("UnicodeDecodeError. ESP probably restarted")




signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    if len(sys.argv) <4:
        print('log.py -p "TTY port" -b "baudrate" -n "logger name"\n')
        sys.exit(2)

    main(sys.argv[1:])

