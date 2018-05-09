Incident Analysis
=================

Installation is Unreachable or Unavailable
------------------------------------------

Hostname Resolution Failure, No Such Domain
```````````````````````````````````````````

    Symptoms:

        * ``dig $HOSTNAME`` output contains ``status: NXDOMAIN``
        * Firefox: "Hmm. We’re having trouble finding that site." (older version "Server not found")

    Cause:

        The DNS server reports that the hostname doesn't exist.

    Solution:

        Ensure the DNS records are corrected. See :doc:`/devops/openshift/dns`.


Hostname Resulution Failure, DNS Server Misbehaving
```````````````````````````````````````````````````

   Symptoms:

      * ``dig $HOSTNAME`` output contains ``status: SERFAIL``
      * Firefox: "Hmm. We’re having trouble finding that site." (older version "Server not found")

   Causes: DNS server down or misconfigured


Connection Refused
``````````````````

   Symptoms:

       * ``curl -sS -o /dev/null --connect-timeout 10 https://${HOSTNAME}/`` fails wtih "Connection refused"
       * Firefox: "Unable to connect"

   Cause:

        * Endpoint (HAProxy) unavailable
        * DNS is misconfigured


   Solution:

        * Ensure HAProxy is available:
            * check the `VSHN Status Page`_
            * check if requests suceed:
                * ``curl -sS -o /dev/null http://5.102.151.2``
                * ``curl -sS -o /dev/null http://5.102.151.3``
        * Ensure DNS is set up correctly. See :ref:`verify-dns-records`.


Connection Time-Out
```````````````````

   Symptoms:

       * ``curl -sS -o /dev/null --connect-timeout 10 https://${HOSTNAME}/`` fails with "Connection timed out"
       * Firefox: afer a long delay, "The connection has timed out"

   Solution:

        * Ensure HAProxy is available:
            * check the `VSHN Status Page`_
            * check if requests suceed:
                * ``curl -sS -o /dev/null http://5.102.151.2``
                * ``curl -sS -o /dev/null http://5.102.151.3``
        * Ensure DNS is set up correctly. See :ref:`verify-dns-records`.


Application Unavailable
```````````````````````

   Symptoms:

       * Browser: error page stating "Application is not available"

   Cause: No instance of the application is ready

   Solution:

       * Check if there is a running and ready instance::

             $ oc project toco-nice-${INSTALLATION}
             $ oc get pods
             NAME           READY     STATUS    RESTARTS   AGE
             nice-1-r8ks6   2/2       Running   0          4h
             solr-1-s3bpd   1/1       Running   0          4h

         There must be at least one ready (``2/2``) nice-* instance.

       * Check for events::

             $ oc describe pod ${POD}
             …
             Events:
               FirstSeen LastSeen    Count   From                    SubObjectPath       Type        Reason      Message
               --------- --------    -----   ----                    -------------       --------    ------      -------
               …
               25m       25m     1   kubelet, node26.prod.zrh.appuio.ch  spec.containers{nice}   Normal      Started     Started container
               25m       24m     9   kubelet, node26.prod.zrh.appuio.ch  spec.containers{nice}   Warning     Unhealthy   Readiness probe failed: Get http://10.1.4.249:8080/status-tocco: net/http: request canceled (Client.Timeout exceeded while awaiting headers)

       * Check logs::

             oc logs ${POD}

         and logs of previous pods (before a restart)::

             oc logs -p ${POD}

       * Startup error
       * liveness/readiness probes

       NOTE: metion what to do when application doesn't start


Domain / Host not Configured (Code 404)
```````````````````````````````````````

    Symptoms:

        Browser: Tocco-themed "Error 404: Not Found" is showna.

    Caused:

        CMS configuration missing or incorrect (https vs http and www.domain vs domain)

    Solution:

        In Nice, go to Web → Content Management, double click on the respective domain. Ensure domain is entered as URL
        or alias. Ensure both, an entry for http:// and for https:// exists.


Invalid SSL/TLS Certifcate
``````````````````````````

   Symptoms:

        * ``curl -sS -o /dev/null --connect-timeout 10 https://${HOSTNAME}/`` reports "SSL: no alternative
          certificate for …" (or similar)
        * Firefox: Your connection is not secure

   Cause: no certificate issued, no route configured


Slow System or Keeps Restarting
-------------------------------

System is Responding but only with Delay
````````````````````````````````````````

   Sympoms:

        The system generally slow and/or unavailable for short periods of time

   Cause: DB connection pool exhausted, DB server overloaded, thread pool exhausted, low memory, …

Mails
-----

Mails Can't be Sent
```````````````````

   Symptoms:

       Error message when sending mails (message in logs).


Outgoing Mails are not Received
```````````````````````````````

   Symptoms:

      Log indicates that message was sent (``Mail sent!`` in logs) but mail is never received.


   Cause: Spam filtered (DKIM, SPF incorrect), relay blocked, mail rejected (SPI, DKIM), Sender rewrite not set up


Search Index Unavailable
````````````````````````

   Symptoms:

        * Search no longer works
        * Log shows Solr-related error messages


  Cause: index corrption, solr crashed, out of disk space


Search index inconsistent
`````````````````````````

   Symptoms:

        * Search works but there are missing results

   Cause: Solr wasn't available (e.g. restart), application crash, Solr write error
