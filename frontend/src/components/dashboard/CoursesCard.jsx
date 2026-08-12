import { useEffect, useState } from "react";
import { getCourses } from "../../api/dashboard";

function CoursesCard() {

    const [courses, setCourses] = useState([]);
    const MAX_STUDENTS = 30; // Capacidad máxima por curso

    useEffect(() => {

        loadCourses();

    }, []);

    const loadCourses = async () => {
        try {
            const data = await getCourses();
            setCourses(data);
        } catch (error) {
            console.error(error);
        }
    };

    const maxStudents =
        Math.max(
            ...courses.map(
                c => c.students
            ),
            1
        );

    return (

        <div className="students-card">

            <div className="students-header">

                <div className="students-title">
                    Estudiantes por
                    <br />
                    Curso
                </div>
                
                <button
                    className="add-btn"
                >
                    Agregar
                </button> 

            </div>

            <div className="students-subtitle">
                Distribución actual
            </div>

            <div className="course-list">

                {
                    courses.map(
                        (course, index) => {
                            // Calcular porcentaje basado en 30 (tope fijo)
                            const percentage = Math.min((course.students / MAX_STUDENTS) * 100, 100);

                            return (
                                <div
                                    key={course.course_id}
                                    className="course-item"
                                >

                                    <div className="course-header">

                                        <span className="course-name">
                                            {course.course}
                                        </span>

                                        <span className="course-count">
                                            {course.students}
                                        </span>

                                    </div>

                                    <div className="course-bar">

                                        <div
                                            className="course-progress green"
                                            style={{
                                                width: `${percentage}%`
                                            }}
                                        />

                                    </div>

                                </div>
                            );
                        }
                    
                    )
                }

            </div>

        </div>

    );

}

export default CoursesCard;