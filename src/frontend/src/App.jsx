import { Routes, Route } from 'react-router-dom'

import Login from './pages/Login'
import Home from './pages/Home'
import ProtectedRoute from './components/ProtectedRoute'
import Teams from './pages/Teams'

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
       path='/teams'
       element={
        <ProtectedRoute>
          <Teams />
        </ProtectedRoute>
       }
     />
    </Routes>
  )
}

export default App

/*<Route
        path='/leagues'
        element={
          <ProtectedRoute>
            <Leagues />
          </ProtectedRoute>
        }
      />*/