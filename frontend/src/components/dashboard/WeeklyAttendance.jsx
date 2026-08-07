import { useEffect, useState } from "react";
import { getWeeklyAttendance } from "../../api/dashboard";

function WeeklyAttendance() {

    const [data, setData] = useState([]);
    const [weekOffset, setWeekOffset] = useState(0);
   

    useEffect(() => {

        loadAttendance();

    }, [weekOffset]);

    const loadAttendance = async () => {

        try {

            const data = await getWeeklyAttendance(weekOffset);
            setData(data);
        } catch (error) {

            console.error(error);

        }

    };

    const getDay = (dateString) => {

        const [year, month, day] = dateString
            .split("-")
            .map(Number);

        const date = new Date(
            year,
            month - 1,
            day
        );

        const days = [
            "Dom",
            "Lun",
            "Mar",
            "Mié",
            "Jue",
            "Vie",
            "Sáb"
        ];

        return days[date.getDay()];

    };

    const isWeekend = (dateString) => {

        const [year, month, day] = dateString
            .split("-")
            .map(Number);

        const date = new Date(
            year,
            month - 1,
            day
        );

        const dayOfWeek = date.getDay();

        return dayOfWeek === 0 || dayOfWeek === 6;

    };

    const weeklyAverage =
    data.length > 0
    ? (
        data.reduce(
            (sum, item) => sum + item.attendance,
            0
        ) / data.length
    ).toFixed(1)
    : 0;


    const orderedData = [...data].sort((a, b) => {

        const getOrder = (dateString) => {

            const [year, month, day] = dateString
                .split("-")
                .map(Number);

            const date = new Date(
                year,
                month - 1,
                day
            );

            const dayOfWeek = date.getDay();

            return dayOfWeek === 0
                ? 7
                : dayOfWeek;

        };

        return getOrder(a.date) - getOrder(b.date);

    });

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

                <select
                    value={weekOffset}
                    onChange={(e)=>setWeekOffset(Number(e.target.value))}
                    className="border rounded-lg px-3 py-2 text-sm"
                >

                    <option value={0}>
                        Esta semana
                    </option>

                    <option value={1}>
                        Hace 1 semana
                    </option>

                    <option value={2}>
                        Hace 2 semanas
                    </option>

                    <option value={3}>
                        Hace 3 semanas
                    </option>

                </select>

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
                        orderedData.map((item) => (

                            <div
                                key={item.date}
                                className="chart-bar-group"
                            >

                                <div className="chart-bars">

                                    <div
                                        className={
                                            isWeekend(item.date)
                                                ? "chart-bar gray"
                                                : item.attendance >= 80
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

                        Normal (&gt; 80%)

                    </div>

                    <div className="legend-item">

                        <span className="legend-dot red"></span>

                        Baja (&lt; 80%)

                    </div>

                    <div className="legend-item">

                        <span className="legend-dot gray"></span>

                        Fin de semana

                    </div>

                    

                </div>

                <div className="chart-average">

                        Promedio semanal:
                        <strong>
                            {" "}
                            {weeklyAverage}%
                        </strong>

                    </div>

            </div>

        </div>

    );

}

export default WeeklyAttendance;