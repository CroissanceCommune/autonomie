Access FTP downloaded files through autonomie
=============================================

Autonomie provides views to download Treasury files, IncomeStatements and Salary sheets.

Files should be stored in the following directories :

* tresorerie/
* resultat/
* salaire/

Under a structure of tresorerie/<year>/<month>/

Files should be named with following the pattern
<code_compta>_year_month...

.. warning:: File security access is based on the filenames

The root path for these directories should be set in the ini file under the
main app section as autonomie.ftpdir::

.. code-block:: inifile

    [app:autonomie]
    ...
    autonomie.ftpdir=/var/ftpdir/caename/documents/
