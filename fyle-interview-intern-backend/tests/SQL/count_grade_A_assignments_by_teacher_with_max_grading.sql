-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT t.id AS teacher_id, COUNT(*) AS grade_A_count
FROM assignments a
JOIN teachers t ON a.teacher_id = t.id
WHERE a.grade = 'A'
GROUP BY t.id
HAVING COUNT(*) = (
    SELECT MAX(graded_count)
    FROM (
        SELECT COUNT(*) AS graded_count
        FROM assignments
        GROUP BY teacher_id
    ) AS max_counts
);
