WITH temp AS(
	SELECT vehicle_no,
	LAG(odometer, 1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS previous_odometer,
	odometer AS current_odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_odometer,
	time_stamp AS current_time_stamp,
	LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_time_stamp,
	LAG(alert_type, 1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS previous_alert,
	alert_type AS current_alert, LAG(alert_type, -1) OVER (PARTITION BY vehicle_no ORDER BY vehicle_no, time_stamp) AS next_alert
	FROM gdex.vtracker_trackeralert
	WHERE time_stamp >= '2022-05-05 0:0:0' AND time_stamp < '2022-05-06 0:0:0'
	ORDER BY vehicle_no, time_stamp
)
SELECT vehicle_no,
ROUND(EXTRACT(EPOCH FROM next_time_stamp - current_time_stamp)/60, 2) AS duration
FROM temp
WHERE previous_alert = 7 AND current_alert = 8 AND next_alert = 7
AND previous_odometer = current_odometer AND current_odometer = next_odometer