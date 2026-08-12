import StatsCards from "./StatsCards";
import CoursesCard from "./CoursesCard";
import WeeklyAttendance from "./WeeklyAttendance";
import { LayoutDashboard } from 'lucide-react';

import "../../css/dashboard.css";

function Dashboard() {
    return (
       

        <div className="mx-auto max-w-7xl p-6">
            {/* HEADER - Mismo estilo que Cursos */}
            <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                    <LayoutDashboard className="h-6 w-6 text-primary" aria-hidden="true" />
                    <div>
                        <h1 className="font-roboto text-xl font-bold text-moss">Dashboard</h1>
                        <p className="font-lato text-sm text-gray-500">
                            Resumen general del sistema, estadísticas y métricas clave.
                        </p>
                    </div>
                </div>
                
            </div>

            <StatsCards />

            <div className="main-grid">
                <WeeklyAttendance />
                <CoursesCard />
            </div>

        </div>
    );
}

export default Dashboard;