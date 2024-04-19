-- Write query to get number of graded assignments for each student:
SELECT s.id AS student_id, COUNT(*) AS graded_assignment_count
FROM assignments a
JOIN students s ON a.student_id = s.id
WHERE a.state = 'GRADED'
GROUP BY s.id;
