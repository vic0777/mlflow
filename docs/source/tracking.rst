.. _tracking:

===============
MLflow Tracking
===============

The MLflow Tracking component is an API and UI for logging parameters, code versions, metrics, and output files
when running your machine learning code and for later visualizing the results.
MLflow Tracking lets you log and query experiments using :ref:`Python <python-api>`, :ref:`REST <rest-api>`, :ref:`R-api`, 
and :ref:`java_api` APIs.

.. contents:: Table of Contents
  :local:
  :depth: 2

Concepts
========

MLflow Tracking is organized around the concept of *runs*, which are executions of some piece of
data science code. Each run records the following information:

Code Version
    Git commit hash used for the run, if it was run from an :ref:`MLflow Project <projects>`.

Start & End Time
    Start and end time of the run

Source
    Name of the file to launch the run, or the project name and entry point for the run
    if run from an :ref:`MLflow Project <projects>`.

Parameters
    Key-value input parameters of your choice. Both keys and values are strings.

Metrics
    Key-value metrics where the value is numeric. Each metric can be updated throughout the
    course of the run (for example, to track how your model's loss function is converging), and
    MLflow records and lets you visualize the metric's full history.

Artifacts
    Output files in any format. For example, you can record images (for example, PNGs), models
    (for example, a pickled scikit-learn model), or even data files (for example, a
    `Parquet <https://parquet.apache.org/>`_ file) as artifacts.

You can record runs using MLflow Python, R, Java, and REST APIs from anywhere you run your code. For
example, you can record them in a standalone program, on a remote cloud machine, or in an
interactive notebook. If you record runs in an :ref:`MLflow Project <projects>`, MLflow
remembers the project URI and source version.

You can optionally organize runs into *experiments*, which group together runs for a
specific task. You can create an experiment using the ``mlflow experiments`` CLI, with
:py:func:`mlflow.create_experiment`, or using the corresponding REST parameters. The MLflow API and
UI let you create and search for experiments.

Once your runs have been recorded, you can query them using the :ref:`tracking_ui` or the MLflow
API.

.. _where-runs-are-recorded:

Where Runs Are Recorded
=======================

MLflow runs can be recorded to local files, to a SQLAlchemy compatible database, or remotely
to a tracking server.
By default, the MLflow Python API logs runs locally to files in an ``mlruns`` directory wherever you
ran your program. You can then run ``mlflow ui`` to see the logged runs. 

To log runs remotely, set the ``MLFLOW_TRACKING_URI`` environment variable to a tracking server's URI or 
call :py:func:`mlflow.set_tracking_uri`.

There are different kinds of remote tracking URIs:

- Local file path (specified as ``file:/my/local/dir``), where data is just directly stored locally.
- Database encoded as ``<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>``. Mlflow supports the dialects ``mysql``, ``mssql``, ``sqlite``, and ``postgresql``. For more details, see `SQLAlchemy database uri <https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls>`_.
- HTTP server (specified as ``https://my-server:5000``), which is a server hosting an :ref:`MLFlow tracking server <tracking_server>`.
- Databricks workspace (specified as ``databricks`` or as ``databricks://<profileName>``, a `Databricks CLI profile <https://github.com/databricks/databricks-cli#installation>`_.

Logging Data to Runs
====================

You can log data to runs using the MLflow Python, R, Java, or REST API. This section
shows the Python API.

.. _basic_logging_functions:

Basic Logging Functions
-----------------------

:py:func:`mlflow.set_tracking_uri` connects to a tracking URI. You can also set the
``MLFLOW_TRACKING_URI`` environment variable to have MLflow find a URI from there. In both cases,
the URI can either be a HTTP/HTTPS URI for a remote server, a database connection string, or a
local path to log data to a directory. The URI defaults to ``mlruns``.

:py:func:`mlflow.tracking.get_tracking_uri` returns the current tracking URI.

:py:func:`mlflow.create_experiment` creates a new experiment and returns its ID. Runs can be
launched under the experiment by passing the experiment ID to ``mlflow.start_run``.

:py:func:`mlflow.set_experiment` sets an experiment as active. If the experiment does not exist,
creates a new experiment. If you do not specify an experiment in :py:func:`mlflow.start_run`, new
runs are launched under this experiment.

:py:func:`mlflow.start_run` returns the currently active run (if one exists), or starts a new run
and returns a :py:class:`mlflow.ActiveRun` object usable as a context manager for the
current run. You do not need to call ``start_run`` explicitly: calling one of the logging functions
with no active run automatically starts a new one.

:py:func:`mlflow.end_run` ends the currently active run, if any, taking an optional run status.

:py:func:`mlflow.active_run` returns a :py:class:`mlflow.entities.Run` object corresponding to the
currently active run, if any.

:py:func:`mlflow.log_param` logs a single key-value param in the currently active run. The key and
value are both strings. Use :py:func:`mlflow.log_params` to log multiple params at once.

:py:func:`mlflow.log_metric` logs a single key-value metric. The value must always be a number.
MLflow remembers the history of values for each metric. Use :py:func:`mlflow.log_metrics` to log
multiple metrics at once.

:py:func:`mlflow.set_tag` sets a single key-value tag in the currently active run. The key and
value are both strings. Use :py:func:`mlflow.set_tags` to set multiple tags at once.

:py:func:`mlflow.log_artifact` logs a local file as an artifact, optionally taking an
``artifact_path`` to place it in within the run's artifact URI. Run artifacts can be organized into
directories, so you can place the artifact in a directory this way.

:py:func:`mlflow.log_artifacts` logs all the files in a given directory as artifacts, again taking
an optional ``artifact_path``.

:py:func:`mlflow.get_artifact_uri` returns the URI that artifacts from the current run should be
logged to.


Launching Multiple Runs in One Program
--------------------------------------

Sometimes you want to launch multiple MLflow runs in the same program: for example, maybe you are
performing a hyperparameter search locally or your experiments are just very fast to run. This is
easy to do because the ``ActiveRun`` object returned by :py:func:`mlflow.start_run` is a Python
`context manager <https://docs.python.org/2.5/whatsnew/pep-343.html>`_. You can "scope" each run to
just one block of code as follows:

.. code-block:: py

   with mlflow.start_run():
       mlflow.log_param("x", 1)
       mlflow.log_metric("y", 2)
       ...

The run remains open throughout the ``with`` statement, and is automatically closed when the
statement exits, even if it exits due to an exception.

.. _organizing-runs-in-experiments:

Organizing Runs in Experiments
==============================

MLflow allows you to group runs under experiments, which can be useful for comparing runs intended
to tackle a particular task. You can create experiments using the :ref:`cli` (``mlflow experiments``) or
the :py:func:`mlflow.create_experiment` Python API. You can pass the experiment ID for a individual run
using the CLI (for example, ``mlflow run ... --experiment-id [ID]``) or the ``MLFLOW_EXPERIMENT_ID``
environment variable.

.. code-block:: bash

    # Prints "created an experiment with ID <id>
    mlflow experiments create fraud-detection
    # Set the ID via environment variables
    export MLFLOW_EXPERIMENT_ID=<id>

.. code-block:: py

    # Launch a run. The experiment ID is inferred from the MLFLOW_EXPERIMENT_ID environment
    # variable, or from the --experiment-id parameter passed to the MLflow CLI (the latter
    # taking precedence)
    with mlflow.start_run():
        mlflow.log_param("a", 1)
        mlflow.log_metric("b", 2)

Managing Experiments and Runs with the Tracking Service API
-----------------------------------------------------------

MLflow provides a more detailed Tracking Service API for managing experiments and runs directly,
which is available through client SDK in the :py:mod:`mlflow.tracking` module.
This makes it possible to query data about past runs, log additional information about them, create experiments, 
add tags to a run, and more.

.. rubric:: Example

.. code-block:: py

    from  mlflow.tracking import MlflowClient
    client = MlflowClient()
    experiments = client.list_experiments() # returns a list of mlflow.entities.Experiment
    run = client.create_run(experiments[0].experiment_id) # returns mlflow.entities.Run
    client.log_param(run.info.run_uuid, "hello", "world")
    client.set_terminated(run.info.run_uuid)

.. _tracking_ui:

Adding Tags to Runs
~~~~~~~~~~~~~~~~~~~

The :py:func:`mlflow.tracking.MlflowClient.set_tag` function lets you add custom tags to runs. For example:

.. code-block:: py

  client.set_tag(run.info.run_uuid, "tag_key", "tag_value")
  
.. important:: Do not use the prefix ``mlflow`` for a tag.  This prefix is reserved for use by MLflow.


Tracking UI
===========

The Tracking UI lets you visualize, search and compare runs, as well as download run artifacts or
metadata for analysis in other tools. If you have been logging runs to a local ``mlruns`` directory,
run ``mlflow ui`` in the directory above it, and it loads the corresponding runs.
Alternatively, the :ref:`MLflow tracking server <tracking_server>` serves the same UI and enables remote storage of run artifacts.

The UI contains the following key features:

* Experiment-based run listing and comparison
* Searching for runs by parameter or metric value
* Visualizing run metrics
* Downloading run results

.. _tracking_query_api:

Querying Runs Programmatically
==============================

All of the functions in the Tracking UI can be accessed programmatically. This makes it easy to do several common tasks:

* Query and compare runs using any data analysis tool of your choice, for example, **pandas**. 
* Determine the artifact URI for a run to feed some of its artifacts into a new run when executing a workflow. For an example of querying runs and constructing a multistep workflow, see the MLflow `Multistep Workflow Example project <https://github.com/mlflow/mlflow/blob/15cc05ce2217b7c7af4133977b07542934a9a19f/examples/multistep_workflow/main.py#L63>`_.
* Load artifacts from past runs as :ref:`models`. For an example of training, exporting, and loading a model, and predicting using the model, see the MLFlow `TensorFlow example <https://github.com/mlflow/mlflow/tree/master/examples/tensorflow>`_.
* Run automated parameter search algorithms, where you query the metrics from various runs to submit new ones. For an example of running automated parameter search algorithms, see the MLflow `Hyperparameter Tuning Example project <https://github.com/mlflow/mlflow/blob/master/examples/hyperparam/README.rst>`_.


.. _tracking_server:

MLflow Tracking Servers
=======================

.. contents:: In this section:
  :local:
  :depth: 2

You run an MLflow tracking server using ``mlflow server``.  An example configuration for a server is:

.. code-block:: bash

    mlflow server \
        --backend-store-uri /mnt/persistent-disk \
        --default-artifact-root s3://my-mlflow-bucket/ \
        --host 0.0.0.0

Storage
-------

An MLflow tracking server has two components for storage: a *backend store* and an *artifact store*.

The backend store is where MLflow Tracking Server stores experiment and run metadata as well as
params, metrics, and tags for runs. MLflow supports two types of backend stores: *file store* and
*database-backed store*.

Use ``--backend-store-uri`` to configure the type of backend store. You specify a *file store*
backend as ``./path_to_store`` or ``file:/path_to_store`` and a *database-backed store* as
`SQLAlchemy database URI <https://docs.sqlalchemy.org/en/latest/core/engines
.html#database-urls>`_. The database URI typically takes the format ``<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>``.
MLflow supports the database dialects ``mysql``, ``mssql``, ``sqlite``, and ``postgresql``.
Drivers are optional. If you do not specify a driver, SQLAlchemy uses a dialect's default driver.
For backwards compatibility, ``--file-store`` is an alias for ``--backend-store-uri``.

.. important::

    ``mlflow server`` will fail against a database-backed store with an out-of-date database schema.
    To prevent this, upgrade your database schema to the latest supported version via
    ``mlflow db upgrade [db_uri]``. Note that schema migrations can result in database downtime, may
    take longer on larger databases, and are not guaranteed to be transactional. As such, always
    take a backup of your database prior to running ``mlflow db upgrade`` - consult your database's
    documentation for instructions on taking a backup.


By default ``--backend-store-uri`` is set to the local ``./mlruns`` directory (the same as when
running ``mlflow run`` locally), but when running a server, make sure that this points to a
persistent (that is, non-ephemeral) file system location.


The artifact store is a location suitable for large data (such as an S3 bucket or shared NFS
file system) and is where clients log their artifact output (for example, models).
``artifact_location`` is a property recorded on :py:class:`mlflow.entities.Experiment` for
default location to store artifacts for all runs in this experiment. Additional, ``artifact_uri``
is a property on :py:class:`mlflow.entities.RunInfo` to indicate location where all artifacts for
this run are stored.

Use ``--default-artifact-root`` (defaults to local ``./mlruns`` directory) to configure default
location to server's artifact store. This will be used as artifact location for newly-created
experiments that do not specify one. Once you create an experiment, ``--default-artifact-root``
is no longer relevant to that experiment.

To allow the server and clients to access the artifact location, you should configure your cloud
provider credentials as normal. For example, for S3, you can set the ``AWS_ACCESS_KEY_ID``
and ``AWS_SECRET_ACCESS_KEY`` environment variables, use an IAM role, or configure a default
profile in ``~/.aws/credentials``.
See `Set up AWS Credentials and Region for Development <https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/setup-credentials.html>`_ for more info.

.. important::

  If you do not specify a ``--default-artifact-root`` or an artifact URI when creating the experiment
  (for example, ``mlflow experiments create --artifact-location s3://<my-bucket>``), the artifact root
  is a path inside the file store. Typically this is not an appropriate location, as the client and
  server probably refer to different physical locations (that is, the same path on different disks).

Supported Artifact Stores
~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to local file paths, MLflow supports the following storage systems as artifact
stores: Amazon S3, Azure Blob Storage, Google Cloud Storage, SFTP server, and NFS.

Amazon S3
^^^^^^^^^

To store artifacts in S3, specify a URI of the form ``s3://<bucket>/<path>``. MLflow obtains
credentials to access S3 from your machine's IAM role, a profile in ``~/.aws/credentials``, or
the environment variables ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` depending on which of
these are available. For more information on how to set credentials, see
`Set up AWS Credentials and Region for Development <https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/setup-credentials.html>`_.

To store artifacts in a custom endpoint, set the ``MLFLOW_S3_ENDPOINT_URL`` to your endpoint's URL.
For example, if you have a Minio server at 1.2.3.4 on port 9000:

.. code-block:: bash

  export MLFLOW_S3_ENDPOINT_URL=http://1.2.3.4:9000

Azure Blob Storage
^^^^^^^^^^^^^^^^^^

To store artifacts in Azure Blob Storage, specify a URI of the form
``wasbs://<container>@<storage-account>.blob.core.windows.net/<path>``.
MLflow expects Azure Storage access credentials in the
``AZURE_STORAGE_CONNECTION_STRING`` or ``AZURE_STORAGE_ACCESS_KEY`` environment variables (preferring
a connection string if one is set), so you must set one of these variables on both your client
application and your MLflow tracking server. Finally, you must run ``pip install azure-storage``
separately (on both your client and the server) to access Azure Blob Storage; MLflow does not declare
a dependency on this package by default.

Google Cloud Storage
^^^^^^^^^^^^^^^^^^^^

To store artifacts in Google Cloud Storage, specify a URI of the form ``gs://<bucket>/<path>``.
You should configure credentials for accessing the GCS container on the client and server as described
in the `GCS documentation <https://google-cloud.readthedocs.io/en/latest/core/auth.html>`_.
Finally, you must run ``pip install google-cloud-storage`` (on both your client and the server)
to access Google Cloud Storage; MLflow does not declare a dependency on this package by default.

FTP server
^^^^^^^^^^^

Specify a URI of the form ftp://user@host/path/to/directory to store artifacts in a FTP server. 
The URI may optionally include a password for logging into the server, e.g. ``ftp://user:pass@host/path/to/directory``

SFTP Server
^^^^^^^^^^^

To store artifacts in an SFTP server, specify a URI of the form ``sftp://user@host/path/to/directory``.
You should configure the client to be able to log in to the SFTP server without a password over SSH (e.g. public key, identity file in ssh_config, etc.).

The format ``sftp://user:pass@host/`` is supported for logging in. However, for safety reasons this is not recommended.

When using this store, ``pysftp`` must be installed on both the server and the client. Run ``pip install pysftp`` to install the required package.

NFS
^^^

To store artifacts in an NFS mount, specify a URI as a normal file system path, e.g., ``/mnt/nfs``.
This path must the same on both the server and the client -- you may need to use symlinks or remount
the client in order to enforce this property.


HDFS
^^^^

To store artifacts in HDFS, specify a ``hdfs:`` URI. It can contain host and port:

|     ``hdfs://<host>:<port>/<path>`` or just the path:
|     ``hdfs://<path>``
|

There are also two ways to authenticate to HDFS:

- Use current UNIX account authorization
- Kerberos credentials using following environment variables:

.. code-block:: bash

  export MLFLOW_KERBEROS_TICKET_CACHE=/tmp/krb5cc_22222222
  export MLFLOW_KERBEROS_USER=user_name_to_use

Most of the cluster contest settings is read from ```hdfs-site.xml``` accessed by the HDFS native driver
driver using the ``CLASSPATH`` environment variable.

Optionally one can select a different version of the HDFS driver library using:

.. code-block:: bash

  export MLFLOW_HDFS_DRIVER=libhdfs3

The default one is ```libhdfs```.

Networking
----------

The ``--host`` option exposes the service on all interfaces. If running a server in production, we
would recommend not exposing the built-in server broadly (as it is unauthenticated and unencrypted),
and instead putting it behind a reverse proxy like NGINX or Apache httpd, or connecting over VPN.
Additionally, you should ensure that the ``--backend-store-uri`` (which defaults to the
``./mlruns`` directory) points to a persistent (non-ephemeral) disk or database connection.

Logging to a Tracking Server
----------------------------

To log to a tracking server, set the ``MLFLOW_TRACKING_URI`` environment variable to the server's URI, 
along with its scheme and port (for example, ``http://10.0.0.1:5000``) or call :py:func:`mlflow.set_tracking_uri`. 

The :py:func:`mlflow.start_run`, :py:func:`mlflow.log_param`, and :py:func:`mlflow.log_metric` calls 
then make API requests to your remote tracking server.

.. code-block:: py

    import mlflow
    with mlflow.start_run():
        mlflow.log_param("a", 1)
        mlflow.log_metric("b", 2)

.. _system_tags:

System Tags
===========

You can annotate runs with arbitrary tags. Tag keys that start with ``mlflow.`` are reserved for
internal use. The following tags are set automatically by MLflow, when appropriate:

+-------------------------------+----------------------------------------------------------------------------------------+
| Key                           | Description                                                                            |
+===============================+========================================================================================+
| ``mlflow.runName``            | Human readable name that identifies this run.                                          |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.parentRunId``        | The ID of the parent run, if this is a nested run.                                     |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.user``               | Identifier of the user who created the run.                                            |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.source.type``        | Source type (possible values are ``"NOTEBOOK"``, ``"JOB"``, ``"PROJECT"``,             |
|                               | ``"LOCAL"``, and ``"UNKNOWN"``)                                                        |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.source.name``        | Source identifier (e.g., GitHub URL, local Python filename, name of notebook)          |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.source.git.commit``  | Commit hash of the executed code, if in a git repository.                              |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.source.git.branch``  | Name of the branch of the executed code, if in a git repository.                       |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.source.git.repoURL`` | URL that the executed code was cloned from.                                            |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.project.env``        | One of "docker" or "conda", indicating the runtime context used by the MLflow project. |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.project.entryPoint`` | Name of the project entry point associated with the current run, if any.               |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.docker.image.name``  | Name of the Docker image used to execute this run.                                     |
+-------------------------------+----------------------------------------------------------------------------------------+
| ``mlflow.docker.image.id``    | ID of the Docker image used to execute this run.                                       |
+-------------------------------+----------------------------------------------------------------------------------------+
