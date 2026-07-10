A medication tracker: an owned `Cabinet` logs doses using the on-chain clock's millisecond
timestamp; logging a dose aborts if fewer than four hours (in milliseconds) have passed since
the previous one. Views: the last-dose timestamp and the total doses logged.
