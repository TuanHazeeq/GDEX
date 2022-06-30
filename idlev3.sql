WITH temp AS
(SELECT vehicle_no, 
odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_odometer,
time_stamp, LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_time_stamp,
alert_type, LAG(alert_type, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_alert,
location,coordinate
FROM gdex.vtracker_trackeralert
WHERE time_stamp >= '2022-05-02 0:0:0' AND time_stamp < '2022-05-03 0:0:0'
ORDER BY vehicle_no, time_stamp)
SELECT vehicle_no,
to_char(time_stamp, 'YYYY-MM-DD HH24:MI:SS') AS from,to_char(next_time_stamp, 'YYYY-MM-DD HH24:MI:SS') AS to,
ROUND(EXTRACT(EPOCH FROM next_time_stamp - time_stamp)/60, 2) AS duration, location,coordinate FROM temp
WHERE alert_type = 8 AND next_alert = 7
AND odometer = next_odometer
AND vehicle_no = 'BPD2957'