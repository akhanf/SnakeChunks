% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/margin_stats.R
\name{RowStats}
\alias{RowStats}
\title{compute row statistics on a data.frame or matrix.}
\usage{
RowStats(x, verbose = 0)
}
\arguments{
\item{x}{data.frame or matrix}

\item{verbose=0}{level of verbosity}

\item{selected.stats=NULL}{if specified, restrict the computation to a subset of the supported statistics.}
}
\description{
statistics are computed on each row by passing the data frame/matrux to MarginStats() with marrgin=1.
}
\author{
Jacques van Helden
}
