WITH tempTable AS(
SELECT id, vehicle_no, time_stamp, odometer, speed, ignition,
(odometer - LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp DESC)) as mileage,
ST_MAKELINE((LAG(coordinate, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp DESC)::geometry), coordinate::geometry)
FROM vtracker_trackerfeed
WHERE DATE(time_stamp) ='2022-04-04'
	AND vehicle_no = 'BMS4323c'
GROUP BY vehicle_no, time_stamp,odometer, coordinate, id
ORDER BY vehicle_no, time_stamp DESC
)
SELECT time_stamp, vehicle_no, speed, ignition, mileage, odometer,st_makeline,
ST_LENGTH(ST_TRANSFORM(st_makeline,3380))/1000 AS linemileage
FROM tempTable
ORDER BY time_stamp