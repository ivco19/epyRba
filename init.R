# This file is part of the
#   Arcovid19 (https://ivco19.github.io/).
# Copyright (c) 2020, Arcovid Team
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/epyRba/master/LICENSE

r = getOption("repos")
r["CRAN"] = "http://cran.us.r-project.org"

options(repos=r)

## Install R packages
packages <- c(
    "dplyr", "devtools",
    "deSolve", "rjson", "minpack.lm", "readr")

install_if_missing <- function(p) {
    if (!p %in% rownames(installed.packages())) {
        install.packages(p)
    }
}

invisible(sapply(packages, install_if_missing))
