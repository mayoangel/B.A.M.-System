import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth, roleHomePath, ROLE_ADMIN, ROLE_DOCENTE, ROLE_TUTOR } from './auth/AuthContext.jsx'
import ProtectedRoute from './components/auth/ProtectedRoute.jsx'
import LoginPage from './components/auth/LoginPage.jsx'
import AppShell from './components/layout/AppShell.jsx'
import StudentEnrollment from './components/enrollment/StudentEnrollment.jsx'
import AttendanceSession from './components/attendance/AttendanceSession.jsx'
import StudentManagement from './components/management/StudentManagement.jsx'
import CourseManagement from './components/courses/CourseManagement.jsx'
import MyChildrenPanel from './components/tutor/MyChildrenPanel.jsx'

function LoginRoute() {
  const { isAuthenticated, user } = useAuth()
  if (isAuthenticated) {
    return <Navigate to={roleHomePath(user.role)} replace />
  }
  return <LoginPage />
}

function RoleHomeRedirect() {
  const { user } = useAuth()
  return <Navigate to={roleHomePath(user?.role)} replace />
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginRoute />} />

          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppShell />
              </ProtectedRoute>
            }
          >
            <Route index element={<RoleHomeRedirect />} />

            <Route
              path="registro-alumno"
              element={
                <ProtectedRoute allowedRoles={[ROLE_ADMIN, ROLE_DOCENTE]}>
                  <StudentEnrollment />
                </ProtectedRoute>
              }
            />

            <Route
              path="pase-de-lista"
              element={
                <ProtectedRoute allowedRoles={[ROLE_ADMIN, ROLE_DOCENTE]}>
                  <AttendanceSession />
                </ProtectedRoute>
              }
            />

            <Route
              path="administracion"
              element={
                <ProtectedRoute allowedRoles={[ROLE_ADMIN]}>
                  <StudentManagement />
                </ProtectedRoute>
              }
            />

            <Route
              path="cursos"
              element={
                <ProtectedRoute allowedRoles={[ROLE_ADMIN]}>
                  <CourseManagement />
                </ProtectedRoute>
              }
            />

            <Route
              path="mis-hijos"
              element={
                <ProtectedRoute allowedRoles={[ROLE_TUTOR]}>
                  <MyChildrenPanel />
                </ProtectedRoute>
              }
            />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
