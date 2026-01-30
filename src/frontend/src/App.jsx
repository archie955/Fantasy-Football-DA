import { Routes, Route } from 'react-router-dom'

import Login from './pages/Login'
import Home from './pages/Home'
import ProtectedRoute from './components/ProtectedRoute'
import Teams from './pages/Teams'
import Players from './pages/Players'

function App() {

  return (
    <Routes>

      <Route path='/' element={<Login />} />

      <Route
        path='/home'
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />

      <Route
        path='/league'
        element={
          <ProtectedRoute>
            <Teams />
          </ProtectedRoute>
        }
      />

      <Route
        path='team'
        element={
          <ProtectedRoute>
            <Players />
          </ProtectedRoute>
        }
      />

      
    </Routes>
  )
}

export default App