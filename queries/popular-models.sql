COPY (SELECT model,
             COUNT(*)/365 AS approx_diskyears,
             SUM(failed ::int) AS fail_count
      FROM raw_logs GROUP BY model
      ORDER BY approx_diskyears DESC
      LIMIT 20)
TO STDOUT WITH CSV DELIMITER '|';
