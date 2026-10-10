# Dataset provenance

AirPassengers is the monthly total of international airline passengers, 1949–1960, in thousands. There are 144 observations. R datasets documentation attributes it to Box and Jenkins (1976), *Time Series Analysis: Forecasting and Control*.

- Primary description: https://www.stat.ethz.ch/R-manual/R-devel/RHOME/library/datasets/html/AirPassengers.html
- CSV mirror: https://github.com/vincentarelbundock/Rdatasets/blob/master/csv/datasets/AirPassengers.csv
- Local snapshot: `airpassengers.csv`; no live network request is needed to run the application.
- Columns: `time` is fractional year; `value` is passengers in thousands. The row-name column is unused.
- Dataset is a third-party R example dataset. The repository MIT license applies to our code; it does not relicense this dataset. Preserve the source attribution when redistributing and check the upstream terms for your use.

Evaluation trains through December 1959 and holds out all twelve months of 1960. Three twelve-month validation periods precede that holdout. No simulated dates or fabricated source data are added to this historical series.

Snapshot Git blob: `ebb4c40463f510a3fda99b1e2648d70ad95079b4`. Local CSV SHA-256: `bdb98adbd418a6de6842a742e0602f363c3b841c26677e7e61a1e055e9509bd8`.
