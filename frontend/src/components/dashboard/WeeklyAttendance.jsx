import { useEffect, useState } from "react";
import { getWeeklyAttendance } from "../../api/dashboard";

function WeeklyAttendance() {

    const [data, setData] = useState([]);

    useEffect(() => {

        loadAttendance();

    }, []);

    const loadAttendance = async () => {

        try {

            const data = await getWeeklyAttendance();
            setData(data);
        } catch (error) {

            console.error(error);

        }

    };

    const getDay = (date) => {

        const days = [
            "Dom",
            "Lun",
            "Mar",
            "Mié",
            "Jue",
            "Vie",
            "Sáb"
        ];

        return days[
            new Date(date).getDay()
        ];

    };

    return (

        <div className="chart-card">

            <div className="chart-header">

                <div>

                    <div className="chart-title">
                        Asistencia Semanal
                    </div>

                    <div className="chart-subtitle">
                        Datos obtenidos del sistema
                    </div>

                </div>

            </div>

            <div className="chart-wrapper">

                <div className="y-axis">

                    <span>100%</span>
                    <span>75%</span>
                    <span>50%</span>
                    <span>25%</span>
                    <span>0%</span>

                </div>

                <div className="chart-container">

                    {
                        data.map((item) => (

                            <div
                                key={item.date}
                                className="chart-bar-group"
                            >

                                <div className="chart-bars">

                                    <div
                                        className={
                                            item.attendance >= 80
                                                ? "chart-bar green"
                                                : "chart-bar red"
                                        }
                                        style={{
                                            height:
                                                `${item.attendance * 1.8}px`
                                        }}
                                    />

                                </div>

                                <div className="chart-day">
                                    {getDay(item.date)}
                                </div>

                                <div className="chart-date">
                                    {item.date}
                                </div>

                            </div>

                        ))
                    }

                </div>

            </div>

            <div className="chart-footer">

                <div className="chart-legend">

                    <div className="legend-item">

                        <span className="legend-dot green"></span>

                        Normal (mayor que 80%)

                    </div>

                    <div className="legend-item">

                        <span className="legend-dot red"></span>

                        Baja (menoor que 80%)

                    </div>

                </div>

            </div>

        </div>

    );

}

export default WeeklyAttendance;