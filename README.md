# Backblaze Data Analysis

A collection of scripts to prepare and process data published by Backblaze, to
generate failure rate curves over the age of a disk. The scripts needed for the
final generation of plots are kept in [failure-analysis repo][].

The steps described below assumes the presence of directories `2013`, `2014`
etc. within [`data` directory][], containing [Hard Drive Test Data from
Backblaze][backblaze] in csv format (i.e. in extracted form).

[failure-analysis repo]: https://gitlab.com/johncf/failure-analysis
[`data` directory]: ./data
[backblaze]: https://www.backblaze.com/b2/hard-drive-test-data.html

### Usage

1.  ```sh
    make db-init
    ```

    This will create a Postgres database named backblaze, process csv files
    nested in `data` directory and load it into the database.

2.  ```sh
    make plot-all
    ```

    Dependency chain: `plot-all -> plot-metadata -> popular-models`

    - `popular-models` will query the database for the 20 most popular disk
      models and creates a file that lists them.
    - `plot-metadata` processes data for each model listed in `popular-models`
      file and generates csv files required for plotting as well as a
      `plot-metadata` file that lists all these files needed.
    - `plot-all` uses the `plot-metadata` file to actually generate plots.

3.  ```sh
    make Results.md
    ```

    Uses `plot-metadata` file to create a markdown file that embeds all
    generated plots.

### Results

See <https://johncf.github.io/failure-analysis.html>
