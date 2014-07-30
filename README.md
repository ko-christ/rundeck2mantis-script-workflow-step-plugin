rundeck2mantis-script-workflow-step-plugin
------

This directory contains a Rundeck script-based Workflow Step Plugin to attach output of a Rundeck job to a Mantis Bug Tracker ticket.

Build
====

    make

produces:

    rundeck2mantis-script-workflow-step-plugin.zip

Installation
=====

Install the plugin in your `$RDECK_BASE/libext` directory:

    service rundeckd stop
    mv rundeck2mantis-script-workflow-step-plugin.zip $RDECK_BASE/libext
    service rundeckd start

Requirements
=====

Rundeck 2.0+
Python 2.6+ and Python modules
`suds`

Usage
=====

Plugin should be available under Job Create/Edit form, `Add a Step` -> `Workflow Steps`
Use it as a last workflow step plugin.

Files
=====

`rundeck2mantis-script-workflow-step-plugin/plugin.yaml`

:   Defines the metadata for the plugin

`rundeck2mantis-script-workflow-step-plugin/contents/`

:   directory containing necessary scripts or assets

`rundeck2mantis-script-workflow-step-plugin/rundeck2mantis.py`

:   the script defined in plugin.yaml to be executed for the plugin

`rundeck2mantis-script-workflow-step-plugin/rundeck2mantis.conf`

:   Configuration file for rundeck2mantis.py


Configuration File
=====

`rundeck2mantis.conf` configuration file with the following options:

`MANTISURL` = `https://support.mycompany.com/api/soap/mantisconnect.php?wsdl` 	# `MantisBT SOAP API URL`

`USERNAME` = `administrator` 	# `a MantisBT user with suitable access level, usually the administrator`

`PASSWD` = `root`

`TOKEN` = `Rda218eba1ff45jk7858b8ae88a77fN2` 	# `Sample Rundeck API Token to use.`

`API_V` = `11` 		# `API Version to use. Default 11.`

Plugin metadata
=====

The `plugin.yaml` file declares one script based service provider for the `WorkflowNodeStep` service.

Licence
=====

Copyright 2014 National Documentation Centre

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


