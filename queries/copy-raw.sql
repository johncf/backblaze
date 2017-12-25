COPY raw_logs (datestamp, model, serial, failed, poh, lba_r, lba_w)
FROM STDIN WITH DELIMITER AS ',' NULL AS '';
