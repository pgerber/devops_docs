#
Y
#

Lifecycle
=========

New customer:

1. Pilot system is created
2. Pilot system is promoted to production

Regular operation:

* Test system are created and removed
* Production system is copied to test
* Backup is restored

Customer leaves:

* All test systems are removed
* Production system is removed


Generic Test Systems (testNNN.tocco.ch)
=======================================

* Create new test$((NNN-1)).tocco.ch system based on test$((NNN)).tocco.ch


New Installation
================

#. Configure databases (hieradata)
#. Configure Solr core
#. a) Create database
   b) Copy database (from production)
#. Create DNS entry
#. Create OpenShift project
#. Create TeamCity project for customer
#. Create TeamCity project for instalation
#. Configure monitoring
#. Update configation in BO
