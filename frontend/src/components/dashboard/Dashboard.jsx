import Sidebar from "./Sidebar";
import Header from "./Header";
import StatsCards from "./StatsCards";
import CoursesCard from "./CoursesCard";
import WeeklyAttendance from "./WeeklyAttendance";

import "../../css/dashboard.css";

function Dashboard() {

    return (

        <div className="container">

            <Sidebar />

            <main className="main">

                <Header />

                <div className="content">

                    <StatsCards />

                    <div className="main-grid">

                        <WeeklyAttendance />

                        <CoursesCard />

                    </div>

                </div>

            </main>

        </div>

    );

}

export default Dashboard;