SELECT vehicle_no, time_stamp as start_time,
LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC) AS end_time,
(LAG(time_stamp, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC) - time_stamp) AS duration,
odometer, LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC) AS end_odo,
(LAG(odometer, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC)-odometer) as mileage,
ST_MAKELINE(coordinate::geometry, LAG(coordinate, -1) OVER (PARTITION BY vehicle_no, DATE(time_stamp) ORDER BY vehicle_no, time_stamp ASC)::geometry)
FROM vtracker_trackerfeed, areas a
WHERE speed != '0'
GROUP BY vehicle_no, DATE(time_stamp),time_stamp,odometer, coordinate
ORDER BY vehicle_no, time_stamp DESC
LIMIT 100