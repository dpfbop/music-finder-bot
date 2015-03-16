#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time
from daemon import Daemon

class MyDaemon(Daemon):
    def run(self):
        main()
        

if __name__ == "__main__":
    from main import *
    import config
    config = reload(config)
    daemon = MyDaemon('/tmp/daemon-' + config.BOT_NAME + '-' + '.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            if not config.BOT_ENABLED:
                print config.BOT_NAME + " bot is not enabled."
                sys.exit(0)
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.stop()
            if not config.BOT_ENABLED:
                print config.BOT_NAME + " bot is not enabled."
                sys.exit(0)
            daemon.start()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
