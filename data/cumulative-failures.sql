-- cumulative failures over power_hrs -- C(t)
COPY (SELECT power_hrs, SUM(disk_count) OVER (ORDER BY power_hrs)
      FROM (SELECT power_hrs, COUNT(dl.serial_no) AS disk_count
            FROM disk_logs AS dl INNER JOIN disk_fails AS df
                 ON dl.serial_no = df.serial_no AND
                    dl.datestamp = df.datestamp
            GROUP BY power_hrs) AS cu)
TO STDOUT WITH CSV DELIMITER ',';
