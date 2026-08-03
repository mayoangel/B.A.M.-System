import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { LogIn, Mail, Lock } from 'lucide-react'
import { useAuth, roleHomePath } from '../../auth/AuthContext.jsx'
import { ApiError } from '../../api/client.js'
import Button from '../ui/Button.jsx'
import TextInput from '../ui/TextInput.jsx'
import Alert from '../ui/Alert.jsx'

/**
 * Pantalla de acceso única para Administradores, Docentes y Tutores. El
 * backend identifica el rol a partir del correo (Empleados vs Tutores) y la
 * redirección posterior al panel correspondiente la decide `roleHomePath`.
 */
export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!email || !password) {
      setError('Ingresa tu correo y contraseña para continuar.')
      return
    }

    setSubmitting(true)
    try {
      const user = await login(email.trim(), password)
      const redirectTo = location.state?.from || roleHomePath(user.role)
      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'No se pudo iniciar sesión.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-sm rounded-2xl border border-gray-100 bg-white p-8 shadow-md">
        <div className="mb-8 flex flex-col items-center gap-3">
          <img src="/logo.svg" alt="B.A.M. System" className="h-14 w-14" />
          <div className="text-center">
            <h1 className="font-roboto text-xl font-bold text-moss">B.A.M. System</h1>
            <p className="font-lato text-sm text-gray-500">Inicia sesión para continuar</p>
          </div>
        </div>

        <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
          <TextInput
            label="Correo electrónico"
            type="email"
            icon={Mail}
            placeholder="tucorreo@bam.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="username"
            autoFocus
          />

          <TextInput
            label="Contraseña"
            type="password"
            icon={Lock}
            placeholder="********"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          {error && (
            <Alert variant="error">
              <p>{error}</p>
            </Alert>
          )}

          <Button type="submit" icon={LogIn} loading={submitting} className="mt-2 w-full">
            Iniciar sesión
          </Button>
        </form>
      </div>
    </div>
  )
}
