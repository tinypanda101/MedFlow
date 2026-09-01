-- Medflow Seed Data
--psql -U postgres -d medflow
-- \i seed.sql

--Hospitals
INSERT INTO hospitals (id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Lakeland Regional', 'Polk', 500, 101),
    (2, 'Tampa General', 'Hillsborough', 1800, 102);


--Technician id,name,hospital_Id
INSERT INTO technicians (id, name, hospital_id) VALUES
    (201, 'W. Jacob', 1),
    (202, 'S. Kyle', 1);

--Equipment
INSERT INTO equipment (id, serial_number, model, status, charge_level, hospital_id) VALUES
    (1, 'PR-1001', 'Super Printer 5000', 'In-Use', 18.5, 1),
    (2, 'PR-1002', 'Super Printer 5000', 'Available', 76.0, 1),
    (3, 'XR-2050', 'Xtra Xray', 'In-Use', 9.0, 2),
    (4, 'PR-1003', 'Super Printer 5000', 'Maintenance', 42.0, 1);

--Work_Orders
INSERT INTO work_orders (id, title, priority, status, equipment_id, technician_id) VALUES
    (1, 'Jammed Belt Fix', 'Critical', 'Pending', 1, 201),
    (2, 'Playtime', 'Low', 'Pending', 3, 202),
    (3, 'Print Urgent Forms', 'Medium', 'Completed', 2, 201),
    (4, 'Intern Teaching', 'Low', 'Failed', 4, 201);

INSERT INTO service_report (work_order_id, file_url, notes) VALUES
    (1, 's3://medflow-diagnostics/PR-1001.pdf', 'Turning it off and on again didnt work');

SELECT setval('hospitals_id_seq', (SELECT MAX(id) FROM hospitals));
SELECT setval('technicians_id_seq', (SELECT MAX(id) FROM technicians));
SELECT setval('equipment_id_seq', (SELECT MAX(id) FROM equipment));
SELECT setval('work_orders_id_seq', (SELECT MAX(id) FROM work_orders));
SELECT setval('service_report_id_seq', (SELECT MAX(id) FROM service_report));