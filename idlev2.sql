WITH temp AS(SELECT vehicle_no, odometer,MAX(time_stamp) - MIN(time_stamp) AS duration
FROM gdex.vtracker_trackerfeed
WHERE time_stamp >= '2022-04-04 0:0:0' AND time_stamp < '2022-04-05 0:0:0'
AND ignition = 'true'
GROUP BY vehicle_no, odometer
HAVING MAX(time_stamp) - MIN(time_stamp) > '30 minute'::interval
ORDER BY vehicle_no)
SELECT vehicle_no, SUM(duration) FROM temp
GROUP BY vehicle_no
ORDER BY vehicle_no