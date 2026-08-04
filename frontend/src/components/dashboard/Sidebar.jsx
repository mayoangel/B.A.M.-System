import {
    FaTableCells,
    FaUserGraduate,
    FaUsers,
    FaIdBadge,
    FaBookOpen,
    FaRightFromBracket
} from "react-icons/fa6";
import { Link } from "react-router-dom";
const { logout } = useAuth()

function Sidebar() {

    return (

        <aside className="sidebar">

            <div className="logo">

                <svg
                    className="logo-icon"
                    viewBox="0 0 64 64"
                    fill="none"
                >
                    <polygon
                        points="32,10 58,22 32,34 6,22"
                        fill="#2d5a3d"
                    />

                    <path
                        d="M16 28 L32 36 L48 28 V40 C48 44 16 44 16 40 Z"
                        fill="#2d5a3d"
                    />

                    <line
                        x1="20"
                        y1="26"
                        x2="20"
                        y2="42"
                        stroke="#2d5a3d"
                        strokeWidth="2"
                    />

                    <circle
                        cx="20"
                        cy="44"
                        r="2.5"
                        fill="#2d5a3d"
                    />
                </svg>

                <span className="logo-text">
                    B.A.M.
                </span>

            </div>

            <hr className="linea-divisoria" />

            <nav className="nav">

                {/* EN ESTA PARTE SOLO CAMBIAR A LAS DIRECCIONES DE LAS DEMAS PAGINAS */}
                
                <Link to="/dashboard" className="nav-item">
                    <FaTableCells />
                    Dashboard
                </Link>

                <Link to="/administracion" className="nav-item">
                    <FaUserGraduate />
                    Estudiantes
                </Link>

                <Link to="/cursos" className="nav-item">
                    <FaBookOpen />
                    Cursos
                </Link>

                <Link to="/pase-de-lista" className="nav-item">
                    <FaUsers />
                    Pase de lista
                </Link>

            </nav>

            <hr className="linea-divisoria" />

            <Button onClick={logout}></Button>

        </aside>

    );

}

export default Sidebar;