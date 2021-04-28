# Introduction

Manetu-ql is a sample python application that demonstrates GraphQL access to
Manetu.io. Through the use of either a personal access token (PAT) or an
extracted JWT from your login, you can access Manetu's GraphQL API to access
your provider data.

> **Note:** This is a python3 project and will not run under python2.

# License

This project is licensed under a simple MIT-style license with simple
restrictions. See the `LICENSE` file for details.

# Building

The build is controlled with the `Makefile`. As pure python code, there is no
real "build" per se, and you can just run it from the directory where you
checked it out of. However, the `Makefile` does control building the `wheel`
installation package. See the `Installing` section for details.

Do note that this is a python3 project, so install (preferably the latest)
python3 on your system according to your OS's best practises. For example, on
MacOS use brew:

```
> brew update
> brew install python3
```

# Installing

Since there's multiple files to install, a "binary" installation file is
created. This file is in the PIP `wheel` format which is a python installation
package. Note that this package is limited to python3 (i.e. it is NOT a
`universal wheel`) because this project is designed for python3 only. This
means that you can install it on any machine with both python3 and PIP
installed.

We use PIP because that let's us uninstall and update when we want to, since
the wheel format doesn't provide uninstallation per se.

The installation file has a "`whl`" extension and is typically called:
`manetu_ql-1.0.0-py3-none-any.whl` with the version tag (1.0.0) changed as
appropriate.

To install, do this:
  - If you already have the wheel, do:

    `$ pip3 install manetu_ql-1.0.0-py3-none-any.whl`

  - If you do not, first make it:

    `$ make`

    then install as above.

To uninstall, do this: `$ pip3 uninstall manetu_ql`

# Using the project as a library for your own apps

Once you install the package wheel as descirbed above, the mql package which
contains all the source for this application is installed in your site-packages
directory. To use it as a library, simply import what you need out of it.

# Usage examples

TBD.
