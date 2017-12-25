-- see original here: https://gitlab.com/johncf/failure-analysis
-- observed population over power_hrs -- N(t)
COPY (WITH cgs AS (SELECT power_hrs,
                          SUM(contrib_step) AS contrib_group
                   FROM (SELECT 1 AS contrib_step,
                                min_power_hrs AS power_hrs
                         FROM disk_summary
                         UNION ALL
                         SELECT -1 AS contrib_step,
                                max_power_hrs AS power_hrs
                         FROM disk_summary) AS pop_contrib_steps
                   GROUP BY power_hrs) -- ORDER BY power_hrs ??
      SELECT power_hrs,
             SUM(contrib_group) OVER (ORDER BY power_hrs) AS observed_pop
      FROM cgs)
TO STDOUT WITH CSV DELIMITER ','
