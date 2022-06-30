SELECT a.vehicle_no, a.odometer, a.time_stamp, a.ignition, b.alert_type
FROM gdex.vtracker_trackerfeed a INNER JOIN gdex.vtracker_trackeralert b
ON a.vehicle_no = b.vehicle_no
AND a.time_stamp = b.time_stamp
WHERE a.time_stamp >= '2022-04-05 0:0:0' AND a.time_stamp < '2022-04-06 0:0:0'
AND a.vehicle_no = 'BHG7092'
ORDER BY a.vehicle_no, a.odometer