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
