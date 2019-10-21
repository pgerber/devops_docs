S3 Buckets
==========

Naming Conventions for S3
--------------------------
================= ============================
 S3 user name      nice-**${customer}**
 S3 bucket name    tocco-nice-**${customer}**
================= ============================


Access the Web Interface
------------------------

S3 users and buckets can be managed via the web interface available at https://control.cloudscale.ch/objects.


Create a new S3 user
--------------------

Press the button *Create a new Object User* at the top-right. The *Display Name* is the name of the S3 user,
choose it accordingly to the naming convention above.

.. figure:: resources/s3_cloudscale_webclient.png

.. figure:: resources/create_new_user.png

Alternatively, users can be created via API. Here an example using ``curl``:

.. parsed-literal::

        curl -i -H 'Authorization: Bearer **${MY_ACCESS_TOKEN}**' -F display_name=\ **${NEW_USERNAME}** https\://api.cloudscale.ch/v1/objects-users

.. tip::

    API tokens can be managed `here <https://control.cloudscale.ch/user/api-tokens>`__.

.. tip::

    API documentation can be found `here <https://www.cloudscale.ch/en/api/v1#objects-users>`__


.. _s3-obtain-key:

Obtain the Access and Security Keys
-----------------------------------

The *Access Key* and *Secret Key* values correspond to the ``s3.main.accessKeyId`` and
``s3.main.secretAccessKey``, respectively, within the ``s3.properties`` file.

.. figure:: resources/check_keys.png

.. todo::

    Link to S3 properties description.


Create new S3 Bucket
--------------------

On the same page, press the button *Add a bucket* and pick a name in adherence to the
convention introduced above.

.. figure:: resources/add_bucket.png
