EPyRBa - Epicalc Python and R Backend
=====================================

Backend and mini-fronend for Epicalc in R

Installation
------------

.. code:: bash

    $ pip install -r requirements.txt
    $ Rscript init.R
    $ export FLASK_APP=epyrba
    $ flask run --port 5001

And then open your webbrowser in http://localhost:5001


### Deplyment

- run `$heroku create`
- Install R aside Python in heroku
  https://www.r-bloggers.com/running-an-r-script-on-heroku/
- git push heroku master


Authors
-------

-  Juan B Cabral (CIFASIS-UNR, IATE-OAC-UNC).
-  Mauricio Koraj (Liricus SRL.).
-  Vanessa Daza (IATE-OAC-UNC, FaMAF-UNC).
-  Mariano Dominguez (IATE-OAC-UNC, FaMAF-UNC).
-  Marcelo Lares (IATE-OAC-UNC, FaMAF-UNC).
-  Nadia Luczywo (LIMI-FCEFyN-UNC, IED-FCE-UNC, FCA-IUA-UNDEF)
-  Dante Paz (IATE-OAC-UNC, FaMAF-UNC).
-  Rodrigo Quiroga (INFIQC-CFQ, FCQ-UNC).
-  Martín de los Ríos (ICTP-SAIFR).
-  Bruno Sanchez (Department of Physics, Duke University).
-  Federico Stasyszyn (IATE-OAC, FaMAF-UNC).


**Afiliations:**

-  `Centro Franco Argentino de Ciencias de la Información y de Sistemas
   (CIFASIS-UNR) <https://www.cifasis-conicet.gov.ar/>`__
-  `Instituto de Astronomía Téorico y Experimental
   (IATE-OAC-UNC) <http://iate.oac.uncor.edu/>`__
-  `Facultad de Matemática Física y Computación
   (FaMAF-UNC) <https://www.famaf.unc.edu.ar/>`__
-  `Laboratorio de Ingeniería y Mantenimiento Industrial
   (LIMI-FCEFyN-UNC) <https://fcefyn.unc.edu.ar/facultad/secretarias/investigacion-y-posgrado/-investigacion/laboratorio-de-ingenieria-y-mantenimiento-industrial/>`__
-  `Instituto De Estadística Y Demografía - Facultad de Ciencias
   Económicas
   (IED-FCE-UNC) <http://www.eco.unc.edu.ar/instituto-de-estadistica-y-demografia>`__
-  `Department of Physics, Duke University <https://phy.duke.edu/>`__
-  `Facultad de Ciencias de la Administación
   (FCA-IUA-UNDEF) <https://www.iua.edu.ar/>`__
-  `Instituto de Investigaciones en Físico-Química de Córdoba
   (INFIQC-CONICET) <http://infiqc-fcq.psi.unc.edu.ar/>`__
-  `Liricus SRL <http://www.liricus.com.ar/>`__
-  `ICTP South American Institute for Fundamental Research
   (ICTP-SAIFR) <ICTP-SAIFR>`__

.. |Build Status| image:: https://travis-ci.org/ivco19/libs.svg?branch=master
   :target: https://travis-ci.org/ivco19/libs
.. |Python 3| image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://badge.fury.io/py/arcovid19
.. |BSD-3| image:: https://img.shields.io/badge/License-BSD3-blue.svg
   :target: https://tldrlegal.com/license/bsd-3-clause-license-(revised)
.. |Documentation Status| image:: https://readthedocs.org/projects/arcovid19/badge/?version=latest
   :target: https://arcovid19.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/arcovid19
   :target: https://pypi.org/project/arcovid19/
