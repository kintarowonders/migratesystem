# migratesystem
Migrates a Gentoo web server's home directories, sites, and configuration.

This script is a work in progress. It will migrate the MySQL databases, nginx
configuration, web directories, home directories. It will merge all users in
the group users' passwd/shadow file entries. This will preserve UIDs on the
system.

Written by John Tate <john@johntate.org> http://johntate.org
