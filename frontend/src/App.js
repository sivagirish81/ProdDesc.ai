import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { ProductProvider } from './context/ProductContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './components/Home';
import ProductForm from './components/ProductForm';
import ContentPreview from './components/ContentPreview';
import Login from './components/Login';
import Register from './components/Register';
import './styles/App.css';

// Create theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

// Protected Route component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return null; // or a loading spinner
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  return children;
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <ProductProvider>
          <Router>
            <div className="app">
              <Navbar />
              <main className="app-content" style={{ paddingTop: '64px', minHeight: '100vh' }}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route
                    path="/generate"
                    element={
                      <ProtectedRoute>
                        <ProductForm />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/preview"
                    element={
                      <ProtectedRoute>
                        <ContentPreview />
                      </ProtectedRoute>
                    }
                  />
                  <Route
                    path="/preview/:productId"
                    element={
                      <ProtectedRoute>
                        <ContentPreview />
                      </ProtectedRoute>
                    }
                  />
                </Routes>
              </main>
            </div>
          </Router>
        </ProductProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;