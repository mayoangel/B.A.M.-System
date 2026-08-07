import { useEffect, useState } from "react";
import { getSummary } from "../../api/dashboard";

import {
    GraduationCap,
    UserCheck,
    Users,
    TriangleAlert
} from "lucide-react";

function StatsCards() {

    const [data, setData] = useState({
        total_students: 0,
        students_growth: 0,
        attendance_today: 0,
        attendance_change: 0,
        present_today: 0,
        active_groups: 0,
        different_courses: 0,
        pending_alerts: 0
    });

    useEffect(() => {
        async function loadSummary() {
            try {
                const data = await getSummary();
                setData(data);
            } catch (error) {
                console.error(error);
            }
        }

        loadSummary();
    }, []);

    
    return (

        <div className="stats-grid">

            <div className="stat-card">

                <div className="stat-content">

                    <div className="stat-label">
                        Total Estudiantes
                    </div>

                    <div className="stat-value">
                        {data.total_students}
                    </div>

                    <div className="stat-change positive">
                        
                        ↗ +{data.students_growth}% este mes
                    </div>

                </div>

                <div className="stat-icon green">
                    <GraduationCap />
                </div>

            </div>

            <div className="stat-card">

                <div className="stat-content">

                    <div className="stat-label">
                        Asistencia Hoy
                    </div>

                    <div className="stat-value">
                        {data.attendance_today}%
                    </div>

                    <div className="stat-change positive">
                        ↗ +{data.attendance_change}% vs ayer
                    </div>

                </div>

                <div className="stat-icon gray">
                    <UserCheck />
                </div>

            </div>

            <div className="stat-card">

                <div className="stat-content">

                    <div className="stat-label">
                        Grupos Activos
                    </div>

                    <div className="stat-value">
                        {data.active_groups}
                    </div>

                    <div className="stat-change">
                        {data.different_courses} cursos disponibles
                    </div>

                </div>

                <div className="stat-icon gray">
                    <Users />
                </div>

            </div>

            <div className="stat-card alert">

                <div className="stat-content">

                    <div className="stat-label">
                        Alertas Pendientes
                    </div>

                    <div className="stat-value">
                        {data.pending_alerts}
                    </div>

                    <div className="stat-change warning">
                        Requieren atención
                    </div>

                </div>

                <div className="stat-icon red">
                    <TriangleAlert />
                </div>

            </div>

        </div>

    );

}

export default StatsCards;